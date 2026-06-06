-- schema_decision_science_infrastructure_planning.sql
-- SQLite-compatible schema for decision science in infrastructure planning.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS alternative_scores;
DROP TABLE IF EXISTS alternatives;
DROP TABLE IF EXISTS scenarios;

CREATE TABLE alternatives (
    alternative_id TEXT PRIMARY KEY,
    alternative_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE alternative_scores (
    alternative_id TEXT PRIMARY KEY,
    baseline REAL,
    climate_stress REAL,
    demand_growth REAL,
    funding_constraint REAL,
    disruption REAL,
    lifecycle_cost REAL,
    equity_score REAL,
    resilience_score REAL,
    environmental_score REAL,
    implementation_feasibility REAL,
    adaptability REAL,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id)
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    probability REAL,
    description TEXT
);

CREATE TABLE scenario_performance (
    alternative_id TEXT,
    scenario_id TEXT,
    value REAL,
    PRIMARY KEY (alternative_id, scenario_id),
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
