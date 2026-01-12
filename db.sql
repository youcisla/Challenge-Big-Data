-- =============================================
-- Olympic Games Database Schema
-- =============================================

-- 1. Hosts Table
-- Stores information about each Olympic Game (Winter and Summer)
CREATE TABLE IF NOT EXISTS hosts (
    game_slug VARCHAR(255) PRIMARY KEY, -- e.g. 'beijing-2022'
    game_end_date TIMESTAMP,
    game_start_date TIMESTAMP,
    game_location VARCHAR(255),
    game_name VARCHAR(255),
    game_season VARCHAR(50), -- 'Summer' or 'Winter'
    game_year INTEGER
);

-- 2. Athletes Table
-- Stores unique athlete information
CREATE TABLE IF NOT EXISTS athletes (
    athlete_url VARCHAR(255) PRIMARY KEY, -- Using URL as unique ID from scraper
    athlete_full_name VARCHAR(255),
    games_participations INTEGER,
    first_game VARCHAR(255),
    athlete_year_birth INTEGER,
    athlete_medals TEXT -- Summary field if needed
);

-- 3. Results Table
-- Stores participation results for every event
CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    game_slug VARCHAR(255) REFERENCES hosts(game_slug),
    event_title VARCHAR(255),
    sport_title VARCHAR(255),
    sport_url VARCHAR(255),
    rank_position VARCHAR(50), -- text because it can be 'DNS', 'DQ' etc.
    country_name VARCHAR(255),
    country_code VARCHAR(10),
    athlete_url VARCHAR(255) REFERENCES athletes(athlete_url),
    athlete_full_name VARCHAR(255),
    value_unit VARCHAR(50), -- e.g. 'm', 'seconds'
    value_type VARCHAR(50)  -- e.g. 'TIME', 'DISTANCE'
);

-- 4. Medals Table
-- Stores specifically the medal wins (Gold, Silver, Bronze)
-- Note: This often overlaps with results but serves as a dedicated dataset.
CREATE TABLE IF NOT EXISTS medals (
    id SERIAL PRIMARY KEY,
    medal_type VARCHAR(50), -- 'GOLD', 'SILVER', 'BRONZE'
    medal_slug VARCHAR(255),
    athlete_url VARCHAR(255) REFERENCES athletes(athlete_url),
    athlete_full_name VARCHAR(255),
    game_slug VARCHAR(255) REFERENCES hosts(game_slug),
    event_title VARCHAR(255),
    sport_title VARCHAR(255),
    country_name VARCHAR(255),
    country_code VARCHAR(10)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_results_game_slug ON results(game_slug);
CREATE INDEX IF NOT EXISTS idx_results_athlete_url ON results(athlete_url);
CREATE INDEX IF NOT EXISTS idx_medals_game_slug ON medals(game_slug);
CREATE INDEX IF NOT EXISTS idx_medals_medal_type ON medals(medal_type);
