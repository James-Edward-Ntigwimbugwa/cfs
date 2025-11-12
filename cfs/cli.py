# What & why: This is the user-facing CLI using Click. Responsibilities:

    # -parse command-line options,

    # -load the template manifest and defaults,

    # -prompt for variables when missing (using manifest metadata),

    # -call the generator to create the project.

# Connection: Uses cfs.core.config_loader to read manifest and cfs.core.generator to scaffold.

#!/usr/bin/env python3
"""
CLI entry point for CFS (Common Folder Structure) generator.
Uses Click for command-line interface management.
"""

import click
import sys
from pathlib import Path
from modules.templates.springboot.generator import SpringGenerator as Generator

@click.group()
@click.version_option()
def main():
    """CFS - Common Folder Structure Generator
    
    A manifest-driven project scaffold generator that creates
    consistent project structures from templates.
    """
    pass


@main.command()
@click.argument('template_name')
@click.option('--project-name', '-p', help='Name of the project')
@click.option('--package-name', help='Base package name (e.g., com.example)')
@click.option('--language', '-l', type=click.Choice(['java', 'kt']), help='Programming language')
@click.option('--api-protocol', '-a', type=click.Choice(['rest', 'graphql', 'websocket']), help='API protocol')
@click.option('--output-dir', '-o', default='.', help='Output directory (default: current directory)')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing files')
@click.option('--dry-run', is_flag=True, help='Show what would be created without creating it')
def init(template_name, project_name, package_name, language, api_protocol, output_dir, force, dry_run):
    """Initialize a new project from a template.
    
    TEMPLATE_NAME: The name of the template to use (e.g., springboot)
    
    Example:
        cfs init springboot --project-name my-api --language java --api-protocol rest
    """
    
    # Get the templates directory
    base_dir = Path(__file__).resolve().parent
    template_path = (base_dir / '..' / 'modules' / 'templates' / template_name).resolve()
    
    if not template_path.exists():
        click.echo(f"Template '{template_name}' not found.", err=True)
        click.echo(f"\nAvailable templates:", err=True)
        templates_dir = (base_dir / '..' / 'modules' / 'templates').resolve()
        for tpl in templates_dir.iterdir():
            if tpl.is_dir() and (tpl / 'manifest.yml').exists():
                click.echo(f"  - {tpl.name}", err=True)
        sys.exit(1)
    
    # Create generator instance
    generator = Generator(template_path)
    
    # Load manifest
    try:
        manifest = generator.load_manifest()
    except Exception as e:
        click.echo(f"loading manifest: {e}", err=True)
        sys.exit(1)
    
    # Collect variables (from options or prompt)
    variables = {}
    for var_name, var_config in manifest.get('variables', {}).items():
        # Check if provided via CLI
        cli_value = locals().get(var_name)
        
        if cli_value:
            variables[var_name] = cli_value
        else:
            # Prompt for value
            var_type = var_config.get('type', 'string')
            var_default = var_config.get('default')
            var_description = var_config.get('description', var_name)
            var_choices = var_config.get('choices')
            
            if var_choices:
                variables[var_name] = click.prompt(
                    var_description,
                    type=click.Choice(var_choices),
                    default=var_default
                )
            else:
                variables[var_name] = click.prompt(
                    var_description,
                    default=var_default
                )
    
    # Display what will be created
    click.echo(f"\n📦 Generating {template_name} project:")
    click.echo(f"   Project name: {variables.get('project_name', 'N/A')}")
    click.echo(f"   Language: {variables.get('language', 'N/A')}")
    click.echo(f"   API Protocol: {variables.get('api_protocol', 'N/A')}")
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
            click.echo("Project generated successfully!")
            click.echo(f"Created files:")
            for item in result['created']:
                click.echo(f"   ✓ {item}")
            
            if result.get('skipped'):
                click.echo(f"\nSkipped (already exist):")
                for item in result['skipped']:
                    click.echo(f"   - {item}")
        
        click.echo(f"\n🎉 Done! Your project is ready at: {output_dir}/{variables.get('project_name', '')}")
        
    except Exception as e:
        click.echo(f"\nError during generation: {e}", err=True)
        if '--debug' in sys.argv:
            raise
        sys.exit(1)


if __name__ == '__main__':
    main()