#!/usr/bin/env python3
"""Initialize database tables"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.models.database import Base, engine
from app.models.league import League
from app.models.team import Team
from app.models.player import Player
from app.models.game import Game
from app.models.standing import Standing
from app.models.statistics import PlayerStatistics, TeamStatistics


def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_database()
