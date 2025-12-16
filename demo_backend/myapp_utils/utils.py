from datetime import datetime
import json
import os
import random
import re
import string
import uuid
from django.conf import settings
import xmltodict


class Utils:
    @classmethod
    def is_valid_uuid(cls, value):
        try:
            uuid.UUID(str(value))

            return True
        except ValueError:
            return False

    @classmethod
    def remove_html_tags(cls, text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    @classmethod
    def generate_random_characters(cls, length):
        if length is None:
            letters = string.ascii_letters + string.digits
            result_str = ''.join(random.choice(letters) for i in range(random.randint(2, 5) * 20))
        else:
            letters = string.ascii_letters + string.digits
            result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
    
    @classmethod
    def remove_special_characters(cls, input_string):
        without_html_tags = re.sub(r'<[^>]*>', '', input_string)
        # Using regex to replace any character that is not alphanumeric or a space with an empty string
        return re.sub(r'[^a-zA-Z0-9\s]', '', without_html_tags)

    @staticmethod
    def validate_and_normalize_phone(phone_number: str, default_country_code: str = "255") -> dict:
        """
        Validate and normalize phone numbers to numeric-only E.164 format (no '+').
        - Accepts numbers with or without country code.
        - Converts local Tanzanian numbers (07..., 06..., 05...) to 255 format.
        - Returns dict with `is_valid`, `message`, and `normalized` (e.g. 255713000111).
        """

        if not phone_number:
            return {"is_valid": False, "message": "Phone number is missing.", "normalized": None}

        # Remove spaces, dashes, and plus sign
        phone_number = phone_number.strip().replace(" ", "").replace("-", "").replace("+", "")

        # Pattern for international numeric format (starts with country code)
        intl_pattern = re.compile(r"^[1-9]\d{7,14}$")

        # Pattern for local Tanzanian formats: 0XXXXXXXXX
        local_pattern = re.compile(r"^0\d{9}$")

        # Validate phone number length
        if len(phone_number) not in [10, 12]:
            return {
                "is_valid": False,
                "message": f"Phone number length is invalid. Expected 10 digits (local) or 12 digits (with country code {default_country_code}).",
                "normalized": None
            }

        # Case 1: Local TZ number (07..., 06..., 05...)
        if local_pattern.match(phone_number):
            normalized = default_country_code + phone_number[1:]
            return {
                "is_valid": True,
                "message": "Converted local number to international numeric format.",
                "normalized": normalized
            }

        # Case 2: Already includes country code (e.g. 2557xxxxxxx)
        if phone_number.startswith(default_country_code) and intl_pattern.match(phone_number):
            return {
                "is_valid": True,
                "message": "Valid international phone number.",
                "normalized": phone_number
            }   

        
        # Invalid
        return {
            "is_valid": False,
            "message": f"Invalid phone number format. Use {default_country_code}XXXXXXXXX.",
            "normalized": None
        }

    @classmethod
    def epoch_to_datetime(cls, epoch_ms: int) -> str:
        """
        Convert an epoch timestamp in milliseconds to a human-readable UTC datetime string.

        Args:
            epoch_ms (int): The epoch timestamp in milliseconds.

        Returns:
            str: The corresponding UTC datetime as a string in 'YYYY-MM-DD HH:MM:SS' format.
        """
        # Convert milliseconds to seconds
        epoch_s = epoch_ms / 1000

        # Create a datetime object from the epoch timestamp
        dt = datetime.fromtimestamp(epoch_s)

        # Format the datetime object into a readable string
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')

        return formatted_time
    
    @classmethod
    def parse_xml_to_json(cls, xml_response: str):
        """
        Convert an XML string to a JSON string.
        :param xml_string: A string containing XML data.
        :return: A string containing the JSON representation of the XML data.
        """
        xml_dict = xmltodict.parse(xml_response)
        json_string = json.dumps(xml_dict, indent=4)
        return json_string
        
    @classmethod
    def read_json_features(cls):
        """
        Reads a JSON file and returns its contents as a dictionary.
        :return: A dictionary containing the JSON data.
        """
        # Construct the full file path
        full_path = os.path.join(settings.BASE_DIR, 'myapp_subscriptions/packages/features.json')
        
        try:
            with open(full_path, 'r') as file:
                features_json = json.load(file)
            return features_json
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {full_path} was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"The file at {full_path} is not a valid JSON file.")

    @classmethod
    def read_json_meeting_control(cls):
        """
        Reads a JSON file and returns its contents as a dictionary.
        :return: A dictionary containing the JSON data.
        """
        # Construct the full file path
        full_path = os.path.join(settings.BASE_DIR, 'myapp_subscriptions/packages/subscriptions.json')
        
        try:
            with open(full_path, 'r') as file:
                features_json = json.load(file)
            return features_json
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {full_path} was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"The file at {full_path} is not a valid JSON file.")

    @classmethod
    def get_timezone(cls):
        """
        Returns a list of time zones with corresponding values and labels in the format:
        {"value": "timezone", "label": "(UTC+/-offset) Region/City"}

        Example of a returned item:
        {"value": "Africa/Cairo", "label": "(UTC+2:00) Cairo"}

        Returns:
            list: A list of dictionaries containing "value" and "label" keys for time zones.
        """
        time_zones = [
            { "value": "Africa/Dar_es_Salaam", "label": "(UTC+3:00) Dar es Salaam, Moscow, Nairobi, Baghdad" },
            { "value": "Pacific/Pago_Pago", "label": "(UTC-12:00) International Date Line West" },
            { "value": "Pacific/Midway", "label": "(UTC-11:00) Midway Island, Samoa" },
            { "value": "Pacific/Honolulu", "label": "(UTC-10:00) Hawaii" },
            { "value": "America/Anchorage", "label": "(UTC-9:00) Alaska" },
            { "value": "America/Los_Angeles", "label": "(UTC-8:00) Pacific Time - US and Canada" },
            { "value": "America/Denver", "label": "(UTC-7:00) Mountain Time - US and Canada" },
            { "value": "America/Chicago", "label": "(UTC-6:00) Central Time - US and Canada" },
            { "value": "America/New_York", "label": "(UTC-5:00) Eastern Time - US and Canada" },
            { "value": "America/Halifax", "label": "(UTC-4:00) Atlantic Time - Canada" },
            { "value": "America/St_Johns", "label": "(UTC-3:30) Newfoundland" },
            { "value": "America/Argentina/Buenos_Aires", "label": "(UTC-3:00) Greenland, Buenos Aires" },
            { "value": "Atlantic/Azores", "label": "(UTC-2:00) Mid-Atlantic" },
            { "value": "Atlantic/Cape_Verde", "label": "(UTC-1:00) Azores, Cape Verde Islands" },
            { "value": "Europe/London", "label": "(UTC+0:00) Greenwich Mean Time, London, Lisbon" },
            { "value": "Europe/Paris", "label": "(UTC+1:00) Central European Time, Paris, Berlin" },
            { "value": "Europe/Athens", "label": "(UTC+2:00) Eastern European Time, Cairo, Athens" },
            { "value": "Asia/Tehran", "label": "(UTC+3:30) Tehran" },
            { "value": "Asia/Dubai", "label": "(UTC+4:00) Dubai, Baku, Muscat" },
            { "value": "Asia/Kabul", "label": "(UTC+4:30) Kabul" },
            { "value": "Asia/Karachi", "label": "(UTC+5:00) Islamabad, Karachi, Tashkent" },
            { "value": "Asia/Colombo", "label": "(UTC+5:30) India Standard Time, Colombo" },
            { "value": "Asia/Kathmandu", "label": "(UTC+5:45) Kathmandu" },
            { "value": "Asia/Dhaka", "label": "(UTC+6:00) Dhaka, Almaty, Yekaterinburg" },
            { "value": "Asia/Yangon", "label": "(UTC+6:30) Yangon, Cocos Islands" },
            { "value": "Asia/Bangkok", "label": "(UTC+7:00) Bangkok, Hanoi, Jakarta" },
            { "value": "Asia/Shanghai", "label": "(UTC+8:00) Beijing, Hong Kong, Singapore, Perth" },
            { "value": "Asia/Tokyo", "label": "(UTC+9:00) Tokyo, Seoul, Yakutsk" },
            { "value": "Australia/Adelaide", "label": "(UTC+9:30) Adelaide, Darwin" },
            { "value": "Australia/Sydney", "label": "(UTC+10:00) Sydney, Melbourne, Vladivostok" },
            { "value": "Pacific/Guadalcanal", "label": "(UTC+11:00) Solomon Islands, Magadan" },
            { "value": "Pacific/Auckland", "label": "(UTC+12:00) Auckland, Fiji, Kamchatka" },
            { "value": "Pacific/Apia", "label": "(UTC+13:00) Samoa, Tonga" }
        ]
        return [(zone['value'], zone['label']) for zone in time_zones]

    @classmethod
    def generate_passcode(cls, length=8, digits=2, uppercase=2):
        """
        Generates a complex passcode containing digits, uppercase letters,  characters, and lowercase letters.

        Args:
        - length (int): The total length of the generated passcode. Must be greater than or equal to the sum of `digits`, `uppercase`.
        - digits (int): The number of digits in the passcode. Default is 2.
        - uppercase (int): The number of uppercase letters in the passcode. Default is 2.

        Returns:
        - str: A complex, randomly generated passcode.

        Raises:
        - ValueError: If the `length` is smaller than the sum of `digits`, `uppercase`.
        """
        if length < (digits + uppercase):
            raise ValueError("Length must be at least the sum of digits, uppercase letters, and  characters.")

        # Characters to pick from
        lowercase = string.ascii_lowercase
        digits_char = string.digits
        uppercase_char = string.ascii_uppercase

        # Generate the passcode with required characters
        passcode = [random.choice(digits_char) for _ in range(digits)] + [random.choice(uppercase_char) for _ in range(uppercase)] + [random.choice(lowercase) for _ in range(length - (digits + uppercase))]
        
        # Shuffle to make the passcode more random
        random.shuffle(passcode)
        return ''.join(passcode)

    
    @classmethod
    def get_secure_filename(cls, instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join("meeting_logos/", filename)
    

    @classmethod
    def generate_prefixed_code(cls, prefix="A"):
        """
        Generate a code in the format PREFIX-XXXXXXXX
        where XXXXXXXX is an 8-digit random number.
        Default prefix = A.
        Allowed prefixes: M, A, D.
        """
        allowed_prefixes = ["ACC", "M", "A", "D"]

        if prefix not in allowed_prefixes:
            raise ValueError("Prefix must be one of: 'M', 'A', 'D'.")

        number = random.randint(10_000_000, 99_999_999)  # ensure 8 digits
        return f"{prefix}-{number}"


    