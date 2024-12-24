"""Environment utility to detect runtime environment"""
import os

def is_running_in_docker() -> bool:
    """
    Check if the code is running inside a Docker container
    Returns True if running in Docker, False otherwise
    """
    return os.path.exists('/.dockerenv') or os.getenv('DOCKER_CONTAINER') == 'true'