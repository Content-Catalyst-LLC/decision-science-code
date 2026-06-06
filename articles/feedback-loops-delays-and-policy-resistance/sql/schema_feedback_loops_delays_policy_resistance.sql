-- schema_feedback_loops_delays_policy_resistance.sql
-- SQLite-compatible schema for feedback loops, delays, and policy resistance.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS context_scores;
DROP TABLE IF EXISTS policy_contexts;

CREATE TABLE policy_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE context_scores (
    context_id TEXT PRIMARY KEY,
    reinforcing_pressure REAL,
    balancing_correction REAL,
    implementation_delay REAL,
    resistance_intensity REAL,
    monitoring_quality REAL,
    FOREIGN KEY (context_id) REFERENCES policy_contexts(context_id)
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE scenario_performance (
    context_id TEXT,
    scenario_id TEXT,
    performance REAL,
    PRIMARY KEY (context_id, scenario_id),
    FOREIGN KEY (context_id) REFERENCES policy_contexts(context_id),
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
