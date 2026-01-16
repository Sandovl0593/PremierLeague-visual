-- === Schema ===
DROP SCHEMA IF EXISTS pleague_stats CASCADE;
CREATE SCHEMA IF NOT EXISTS pleague_stats;
SET search_path = 'pleague_stats';

-- === Tabla de equipos ===
CREATE TABLE teams (
    team_code       VARCHAR(3) PRIMARY KEY,
    team_name       VARCHAR(255)
);

-- === Temporadas ===
CREATE TABLE seasons (
    season_id       VARCHAR(3) PRIMARY KEY,
    season_name     VARCHAR(255),
    start_year      INT
);

-- === Equipos por temporada ===
CREATE TABLE season_teams (
    steam_id        INT PRIMARY KEY,
    team_code       VARCHAR(3),
    season_id       VARCHAR(3),
    position        INT,
    points          INT
);

-- === Tabla de registros ===
CREATE TABLE stat_registers (
    stat_id         INT PRIMARY KEY,
    steam_id        INT,
    games_played    INT,
    n_wins          INT,
    n_draws         INT,
    n_losses        INT,
    goals_for       INT,
    goals_against   INT,
    goals_diff      INT
);

-- CONSTRAINTS --
ALTER TABLE season_teams ADD CONSTRAINT fk_teams FOREIGN KEY (team_code) REFERENCES teams(team_code);
ALTER TABLE season_teams ADD CONSTRAINT fk_seasons FOREIGN KEY (season_id) REFERENCES seasons(season_id);
ALTER TABLE stat_registers ADD CONSTRAINT fk_stat_registers FOREIGN KEY (steam_id) REFERENCES season_teams(steam_id);

ALTER TABLE teams ALTER COLUMN team_name SET NOT NULL;
ALTER TABLE season_teams ALTER COLUMN team_code SET NOT NULL;
ALTER TABLE season_teams ALTER COLUMN season_id SET NOT NULL;
ALTER TABLE stat_registers ALTER COLUMN steam_id SET NOT NULL;
