from typing import Dict , Any
import re

class FlutterManifestValidationError(Exception):
    """Raised when Flutter manifest validation fails."""
    pass


    def validate_computed_variables(computed: Dict[str, Any]) -> None:
        """Validate Flutter computed variables."""
        required_computed = ['package_path']

        for var in required_computed:
            if var not in computed:
                raise FlutterManifestValidationError(
                    f"Missing required computed variable for Flutter: {var}"
                )


    def is_valid_flutter_project_name(project_name: str) -> bool:
        """Check if string is a valid Flutter project name."""
        # Flutter project names must be lowercase, use underscores, start with letter
        pattern = r'^[a-z][a-z0-9_]*$'
        return bool(re.match(pattern, project_name))


    def is_valid_package_name(package_name: str) -> bool:
        """Check if string is a valid package name (reverse domain notation)."""
        pattern = r'^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$'
        return bool(re.match(pattern, package_name))


    def validate_package_name_config(var_name: str, config: Dict[str, Any]) -> None:
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
