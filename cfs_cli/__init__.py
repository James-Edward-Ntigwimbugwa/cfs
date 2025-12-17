# Basic package init; we declare a version. Not strictly needed but useful for


def get_version() -> str:
    """Get version from package metadata or fallback to default."""
    try:
        from importlib.metadata import version
        return version("cfs-cli")
    except Exception:
        # Fallback version for development
        return "0.2.1"
    
__version__= get_version()

from .cli import main