SELECT p.full_name, t.name AS team_name
FROM players p
JOIN player_team pt ON p.player_id = pt.player_id
JOIN teams t ON pt.team_id = t.team_id;


SELECT m.match_id, p.full_name, ms.runs_scored
FROM match_stats ms
JOIN players p ON ms.player_id = p.player_id
JOIN matches m ON ms.match_id = m.match_id
WHERE (ms.match_id, ms.runs_scored) IN (
    SELECT match_id, MAX(runs_scored)
    FROM match_stats
    GROUP BY match_id
);


SELECT m.match_id, c.name AS championship, m.match_date,
       t1.name AS winner_team, t2.name AS opponent_team
FROM matches m
JOIN championships c ON m.championship_id = c.championship_id
JOIN match_participation mp1 ON m.match_id = mp1.match_id AND mp1.is_winner = TRUE
JOIN teams t1 ON mp1.team_id = t1.team_id
JOIN match_participation mp2 ON m.match_id = mp2.match_id AND mp2.team_id != mp1.team_id
JOIN teams t2 ON mp2.team_id = t2.team_id;


SELECT m.match_id, m.match_date, v.name AS venue, v.city
FROM matches m
JOIN venues v ON m.venue_id = v.venue_id
WHERE v.country = 'India';


SELECT c.name AS championship,
       COUNT(DISTINCT m.match_id) AS total_matches,
       COUNT(DISTINCT mp.team_id) AS total_teams
FROM championships c
JOIN matches m ON c.championship_id = m.championship_id
JOIN match_participation mp ON m.match_id = mp.match_id
GROUP BY c.name;


SELECT p.full_name, SUM(ms.catches) AS total_catches
FROM match_stats ms
JOIN players p ON ms.player_id = p.player_id
GROUP BY p.full_name
ORDER BY total_catches DESC
LIMIT 3;
