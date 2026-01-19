from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.models.league import League
from app.models.team import Team
from app.models.player import Player
from app.models.game import Game
from app.models.standing import Standing
from app.models.statistics import PlayerStatistics, TeamStatistics
from pydantic import BaseModel
from datetime import date

router = APIRouter()


# Pydantic models for API responses
class LeagueResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    logo_url: Optional[str]
    source_platform: Optional[str]
    active: bool
    
    class Config:
        from_attributes = True


class TeamResponse(BaseModel):
    id: int
    league_id: int
    name: str
    slug: str
    abbreviation: Optional[str]
    logo_url: Optional[str]
    
    class Config:
        from_attributes = True


class PlayerResponse(BaseModel):
    id: int
    team_id: int
    first_name: str
    last_name: str
    full_name: str
    jersey_number: Optional[int]
    position: Optional[str]
    photo_url: Optional[str]
    
    class Config:
        from_attributes = True


class GameResponse(BaseModel):
    id: int
    league_id: int
    home_team_id: int
    away_team_id: int
    game_date: date
    game_time: Optional[str]
    status: str
    home_score: Optional[int]
    away_score: Optional[int]
    venue: Optional[str]
    
    class Config:
        from_attributes = True


class StandingResponse(BaseModel):
    id: int
    league_id: int
    team_id: int
    season: str
    rank: int
    wins: int
    losses: int
    ties: int
    points: int
    goals_for: int
    goals_against: int
    goal_difference: int
    games_played: int
    
    class Config:
        from_attributes = True


# League endpoints
@router.get("/leagues", response_model=List[LeagueResponse])
async def get_leagues(
    active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all leagues"""
    query = db.query(League)
    if active is not None:
        query = query.filter(League.active == active)
    leagues = query.offset(skip).limit(limit).all()
    return leagues


@router.get("/leagues/{league_id}", response_model=LeagueResponse)
async def get_league(league_id: int, db: Session = Depends(get_db)):
    """Get a specific league"""
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return league


@router.get("/leagues/{league_id}/teams", response_model=List[TeamResponse])
async def get_league_teams(league_id: int, db: Session = Depends(get_db)):
    """Get all teams in a league"""
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return league.teams


@router.get("/leagues/{league_id}/standings", response_model=List[StandingResponse])
async def get_league_standings(
    league_id: int,
    season: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get league standings"""
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    
    query = db.query(Standing).filter(Standing.league_id == league_id)
    if season:
        query = query.filter(Standing.season == season)
    
    standings = query.order_by(Standing.rank).all()
    return standings


@router.get("/leagues/{league_id}/games", response_model=List[GameResponse])
async def get_league_games(
    league_id: int,
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """Get games for a league"""
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    
    query = db.query(Game).filter(Game.league_id == league_id)
    if date_from:
        query = query.filter(Game.game_date >= date_from)
    if date_to:
        query = query.filter(Game.game_date <= date_to)
    
    games = query.order_by(Game.game_date.desc()).all()
    return games


# Team endpoints
@router.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: Session = Depends(get_db)):
    """Get a specific team"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.get("/teams/{team_id}/players", response_model=List[PlayerResponse])
async def get_team_players(team_id: int, db: Session = Depends(get_db)):
    """Get all players on a team"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team.players


@router.get("/teams/{team_id}/games", response_model=List[GameResponse])
async def get_team_games(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Get all games for a team"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    games = db.query(Game).filter(
        (Game.home_team_id == team_id) | (Game.away_team_id == team_id)
    ).order_by(Game.game_date.desc()).all()
    return games


# Player endpoints
@router.get("/players/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: int, db: Session = Depends(get_db)):
    """Get a specific player"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/players/{player_id}/stats")
async def get_player_stats(
    player_id: int,
    season: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get player statistics"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    query = db.query(PlayerStatistics).filter(PlayerStatistics.player_id == player_id)
    if season:
        query = query.filter(PlayerStatistics.season == season)
    
    stats = query.all()
    return stats
