import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Scraping settings
SCRAPING_SETTINGS = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'TIMEOUT': 30,
    'MAX_RETRIES': 3
}

# Data storage settings
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src', 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# Create data directories if they don't exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# API settings (if needed)
API_KEYS = {
    # Add your API keys here
    # 'SOME_API_KEY': os.getenv('SOME_API_KEY')
} 