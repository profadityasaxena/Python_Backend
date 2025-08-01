-- 1. Players
CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    birth_date DATE,
    batting_style VARCHAR(30),
    bowling_style VARCHAR(30)
);

-- 2. Teams
CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    founded_year INT
);

-- 3. Player-Team (many-to-many)
CREATE TABLE player_team (
    player_id INT REFERENCES players(player_id),
    team_id INT REFERENCES teams(team_id),
    start_year INT,
    end_year INT,
    PRIMARY KEY (player_id, team_id)
);

-- 4. Championships
CREATE TABLE championships (
    championship_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    format VARCHAR(30),
    start_date DATE,
    end_date DATE
);

-- 5. Venues
CREATE TABLE venues (
    venue_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
);

-- 6. Matches
CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    championship_id INT REFERENCES championships(championship_id),
    venue_id INT REFERENCES venues(venue_id),
    match_date DATE,
    overs INT,
    result TEXT
);

-- 7. Match Participation (team-wise)
CREATE TABLE match_participation (
    match_id INT REFERENCES matches(match_id),
    team_id INT REFERENCES teams(team_id),
    is_winner BOOLEAN,
    PRIMARY KEY (match_id, team_id)
);

-- 8. Match Stats (player-wise)
CREATE TABLE match_stats (
    match_id INT REFERENCES matches(match_id),
    player_id INT REFERENCES players(player_id),
    runs_scored INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    wickets_taken INT DEFAULT 0,
    overs_bowled NUMERIC(4,1) DEFAULT 0.0,
    catches INT DEFAULT 0,
    PRIMARY KEY (match_id, player_id)
);
