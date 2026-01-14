-- =============================================
-- Olympic Games Final Dataset Schema
-- =============================================

-- Drop old tables if they exist to start fresh
DROP TABLE IF EXISTS medals CASCADE;
DROP TABLE IF EXISTS results CASCADE;
DROP TABLE IF EXISTS athletes CASCADE;
DROP TABLE IF EXISTS hosts CASCADE;
DROP TABLE IF EXISTS olympic_stats CASCADE;

-- Single table to match the provided CSV structure (Aggregated Data)
CREATE TABLE IF NOT EXISTS olympic_stats (
    id SERIAL PRIMARY KEY,
    year INTEGER,
    slug_game VARCHAR(255),
    country_3_letter_code VARCHAR(10),
    bronze_medals INTEGER,
    gold_medals INTEGER,
    silver_medals INTEGER,
    total_medals INTEGER,
    total_athletes INTEGER,
    avg_age_athletes FLOAT,
    medals_in_current_year INTEGER,
    game_slug VARCHAR(255),
    city VARCHAR(255),
    season VARCHAR(50),
    game_name VARCHAR(255),
    cumulative_medals FLOAT,
    is_host INTEGER
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_stats_slug_game ON olympic_stats(slug_game);
CREATE INDEX IF NOT EXISTS idx_stats_country ON olympic_stats(country_3_letter_code);
CREATE INDEX IF NOT EXISTS idx_stats_year ON olympic_stats(year);
