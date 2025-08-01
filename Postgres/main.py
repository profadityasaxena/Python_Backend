#!/usr/bin/env python  # Shebang for Unix environments
# coding: utf-8  # Encoding declaration

# =========================================
# Block: Install required packages (remove if running outside Jupyter)
# =========================================
# get_ipython().system('pip install fastapi[all] sqlalchemy psycopg2-binary uvicorn')  # Install dependencies in Jupyter

# =========================================
# Block: Imports
# =========================================
from fastapi import FastAPI, Depends, HTTPException  # FastAPI core imports
from sqlalchemy import (  # SQLAlchemy core imports
    create_engine, Column, Integer, String, Date, Boolean, ForeignKey, Text, Numeric
)
from sqlalchemy.ext.declarative import declarative_base  # Base class for models
from sqlalchemy.orm import sessionmaker, relationship, Session  # ORM session and relationships
from pydantic import BaseModel  # Pydantic for data validation
from typing import Optional, List  # Type hints
from datetime import date  # Date type

# =========================================
# Block: Database Setup
# =========================================
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/postgres"  # Database connection string
engine = create_engine(DATABASE_URL)  # Create SQLAlchemy engine
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)  # Session factory
Base = declarative_base()  # Base class for ORM models

# =========================================
# Block: SQLAlchemy Models
# =========================================

class Player(Base):  # Player model
    __tablename__ = "players"  # Table name
    player_id = Column(Integer, primary_key=True)  # Primary key
    full_name = Column(String(100), nullable=False)  # Player full name
    country = Column(String(50))  # Country
    birth_date = Column(Date)  # Birth date
    batting_style = Column(String(30))  # Batting style
    bowling_style = Column(String(30))  # Bowling style
    teams = relationship("PlayerTeam", back_populates="player")  # Relationship to PlayerTeam
    stats = relationship("MatchStats", back_populates="player")  # Relationship to MatchStats

class Team(Base):  # Team model
    __tablename__ = "teams"  # Table name
    team_id = Column(Integer, primary_key=True)  # Primary key
    name = Column(String(100), nullable=False)  # Team name
    country = Column(String(50), nullable=False)  # Country
    founded_year = Column(Integer)  # Founded year
    players = relationship("PlayerTeam", back_populates="team")  # Relationship to PlayerTeam
    participations = relationship("MatchParticipation", back_populates="team")  # Relationship to MatchParticipation

class PlayerTeam(Base):  # PlayerTeam association model
    __tablename__ = "player_team"  # Table name
    player_id = Column(Integer, ForeignKey("players.player_id"), primary_key=True)  # FK to Player
    team_id = Column(Integer, ForeignKey("teams.team_id"), primary_key=True)  # FK to Team
    start_year = Column(Integer)  # Start year
    end_year = Column(Integer)  # End year
    player = relationship("Player", back_populates="teams")  # Relationship to Player
    team = relationship("Team", back_populates="players")  # Relationship to Team

class Championship(Base):  # Championship model
    __tablename__ = "championships"  # Table name
    championship_id = Column(Integer, primary_key=True)  # Primary key
    name = Column(String(100))  # Championship name
    format = Column(String(30))  # Format
    start_date = Column(Date)  # Start date
    end_date = Column(Date)  # End date
    matches = relationship("Match", back_populates="championship")  # Relationship to Match

class Venue(Base):  # Venue model
    __tablename__ = "venues"  # Table name
    venue_id = Column(Integer, primary_key=True)  # Primary key
    name = Column(String(100))  # Venue name
    city = Column(String(50))  # City
    country = Column(String(50))  # Country
    matches = relationship("Match", back_populates="venue")  # Relationship to Match

class Match(Base):  # Match model
    __tablename__ = "matches"  # Table name
    match_id = Column(Integer, primary_key=True)  # Primary key
    championship_id = Column(Integer, ForeignKey("championships.championship_id"))  # FK to Championship
    venue_id = Column(Integer, ForeignKey("venues.venue_id"))  # FK to Venue
    match_date = Column(Date)  # Match date
    overs = Column(Integer)  # Overs
    result = Column(Text)  # Result
    championship = relationship("Championship", back_populates="matches")  # Relationship to Championship
    venue = relationship("Venue", back_populates="matches")  # Relationship to Venue
    participations = relationship("MatchParticipation", back_populates="match")  # Relationship to MatchParticipation
    stats = relationship("MatchStats", back_populates="match")  # Relationship to MatchStats

class MatchParticipation(Base):  # MatchParticipation association model
    __tablename__ = "match_participation"  # Table name
    match_id = Column(Integer, ForeignKey("matches.match_id"), primary_key=True)  # FK to Match
    team_id = Column(Integer, ForeignKey("teams.team_id"), primary_key=True)  # FK to Team
    is_winner = Column(Boolean)  # Winner flag
    match = relationship("Match", back_populates="participations")  # Relationship to Match
    team = relationship("Team", back_populates="participations")  # Relationship to Team

