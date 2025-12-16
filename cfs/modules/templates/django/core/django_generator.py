from pathlib import Path
import subprocess
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader


def check_django_installed() -> bool:
    "check if python is installed"

    try:
        result = subprocess.run(
            ["python", "--version"], timeout=20, capture_output=True
        )

        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


class DjangoGenerator:
    
    def  __init__(self , template_path: Path):
        self.template_path = Path(template_path)
        self.jinja_env = None
        self.manifest = None

    
    def load_manifest(self) -> Dict[str, Any]:
        from .django_manifest_loader import DjangoManifestLoader

        loader = DjangoManifestLoader.load_manifest()

        files_source = self.manifest.get('files_source' , 'src_templates')
        template_files_path = self.template_path / files_source

        if not template_files_path.exists():
            template_files_path.mkdir(parents=True, exist_ok=True)

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_files_path)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        self.jinja_env.filters['to_package_path'] = self._to_package_path
        self.jinja_env.filters['to_snack_case'] = self._to_snak_case
        self.jinja_env.filters['to_snack_case'] = self._to_snake_case

    @staticmethod
    def _to_package_path(package_name : str) -> str:

        return package_name.replace('.' , '/')
    
    @staticmethod
    def _to_snake_case(text: str) -> str:
        text = text.replace('-' , '_')

        return text.lower()

