from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class PlayerStatistics(Base):
    __tablename__ = "player_statistics"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, index=True)
    season = Column(String(50), nullable=False, index=True)
    games_played = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    points = Column(Integer, default=0)
    shots = Column(Integer, default=0)
    shots_on_goal = Column(Integer, default=0)
    penalty_minutes = Column(Integer, default=0)
    plus_minus = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    player = relationship("Player", back_populates="player_statistics")

    def __repr__(self):
        return f"<PlayerStatistics(id={self.id}, player_id={self.player_id}, season={self.season})>"


class TeamStatistics(Base):
    __tablename__ = "team_statistics"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    season = Column(String(50), nullable=False, index=True)
    games_played = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    goal_difference = Column(Integer, default=0)
    shots_per_game = Column(Float, default=0.0)
    goals_per_game = Column(Float, default=0.0)
    power_play_percentage = Column(Float, default=0.0)
    penalty_kill_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    team = relationship("Team", back_populates="team_statistics")

    def __repr__(self):
        return f"<TeamStatistics(id={self.id}, team_id={self.team_id}, season={self.season})>"
