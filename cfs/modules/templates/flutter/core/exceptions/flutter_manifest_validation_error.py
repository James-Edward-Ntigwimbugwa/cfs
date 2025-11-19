from typing import Dict , Any
import re

class FlutterManifestValidationError(Exception):

    def _validate_computed_variables(computed: Dict[str , Any]) -> None:

        require_computed = ['project_name']

        for var in require_computed:

            if var not in computed:
                raise FlutterManifestValidationError(
                    f"Missing required argument for flutter : {var}"
                )
            
    def _is_valid_file_name(file_name: str) -> bool:
        """Check if string is a valid Maven artifact ID."""
        pattern = r'^[a-z][a-z0-9-]*$'
        return bool(re.match(pattern, file_name))
