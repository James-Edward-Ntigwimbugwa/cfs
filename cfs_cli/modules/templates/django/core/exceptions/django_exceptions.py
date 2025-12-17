"""
Django-specific exception classes.
"""


class DjangoManifestValidationError(Exception):
    """Raised when Django manifest validation fails."""
    pass


class DjangoGeneratorError(Exception):
    """Raised when Django generation fails."""
    pass