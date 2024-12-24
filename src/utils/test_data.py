from typing import Dict
import random
import string

class TestDataGenerator:
    @staticmethod
    def generate_vin() -> str:
        """Generate a random 17-character VIN"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(17))

    @staticmethod
    def generate_license_plate() -> str:
        """Generate a random license plate number"""
        letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
        numbers = ''.join(random.choice(string.digits) for _ in range(3))
        return f"{letters}{numbers}"

    @staticmethod
    def generate_ein() -> str:
        """Generate a random EIN number"""
        first = ''.join(random.choice(string.digits) for _ in range(2))
        second = ''.join(random.choice(string.digits) for _ in range(7))
        return f"{first}-{second}"