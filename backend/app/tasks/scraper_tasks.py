import logging
from celery import Task
from app.celery_app import celery_app
from app.scrapers.scraper_manager import ScraperManager
from app.models.database import SessionLocal
from app.models.league import League

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.scraper_tasks.scrape_all_leagues")
def scrape_all_leagues(self: Task):
    """Scrape all active leagues"""
    db = SessionLocal()
    manager = ScraperManager()
    
    try:
        active_leagues = db.query(League).filter(League.active == True).all()
        logger.info(f"Starting scrape for {len(active_leagues)} active leagues")
        
        for league in active_leagues:
            if not league.source_url or not league.source_platform:
                logger.warning(f"League {league.name} missing source_url or source_platform")
                continue
            
            try:
                success = manager.scrape_league(league.source_platform, league.source_url)
                if success:
                    logger.info(f"Successfully scraped league: {league.name}")
                else:
                    logger.error(f"Failed to scrape league: {league.name}")
            except Exception as e:
                logger.error(f"Error scraping league {league.name}: {e}")
        
        return {"status": "completed", "leagues_processed": len(active_leagues)}
    except Exception as e:
        logger.error(f"Error in scrape_all_leagues task: {e}")
        raise
    finally:
        manager.close()
        db.close()


@celery_app.task(bind=True, name="app.tasks.scraper_tasks.scrape_single_league")
def scrape_single_league(self: Task, league_id: int):
    """Scrape a single league by ID"""
    db = SessionLocal()
    manager = ScraperManager()
    
    try:
        league = db.query(League).filter(League.id == league_id).first()
        if not league:
            logger.error(f"League with ID {league_id} not found")
            return {"status": "error", "message": "League not found"}
        
        if not league.source_url or not league.source_platform:
            logger.error(f"League {league.name} missing source_url or source_platform")
            return {"status": "error", "message": "Missing source information"}
        
        success = manager.scrape_league(league.source_platform, league.source_url)
        if success:
            logger.info(f"Successfully scraped league: {league.name}")
            return {"status": "success", "league": league.name}
        else:
            logger.error(f"Failed to scrape league: {league.name}")
            return {"status": "error", "league": league.name}
    except Exception as e:
        logger.error(f"Error in scrape_single_league task: {e}")
        raise
    finally:
        manager.close()
        db.close()
