import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv('BASE_URL', 'https://example.com')
        self.api_url = os.getenv('API_URL', 'http://10.10.10.61:8081/qm/cam')
        self.timeout = int(os.getenv('TIMEOUT', '30000'))
        
config = Config()