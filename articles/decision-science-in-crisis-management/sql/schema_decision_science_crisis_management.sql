PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS option_scores;
DROP TABLE IF EXISTS response_options;
DROP TABLE IF EXISTS scenarios;

CREATE TABLE response_options (
    option_id TEXT PRIMARY KEY,
    option_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE option_scores (
    option_id TEXT PRIMARY KEY,
    baseline REAL,
    rapid_escalation REAL,
    resource_constraint REAL,
    public_trust_stress REAL,
    cascading_failure REAL,
    speed_score REAL,
    feasibility_score REAL,
    equity_score REAL,
    trust_score REAL,
    continuity_score REAL,
    adaptability REAL,
    FOREIGN KEY (option_id) REFERENCES response_options(option_id)
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
    PRIMARY KEY (option_id, scenario_id)
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
