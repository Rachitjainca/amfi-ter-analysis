"""
AMFI TER Analysis for GitHub Actions
Runs daily to compare TER changes and generate reports
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ter_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create directories
Path('downloads').mkdir(exist_ok=True)
Path('output').mkdir(exist_ok=True)
Path('logs').mkdir(exist_ok=True)
Path('history').mkdir(exist_ok=True)

STATE_FILE = 'ter_state.json'
API_URL = 'https://www.amfiindia.com/api/populate-te-rdata-revised'

def get_default_state():
    """Get default state structure"""
    today = datetime.now().date()
    return {
        'last_processed_date': str(today),
        'month_year': f"{today.year}-{today.month:02d}",
        'file_history': {},
        'daily_snapshots': {}
    }

def load_state():
    """Load state from JSON file and validate/migrate schema"""
    default_state = get_default_state()
    
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                loaded_state = json.load(f)
            
            for key in default_state.keys():
                if key not in loaded_state:
                    logger.info(f"Missing key '{key}' in state, using default value")
                    loaded_state[key] = default_state[key]
            
            if 'month_year' not in loaded_state and 'last_year' in loaded_state and 'last_month' in loaded_state:
                loaded_state['month_year'] = f"{loaded_state['last_year']}-{loaded_state['last_month']:02d}"
                logger.info(f"Migrated old state format to new format: month_year={loaded_state['month_year']}")
            
            return loaded_state
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            return default_state
    return default_state

def save_state(state):
    """Save state to JSON file"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        logger.info("State saved successfully")
    except Exception as e:
        logger.error(f"Error saving state: {e}")

def download_ter_file(year, month):
    """Download TER file from AMFI API"""
    try:
        logger.info(f"Downloading TER file for {year}-{month:02d}...")
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        filename = f"downloads/TER_{year}_{month:02d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        with open(filename, 'wb') as f:
            f.write(response.content)
        logger.info(f"Downloaded: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error downloading TER file: {e}")
        return None

def analyze_and_report():
    """Main analysis function"""
    logger.info("Starting AMFI TER Analysis")
    state = load_state()
    today = datetime.now().date()
    logger.info(f"Current date: {today}")
