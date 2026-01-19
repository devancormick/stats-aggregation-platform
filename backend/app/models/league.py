from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    source_url = Column(String(500), nullable=True)
    source_platform = Column(String(100), nullable=True)
    logo_url = Column(String(500), nullable=True)
    active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    teams = relationship("Team", back_populates="league", cascade="all, delete-orphan")
    games = relationship("Game", back_populates="league", cascade="all, delete-orphan")
    standings = relationship("Standing", back_populates="league", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<League(id={self.id}, name='{self.name}')>"
