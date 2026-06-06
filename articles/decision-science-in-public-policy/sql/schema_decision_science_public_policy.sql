-- schema_decision_science_public_policy.sql
-- SQLite-compatible schema for decision science in public policy.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS policy_scores;
DROP TABLE IF EXISTS policies;
DROP TABLE IF EXISTS scenarios;

CREATE TABLE policies (
    policy_id TEXT PRIMARY KEY,
    policy_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE policy_scores (
    policy_id TEXT PRIMARY KEY,
    efficiency REAL,
    equity REAL,
    resilience REAL,
    feasibility REAL,
    legitimacy REAL,
    implementation_capacity REAL,
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE scenario_performance (
    policy_id TEXT,
    scenario_id TEXT,
    performance REAL,
    PRIMARY KEY (policy_id, scenario_id),
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id),
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
