"""
Flutter Generator
"""
from pathlib import Path
from typing import Dict, Any
from .flutter_manifest_loader import FlutterManifestLoader

class FlutterGeneratorError(Exception):
    pass


class FlutterGenerator:

    def __init__(self , template_path : Path):
        """
        Initialize a Flutter Genetar
        """

        self.template_path = Path(template_path)
        self.manifest = None
        self.jinja_env = None


    def load_manifest(self) -> Dict[str , Any]:

        """
        Load manifest.yaml for Flutter projects
        """
        loader = FlutterManifestLoader(self.template_path)
        self.manifest = loader.load()