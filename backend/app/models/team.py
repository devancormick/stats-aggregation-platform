from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, index=True)
    abbreviation = Column(String(10), nullable=True)
    logo_url = Column(String(500), nullable=True)
    source_team_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    league = relationship("League", back_populates="teams")
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    home_games = relationship("Game", foreign_keys="Game.home_team_id", back_populates="home_team")
    away_games = relationship("Game", foreign_keys="Game.away_team_id", back_populates="away_team")
    standings = relationship("Standing", back_populates="team", cascade="all, delete-orphan")
    team_statistics = relationship("TeamStatistics", back_populates="team", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', league_id={self.league_id})>"
