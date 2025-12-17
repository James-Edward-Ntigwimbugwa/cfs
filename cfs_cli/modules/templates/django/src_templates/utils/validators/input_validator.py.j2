import base64
import re
import sys
import uuid
from urllib.parse import urlparse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class InputValidator:
    @staticmethod
    def null_checker(object, required_fields):
        for field_name in required_fields:
            field_value = getattr(object, field_name, None)
            if field_value is None:
                return False
        return True

    @staticmethod
    def empty_and_null_checker(object, required_fields):
        for field_name in required_fields:
            field_value = getattr(object, field_name, None)
            if field_value is None or field_value == '':
                return False
        return True

    def is_valid_uuid(value):
        try:
            uuid.UUID(str(value))
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_phone_number(phone_number):
        phone_patterns = {
            'Tanzania': r'(?:\+?255|0)[67]\d{8}'
        }

        combined_pattern = r'|'.join(phone_patterns.values())
        full_pattern = f'^({combined_pattern})$'

        return bool(re.match(full_pattern, phone_number))

    
    @staticmethod
    def is_valid_nida(nida_number):
        """
        Validates a Tanzanian NIDA number.
        Must be exactly 20 digits long.
        """
        pattern = r'^\d{20}$'
        return bool(re.match(pattern, nida_number))

    @staticmethod
    def is_valid_email(email):
        validator = EmailValidator()
        try:
            validator(email)
            return True
        except ValidationError:
            return False

    @staticmethod
    def validate_base64_string_size(value):
        """
        Validates the size of a base64 string.

        Args:
            value (str): The base64 string to be validated.

        Returns:
            bool: True if the size of the decoded string is less than or equal to 10 MB (megabytes),
                  False otherwise.
        """
        # Decode the base64 string to bytes
        decoded_bytes = base64.b64decode(value)

        # Get the size of the decoded bytes in bytes
        size_in_bytes = sys.getsizeof(decoded_bytes)

        # Convert bytes to kilobytes for a more readable size
        size_in_kilobytes = size_in_bytes / 1024
        return True if size_in_kilobytes <= 10 * 1024 else False

    @staticmethod
    def is_strong_password(password):
        try:
            validate_password(password)
            return True

        except ValidationError as _:
            return False

    @staticmethod
    def is_valid_url(value):
        try:
            result = urlparse(value)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False