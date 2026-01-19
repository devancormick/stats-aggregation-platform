from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    full_name = Column(String(255), nullable=False, index=True)
    jersey_number = Column(Integer, nullable=True)
    position = Column(String(50), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    height = Column(String(20), nullable=True)
    weight = Column(Integer, nullable=True)
    photo_url = Column(String(500), nullable=True)
    source_player_id = Column(String(100), nullable=True)
    active = Column(String(10), default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    team = relationship("Team", back_populates="players")
    player_statistics = relationship("PlayerStatistics", back_populates="player", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Player(id={self.id}, name='{self.full_name}', team_id={self.team_id})>"
