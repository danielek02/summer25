import pytest
from src.scrapers.bond_scraper import BondScraper
from unittest.mock import patch, MagicMock

@pytest.fixture
def scraper():
    return BondScraper()

def test_scraper_initialization(scraper):
    """Test if the scraper initializes correctly."""
    assert scraper is not None
    assert hasattr(scraper, 'search')
    assert hasattr(scraper, 'tools')
    assert len(scraper.tools) == 2

@patch('requests.get')
def test_scrape_website(mock_get, scraper):
    """Test website scraping functionality."""
    # Mock response
    mock_response = MagicMock()
    mock_response.text = "<html><body>Test content</body></html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = scraper.scrape_website("http://test.com")
    assert "Test content" in result
    mock_get.assert_called_once()

def test_save_results(scraper):
    """Test saving results functionality."""
    test_results = {"data": "test"}
    test_query = "test query"
    
    # This will create a file, but we're not testing the file contents
    # as the filename includes a timestamp
    scraper.save_results(test_results, test_query)
    # No assertion needed as we're just testing it doesn't raise an exception 