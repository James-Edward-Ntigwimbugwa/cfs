"""
Spring Boot specific manifest loader.
Validates Spring Boot project configurations and Java/Kotlin specific requirements.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

from cfs.modules.templates.springboot.core.exceptions.spring_manifest_validation_error import SpringManifestValidationError


def _validate_computed_variables(computed: Dict[str, Any]) -> None:
    """Validate Spring Boot computed variables."""
    required_computed = ['package_path', 'main_class_name', 'language_dir', 'file_extension']

    for var in required_computed:
        if var not in computed:
            raise SpringManifestValidationError(
                f"Missing required computed variable for Spring Boot: {var}"
            )


def _validate_spring_file_path(path: str, source: str) -> None:
    """Validate Spring Boot specific file paths."""
    # Check for Application file
    if 'Application.' in path:
        if not ('{{ file_extension }}' in path or path.endswith('.java') or path.endswith('.kt')):
            raise SpringManifestValidationError(
                f"Application file must use dynamic file extension: {path}"
            )

    # Check for pom.xml or build.gradle
    if 'pom.xml' in path or 'build.gradle' in path:
        if not source:
            raise SpringManifestValidationError(
                f"Build file must have a template source: {path}"
            )


def _is_valid_java_package(package: str) -> bool:
    """Check if string is a valid Java package name."""
    pattern = r'^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$'
    return bool(re.match(pattern, package))


def _is_valid_artifact_id(artifact_id: str) -> bool:
    """Check if string is a valid Maven artifact ID."""
    pattern = r'^[a-z][a-z0-9-]*$'
    return bool(re.match(pattern, artifact_id))


def _validate_package_name_config(var_name: str, config: Dict[str, Any]) -> None:
    """Validate package_name variable configuration."""
    validation = config.get('validation')
    if not validation:
        raise SpringManifestValidationError(
            "package_name must have validation regex for Java package format"
        )

    # Check that validation allows Java package format
    test_package = "com.example.app"
    if not re.match(validation, test_package):
        raise SpringManifestValidationError(
            f"package_name validation regex must accept valid Java packages like '{test_package}'"
        )


def _validate_spring_structure(structure: List[Dict[str, Any]]) -> None:
    """
    Validate Spring Boot specific structure definitions.

    Args:
        structure: List of structure items

    Raises:
        SpringManifestValidationError: If validation fails
    """
    if not isinstance(structure, list):
        raise SpringManifestValidationError("Structure must be a list")

    # Check for required Spring Boot directories
    required_paths = [
        'src/main/{{ language_dir }}',
        'src/main/resources',
        'src/test/{{ language_dir }}'
    ]

    structure_paths = [item.get('path', '') for item in structure]

    for required in required_paths:
        # Check if any path contains the required path
        found = any(required in path for path in structure_paths)
        if not found:
            raise SpringManifestValidationError(
                f"Spring Boot structure must include: {required}"
            )

    for idx, item in enumerate(structure):
        if not isinstance(item, dict):
            raise SpringManifestValidationError(
                f"Structure item {idx} must be a dictionary"
            )

        if 'path' not in item:
            raise SpringManifestValidationError(
                f"Structure item {idx} missing required 'path' field"
            )

        if 'type' not in item:
            raise SpringManifestValidationError(
                f"Structure item {idx} missing required 'type' field"
            )

        item_type = item['type']
        if item_type not in ['dir', 'file']:
            raise SpringManifestValidationError(
                f"Structure item {idx} has invalid type '{item_type}'"
            )

        # Files must have a source
        if item_type == 'file' and 'source' not in item:
            raise SpringManifestValidationError(
                f"File structure item {idx} (path: {item['path']}) must have 'source' field"
            )

        # Validate Spring Boot file patterns
        path = item['path']
        if item_type == 'file':
            _validate_spring_file_path(path, item.get('source', ''))


class SpringManifestLoader:
    """Loads and validates Spring Boot template manifests."""
    
    # Spring Boot specific constants
    VALID_JAVA_VERSIONS = ['8', '11', '17', '21']
    VALID_SPRING_BOOT_VERSIONS = ['2.7', '3.0', '3.1', '3.2', '3.3']
    VALID_BUILD_TOOLS = ['maven', 'gradle']
    VALID_LANGUAGES = ['java', 'kt']
    VALID_API_PROTOCOLS = ['rest', 'graphql', 'websocket', 'grpc']
    
    def __init__(self, template_path: Path):
        """
        Initialize the Spring Boot manifest loader.
        
        Args:
            template_path: Path to the Spring Boot template directory
        """
        self.template_path = Path(template_path)
        self.manifest_path = self.template_path / "manifest.yml"
        
    def load(self) -> Dict[str, Any]:
        """
        Load and parse the Spring Boot manifest file.
        
        Returns:
            Parsed manifest dictionary
            
        Raises:
            FileNotFoundError: If manifest.yml doesn't exist
            SpringManifestValidationError: If manifest is invalid
        """
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Spring Boot manifest not found at {self.manifest_path}")
        
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            try:
                manifest = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise SpringManifestValidationError(f"Invalid YAML in manifest: {e}")
        
        # Validate manifest structure
        self._validate_manifest(manifest)
        
        return manifest
    
    def _validate_manifest(self, manifest: Dict[str, Any]) -> None:
        """
        Validate the Spring Boot manifest structure and required fields.
        
        Args:
            manifest: The parsed manifest dictionary
            
        Raises:
            SpringManifestValidationError: If validation fails
        """
        # Check required top-level fields
        required_fields = ['name', 'description', 'version']
        for field in required_fields:
            if field not in manifest:
                raise SpringManifestValidationError(f"Missing required field: {field}")
        
        # Validate that this is a Spring Boot template
        if manifest['name'] != 'springboot':
            raise SpringManifestValidationError(
                f"Expected Spring Boot template, got: {manifest['name']}"
            )
        
        # Validate variables if present
        if 'variables' in manifest:
            self._validate_spring_variables(manifest['variables'])
        
        # Validate structure if present
        if 'structure' in manifest:
            _validate_spring_structure(manifest['structure'])
        
        # Validate computed variables
        if 'computed' in manifest:
            _validate_computed_variables(manifest['computed'])
    
    def _validate_spring_variables(self, variables: Dict[str, Any]) -> None:
        """
        Validate Spring Boot specific variable definitions.
        
        Args:
            variables: Dictionary of variable definitions
            
        Raises:
            SpringManifestValidationError: If validation fails
        """
        # Required Spring Boot variables
        required_spring_vars = ['project_name', 'package_name', 'language']
        for var in required_spring_vars:
            if var not in variables:
                raise SpringManifestValidationError(
                    f"Missing required Spring Boot variable: {var}"
                )
        
        for var_name, var_config in variables.items():
            if not isinstance(var_config, dict):
                raise SpringManifestValidationError(
                    f"Variable '{var_name}' must be a dictionary"
                )
            
            # Validate Spring Boot specific variables
            if var_name == 'package_name':
                _validate_package_name_config(var_name, var_config)
            elif var_name == 'language':
                self._validate_language_config(var_name, var_config)
            elif var_name == 'java_version':
                self._validate_java_version_config(var_name, var_config)
            elif var_name == 'api_protocol':
                self._validate_api_protocol_config(var_name, var_config)
            
            # General validation
            var_type = var_config.get('type', 'string')
            valid_types = ['string', 'choice', 'boolean', 'integer']
            if var_type not in valid_types:
                raise SpringManifestValidationError(
                    f"Invalid type '{var_type}' for variable '{var_name}'"
                )
            
            # If type is choice, choices must be present
            if var_type == 'choice' and 'choices' not in var_config:
                raise SpringManifestValidationError(
                    f"Variable '{var_name}' with type 'choice' must have 'choices' field"
                )
            
            # Validate validation regex if present
            if 'validation' in var_config:
                try:
                    re.compile(var_config['validation'])
                except re.error as e:
                    raise SpringManifestValidationError(
                        f"Invalid validation regex for variable '{var_name}': {e}"
                    )

    def _validate_language_config(self, var_name: str, config: Dict[str, Any]) -> None:
        """Validate language variable configuration."""
        if config.get('type') != 'choice':
            raise SpringManifestValidationError(
                "language variable must be of type 'choice'"
            )
        
        choices = config.get('choices', [])
        for lang in self.VALID_LANGUAGES:
            if lang not in choices:
                raise SpringManifestValidationError(
                    f"language choices must include '{lang}'"
                )
    
    def _validate_java_version_config(self, var_name: str, config: Dict[str, Any]) -> None:
        """Validate java_version variable configuration."""
        default = config.get('default')
        if default and default not in self.VALID_JAVA_VERSIONS:
            raise SpringManifestValidationError(
                f"java_version default '{default}' must be one of: {self.VALID_JAVA_VERSIONS}"
            )
    
    def _validate_api_protocol_config(self, var_name: str, config: Dict[str, Any]) -> None:
        """Validate api_protocol variable configuration."""
        if config.get('type') != 'choice':
            raise SpringManifestValidationError(
                "api_protocol variable must be of type 'choice'"
            )
        
        choices = config.get('choices', [])
        for choice in choices:
            if choice not in self.VALID_API_PROTOCOLS:
                raise SpringManifestValidationError(
                    f"Invalid api_protocol choice '{choice}'. Must be one of: {self.VALID_API_PROTOCOLS}"
                )

    def validate_user_input(
        self, 
        manifest: Dict[str, Any], 
        variables: Dict[str, Any]
    ) -> List[str]:
        """
        Validate user-provided variable values against Spring Boot manifest.
        
        Args:
            manifest: The loaded manifest
            variables: User-provided variable values
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        manifest_vars = manifest.get('variables', {})
        
        # Check for required Spring Boot variables
        required_vars = ['project_name', 'package_name', 'language']
        for var in required_vars:
            if var not in variables and var not in manifest_vars.get(var, {}).get('default'):
                errors.append(f"Missing required Spring Boot variable: {var}")
        
        for var_name, var_config in manifest_vars.items():
            value = variables.get(var_name)
            if value is None:
                continue
            
            # Spring Boot specific validations
            if var_name == 'package_name':
                if not _is_valid_java_package(value):
                    errors.append(
                        f"Invalid Java package name: {value}. "
                        "Must be lowercase, dot-separated identifiers (e.g., com.example.app)"
                    )
            
            elif var_name == 'project_name':
                if not _is_valid_artifact_id(value):
                    errors.append(
                        f"Invalid Maven artifact ID: {value}. "
                        "Must be lowercase, use hyphens (e.g., my-spring-app)"
                    )
            
            elif var_name == 'language':
                if value not in self.VALID_LANGUAGES:
                    errors.append(
                        f"Invalid language: {value}. Must be one of: {self.VALID_LANGUAGES}"
                    )
            
            elif var_name == 'java_version':
                if value not in self.VALID_JAVA_VERSIONS:
                    errors.append(
                        f"Invalid Java version: {value}. Must be one of: {self.VALID_JAVA_VERSIONS}"
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

