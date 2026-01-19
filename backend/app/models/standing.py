from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class Standing(Base):
    __tablename__ = "standings"

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    season = Column(String(50), nullable=False, index=True)
    rank = Column(Integer, nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    ties = Column(Integer, default=0)
    points = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    goal_difference = Column(Integer, default=0)
    win_percentage = Column(Float, default=0.0)
    games_played = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    league = relationship("League", back_populates="standings")
    team = relationship("Team", back_populates="standings")

    def __repr__(self):
        return f"<Standing(id={self.id}, team_id={self.team_id}, rank={self.rank}, season={self.season})>"
