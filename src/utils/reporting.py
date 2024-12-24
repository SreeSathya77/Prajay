from datetime import datetime
import json
import os

class TestReport:
    def __init__(self):
        self.results = []
        
    def add_result(self, test_name, status, duration, error=None):
        self.results.append({
            'test_name': test_name,
            'status': status,
            'duration': duration,
            'error': str(error) if error else None,
            'timestamp': datetime.now().isoformat()
        })
        
    def save_report(self, path='reports'):
        os.makedirs(path, exist_ok=True)
        filename = f"{path}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)