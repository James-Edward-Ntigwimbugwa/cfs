"""
Flutter specific manifest loader.
Validates Flutter project configurations and Dart specific requirements.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, Any, List

from cfs_cli.modules.templates.flutter.core.exceptions.flutter_exceptions import FlutterManifestValidationError


def _validate_computed_variables(computed: Dict[str, Any]) -> None:
    """Validate Flutter computed variables."""
    required_computed = ['org_identifier' , 'app_name']

    for var in required_computed:
        if var not in computed:
            raise FlutterManifestValidationError(
                f"Missing required computed variable for Flutter: {var}"
            )


def _is_valid_flutter_project_name(project_name: str) -> bool:
    """Check if string is a valid Flutter project name."""
    # Flutter project names must be lowercase, use underscores, start with letter
    pattern = r'^[a-z][a-z0-9_]*$'
    return bool(re.match(pattern, project_name))


def _is_valid_package_name(package_name: str) -> bool:
    """Check if string is a valid package name (reverse domain notation)."""
    pattern = r'^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$'
    return bool(re.match(pattern, package_name))


def _validate_package_name_config(var_name: str, config: Dict[str, Any]) -> None:
    """Validate package_name variable configuration."""
    validation = config.get('validation')
    if not validation:
        raise FlutterManifestValidationError(
            "package_name must have validation regex for package format"
        )

    # Check that validation allows package format
    test_package = "com.example.app"
    if not re.match(validation, test_package):
        raise FlutterManifestValidationError(
            f"package_name validation regex must accept valid packages like '{test_package}'"
        )


class FlutterManifestLoader:
    """Loads and validates Flutter template manifests."""
    
    # Flutter specific constants
    VALID_API_PROTOCOLS = ['rest', 'graphql', 'websocket']
    
    def __init__(self, template_path: Path):
        """
        Initialize the Flutter manifest loader.
        
        Args:
            template_path: Path to the Flutter template directory
        """
        self.template_path = Path(template_path)
        self.manifest_path = self.template_path / "manifest.yaml"
        
    def load_manifest(self) -> Dict[str, Any]:
        """
        Load and parse the Flutter manifest file.
        
        Returns:
            Parsed manifest dictionary
            
        Raises:
            FileNotFoundError: If manifest.yml doesn't exist
            FlutterManifestValidationError: If manifest is invalid
        """
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Flutter manifest not found at {self.manifest_path}")
        
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            try:
                manifest = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise FlutterManifestValidationError(f"Invalid YAML in manifest: {e}")
        
        # Validate manifest structure
        self._validate_manifest(manifest)
        
        return manifest
    
    def _validate_manifest(self, manifest: Dict[str, Any]) -> None:
        """
        Validate the Flutter manifest structure and required fields.
        
        Args:
            manifest: The parsed manifest dictionary
            
        Raises:
            FlutterManifestValidationError: If validation fails
        """
        # Check required top-level fields
        required_fields = ['name', 'description', 'version']
        for field in required_fields:
            if field not in manifest:
                raise FlutterManifestValidationError(f"Missing required field: {field}")
        
        # Validate that this is a Flutter template
        if manifest['name'] != 'flutter':
            raise FlutterManifestValidationError(
                f"Expected Flutter template, got: {manifest['name']}"
            )
        
        # Validate variables if present
        if 'variables' in manifest:
            self._validate_flutter_variables(manifest['variables'])
        
        # Validate computed variables
        if 'computed' in manifest:
            _validate_computed_variables(manifest['computed'])
    
    def _validate_flutter_variables(self, variables: Dict[str, Any]) -> None:
        """
        Validate Flutter specific variable definitions.
        
        Args:
            variables: Dictionary of variable definitions
            
        Raises:
            FlutterManifestValidationError: If validation fails
        """
        # Required Flutter variables
        required_flutter_vars = ['project_name', 'package_name']
        for var in required_flutter_vars:
            if var not in variables:
                raise FlutterManifestValidationError(
                    f"Missing required Flutter variable: {var}"
                )
        
        for var_name, var_config in variables.items():
            if not isinstance(var_config, dict):
                raise FlutterManifestValidationError(
                    f"Variable '{var_name}' must be a dictionary"
                )
            
            # Validate Flutter specific variables
            if var_name == 'package_name':
                _validate_package_name_config(var_name, var_config)
            elif var_name == 'project_name':
                self._validate_project_name_config(var_name, var_config)
            elif var_name == 'api_protocol':
                self._validate_api_protocol_config(var_name, var_config)
            
            # General validation
            var_type = var_config.get('type', 'string')
            valid_types = ['string', 'choice', 'boolean', 'integer']
            if var_type not in valid_types:
                raise FlutterManifestValidationError(
                    f"Invalid type '{var_type}' for variable '{var_name}'"
                )
            
            # If type is choice, choices must be present
            if var_type == 'choice' and 'choices' not in var_config:
                raise FlutterManifestValidationError(
                    f"Variable '{var_name}' with type 'choice' must have 'choices' field"
                )
            
            # Validate validation regex if present
            if 'validation' in var_config:
                try:
                    re.compile(var_config['validation'])
                except re.error as e:
                    raise FlutterManifestValidationError(
                        f"Invalid validation regex for variable '{var_name}': {e}"
                    )

    def _validate_project_name_config(self, var_name: str, config: Dict[str, Any]) -> None:
        """Validate project_name variable configuration."""
        validation = config.get('validation')
        if validation:
            test_name = "my_flutter_app"
            if not re.match(validation, test_name):
                raise FlutterManifestValidationError(
                    f"project_name validation regex must accept valid Flutter names like '{test_name}'"
                )
    
    def _validate_api_protocol_config(self, var_name: str, config: Dict[str, Any]) -> None:
        """Validate api_protocol variable configuration."""
        if config.get('type') != 'choice':
            raise FlutterManifestValidationError(
                "api_protocol variable must be of type 'choice'"
            )
        
        choices = config.get('choices', [])
        for choice in choices:
            if choice not in self.VALID_API_PROTOCOLS:
                raise FlutterManifestValidationError(
                    f"Invalid api_protocol choice '{choice}'. Must be one of: {self.VALID_API_PROTOCOLS}"
                )

    def validate_user_input(
        self, 
        manifest: Dict[str, Any], 
        variables: Dict[str, Any]
    ) -> List[str]:
        """
        Validate user-provided variable values against Flutter manifest.
        
        Args:
            manifest: The loaded manifest
            variables: User-provided variable values
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        manifest_vars = manifest.get('variables', {})
        
        # Check for required Flutter variables
        required_vars = ['project_name', 'package_name']
        for var in required_vars:
            if var not in variables:
                default = manifest_vars.get(var, {}).get('default')
                if not default:
                    errors.append(f"Missing required Flutter variable: {var}")
        
        for var_name, var_config in manifest_vars.items():
            value = variables.get(var_name)
            if value is None:
                continue
            
            # Flutter specific validations
            if var_name == 'package_name':
                if not _is_valid_package_name(value):
                    errors.append(
                        f"Invalid package name: {value}. "
                        "Must be lowercase, dot-separated identifiers (e.g., com.example.app)"
                    )
            
            elif var_name == 'project_name':
                if not _is_valid_flutter_project_name(value):
                    errors.append(
                        f"Invalid Flutter project name: {value}. "
                        "Must be lowercase, use underscores, start with a letter (e.g., my_flutter_app)"
                    )
            
            elif var_name == 'api_protocol':
                if value not in self.VALID_API_PROTOCOLS:
                    errors.append(
                        f"Invalid API protocol: {value}. Must be one of: {self.VALID_API_PROTOCOLS}"
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