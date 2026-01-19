import logging
from typing import Dict, List, Optional
from app.scrapers.base_scraper import BaseScraper
from app.models.database import SessionLocal
from app.models.league import League
from app.models.team import Team
from app.models.player import Player
from app.models.game import Game
from app.models.standing import Standing
from app.models.statistics import PlayerStatistics, TeamStatistics

logger = logging.getLogger(__name__)


class ScraperManager:
    """Manages scrapers and coordinates data storage"""
    
    def __init__(self):
        self.scrapers: Dict[str, BaseScraper] = {}
        self.db = SessionLocal()
    
    def register_scraper(self, platform_name: str, scraper: BaseScraper):
        """Register a scraper for a platform"""
        self.scrapers[platform_name] = scraper
        logger.info(f"Registered scraper for platform: {platform_name}")
    
    def scrape_league(self, platform_name: str, league_url: str) -> bool:
        """Scrape all data for a league"""
        if platform_name not in self.scrapers:
            logger.error(f"No scraper registered for platform: {platform_name}")
            return False
        
        scraper = self.scrapers[platform_name]
        
        try:
            # Scrape league info
            league_data = scraper.scrape_league_info(league_url)
            league = self._upsert_league(league_data, platform_name)
            
            # Scrape standings
            standings_data = scraper.scrape_standings(league_url)
            self._upsert_standings(league.id, standings_data)
            
            # Scrape scores
            scores_data = scraper.scrape_scores(league_url)
            self._upsert_games(league.id, scores_data)
            
            # Scrape rosters and player stats for each team
            for team in league.teams:
                if team.source_team_id:
                    roster_data = scraper.scrape_rosters(team.source_team_id)
                    self._upsert_roster(team.id, roster_data)
            
            self.db.commit()
            logger.info(f"Successfully scraped league: {league.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error scraping league: {e}")
            self.db.rollback()
            return False
        finally:
            scraper.cleanup()
    
    def _upsert_league(self, data: Dict, platform_name: str) -> League:
        """Create or update league"""
        league = self.db.query(League).filter_by(slug=data.get('slug')).first()
        
        if not league:
            league = League(
                name=data.get('name'),
                slug=data.get('slug'),
                description=data.get('description'),
                source_url=data.get('source_url'),
                source_platform=platform_name,
                logo_url=data.get('logo_url'),
                active=True
            )
            self.db.add(league)
        else:
            league.name = data.get('name', league.name)
            league.description = data.get('description', league.description)
            league.source_url = data.get('source_url', league.source_url)
            league.logo_url = data.get('logo_url', league.logo_url)
        
        self.db.flush()
        return league
    
    def _upsert_standings(self, league_id: int, standings_data: List[Dict]):
        """Create or update standings"""
        for standing_data in standings_data:
            team = self._find_or_create_team(league_id, standing_data.get('team_name'))
            
            standing = self.db.query(Standing).filter_by(
                league_id=league_id,
                team_id=team.id,
                season=standing_data.get('season', '2024')
            ).first()
            
            if not standing:
                standing = Standing(
                    league_id=league_id,
                    team_id=team.id,
                    season=standing_data.get('season', '2024'),
                    rank=standing_data.get('rank', 0),
                    wins=standing_data.get('wins', 0),
                    losses=standing_data.get('losses', 0),
                    ties=standing_data.get('ties', 0),
                    points=standing_data.get('points', 0),
                    goals_for=standing_data.get('goals_for', 0),
                    goals_against=standing_data.get('goals_against', 0),
                    goal_difference=standing_data.get('goal_difference', 0),
                    games_played=standing_data.get('games_played', 0)
                )
                self.db.add(standing)
            else:
                standing.rank = standing_data.get('rank', standing.rank)
                standing.wins = standing_data.get('wins', standing.wins)
                standing.losses = standing_data.get('losses', standing.losses)
                standing.points = standing_data.get('points', standing.points)
    
    def _upsert_games(self, league_id: int, games_data: List[Dict]):
        """Create or update games"""
        for game_data in games_data:
            home_team = self._find_or_create_team(league_id, game_data.get('home_team'))
            away_team = self._find_or_create_team(league_id, game_data.get('away_team'))
            
            game = self.db.query(Game).filter_by(
                league_id=league_id,
                source_game_id=game_data.get('source_game_id')
            ).first()
            
            if not game:
                game = Game(
                    league_id=league_id,
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    game_date=game_data.get('game_date'),
                    game_time=game_data.get('game_time'),
                    status=game_data.get('status', 'scheduled'),
                    home_score=game_data.get('home_score'),
                    away_score=game_data.get('away_score'),
                    venue=game_data.get('venue'),
                    source_game_id=game_data.get('source_game_id')
                )
                self.db.add(game)
            else:
                game.status = game_data.get('status', game.status)
                game.home_score = game_data.get('home_score', game.home_score)
                game.away_score = game_data.get('away_score', game.away_score)
    
    def _upsert_roster(self, team_id: int, roster_data: List[Dict]):
        """Create or update team roster"""
        for player_data in roster_data:
            player = self.db.query(Player).filter_by(
                team_id=team_id,
                source_player_id=player_data.get('source_player_id')
            ).first()
            
            if not player:
                player = Player(
                    team_id=team_id,
                    first_name=player_data.get('first_name', ''),
                    last_name=player_data.get('last_name', ''),
                    full_name=player_data.get('full_name', ''),
                    jersey_number=player_data.get('jersey_number'),
                    position=player_data.get('position'),
                    photo_url=player_data.get('photo_url'),
                    source_player_id=player_data.get('source_player_id'),
                    active=True
                )
                self.db.add(player)
    
    def _find_or_create_team(self, league_id: int, team_name: str) -> Team:
        """Find or create a team"""
        if not team_name:
            raise ValueError("Team name is required")
        
        slug = team_name.lower().replace(' ', '-')
        team = self.db.query(Team).filter_by(league_id=league_id, slug=slug).first()
        
        if not team:
            team = Team(
                league_id=league_id,
                name=team_name,
                slug=slug,
                active=True
            )
            self.db.add(team)
            self.db.flush()
        
        return team
    
    def close(self):
        """Close database connection"""
        self.db.close()
