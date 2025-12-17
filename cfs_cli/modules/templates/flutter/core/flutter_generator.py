"""
Flutter specific project generator.
Handles Dart project generation with Flutter conventions.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from .exceptions.flutter_exceptions import FlutterGeneratorError


def _check_flutter_installed() -> bool:
    """
    Check if Flutter is installed and accessible.

    Returns:
        True if Flutter is installed, False otherwise
    """
    try:
        result = subprocess.run(
            ['flutter', '--version'],
            capture_output=True,
            text=True,
            timeout=20
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


class FlutterGenerator:
    """Generates Flutter projects from templates."""

    def __init__(self, template_path: Path):
        """
        Initialize the Flutter generator.

        Args:
            template_path: Path to the Flutter template directory
        """
        self.template_path = Path(template_path)
        self.manifest = None
        self.jinja_env = None

    def load_manifest(self) -> Dict[str, Any]:
        """
        Load the Flutter template manifest.

        Returns:
            Parsed manifest dictionary
        """
        from .flutter_manifest_loader import FlutterManifestLoader

        loader = FlutterManifestLoader(self.template_path)
        self.manifest = loader.load_manifest()

        # Set up Jinja2 environment with Flutter specific filters
        files_source = self.manifest.get('files_source', 'src_templates')
        template_files_path = self.template_path / files_source

        # Create template directory if it doesn't exist (for future use)
        if not template_files_path.exists():
            template_files_path.mkdir(parents=True, exist_ok=True)

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_files_path)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        # Add Flutter specific filters
        self.jinja_env.filters['to_package_path'] = self._to_package_path
        self.jinja_env.filters['to_snake_case'] = self._to_snake_case

        return self.manifest

    @staticmethod
    def _to_package_path(package_name: str) -> str:
        """Convert package name to filesystem path."""
        return package_name.replace('.', '/')

    @staticmethod
    def _to_snake_case(text: str) -> str:
        """Convert text to snake_case."""
        # Replace hyphens and spaces with underscores
        text = text.replace('-', '_').replace(' ', '_')
        # Convert to lowercase
        return text.lower()

    def _compute_flutter_variables(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute Flutter specific derived variables.

        Args:
            variables: User-provided variables

        Returns:
            Variables with Flutter computed values added
        """
        if not self.manifest:
            raise FlutterGeneratorError("Manifest not loaded")

        # Start with user variables
        all_vars = variables.copy()

        # Add defaults for missing variables
        for var_name, var_config in self.manifest.get('variables', {}).items():
            if var_name not in all_vars and 'default' in var_config:
                all_vars[var_name] = var_config['default']

        # Compute Flutter specific variables
        computed = self.manifest.get('computed', {})
        for computed_name, computed_expr in computed.items():
            try:
                # Create a Jinja2 template from the expression
                template = self.jinja_env.from_string(computed_expr)
                all_vars[computed_name] = template.render(**all_vars)
            except Exception as e:
                raise FlutterGeneratorError(
                    f"Error computing Flutter variable '{computed_name}': {e}"
                )

        # Add additional Flutter computed variables
        if 'package_name' in all_vars:
            all_vars['package_path'] = self._to_package_path(all_vars['package_name'])

        if 'project_name' in all_vars:
            # Ensure project name is in snake_case
            all_vars['project_name'] = self._to_snake_case(all_vars['project_name'])

        return all_vars

    def _render_path(self, path_template: str, variables: Dict[str, Any]) -> str:
        """
        Render a path template with variables.

        Args:
            path_template: Path with Jinja2 template syntax
            variables: Variables to render with

        Returns:
            Rendered path string
        """
        try:
            template = self.jinja_env.from_string(path_template)
            return template.render(**variables)
        except Exception as e:
            raise FlutterGeneratorError(f"Error rendering path '{path_template}': {e}")

    def _process_structure(
        self,
        variables: Dict[str, Any],
        output_dir: Path,
        force: bool,
        result: Dict[str, List[str]]
    ) -> None:
        """
        Process the manifest 'structure' section and create directories/files.

        Args:
            variables: Computed variables
            output_dir: Output directory
            force: Overwrite existing files
            result: Dictionary to track created/skipped files
        """
        structure = self.manifest.get('structure', [])

        if not structure:
            print("⚠️  Warning: No structure defined in manifest")
            return

        files_source = self.manifest.get('files_source', 'src_templates')
        template_files_path = self.template_path / files_source

        for item in structure:
            item_type = item.get('type')
            path_template = item.get('path')

            if not path_template:
                raise FlutterGeneratorError(f"Missing 'path' in structure item: {item}")

            # Render the path
            rendered_path = self._render_path(path_template, variables)
            full_path = output_dir / rendered_path

            if item_type == 'dir':
                # Create directory
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    result['created'].append(str(rendered_path))
                except Exception as e:
                    raise FlutterGeneratorError(f"Failed to create directory {rendered_path}: {e}")

            elif item_type == 'file':
                # Get source template
                source_template = item.get('source')
                if not source_template:
                    raise FlutterGeneratorError(
                        f"Missing 'source' for file: {path_template}\n"
                        f"Every file in manifest structure must have a 'source' field."
                    )

                # Check if file exists
                if full_path.exists() and not force:
                    result['skipped'].append(str(rendered_path))
                    continue

                # Ensure parent directory exists
                full_path.parent.mkdir(parents=True, exist_ok=True)

                # Render source template name (for dynamic extensions)
                source_template = self._render_path(source_template, variables)

                # Check if template file exists
                template_file_path = template_files_path / source_template
                if not template_file_path.exists():
                    raise FlutterGeneratorError(
                        f"Template file not found: {source_template}\n"
                        f"Expected at: {template_file_path}\n"
                        f"For manifest path: {path_template}"
                    )

                try:
                    # Load and render the template
                    template = self.jinja_env.get_template(source_template)
                    content = template.render(**variables)

                    # Write the file
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    result['created'].append(str(rendered_path))

                except TemplateNotFound:
                    raise FlutterGeneratorError(
                        f"Template not found: {source_template}\n"
                        f"Expected at: {template_file_path}"
                    )
                except Exception as e:
                    raise FlutterGeneratorError(
                        f"Error rendering template '{source_template}': {e}"
                    )
            else:
                raise FlutterGeneratorError(
                    f"Invalid type '{item_type}' in structure. Must be 'dir' or 'file'."
                )

    def _run_flutter_hook(
        self,
        hook_name: str,
        variables: Dict[str, Any],
        output_dir: Path
    ) -> None:
        """
        Execute a Flutter hook script.

        Args:
            hook_name: Name of the hook (pre_gen, post_gen)
            variables: Variables to pass to the hook
            output_dir: Output directory
        """
        if not self.manifest:
            return

        hooks = self.manifest.get('hooks', {})
        hook_config = hooks.get(hook_name)

        if not hook_config:
            return

        script_path = self.template_path / hook_config.get('script')

        if not script_path.exists():
            print(f"⚠️  Warning: Flutter hook script not found: {script_path}")
            return

        description = hook_config.get('description', f'Running {hook_name} hook')
        print(f"🔧 {description}...")

        # Prepare environment variables with Flutter specifics
        env = os.environ.copy()
        for key, value in variables.items():
            env[f"FLUTTER_{key.upper()}"] = str(value)

        # Add Flutter specific environment variables
        env['OUTPUT_DIR'] = str(output_dir)
        env['PROJECT_DIR'] = str(output_dir / variables.get('project_name', 'flutter_app'))

        try:
            result = subprocess.run(
                ['bash', str(script_path)],
                env=env,
                cwd=output_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout for flutter create
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                raise FlutterGeneratorError(
                    f"Flutter hook {hook_name} failed: {error_msg}"
                )
            elif result.stdout:
                print(result.stdout.strip())

        except subprocess.TimeoutExpired:
            raise FlutterGeneratorError(f"Flutter hook {hook_name} timed out")
        except Exception as e:
            raise FlutterGeneratorError(f"Error running Flutter hook {hook_name}: {e}")

    def generate(
        self,
        variables: Dict[str, Any],
        output_dir: Path,
        force: bool = False,
        dry_run: bool = False
    ) -> Dict[str, List[str]]:
        """
        Generate the Flutter project structure.

        Args:
            variables: User-provided variable values
            output_dir: Directory to create the project in
            force: Overwrite existing files
            dry_run: Show what would be created without creating it

        Returns:
            Dictionary with 'created', 'skipped', or 'would_create' lists
        """
        if not self.manifest:
            raise FlutterGeneratorError(
                "Manifest not loaded. Call load_manifest() first."
            )

        # Check if Flutter is installed
        if not dry_run and not _check_flutter_installed():
            raise FlutterGeneratorError(
                "Flutter is not installed or not in PATH. "
                "Please install Flutter from https://flutter.dev/docs/get-started/install"
            )

        # Validate inputs with Flutter specific rules
        from .flutter_manifest_loader import FlutterManifestLoader
        loader = FlutterManifestLoader(self.template_path)
        errors = loader.validate_user_input(self.manifest, variables)

        if errors:
            raise FlutterGeneratorError(
                "Flutter validation errors:\n" + "\n".join(f"  • {e}" for e in errors)
            )

        # Compute all variables with Flutter specifics
        all_variables = self._compute_flutter_variables(variables)

        output_dir = Path(output_dir)
        project_dir = output_dir / all_variables.get('project_name', 'flutter_app')

        result = {
            'created': [],
            'skipped': [],
            'would_create': []
        }

        if dry_run:
            result['would_create'].append(str(project_dir))
            print(f"Would create Flutter project at: {project_dir}")
            print(f"  Package name: {all_variables.get('package_name')}")
            print(f"  API protocol: {all_variables.get('api_protocol')}")
            return result

        # Check if project already exists
        if project_dir.exists() and not force:
            raise FlutterGeneratorError(
                f"Project directory already exists: {project_dir}\n"
                "Use --force to overwrite."
            )

        # Run pre-generation hook (creates Flutter project)
        try:
            self._run_flutter_hook('pre_gen', all_variables, output_dir)
            result['created'].append(str(project_dir))
        except FlutterGeneratorError as e:
            raise FlutterGeneratorError(f"Failed to create Flutter project: {e}")

        # Process structure (create directories and files from templates)
        if project_dir.exists():
            try:
                self._process_structure(all_variables, output_dir, force, result)
            except FlutterGeneratorError as e:
                raise FlutterGeneratorError(f"Failed to process structure: {e}")

        # Run post-generation hook (installs packages)
        if project_dir.exists():
            try:
                self._run_flutter_hook('post_gen', all_variables, output_dir)
            except FlutterGeneratorError as e:
                print(f"⚠️  Warning: Post-generation setup had issues: {e}")

        return result