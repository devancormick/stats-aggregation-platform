import time
import logging
import requests
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from app.config import settings

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for all league platform scrapers"""
    
    def __init__(self, platform_name: str, base_url: str):
        self.platform_name = platform_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.request_timeout = settings.request_timeout
        self.max_retries = settings.max_retries
        self.retry_delay = settings.retry_delay
        self.rate_limit_delay = settings.rate_limit_delay
        
    def fetch_page(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        """Fetch a webpage and return BeautifulSoup object with retry logic"""
        for attempt in range(self.max_retries):
            try:
                time.sleep(self.rate_limit_delay)
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.request_timeout
                )
                response.raise_for_status()
                return BeautifulSoup(response.content, 'lxml')
            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed for {url}: {e}"
                )
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
                    return None
        return None
    
    def extract_text(self, soup: BeautifulSoup, selector: str, default: str = "") -> str:
        """Extract text from a CSS selector"""
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else default
    
    def extract_all_text(self, soup: BeautifulSoup, selector: str) -> list[str]:
        """Extract all text from a CSS selector"""
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements if elem]
    
    def extract_attribute(self, soup: BeautifulSoup, selector: str, attribute: str, default: str = "") -> str:
        """Extract an attribute value from a CSS selector"""
        element = soup.select_one(selector)
        return element.get(attribute, default) if element else default
    
    @abstractmethod
    def scrape_league_info(self, league_url: str) -> Dict[str, Any]:
        """Scrape league information"""
        pass
    
    @abstractmethod
    def scrape_standings(self, league_url: str) -> list[Dict[str, Any]]:
        """Scrape league standings"""
        pass
    
    @abstractmethod
    def scrape_scores(self, league_url: str, date: Optional[str] = None) -> list[Dict[str, Any]]:
        """Scrape game scores"""
        pass
    
    @abstractmethod
    def scrape_rosters(self, team_url: str) -> list[Dict[str, Any]]:
        """Scrape team rosters"""
        pass
    
    @abstractmethod
    def scrape_player_stats(self, player_url: str) -> Dict[str, Any]:
        """Scrape player statistics"""
        pass
    
    def cleanup(self):
        """Clean up resources"""
        self.session.close()
