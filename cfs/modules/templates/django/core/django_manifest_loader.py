"""
Django specific manifest loader.
Validates Django project configurations and Python/Django specific requirements.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, Any, List

from cfs.modules.templates.django.core.exceptions.django_exceptions import DjangoManifestValidationError


def _validate_computed_variables(computed: Dict[str, Any]) -> None:
    """Validate Django computed variables."""
    required_computed = ['package_prefix', 'django_project_name']

    for var in required_computed:
        if var not in computed:
            raise DjangoManifestValidationError(
                f"Missing required computed variable for Django: {var}"
            )


def _is_valid_django_project_name(project_name: str) -> bool:
    """Check if string is a valid Django project name."""
    # Django project names must be lowercase, use underscores, start with letter
    pattern = r'^[a-z][a-z0-9_]*$'
    return bool(re.match(pattern, project_name))


def _is_valid_package_name(package_name: str) -> bool:
    """Check if string is a valid Python package name."""
    pattern = r'^[a-z][a-z0-9_]*$'
    return bool(re.match(pattern, package_name))


def _validate_package_name_config(var_name: str, config: Dict[str, Any]) -> None:
    """Validate package_name variable configuration."""
    validation = config.get('validation')
    if not validation:
        raise DjangoManifestValidationError(
            "package_name must have validation regex for Python package format"
        )

    # Check that validation allows Python package format
    test_package = "myapp"
    if not re.match(validation, test_package):
        raise DjangoManifestValidationError(
            f"package_name validation regex must accept valid Python packages like '{test_package}'"
        )


class DjangoManifestLoader:
    """Loads and validates Django template manifests."""

    # Django specific constants
    VALID_DATABASE_ENGINES = ['postgresql', 'mysql', 'sqlite']
    VALID_PYTHON_VERSIONS = ['3.9', '3.10', '3.11', '3.12']

    def __init__(self, template_path: Path):
        """
        Initialize the Django manifest loader.

        Args:
            template_path: Path to the Django template directory
        """
        self.template_path = Path(template_path)
        self.manifest_path = self.template_path / "manifest.yml"

    def load_manifest(self) -> Dict[str, Any]:
        """
        Load and parse the Django manifest file.

        Returns:
            Parsed manifest dictionary

        Raises:
            FileNotFoundError: If manifest.yml doesn't exist
            DjangoManifestValidationError: If manifest is invalid
        """
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Django manifest not found at {self.manifest_path}")

        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            try:
                manifest = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise DjangoManifestValidationError(f"Invalid YAML in manifest: {e}")

        # Validate manifest structure
        self._validate_manifest(manifest)

        return manifest

    def _validate_manifest(self, manifest: Dict[str, Any]) -> None:
        """
        Validate the Django manifest structure and required fields.

        Args:
            manifest: The parsed manifest dictionary

        Raises:
            DjangoManifestValidationError: If validation fails
        """
        # Check required top-level fields
        required_fields = ['name', 'description', 'version']
        for field in required_fields:
            if field not in manifest:
                raise DjangoManifestValidationError(f"Missing required field: {field}")

        # Validate that this is a Django template
        if manifest['name'] != 'django':
            raise DjangoManifestValidationError(
                f"Expected Django template, got: {manifest['name']}"
            )

        # Validate variables if present
        if 'variables' in manifest:
            self._validate_django_variables(manifest['variables'])

        # Validate computed variables
        if 'computed' in manifest:
            _validate_computed_variables(manifest['computed'])

    def _validate_django_variables(self, variables: Dict[str, Any]) -> None:
        """
        Validate Django specific variable definitions.

        Args:
            variables: Dictionary of variable definitions

        Raises:
            DjangoManifestValidationError: If validation fails
        """
        # Required Django variables
        required_django_vars = ['project_name', 'package_name']
        for var in required_django_vars:
            if var not in variables:
                raise DjangoManifestValidationError(
                    f"Missing required Django variable: {var}"
                )

        for var_name, var_config in variables.items():
            if not isinstance(var_config, dict):
                raise DjangoManifestValidationError(
                    f"Variable '{var_name}' must be a dictionary"
                )

            # Validate Django specific variables
            if var_name == 'package_name':
                _validate_package_name_config(var_name, var_config)
            elif var_name == 'project_name':
                self._validate_project_name_config(var_name, var_config)
            elif var_name == 'database_engine':
                self._validate_database_engine_config(var_name, var_config)
            elif var_name == 'python_version':
                self._validate_python_version_config(var_name, var_config)

            # General validation
            var_type = var_config.get('type', 'string')
            valid_types = ['string', 'choice', 'boolean', 'integer']
            if var_type not in valid_types:
                raise DjangoManifestValidationError(
                    f"Invalid type '{var_type}' for variable '{var_name}'"
                )

            # If type is choice, choices must be present
            if var_type == 'choice' and 'choices' not in var_config:
                raise DjangoManifestValidationError(
                    f"Variable '{var_name}' with type 'choice' must have 'choices' field"
                )

            # Validate validation regex if present
            if 'validation' in var_config:
                try:
                    re.compile(var_config['validation'])
                except re.error as e:
                    raise DjangoManifestValidationError(
                        f"Invalid validation regex for variable '{var_name}': {e}"
                    )

    def _validate_project_name_config(self, var_name: str, config: Dict[str, Any]) -> None:
        """Validate project_name variable configuration."""
        validation = config.get('validation')
        if validation:
            test_name = "django_backend"
            if not re.match(validation, test_name):
                raise DjangoManifestValidationError(
                    f"project_name validation regex must accept valid Django names like '{test_name}'"
                )

    def _validate_database_engine_config(self, var_name: str, config: Dict[str, Any]) -> None:
        """Validate database_engine variable configuration."""
        if config.get('type') != 'choice':
            raise DjangoManifestValidationError(
                "database_engine variable must be of type 'choice'"
            )

        choices = config.get('choices', [])
        for choice in choices:
            if choice not in self.VALID_DATABASE_ENGINES:
                raise DjangoManifestValidationError(
                    f"Invalid database_engine choice '{choice}'. Must be one of: {self.VALID_DATABASE_ENGINES}"
                )

    def _validate_python_version_config(self, var_name: str, config: Dict[str, Any]) -> None:
        """Validate python_version variable configuration."""
        default = config.get('default')
        if default and default not in self.VALID_PYTHON_VERSIONS:
            raise DjangoManifestValidationError(
                f"python_version default '{default}' must be one of: {self.VALID_PYTHON_VERSIONS}"
            )

    def validate_user_input(
            self,
            manifest: Dict[str, Any],
            variables: Dict[str, Any]
    ) -> List[str]:
        """
        Validate user-provided variable values against Django manifest.

        Args:
            manifest: The loaded manifest
            variables: User-provided variable values

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        manifest_vars = manifest.get('variables', {})

        # Check for required Django variables
        required_vars = ['project_name', 'package_name']
        for var in required_vars:
            if var not in variables:
                default = manifest_vars.get(var, {}).get('default')
                if not default:
                    errors.append(f"Missing required Django variable: {var}")

        for var_name, var_config in manifest_vars.items():
            value = variables.get(var_name)
            if value is None:
                continue

            # Django specific validations
            if var_name == 'package_name':
                if not _is_valid_package_name(value):
                    errors.append(
                        f"Invalid package name: {value}. "
                        "Must be lowercase, use underscores (e.g., myapp)"
                    )

            elif var_name == 'project_name':
                if not _is_valid_django_project_name(value):
                    errors.append(
                        f"Invalid Django project name: {value}. "
                        "Must be lowercase, use underscores, start with a letter (e.g., django_backend)"
                    )

            elif var_name == 'database_engine':
                if value not in self.VALID_DATABASE_ENGINES:
                    errors.append(
                        f"Invalid database engine: {value}. Must be one of: {self.VALID_DATABASE_ENGINES}"
                    )

            elif var_name == 'python_version':
                if value not in self.VALID_PYTHON_VERSIONS:
                    errors.append(
                        f"Invalid Python version: {value}. Must be one of: {self.VALID_PYTHON_VERSIONS}"
                    )

            # Validate against regex if present
            if 'validation' in var_config:
                pattern = var_config['validation']
                if not re.match(pattern, str(value)):
                    errors.append(
                        f"Variable '{var_name}' value '{value}' does not match pattern: {pattern}"
                    )

            # Validate choice
            if var_config.get('type') == 'choice':
                choices = var_config.get('choices', [])
                if value not in choices:
                    errors.append(
                        f"Variable '{var_name}' value '{value}' must be one of: {choices}"
                    )

        return errors