class MatchStats(Base):  # MatchStats model
    __tablename__ = "match_stats"  # Table name
    match_id = Column(Integer, ForeignKey("matches.match_id"), primary_key=True)  # FK to Match
    player_id = Column(Integer, ForeignKey("players.player_id"), primary_key=True)  # FK to Player
    runs_scored = Column(Integer, default=0)  # Runs scored
    balls_faced = Column(Integer, default=0)  # Balls faced
    wickets_taken = Column(Integer, default=0)  # Wickets taken
    overs_bowled = Column(Numeric(4,1), default=0.0)  # Overs bowled
    catches = Column(Integer, default=0)  # Catches
    match = relationship("Match", back_populates="stats")  # Relationship to Match
    player = relationship("Player", back_populates="stats")  # Relationship to Player

# =========================================
# Block: Pydantic Schemas
# =========================================

class PlayerBase(BaseModel):  # Base schema for Player
    full_name: str  # Full name
    country: Optional[str]  # Country
    birth_date: Optional[date]  # Birth date
    batting_style: Optional[str]  # Batting style
    bowling_style: Optional[str]  # Bowling style

class PlayerCreate(PlayerBase):  # Schema for creating Player
    pass  # No extra fields

class PlayerSchema(PlayerBase):  # Schema for reading Player
    player_id: int  # Player ID
    class Config:  # ORM mode config
        orm_mode = True

class TeamBase(BaseModel):  # Base schema for Team
    name: str  # Team name
    country: str  # Country
    founded_year: Optional[int]  # Founded year

class TeamCreate(TeamBase):  # Schema for creating Team
    pass  # No extra fields

class TeamSchema(TeamBase):  # Schema for reading Team
    team_id: int  # Team ID
    class Config:  # ORM mode config
        orm_mode = True

class MatchBase(BaseModel):  # Base schema for Match
    championship_id: int  # Championship ID
    venue_id: int  # Venue ID
    match_date: date  # Match date
    overs: int  # Overs
    result: Optional[str]  # Result

class MatchCreate(MatchBase):  # Schema for creating Match
    pass  # No extra fields

class MatchSchema(MatchBase):  # Schema for reading Match
    match_id: int  # Match ID
    class Config:  # ORM mode config
        orm_mode = True

# =========================================
# Block: DB Dependency Injection
# =========================================

def get_db():  # Dependency for DB session
    db = SessionLocal()  # Create session
    try:
        yield db  # Yield session
    finally:
        db.close()  # Close session

# =========================================
# Block: FastAPI App Initialization
# =========================================
app = FastAPI(  # FastAPI app instance
    title="🏏 Cricket Backend API",  # App title
    version="1.0",  # Version
    description="A FastAPI backend with PostgreSQL and SQLAlchemy for cricket data."  # Description
)
Base.metadata.create_all(bind=engine)  # Create tables

# =========================================
# Block: Endpoints for Players
# =========================================

@app.post("/players/", response_model=PlayerSchema)  # Endpoint to create player
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):  # Create player function
    db_player = Player(**player.dict())  # Create Player instance
    db.add(db_player)  # Add to session
    db.commit()  # Commit transaction
    db.refresh(db_player)  # Refresh instance
    return db_player  # Return created player

@app.get("/players/", response_model=List[PlayerSchema])  # Endpoint to get all players
def get_all_players(db: Session = Depends(get_db)):  # Get all players function
    return db.query(Player).all()  # Query all players

@app.get("/players/{player_id}", response_model=PlayerSchema)  # Endpoint to get player by ID
def get_player_by_id(player_id: int, db: Session = Depends(get_db)):  # Get player by ID function
    player = db.query(Player).filter(Player.player_id == player_id).first()  # Query player
    if not player:  # If not found
        raise HTTPException(status_code=404, detail="Player not found")  # Raise 404
    return player  # Return player

# =========================================
# Block: Endpoints for Teams
# =========================================

@app.post("/teams/", response_model=TeamSchema)  # Endpoint to create team
def create_team(team: TeamCreate, db: Session = Depends(get_db)):  # Create team function
    db_team = Team(**team.dict())  # Create Team instance
    db.add(db_team)  # Add to session
    db.commit()  # Commit transaction
    db.refresh(db_team)  # Refresh instance
    return db_team  # Return created team

@app.get("/teams/", response_model=List[TeamSchema])  # Endpoint to get all teams
def get_all_teams(db: Session = Depends(get_db)):  # Get all teams function
    return db.query(Team).all()  # Query all teams

# =========================================
# Block: Endpoints for Matches
# =========================================

@app.post("/matches/", response_model=MatchSchema)  # Endpoint to create match
def create_match(match: MatchCreate, db: Session = Depends(get_db)):  # Create match function
    db_match = Match(**match.dict())  # Create Match instance
    db.add(db_match)  # Add to session
    db.commit()  # Commit transaction
    db.refresh(db_match)  # Refresh instance
    return db_match  # Return created match

@app.get("/matches/", response_model=List[MatchSchema])  # Endpoint to get all matches
def get_all_matches(db: Session = Depends(get_db)):  # Get all matches function
    return db.query(Match).all()  # Query all matches

# =========================================
# Block: App Startup (run with: uvicorn main:app --reload)
# =========================================
# Remove this line if running outside Jupyter
# get_ipython().system('uvicorn main:app --reload')  # Run app in Jupyter
