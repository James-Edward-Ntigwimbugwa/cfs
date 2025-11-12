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
    Uses match/case for framework selection (Python 3.10+).
    
    Args:
        template_name: Name of the framework template
        
    Returns:
        Tuple of (GeneratorClass, ManifestLoaderClass)
        
    Raises:
        ImportError: If framework modules cannot be loaded
    """
    match template_name:
        case 'springboot':
            try:
                from modules.templates.springboot.core.spring_manifest_loader import SpringGenerator
                from modules.templates.springboot.core.spring_manifest_loader import SpringManifestLoader
                return SpringGenerator, SpringManifestLoader
            except ImportError as e:
                raise ImportError(f"Failed to load Spring Boot modules: {e}")
        
        # case 'flutter':
        #     try:
        #         from modules.templates.flutter.core.flutter_generator import FlutterGenerator
        #         from modules.templates.flutter.core.flutter_manifest_loader import FlutterManifestLoader
        #         return FlutterGenerator, FlutterManifestLoader
        #     except ImportError as e:
        #         raise ImportError(f"Failed to load Flutter modules: {e}")
        
        # case 'react':
        #     try:
        #         from modules.templates.react.core.react_generator import ReactGenerator
        #         from modules.templates.react.core.react_manifest_loader import ReactManifestLoader
        #         return ReactGenerator, ReactManifestLoader
        #     except ImportError as e:
        #         raise ImportError(f"Failed to load React modules: {e}")
        
        # case 'django':
        #     try:
        #         from modules.templates.django.core.django_generator import DjangoGenerator
        #         from modules.templates.django.core.django_manifest_loader import DjangoManifestLoader
        #         return DjangoGenerator, DjangoManifestLoader
        #     except ImportError as e:
        #         raise ImportError(f"Failed to load Django modules: {e}")
        
        # case 'nextjs':
        #     try:
        #         from modules.templates.nextjs.core.nextjs_generator import NextJSGenerator
        #         from modules.templates.nextjs.core.nextjs_manifest_loader import NextJSManifestLoader
        #         return NextJSGenerator, NextJSManifestLoader
        #     except ImportError as e:
        #         raise ImportError(f"Failed to load Next.js modules: {e}")
        
        # case 'fastapi':
        #     try:
        #         from modules.templates.fastapi.core.fastapi_generator import FastAPIGenerator
        #         from modules.templates.fastapi.core.fastapi_manifest_loader import FastAPIManifestLoader
        #         return FastAPIGenerator, FastAPIManifestLoader
        #     except ImportError as e:
        #         raise ImportError(f"Failed to load FastAPI modules: {e}")
        
        # case 'express':
        #     try:
        #         from modules.templates.express.core.express_generator import ExpressGenerator
        #         from modules.templates.express.core.express_manifest_loader import ExpressManifestLoader
        #         return ExpressGenerator, ExpressManifestLoader
        #     except ImportError as e:
        #         raise ImportError(f"Failed to load Express modules: {e}")
        
        # case 'vue':
        #     try:
        #         from modules.templates.vue.core.vue_generator import VueGenerator
        #         from modules.templates.vue.core.vue_manifest_loader import VueManifestLoader
        #         return VueGenerator, VueManifestLoader
        #     except ImportError as e:
        #         raise ImportError(f"Failed to load Vue modules: {e}")
        
        case _:
            raise ImportError(
                f"Unknown template '{template_name}'. "
                f"Supported frameworks: springboot, flutter, react, django, nextjs, fastapi, express, vue"
            )


def list_available_templates() -> None:
    """List all available templates by scanning the templates directory."""
    base_dir = Path(__file__).resolve().parent
    templates_dir = (base_dir / 'modules' / 'templates').resolve()
    
    if not templates_dir.exists():
        click.echo("No templates directory found.", err=True)
        return
    
    click.echo("\nAvailable templates:", err=True)
    for tpl in sorted(templates_dir.iterdir()):
        if tpl.is_dir() and (tpl / 'manifest.yml').exists():
            # Try to load manifest to get description
            try:
                import yaml
                with open(tpl / 'manifest.yml', 'r') as f:
                    manifest = yaml.safe_load(f)
                    description = manifest.get('description', 'No description')
                    click.echo(f"  • {tpl.name:15} - {description}", err=True)
            except:
                click.echo(f"  • {tpl.name}", err=True)


@click.group()
@click.version_option(version='1.0.0', prog_name='CFS')
def main():
    """CFS - Common Folder Structure Generator
    
    A framework-specific, manifest-driven project scaffold generator
    that creates consistent project structures from templates.
    
    Each framework has its own specialized generator and validation rules.
    """
    pass


@main.command()
@click.argument('template_name')
@click.option('--project-name', '-p', help='Name of the project')
@click.option('--package-name', help='Base package name (for Java/Kotlin projects)')
@click.option('--language', '-l', help='Programming language (e.g., java, kt, ts)')
@click.option('--api-protocol', '-a', help='API protocol (e.g., rest, graphql, websocket)')
@click.option('--output-dir', '-o', default='.', help='Output directory (default: current)')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing files')
@click.option('--dry-run', is_flag=True, help='Preview without creating files')
@click.option('--debug', is_flag=True, help='Show debug information')
def init(template_name, project_name, package_name, language, api_protocol, 
         output_dir, force, dry_run, debug):
    """Initialize a new project from a framework template.
    
    TEMPLATE_NAME: The framework template to use
    
    Examples:
        cfs init springboot -p my-api -l java -a rest
        cfs init flutter -p my_app
        cfs init react -p my-web-app --typescript
        cfs init django -p my_site
    """
    
    # Get the templates directory
    base_dir = Path(__file__).resolve().parent
    template_path = (base_dir / 'modules' / 'templates' / template_name).resolve()
    
    if not template_path.exists():
        click.echo(f"❌ Template '{template_name}' not found.", err=True)
        list_available_templates()
        sys.exit(1)
    
    # Load framework-specific modules
    try:
        GeneratorClass, ManifestLoaderClass = get_framework_modules(template_name)
    except ImportError as e:
        click.echo(f"❌ {e}", err=True)
        if debug:
            raise
        sys.exit(1)
    
    # Create generator instance
    generator = GeneratorClass(template_path)
    
    # Load manifest
    try:
        manifest = generator.load_manifest()
        if debug:
            click.echo(f"✓ Loaded {template_name} manifest", err=True)
    except Exception as e:
        click.echo(f"❌ Error loading manifest: {e}", err=True)
        if debug:
            raise
        sys.exit(1)
    
    # Collect variables (from options or prompt)
    variables = {}
    manifest_vars = manifest.get('variables', {})
    
    for var_name, var_config in manifest_vars.items():
        # Check if provided via CLI
        cli_value = None
        
        # Map common CLI options to variable names
        if var_name == 'project_name':
            cli_value = project_name
        elif var_name == 'package_name':
            cli_value = package_name
        elif var_name == 'language':
            cli_value = language
        elif var_name == 'api_protocol':
            cli_value = api_protocol
        
        if cli_value:
            variables[var_name] = cli_value
        else:
            # Prompt for value
            var_type = var_config.get('type', 'string')
            var_default = var_config.get('default')
            var_prompt = var_config.get('prompt', var_name.replace('_', ' ').title())
            var_choices = var_config.get('choices')
            
            if var_choices:
                variables[var_name] = click.prompt(
                    var_prompt,
                    type=click.Choice(var_choices),
                    default=var_default,
                    show_choices=True
                )
            elif var_type == 'boolean':
                variables[var_name] = click.confirm(
                    var_prompt,
                    default=var_default if var_default is not None else False
                )
            else:
                variables[var_name] = click.prompt(
                    var_prompt,
                    default=var_default if var_default else None,
                    show_default=True if var_default else False
                )
    
    # Display what will be created
    click.echo(f"\n📦 Generating {template_name} project:")
    for key, value in variables.items():
        display_key = key.replace('_', ' ').title()
        click.echo(f"   {display_key}: {value}")
    click.echo(f"   Output directory: {output_dir}\n")
    
    if dry_run:
        click.echo("🔍 DRY RUN - No files will be created\n")
    
    # Generate the project
    try:
        result = generator.generate(
            variables=variables,
            output_dir=Path(output_dir),
            force=force,
            dry_run=dry_run
        )
        
        if dry_run:
            click.echo("Would create:")
            for item in result['would_create']:
                click.echo(f"   ✓ {item}")
        else:
            if result['created']:
                click.echo("✨ Created files:")
                for item in result['created']:
                    click.echo(f"   ✓ {item}")
            
            if result.get('skipped'):
                click.echo(f"\n⚠️  Skipped (already exist):")
                for item in result['skipped']:
                    click.echo(f"   - {item}")
        
        project_dir = Path(output_dir) / variables.get('project_name', '')
        click.echo(f"\n🎉 Done! Your {template_name} project is ready at: {project_dir}")
        
        # Show next steps based on framework
        show_next_steps(template_name, variables)
        
    except Exception as e:
        click.echo(f"\n❌ Error during generation: {e}", err=True)
        if debug:
            raise
        sys.exit(1)


def show_next_steps(template_name: str, variables: dict) -> None:
    """Show framework-specific next steps after generation."""
    click.echo("\n📋 Next steps:")
    
    match template_name:
        case 'springboot':
            click.echo("   1. cd into your project directory")
            click.echo("   2. Run: ./mvnw spring-boot:run")
            click.echo("   3. Open http://localhost:8080")
        
        case 'flutter':
            click.echo("   1. cd into your project directory")
            click.echo("   2. Run: flutter pub get")
            click.echo("   3. Run: flutter run")
        
        case 'react':
            click.echo("   1. cd into your project directory")
            click.echo("   2. Run: npm install")
            click.echo("   3. Run: npm start")
        
        case 'django':
            click.echo("   1. cd into your project directory")
            click.echo("   2. Run: pip install -r requirements.txt")
            click.echo("   3. Run: python manage.py runserver")
        
        case 'nextjs':
            click.echo("   1. cd into your project directory")
            click.echo("   2. Run: npm install")
            click.echo("   3. Run: npm run dev")
        
        case 'fastapi':
            click.echo("   1. cd into your project directory")
            click.echo("   2. Run: pip install -r requirements.txt")
            click.echo("   3. Run: uvicorn main:app --reload")
        
        case _:
            click.echo("   1. cd into your project directory")
            click.echo("   2. Check README.md for instructions")


@main.command()
def list():
    """List all available framework templates."""
    list_available_templates()


if __name__ == '__main__':
    main()