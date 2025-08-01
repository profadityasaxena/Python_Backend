-- 1. Insert Players
INSERT INTO players (full_name, country, birth_date, batting_style, bowling_style) VALUES
('Virat Kohli', 'India', '1988-11-05', 'Right-hand bat', 'Right-arm medium'),
('Steve Smith', 'Australia', '1989-06-02', 'Right-hand bat', 'Right-arm legbreak'),
('Kane Williamson', 'New Zealand', '1990-08-08', 'Right-hand bat', 'Right-arm offbreak'),
('Babar Azam', 'Pakistan', '1994-10-15', 'Right-hand bat', 'Right-arm offbreak');

-- 2. Insert Teams
INSERT INTO teams (name, country, founded_year) VALUES
('India National Team', 'India', 1926),
('Australia National Team', 'Australia', 1905),
('New Zealand National Team', 'New Zealand', 1929),
('Pakistan National Team', 'Pakistan', 1952);

-- 3. Insert Player-Team Relationships
INSERT INTO player_team (player_id, team_id, start_year, end_year) VALUES
(1, 1, 2008, NULL),
(2, 2, 2010, NULL),
(3, 3, 2011, NULL),
(4, 4, 2015, NULL);

-- 4. Insert Championships
INSERT INTO championships (name, format, start_date, end_date) VALUES
('ICC World Cup 2023', 'ODI', '2023-10-01', '2023-11-15');

-- 5. Insert Venues
INSERT INTO venues (name, city, country) VALUES
('Narendra Modi Stadium', 'Ahmedabad', 'India'),       -- venue_id = 1
('MCG', 'Melbourne', 'Australia');                      -- venue_id = 2

-- 6. Insert Matches
INSERT INTO matches (championship_id, venue_id, match_date, overs, result) VALUES
(1, 1, '2023-10-15', 50, 'India won by 5 wickets'),     -- match_id = 1
(1, 2, '2023-10-18', 50, 'Australia won by 10 runs');   -- match_id = 2

-- 7. Insert Match Participation
INSERT INTO match_participation (match_id, team_id, is_winner) VALUES
(1, 1, TRUE),   -- India
(1, 2, FALSE),  -- Australia
(2, 2, TRUE),   -- Australia
(2, 3, FALSE);  -- New Zealand

-- 8. Insert Match Stats
-- Match 1
INSERT INTO match_stats (match_id, player_id, runs_scored, balls_faced, wickets_taken, overs_bowled, catches) VALUES
(1, 1, 85, 95, 0, 0.0, 1),  -- Virat Kohli
(1, 2, 60, 70, 1, 10.0, 0); -- Steve Smith

-- Match 2
INSERT INTO match_stats (match_id, player_id, runs_scored, balls_faced, wickets_taken, overs_bowled, catches) VALUES
(2, 2, 45, 52, 0, 0.0, 2),  -- Steve Smith
(2, 3, 78, 88, 0, 0.0, 1);  -- Kane Williamson
