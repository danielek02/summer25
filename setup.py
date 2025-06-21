from setuptools import setup, find_packages

setup(
    name="bond_scraper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.28",
        "beautifulsoup4==4.12.3",
        "requests==2.31.0",
        "python-dotenv==1.0.1",
        "duckduckgo-search==4.4.3",
        "pandas==2.2.1",
        "pytest==8.0.0",
        "black==24.2.0",
        "flake8==7.0.0",
    ],
    python_requires=">=3.8",
) 