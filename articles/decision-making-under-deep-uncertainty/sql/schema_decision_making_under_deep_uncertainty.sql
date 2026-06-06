-- schema_decision_making_under_deep_uncertainty.sql
-- SQLite-compatible schema for decision-making under deep uncertainty.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS thresholds;
DROP TABLE IF EXISTS ambiguity_profiles;
DROP TABLE IF EXISTS performance;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS strategies;

CREATE TABLE strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    base_return REAL,
    volatility REAL,
    adaptability REAL,
    resilience REAL,
    description TEXT
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE performance (
    strategy_id TEXT,
    scenario_id TEXT,
    performance_value REAL,
    PRIMARY KEY (strategy_id, scenario_id),
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE ambiguity_profiles (
    profile_name TEXT,
    scenario_id TEXT,
    weight REAL CHECK (weight >= 0),
    PRIMARY KEY (profile_name, scenario_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE thresholds (
    threshold_name TEXT PRIMARY KEY,
    threshold_value REAL,
    description TEXT
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
