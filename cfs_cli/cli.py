#!/usr/bin/env python3
"""
CLI entry point for CFS (Common Folder Structure) generator.
Uses Click for command-line interface with framework-specific generators.
"""

import click
import sys
from pathlib import Path
from typing import Tuple, Type, Any


def get_framework_modules(template_name: str) -> Tuple[Type, Type]:
    """
    Get framework-specific generator and manifest loader classes.
    Uses match/case for framework selection.

    Args:
        template_name: Name of the framework template

    Returns:
        Tuple of (GeneratorClass, ManifestLoaderClass)

    Raises:
        ImportError: If framework modules cannot be loaded
    """
    match template_name:
        case "springboot":
            from cfs_cli.modules.templates.springboot.core.spring_generator import (
                SpringGenerator,
            )
            from cfs_cli.modules.templates.springboot.core.spring_manifest_loader import (
                SpringManifestLoader,
            )
            return SpringGenerator, SpringManifestLoader
            

        case "flutter":
            from cfs_cli.modules.templates.flutter.core.flutter_generator import (
                FlutterGenerator,
            )
            from cfs_cli.modules.templates.flutter.core.flutter_manifest_loader import (
                FlutterManifestLoader,
            )
            return FlutterGenerator, FlutterManifestLoader
        

        case "django":
            from cfs_cli.modules.templates.django.core.django_generator import (
                DjangoGenerator,
            )
            from cfs_cli.modules.templates.django.core.django_manifest_loader import (
                DjangoManifestLoader,
            )
            return DjangoGenerator, DjangoManifestLoader

        case _:
            raise ImportError(
                f"Unknown template '{template_name}'. "
                f"Supported frameworks: springboot, flutter, django"
            )


def get_templates_directory() -> Path:
    """
    Get the templates directory, works both for installed package and local development.
    
    Returns:
        Path to templates directory
    """
    # Try to find templates directory in installed package
    try:
        import cfs_cli
        package_dir = Path(cfs_cli.__file__).parent
        templates_dir = package_dir / "modules" / "templates"
        if templates_dir.exists():
            return templates_dir
    except (ImportError, AttributeError):
        pass
    
    # Fallback: look relative to this file (local development)
    base_dir = Path(__file__).resolve().parent
    templates_dir = base_dir / "modules" / "templates"
    if templates_dir.exists():
        return templates_dir
    
    # Last resort: check current working directory
    cwd_templates = Path.cwd() / "modules" / "templates"
    if cwd_templates.exists():
        return cwd_templates
    
    raise FileNotFoundError(
        "Could not locate templates directory. "
        "Please ensure cfs_cli is properly installed."
    )


def list_available_templates() -> None:
    """List all available templates by scanning the templates directory."""
    try:
        templates_dir = get_templates_directory()
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        return

    if not templates_dir.exists():
        click.echo("No templates directory found.", err=True)
        return

    click.echo("\nAvailable templates:", err=True)
    for tpl in sorted(templates_dir.iterdir()):
        if tpl.is_dir() and (tpl / "manifest.yml").exists():
            # Try to load manifest to get description
            try:
                import yaml
                with open(tpl / "manifest.yml", "r") as f:
                    manifest = yaml.safe_load(f)
                    description = manifest.get("description", "No description")
                    click.echo(f"  • {tpl.name:15} - {description}", err=True)
            except:
                click.echo(f"  • {tpl.name}", err=True)


def get_version() -> str:
    """Get version from package metadata or fallback to default."""
    try:
        from importlib.metadata import version
        return version("cfs-cli")
    except Exception:
        # Fallback version for development
        return "0.2.1"


@click.group()
@click.version_option(version=get_version(), prog_name="CFS")
def main():
    """CFS - Common Folder Structure Generator

    A framework-specific, manifest-driven project scaffold generator
    that creates consistent project structures from templates.

    Each framework has its own specialized generator and validation rules.
    """
    pass


