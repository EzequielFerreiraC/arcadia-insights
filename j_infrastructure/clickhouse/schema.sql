-- ClickHouse Database Schema
-- Arcadia Insights - OLAP Analytics Database

-- Create database
CREATE DATABASE IF NOT EXISTS arcadia;

-- Choice facts table (denormalized for analytics)
CREATE TABLE IF NOT EXISTS arcadia.choice_facts (
    choice_id String,
    choice_text String,
    episode UInt8,
    chapter UInt8,
    player_id String,
    player_country FixedString(2),
    player_platform String,
    option_selected String,
    timestamp_in_game UInt32,
    created_at DateTime,
    date Date DEFAULT toDate(created_at)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (episode, choice_id, date)
SETTINGS index_granularity = 8192;

-- Daily choice statistics (materialized view)
CREATE TABLE IF NOT EXISTS arcadia.choice_stats_daily (
    date Date,
    choice_id String,
    choice_text String,
    episode UInt8,
    chapter UInt8,
    option_selected String,
    player_count UInt32,
    total_count UInt32
) ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, choice_id, option_selected)
SETTINGS index_granularity = 8192;

-- Player statistics table
CREATE TABLE IF NOT EXISTS arcadia.player_stats (
    player_id String,
    country FixedString(2),
    platform String,
    total_saves UInt32,
    total_choices UInt32,
    unique_episodes UInt8,
    last_save_date DateTime,
    playtime_hours Float32,
    completion_percentage Float32,
    updated_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree(updated_at)
ORDER BY player_id
SETTINGS index_granularity = 8192;

-- Global choice popularity (aggregated)
CREATE TABLE IF NOT EXISTS arcadia.choice_popularity (
    choice_id String,
    choice_text String,
    episode UInt8,
    chapter UInt8,
    option_selected String,
    total_players UInt32,
    percentage Float32,
    last_updated DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree(last_updated)
ORDER BY (episode, choice_id, total_players)
SETTINGS index_granularity = 8192;

-- Episode completion stats
CREATE TABLE IF NOT EXISTS arcadia.episode_stats (
    episode UInt8,
    total_players UInt32,
    avg_choices_per_player Float32,
    avg_playtime_hours Float32,
    completion_rate Float32,
    date Date
) ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, episode)
SETTINGS index_granularity = 8192;
