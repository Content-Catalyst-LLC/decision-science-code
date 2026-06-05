-- schema_decision_theory_science.sql
-- SQLite-compatible schema for comparing decision theory and decision science.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS robustness_results;
DROP TABLE IF EXISTS regret_profiles;
DROP TABLE IF EXISTS utilities;
DROP TABLE IF EXISTS probabilities;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS alternatives;

CREATE TABLE alternatives (
    alternative_id INTEGER PRIMARY KEY,
    alternative_name TEXT NOT NULL UNIQUE,
    strategy_type TEXT,
    implementation_capacity REAL,
    evidence_quality REAL,
    legitimacy REAL
);

CREATE TABLE scenarios (
    scenario_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE probabilities (
    probability_id INTEGER PRIMARY KEY,
    scenario_id INTEGER NOT NULL,
    probability REAL NOT NULL CHECK (probability >= 0 AND probability <= 1),
    probability_set TEXT NOT NULL,
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE utilities (
    utility_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    payoff REAL NOT NULL,
    utility_value REAL,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE regret_profiles (
    regret_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    payoff REAL NOT NULL,
    best_scenario_payoff REAL NOT NULL,
    regret REAL NOT NULL,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE robustness_results (
    robustness_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    threshold REAL NOT NULL,
    robustness_share REAL NOT NULL,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id)
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_strategy TEXT,
    decision_rule TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
