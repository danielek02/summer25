import logging
from scrapers.bond_scraper import BondScraper
from data.processor import BondDataProcessor
from utils.helpers import get_timestamp, save_to_json
import json
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_output_directories():
    """Create necessary output directories."""
    directories = ['output', 'output/raw', 'output/processed']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    # Setup output directories
    setup_output_directories()
    
    # Initialize components
    scraper = BondScraper()  # No LLM provided, will use direct search
    processor = BondDataProcessor()
    
    # Example queries
    queries = [
        "What are the current US Treasury bond yields?",
        "Find information about corporate bond market trends",
        "What are the latest government bond rates?"
    ]
    
    # Process each query
    for query in queries:
        logger.info(f"Processing query: {query}")
        try:
            # Search for bond information
            result = scraper.search_bond_info(query)
            
            # Save raw results
            timestamp = get_timestamp()
            raw_filename = f"output/raw/bond_data_{timestamp}.json"
            save_to_json(result, raw_filename)
            
            # Process the data
            processed_data = processor.process_bond_data(result)
            
            # Analyze trends
            analysis = processor.analyze_trends()
            
            # Save processed data
            processed_filename = f"output/processed/bond_analysis_{timestamp}.json"
            save_to_json(analysis, processed_filename)
            
            # Export to CSV if data is available
            if not processed_data.empty:
                csv_filename = f"output/processed/bond_data_{timestamp}.csv"
                processor.export_to_csv(csv_filename)
            
            # Print results
            print(f"\nResults for query: {query}")
            print("Raw Results:")
            print(json.dumps(result, indent=2))
            print("\nAnalysis:")
            print(json.dumps(analysis, indent=2))
            
        except Exception as e:
            logger.error(f"Error processing query '{query}': {str(e)}")

if __name__ == "__main__":
    main() 