
from pathlib import Path
from typing import Dict , Any
import yaml

from cfs.modules.templates.flutter.core.exceptions.flutter_manifest_validation_error import FlutterManifestValidationError


class FlutterManifestLoader:

    def __init__(self , template_path : Path):

        self.template_path = Path(template_path)
        self.manifest_path = self.template_path / "manifest.yaml"
    
    
    def load(self) ->Dict[str , Any] :
        

        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Flutter Manifest not found at {self.manifest_path}")
        

        with open(self.manifest_path , 'r' , encoding='utf-8') as f:
            try:

                manifest = yaml.safe_load(f)
            
            except yaml.YAMLError as e:
                raise FlutterManifestValidationError