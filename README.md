# Bond Information Scraper

A LangChain-powered application for scraping and analyzing bond information from the web.

## Project Structure

```
.
├── src/
│   ├── data/           # Data storage and processing
│   ├── utils/          # Utility functions and helpers
│   ├── scrapers/       # Web scraping modules
│   └── config/         # Configuration files
├── tests/              # Test files
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory (optional, for API keys if needed)

## Development

- Source code is organized in the `src` directory
- Tests are located in the `tests` directory
- Use `black` for code formatting
- Use `flake8` for linting
- Run tests with `pytest`

## Usage

The application will:
- Search for bond information using web search
- Scrape relevant data from financial websites
- Process and structure the information
- Present the results in a readable format 