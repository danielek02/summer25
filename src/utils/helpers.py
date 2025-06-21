import logging
from typing import Dict, Any
import json
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def save_to_json(data: Dict[str, Any], filename: str) -> None:
    """Save data to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Successfully saved data to {filename}")
    except Exception as e:
        logger.error(f"Error saving data to {filename}: {str(e)}")

def load_from_json(filename: str) -> Dict[str, Any]:
    """Load data from a JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded data from {filename}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {filename}: {str(e)}")
        return {}

def get_timestamp() -> str:
    """Get current timestamp in a formatted string."""
    return datetime.now().strftime("%Y%m%d_%H%M%S") 