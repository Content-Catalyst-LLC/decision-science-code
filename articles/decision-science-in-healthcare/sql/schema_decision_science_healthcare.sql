-- schema_decision_science_healthcare.sql
-- SQLite-compatible schema for decision science in healthcare.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS treatment_scores;
DROP TABLE IF EXISTS treatments;
DROP TABLE IF EXISTS scenarios;

CREATE TABLE treatments (
    treatment_id TEXT PRIMARY KEY,
    treatment_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE treatment_scores (
    treatment_id TEXT PRIMARY KEY,
    expected_benefit REAL,
    adverse_event_risk REAL,
    cost_burden REAL,
    patient_preference_fit REAL,
    equity_score REAL,
    implementation_feasibility REAL,
    FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id)
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE scenario_performance (
    treatment_id TEXT,
    scenario_id TEXT,
    performance REAL,
    PRIMARY KEY (treatment_id, scenario_id),
    FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id),
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
