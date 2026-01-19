#!/usr/bin/env python3
"""Run scraper for a specific league"""
import sys
import argparse
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.scrapers.scraper_manager import ScraperManager
from app.utils.logging_config import setup_logging

setup_logging()


def main():
    parser = argparse.ArgumentParser(description="Run scraper for a league")
    parser.add_argument("platform", help="Platform name")
    parser.add_argument("url", help="League URL to scrape")
    
    args = parser.parse_args()
    
    manager = ScraperManager()
    
    # Register scrapers here when implemented
    # manager.register_scraper("platform_name", PlatformScraper())
    
    try:
        print(f"Scraping {args.platform} league from {args.url}")
        success = manager.scrape_league(args.platform, args.url)
        if success:
            print("Scraping completed successfully!")
        else:
            print("Scraping failed!")
            sys.exit(1)
    finally:
        manager.close()


if __name__ == "__main__":
    main()
