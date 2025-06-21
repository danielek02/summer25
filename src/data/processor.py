import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class BondDataProcessor:
    def __init__(self):
        self.data = pd.DataFrame()
        
    def extract_yield_data(self, text: str) -> Dict[str, float]:
        """Extract yield data from text content."""
        try:
            # Common patterns for yield data
            patterns = {
                '10_year': r'10\s*-\s*year\s*(?:Treasury|bond)\s*yield[:\s]+([\d.]+)',
                '2_year': r'2\s*-\s*year\s*(?:Treasury|bond)\s*yield[:\s]+([\d.]+)',
                '30_year': r'30\s*-\s*year\s*(?:Treasury|bond)\s*yield[:\s]+([\d.]+)',
            }
            
            yields = {}
            for key, pattern in patterns.items():
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    yields[key] = float(match.group(1))
            
            return yields
        except Exception as e:
            logger.error(f"Error extracting yield data: {str(e)}")
            return {}

    def process_bond_data(self, raw_data: Dict) -> pd.DataFrame:
        """Process raw bond data into a structured DataFrame."""
        try:
            # Extract relevant information
            processed_data = []
            
            if isinstance(raw_data, dict):
                # Process yield data if present
                if 'yields' in raw_data:
                    for bond_type, yield_value in raw_data['yields'].items():
                        processed_data.append({
                            'bond_type': bond_type,
                            'yield': yield_value,
                            'timestamp': datetime.now().isoformat()
                        })
                
                # Process other bond information
                if 'results' in raw_data:
                    for result in raw_data['results']:
                        if isinstance(result, dict):
                            processed_data.append({
                                'source': result.get('source', 'unknown'),
                                'content': result.get('content', ''),
                                'timestamp': datetime.now().isoformat()
                            })
            
            # Convert to DataFrame
            df = pd.DataFrame(processed_data)
            self.data = df
            return df
            
        except Exception as e:
            logger.error(f"Error processing bond data: {str(e)}")
            return pd.DataFrame()

    def analyze_trends(self) -> Dict:
        """Analyze trends in the bond data."""
        try:
            if self.data.empty:
                return {"error": "No data available for analysis"}
            
            analysis = {
                "summary": {},
                "trends": {}
            }
            
            # Calculate basic statistics for yields
            if 'yield' in self.data.columns:
                analysis["summary"]["yield_stats"] = {
                    "mean": self.data['yield'].mean(),
                    "std": self.data['yield'].std(),
                    "min": self.data['yield'].min(),
                    "max": self.data['yield'].max()
                }
            
            # Identify trends
            if 'timestamp' in self.data.columns and 'yield' in self.data.columns:
                self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
                self.data = self.data.sort_values('timestamp')
                
                # Calculate yield changes
                if len(self.data) > 1:
                    analysis["trends"]["yield_change"] = {
                        "latest": self.data['yield'].iloc[-1],
                        "change": self.data['yield'].iloc[-1] - self.data['yield'].iloc[0],
                        "percent_change": ((self.data['yield'].iloc[-1] - self.data['yield'].iloc[0]) / 
                                         self.data['yield'].iloc[0] * 100)
                    }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {str(e)}")
            return {"error": str(e)}

    def export_to_csv(self, filename: str) -> bool:
        """Export processed data to CSV file."""
        try:
            if not self.data.empty:
                self.data.to_csv(filename, index=False)
                logger.info(f"Data exported to {filename}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return False 