@main.command()
@click.argument("template_name")
@click.option("--project-name", "-p", help="Name of the project")
@click.option(
    "--package-name", help="Base package name (for Java/Kotlin/Django projects)"
)
@click.option("--language", "-l", help="Programming language (e.g., java, kt, ts)")
@click.option(
    "--api-protocol", "-a", help="API protocol (e.g., rest, graphql, websocket)"
)
@click.option(
    "--database-engine",
    "-d",
    help="Database engine (for Django: postgresql, mysql, sqlite)",
)
@click.option(
    "--python-version", help="Python version (for Django: 3.9, 3.10, 3.11, 3.12)"
)
@click.option("--use-graphql", is_flag=True, help="Include GraphQL support (Django)")
@click.option(
    "--use-celery", is_flag=True, help="Include Celery for async tasks (Django)"
)
@click.option(
    "--output-dir", "-o", default=".", help="Output directory (default: current)"
)
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files")
@click.option("--dry-run", is_flag=True, help="Preview without creating files")
@click.option("--debug", is_flag=True, help="Show debug information")
def init(
    template_name,
    project_name,
    package_name,
    language,
    api_protocol,
    database_engine,
    python_version,
    use_graphql,
    use_celery,
    output_dir,
    force,
    dry_run,
    debug,
):
    """Initialize a new project from a framework template.

    TEMPLATE_NAME: The framework template to use

    Examples:
        cfs init springboot -p my-api -l java -a rest
        cfs init flutter -p my_app
        cfs init django -p my_backend --package-name myapp -d postgresql --use-graphql --use-celery
        cfs init react -p my-web-app
    """

    # Get the templates directory (works for both installed package and local dev)
    try:
        templates_dir = get_templates_directory()
        template_path = templates_dir / template_name
    except FileNotFoundError as e:
        RED = "\033[91m"
        RESET = "\033[0m"
        click.echo(f"{RED}Error: {e}{RESET}", err=True)
        sys.exit(1)

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    if not template_path.exists():
        click.echo(f"{RED}Template '{template_name}' not found.{RESET}", err=True)
        list_available_templates()
        sys.exit(1)

    if debug:
        click.echo(f"Debug: Template path: {template_path}", err=True)
        click.echo(f"Debug: Template exists: {template_path.exists()}", err=True)

    # Load framework-specific modules
    try:
        GeneratorClass, ManifestLoaderClass = get_framework_modules(template_name)
        if debug:
            click.echo(f"Debug: Loaded {GeneratorClass.__name__} and {ManifestLoaderClass.__name__}", err=True)
    except ImportError as e:
        click.echo(f"{RED}{e}{RESET}", err=True)
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # Create generator instance
    generator = GeneratorClass(template_path)

    # Load manifest
    try:
        manifest = generator.load_manifest()
        if debug:
            click.echo(f"{GREEN}✓ Loaded {template_name} manifest{RESET}", err=True)
    except Exception as e:
        click.echo(f"{RED}Error loading manifest: {e}{RESET}", err=True)
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # Collect variables (from options or prompt)
    variables = {}
    manifest_vars = manifest.get("variables", {})

    for var_name, var_config in manifest_vars.items():
        # Check if provided via CLI
        cli_value = None

        # Map CLI options to variable names
        if var_name == "project_name":
            cli_value = project_name
        elif var_name == "package_name":
            cli_value = package_name
        elif var_name == "language":
            cli_value = language
        elif var_name == "api_protocol":
            cli_value = api_protocol
        elif var_name == "database_engine":
            cli_value = database_engine
        elif var_name == "python_version":
            cli_value = python_version
        elif var_name == "use_graphql":
            cli_value = use_graphql if use_graphql else None
        elif var_name == "use_celery":
            cli_value = use_celery if use_celery else None

        if cli_value is not None:
            variables[var_name] = cli_value
        else:
            # Prompt for value
            var_type = var_config.get("type", "string")
            var_default = var_config.get("default")
            var_prompt = var_config.get("prompt", var_name.replace("_", " ").title())
            var_choices = var_config.get("choices")

            if var_choices:
                # Format choices for display
                choices_str = ", ".join(var_choices)
                variables[var_name] = click.prompt(
                    f"{var_prompt} ({choices_str})",
                    type=click.Choice(var_choices),
                    default=var_default,
                    show_choices=False,
                )
            elif var_type == "boolean":
                variables[var_name] = click.confirm(
                    var_prompt,
                    default=var_default if var_default is not None else False,
                )
            else:
                variables[var_name] = click.prompt(
                    var_prompt,
                    default=var_default if var_default else None,
                    show_default=True if var_default else False,
                )

    # Display what will be created
    click.echo(f"{BLUE}📦 Generating {template_name} project:{RESET}")
    for key, value in variables.items():
        display_key = key.replace("_", " ").title()
        click.echo(f"   {display_key}: {GREEN}{value}{RESET}")
    click.echo(f"   Output directory: {GREEN}{output_dir}{RESET}\n")

    if dry_run:
        click.echo(f"{YELLOW}DRY RUN - No files will be created\n{RESET}")

    # Generate the project
    try:
        result = generator.generate(
            variables=variables,
            output_dir=Path(output_dir),
            force=force,
            dry_run=dry_run,
        )

        if dry_run:
            click.echo(f"{YELLOW}Would create:{RESET}")
            for item in result["would_create"]:
                click.echo(f"{YELLOW}   ✓ {item}{RESET}")
        else:
            if result["created"]:
                click.echo(f"{GREEN}✨ Created files:{RESET}")
                for item in result["created"][:10]:  # Show first 10
                    click.echo(f"{GREEN}   ✓ {item}{RESET}")
                if len(result["created"]) > 10:
                    click.echo(
                        f"{GREEN}   ... and {len(result['created']) - 10} more files{RESET}"
                    )

            if result.get("skipped"):
                click.echo(f"\n{YELLOW}Skipped (already exist):{RESET}")
                for item in result["skipped"][:5]:  # Show first 5
                    click.echo(f"{YELLOW}   - {item}{RESET}")
                if len(result["skipped"]) > 5:
                    click.echo(
                        f"{YELLOW}   ... and {len(result['skipped']) - 5} more files{RESET}"
                    )

        project_dir = Path(output_dir) / variables.get("project_name", "")
        click.echo(
            f"\n{GREEN}🎉 Done! Your {template_name} project is ready at: {project_dir}{RESET}\n"
        )

        # Show next steps based on framework
        show_next_steps(template_name, variables)

    except Exception as e:
        click.echo(f"\n{RED}❌ Error during generation: {e}{RESET}", err=True)
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def show_next_steps(template_name: str, variables: dict) -> None:
    """Show framework-specific next steps after generation."""
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    click.echo(f"{CYAN}📋 Next steps:{RESET}")

    match template_name:
        case "springboot":
            click.echo(f"{YELLOW}   1. cd into your project directory{RESET}")
            click.echo(f"{YELLOW}   2. Run: ./mvnw spring-boot:run{RESET}")
            click.echo(f"{YELLOW}   3. Open http://localhost:8080{RESET}")

        case "flutter":
            click.echo(f"{YELLOW}   1. cd into your project directory{RESET}")
            click.echo(f"{YELLOW}   2. Run: flutter pub get{RESET}")
            click.echo(f"{YELLOW}   3. Run: flutter run{RESET}")

        case "django":
            project_name = variables.get("project_name", "django_backend")
            click.echo(f"{YELLOW}   1. cd {project_name}{RESET}")
            click.echo(f"{YELLOW}   2. source venv/bin/activate{RESET}")
            click.echo(
                f"{YELLOW}   3. # Configure .env file with database credentials{RESET}"
            )
            click.echo(f"{YELLOW}   4. python manage.py runserver{RESET}")

        case "react":
            click.echo(f"{YELLOW}   1. cd into your project directory{RESET}")
            click.echo(f"{YELLOW}   2. Run: npm install{RESET}")
            click.echo(f"{YELLOW}   3. Run: npm start{RESET}")

        case "nextjs":
            click.echo(f"{YELLOW}   1. cd into your project directory{RESET}")
            click.echo(f"{YELLOW}   2. Run: npm install{RESET}")
            click.echo(f"{YELLOW}   3. Run: npm run dev{RESET}")

        case "fastapi":
            click.echo(f"{YELLOW}   1. cd into your project directory{RESET}")
            click.echo(f"{YELLOW}   2. Run: pip install -r requirements.txt{RESET}")
            click.echo(f"{YELLOW}   3. Run: uvicorn main:app --reload{RESET}")

        case _:
            click.echo(f"{YELLOW}   1. cd into your project directory{RESET}")
            click.echo(f"{YELLOW}   2. Check README.md for instructions{RESET}")


@main.command()
def list():
    """List all available framework templates."""
    list_available_templates()


if __name__ == "__main__":
    main()
    