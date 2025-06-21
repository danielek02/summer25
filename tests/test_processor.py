import pytest
from src.data.processor import BondDataProcessor
import pandas as pd
from datetime import datetime

@pytest.fixture
def processor():
    return BondDataProcessor()

def test_extract_yield_data(processor):
    """Test yield data extraction from text."""
    test_text = """
    10-year Treasury yield: 3.5%
    2-year bond yield: 4.2%
    30-year Treasury yield: 3.8%
    """
    
    yields = processor.extract_yield_data(test_text)
    assert '10_year' in yields
    assert '2_year' in yields
    assert '30_year' in yields
    assert yields['10_year'] == 3.5
    assert yields['2_year'] == 4.2
    assert yields['30_year'] == 3.8

def test_process_bond_data(processor):
    """Test processing of bond data."""
    test_data = {
        'yields': {
            '10_year': 3.5,
            '2_year': 4.2
        },
        'results': [
            {
                'source': 'test_source',
                'content': 'test content'
            }
        ]
    }
    
    df = processor.process_bond_data(test_data)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'bond_type' in df.columns
    assert 'yield' in df.columns
    assert 'timestamp' in df.columns

def test_analyze_trends(processor):
    """Test trend analysis functionality."""
    # Create test data
    test_data = {
        'yields': {
            '10_year': 3.5,
            '2_year': 4.2
        }
    }
    
    # Process data first
    processor.process_bond_data(test_data)
    
    # Analyze trends
    analysis = processor.analyze_trends()
    assert 'summary' in analysis
    assert 'trends' in analysis
    assert 'yield_stats' in analysis['summary']

def test_export_to_csv(processor, tmp_path):
    """Test CSV export functionality."""
    # Create test data
    test_data = {
        'yields': {
            '10_year': 3.5,
            '2_year': 4.2
        }
    }
    
    # Process data
    processor.process_bond_data(test_data)
    
    # Export to CSV
    filename = tmp_path / "test_export.csv"
    success = processor.export_to_csv(str(filename))
    assert success
    assert filename.exists()
    
    # Verify CSV content
    df = pd.read_csv(filename)
    assert not df.empty
    assert 'bond_type' in df.columns
    assert 'yield' in df.columns 