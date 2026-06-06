-- schema_tradeoffs_values_competing_objectives.sql
-- SQLite-compatible schema for trade-offs, values, and competing objectives.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_scores;
DROP TABLE IF EXISTS scenario_weights;
DROP TABLE IF EXISTS weights;
DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS objectives;
DROP TABLE IF EXISTS alternatives;

CREATE TABLE alternatives (
    alternative_id TEXT PRIMARY KEY,
    alternative_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE objectives (
    objective_id TEXT PRIMARY KEY,
    objective_name TEXT NOT NULL,
    direction TEXT CHECK (direction IN ('benefit', 'cost')),
    description TEXT
);

CREATE TABLE scores (
    alternative_id TEXT,
    objective_id TEXT,
    score REAL CHECK (score >= 0 AND score <= 1),
    evidence_quality TEXT,
    PRIMARY KEY (alternative_id, objective_id),
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (objective_id) REFERENCES objectives(objective_id)
);

CREATE TABLE weights (
    profile_name TEXT,
    objective_id TEXT,
    weight REAL CHECK (weight >= 0),
    PRIMARY KEY (profile_name, objective_id),
    FOREIGN KEY (objective_id) REFERENCES objectives(objective_id)
);

CREATE TABLE scenario_weights (
    scenario_name TEXT,
    objective_id TEXT,
    weight REAL CHECK (weight >= 0),
    PRIMARY KEY (scenario_name, objective_id),
    FOREIGN KEY (objective_id) REFERENCES objectives(objective_id)
);

CREATE TABLE scenario_scores (
    scenario_name TEXT,
    alternative_id TEXT,
    scenario_score REAL,
    regret REAL,
    rank INTEGER,
    PRIMARY KEY (scenario_name, alternative_id),
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id)
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
