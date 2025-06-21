from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_core.language_models import BaseLanguageModel
from bs4 import BeautifulSoup
import requests
import pandas as pd
from typing import List, Dict, Optional
import logging
from datetime import datetime

from src.config.config import SCRAPING_SETTINGS
from src.utils.helpers import save_to_json, get_timestamp

logger = logging.getLogger(__name__)

class BondScraper:
    def __init__(self, llm: Optional[BaseLanguageModel] = None):
        self.search = DuckDuckGoSearchRun()
        self.tools = [
            Tool(
                name="Search",
                func=self.search.run,
                description="Useful for searching information about bonds, yields, and market data"
            ),
            Tool(
                name="ScrapeWebsite",
                func=self.scrape_website,
                description="Useful for scraping content from a specific URL"
            )
        ]
        
        self.prompt = PromptTemplate.from_template(
            """You are a financial data expert. Answer the following questions about bonds and financial markets.
            You have access to the following tools:

            {tools}

            Use the following format:

            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question

            Begin!

            Question: {input}
            {agent_scratchpad}"""
        )

        if llm is None:
            logger.warning("No language model provided. Some features may not work as expected.")
            self.agent_executor = None
        else:
            self.agent = create_react_agent(
                llm=llm,
                tools=self.tools,
                prompt=self.prompt
            )
            
            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                verbose=True
            )

    def scrape_website(self, url: str) -> str:
        """Scrape content from a given URL."""
        try:
            headers = {'User-Agent': SCRAPING_SETTINGS['USER_AGENT']}
            response = requests.get(
                url, 
                headers=headers, 
                timeout=SCRAPING_SETTINGS['TIMEOUT']
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:4000]  # Limit response size
        except Exception as e:
            logger.error(f"Error scraping website {url}: {str(e)}")
            return f"Error scraping website: {str(e)}"

    def search_bond_info(self, query: str) -> Dict:
        """Search for bond information using the search tool."""
        try:
            if self.agent_executor is None:
                # Fallback to direct search if no LLM is available
                search_result = self.search.run(query)
                # Ensure the result is wrapped in a 'results' key as a list
                return {
                    "query": query,
                    "results": [search_result],
                    "source": "direct_search"
                }
            result = self.agent_executor.invoke({"input": query})
            return result
        except Exception as e:
            logger.error(f"Error searching bond info: {str(e)}")
            return {"error": str(e)}

    def process_bond_data(self, data: str) -> pd.DataFrame:
        """Process scraped bond data into a structured format."""
        # This is a placeholder for data processing logic
        # You would implement specific parsing logic based on the data structure
        return pd.DataFrame()

    def save_results(self, results: Dict, query: str) -> None:
        """Save search results to a JSON file."""
        timestamp = get_timestamp()
        filename = f"bond_data_{timestamp}.json"
        data = {
            "query": query,
            "timestamp": timestamp,
            "results": results
        }
        save_to_json(data, filename) 