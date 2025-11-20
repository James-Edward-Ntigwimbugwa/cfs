"""
Spring Boot specific project generator.
Handles Java/Kotlin project generation with Spring Boot conventions.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from cfs.modules.templates.springboot.core.exceptions.spring_generator_error import SpringGeneratorError


class SpringGenerator:
    """Generates Spring Boot projects from templates."""

    def __init__(self, template_path: Path):
        """
        Initialize the Spring Boot generator.

        Args:
            template_path: Path to the Spring Boot template directory
        """
        self.template_path = Path(template_path)
        self.manifest = None
        self.jinja_env = None

    def load_manifest(self) -> Dict[str, Any]:
        """
        Load the Spring Boot template manifest.

        Returns:
            Parsed manifest dictionary
        """
        from .spring_manifest_loader import SpringManifestLoader

        loader = SpringManifestLoader(self.template_path)
        self.manifest = loader.load()

        # Set up Jinja2 environment with Spring Boot specific filters
        files_source = self.manifest.get('files_source', 'src_templates')
        template_files_path = self.template_path / files_source

        if not template_files_path.exists():
            raise SpringGeneratorError(
                f"Spring Boot template files directory not found: {template_files_path}"
            )

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_files_path)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        # Add Spring Boot specific filters
        self.jinja_env.filters['to_package_path'] = self._to_package_path
        self.jinja_env.filters['to_class_name'] = self._to_class_name
        self.jinja_env.filters['to_artifact_id'] = self._to_artifact_id

        return self.manifest

    @staticmethod
    def _to_package_path(package_name: str) -> str:
        """Convert Java package name to filesystem path."""
        return package_name.replace('.', '/')

    @staticmethod
    def _to_class_name(project_name: str) -> str:
        """Convert project name to Java class name."""
        # Convert hyphenated name to PascalCase
        parts = project_name.replace('-', ' ').replace('_', ' ').split()
        return ''.join(word.capitalize() for word in parts)

    @staticmethod
    def _to_artifact_id(name: str) -> str:
        """Convert name to Maven artifact ID format."""
        return name.lower().replace('_', '-').replace(' ', '-')

    def _compute_spring_variables(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute Spring Boot specific derived variables.

        Args:
            variables: User-provided variables

        Returns:
            Variables with Spring Boot computed values added
        """
        if not self.manifest:
            raise SpringGeneratorError("Manifest not loaded")

        # Start with user variables
        all_vars = variables.copy()

        # Add defaults for missing variables
        for var_name, var_config in self.manifest.get('variables', {}).items():
            if var_name not in all_vars and 'default' in var_config:
                all_vars[var_name] = var_config['default']

        # Compute Spring Boot specific variables
        computed = self.manifest.get('computed', {})
        for computed_name, computed_expr in computed.items():
            try:
                # Create a Jinja2 template from the expression
                template = self.jinja_env.from_string(computed_expr)
                all_vars[computed_name] = template.render(**all_vars)
            except Exception as e:
                raise SpringGeneratorError(
                    f"Error computing Spring Boot variable '{computed_name}': {e}"
                )

        # Add additional Spring Boot computed variables
        if 'package_name' in all_vars:
            all_vars['package_path'] = self._to_package_path(all_vars['package_name'])

        if 'project_name' in all_vars:
            all_vars['main_class_name'] = self._to_class_name(all_vars['project_name']) + 'Application'
            all_vars['artifact_id'] = self._to_artifact_id(all_vars['project_name'])

        if 'language' in all_vars:
            all_vars['language_dir'] = 'kotlin' if all_vars['language'] == 'kt' else 'java'
            all_vars['file_extension'] = all_vars['language']

        # Set group_id if not provided
        if 'group_id' not in all_vars and 'package_name' in all_vars:
            # Use first two parts of package name as group_id
            parts = all_vars['package_name'].split('.')
            all_vars['group_id'] = '.'.join(parts[:2]) if len(parts) >= 2 else all_vars['package_name']

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
            raise SpringGeneratorError(f"Error rendering path '{path_template}': {e}")

    def _run_spring_hook(self, hook_name: str, variables: Dict[str, Any], project_dir: Path) -> None:
        """
        Execute a Spring Boot hook script.

        Args:
            hook_name: Name of the hook (pre_gen, post_gen)
            variables: Variables to pass to the hook
            project_dir: Project directory for post_gen hooks
        """
        if not self.manifest:
            return

        hooks = self.manifest.get('hooks', {})
        hook_config = hooks.get(hook_name)

        if not hook_config:
            return

        script_path = self.template_path / hook_config.get('script')

        if not script_path.exists():
            print(f"⚠️  Warning: Spring Boot hook script not found: {script_path}")
            return

        description = hook_config.get('description', f'Running {hook_name} hook')
        print(f"🔧 {description}...")

        # Prepare environment variables with Spring Boot specifics
        env = os.environ.copy()
        for key, value in variables.items():
            env[f"SPRING_{key.upper()}"] = str(value)

        # Add Spring Boot specific environment variables
        env['SPRING_BOOT_VERSION'] = variables.get('spring_boot_version', '3.2.0')
        env['PROJECT_DIR'] = str(project_dir)

        try:
            # Run from project directory for post_gen, template dir for pre_gen
            cwd = project_dir if hook_name == 'post_gen' else self.template_path

            result = subprocess.run(
                ['bash', str(script_path)],
                env=env,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                print(f"⚠️  Warning: Spring Boot hook {hook_name} failed: {result.stderr}")
            elif result.stdout:
                print(result.stdout.strip())

        except subprocess.TimeoutExpired:
            print(f"⚠️  Warning: Spring Boot hook {hook_name} timed out")
        except Exception as e:
            print(f"⚠️  Warning: Error running Spring Boot hook {hook_name}: {e}")

    def _create_spring_project_structure(
        self,
        variables: Dict[str, Any],
        output_dir: Path,
        force: bool,
        dry_run: bool
    ) -> Dict[str, List[str]]:
        """
        Create the Spring Boot project structure.

        Args:
            variables: Computed variables
            output_dir: Output directory
            force: Overwrite existing files
            dry_run: Preview mode

        Returns:
            Dictionary with created/skipped/would_create lists
        """
        result = {
            'created': [],
            'skipped': [],
            'would_create': []
        }

        structure = self.manifest.get('structure', [])

        for item in structure:
            item_type = item['type']
            path_template = item['path']

            # Render the path
            rendered_path = self._render_path(path_template, variables)
            full_path = output_dir / rendered_path

            if dry_run:
                result['would_create'].append(str(rendered_path))
                continue

            if item_type == 'dir':
                # Create directory
                if full_path.exists():
                    result['skipped'].append(str(rendered_path))
                else:
                    full_path.mkdir(parents=True, exist_ok=True)
                    result['created'].append(str(rendered_path))

            elif item_type == 'file':
                # Check if file exists
                if full_path.exists() and not force:
                    result['skipped'].append(str(rendered_path))
                    continue

                # Ensure parent directory exists
                full_path.parent.mkdir(parents=True, exist_ok=True)

                # Get source template
                source_template = item.get('source')
                if not source_template:
                    raise SpringGeneratorError(
                        f"No source specified for Spring Boot file: {path_template}"
                    )

                # Render source template name (for dynamic extensions)
                source_template = self._render_path(source_template, variables)

                try:
                    # Load and render the template
                    template = self.jinja_env.get_template(source_template)
                    content = template.render(**variables)

                    # Write the file
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    result['created'].append(str(rendered_path))

                except TemplateNotFound:
                    raise SpringGeneratorError(
                        f"Spring Boot template file not found: {source_template}\n"
                        f"Expected at: {self.template_path / self.manifest.get('files_source', 'src_templates') / source_template}"
                    )
                except Exception as e:
                    raise SpringGeneratorError(
                        f"Error rendering Spring Boot template '{source_template}': {e}"
                    )

        return result

    def generate(
        self,
        variables: Dict[str, Any],
        output_dir: Path,
        force: bool = False,
        dry_run: bool = False
    ) -> Dict[str, List[str]]:
        """
        Generate the Spring Boot project structure.

        Args:
            variables: User-provided variable values
            output_dir: Directory to create the project in
            force: Overwrite existing files
            dry_run: Show what would be created without creating it

        Returns:
            Dictionary with 'created', 'skipped', or 'would_create' lists
        """
        if not self.manifest:
            raise SpringGeneratorError(
                "Manifest not loaded. Call load_manifest() first."
            )

        # Validate inputs with Spring Boot specific rules
        from .spring_manifest_loader import SpringManifestLoader
        loader = SpringManifestLoader(self.template_path)
        errors = loader.validate_user_input(self.manifest, variables)

        if errors:
            raise SpringGeneratorError(
                "Spring Boot validation errors:\n" + "\n".join(f"  • {e}" for e in errors)
            )

        # Compute all variables with Spring Boot specifics
        all_variables = self._compute_spring_variables(variables)

        output_dir = Path(output_dir)
        project_dir = output_dir / all_variables.get('project_name', 'spring-app')

        # Run pre-generation hook
        if not dry_run:
            self._run_spring_hook('pre_gen', all_variables, project_dir)

        # Create Spring Boot project structure
        result = self._create_spring_project_structure(
            all_variables,
            output_dir,
            force,
            dry_run
        )

        # Run post-generation hook
        if not dry_run and project_dir.exists():
            self._run_spring_hook('post_gen', all_variables, project_dir)

        return result