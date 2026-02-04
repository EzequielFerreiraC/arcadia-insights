-- PostgreSQL Database Schema
-- Arcadia Insights - OLTP Database

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Players table
CREATE TABLE IF NOT EXISTS players (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    country VARCHAR(2) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    game_version VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_saves INTEGER NOT NULL DEFAULT 0,
    total_choices INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX idx_players_country ON players(country);
CREATE INDEX idx_players_platform ON players(platform);
CREATE INDEX idx_players_created_at ON players(created_at);

-- Saves table
CREATE TABLE IF NOT EXISTS saves (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_size_bytes INTEGER NOT NULL,
    checksum VARCHAR(32) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'uploaded',
    s3_path VARCHAR(500),
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    choices_extracted INTEGER NOT NULL DEFAULT 0,
    error_message TEXT
);

CREATE INDEX idx_saves_player_id ON saves(player_id);
CREATE INDEX idx_saves_status ON saves(status);
CREATE INDEX idx_saves_uploaded_at ON saves(uploaded_at);
CREATE UNIQUE INDEX idx_saves_checksum ON saves(checksum);

-- Choices table
CREATE TABLE IF NOT EXISTS choices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    save_id UUID NOT NULL REFERENCES saves(id) ON DELETE CASCADE,
    episode INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    choice_id VARCHAR(100) NOT NULL,
    choice_text VARCHAR(500) NOT NULL,
    option_selected VARCHAR(200) NOT NULL,
    timestamp_in_game INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_choices_player_id ON choices(player_id);
CREATE INDEX idx_choices_save_id ON choices(save_id);
CREATE INDEX idx_choices_episode ON choices(episode);
CREATE INDEX idx_choices_choice_id ON choices(choice_id);
CREATE INDEX idx_choices_created_at ON choices(created_at);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for players table
CREATE TRIGGER update_players_updated_at
    BEFORE UPDATE ON players
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Initial data (optional)
COMMENT ON TABLE players IS 'Player profiles and metadata';
COMMENT ON TABLE saves IS 'Uploaded game save files';
COMMENT ON TABLE choices IS 'Extracted choices from save files';
