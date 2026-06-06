-- schema_decision_science_ai_governance.sql
-- SQLite-compatible schema for decision science in AI governance.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS option_scores;
DROP TABLE IF EXISTS ai_options;
DROP TABLE IF EXISTS scenarios;

CREATE TABLE ai_options (
    option_id TEXT PRIMARY KEY,
    option_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE option_scores (
    option_id TEXT PRIMARY KEY,
    baseline_value REAL,
    safety_stress REAL,
    equity_stress REAL,
    security_stress REAL,
    drift_stress REAL,
    evidence_quality REAL,
    oversight_strength REAL,
    equity_score REAL,
    transparency_score REAL,
    security_readiness REAL,
    implementation_feasibility REAL,
    FOREIGN KEY (option_id) REFERENCES ai_options(option_id)
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    probability REAL,
    description TEXT
);

CREATE TABLE scenario_performance (
    option_id TEXT,
    scenario_id TEXT,
    value REAL,
    PRIMARY KEY (option_id, scenario_id),
    FOREIGN KEY (option_id) REFERENCES ai_options(option_id),
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
