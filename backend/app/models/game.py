from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    game_date = Column(Date, nullable=False, index=True)
    game_time = Column(Time, nullable=True)
    status = Column(String(50), nullable=False, default="scheduled", index=True)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    venue = Column(String(255), nullable=True)
    source_game_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    league = relationship("League", back_populates="games")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_games")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_games")

    def __repr__(self):
        return f"<Game(id={self.id}, home_team_id={self.home_team_id}, away_team_id={self.away_team_id}, date={self.game_date})>"
