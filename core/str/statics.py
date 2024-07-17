from typing import Final

PASSWORD_REGEX: Final = r"([^a-z0-9%*][a-z0-9%]{3,})(?:[^a-z0-9%*]|$)"

RFC_REGEX: Final = r"^([A-ZÑ&]{3,4})?(\d{2})(\d{2})(\d{2})?([A-Z\d]{2})([A\d])$"
