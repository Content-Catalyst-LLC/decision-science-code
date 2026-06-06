-- schema_value_of_information_when_to_wait.sql
-- SQLite-compatible schema for value of information and decision timing.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS information_costs;
DROP TABLE IF EXISTS evidence_posteriors;
DROP TABLE IF EXISTS payoffs;
DROP TABLE IF EXISTS states;
DROP TABLE IF EXISTS actions;

CREATE TABLE actions (
    action_id TEXT PRIMARY KEY,
    action_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE states (
    state_id TEXT PRIMARY KEY,
    state_name TEXT NOT NULL,
    prior_probability REAL CHECK (prior_probability >= 0),
    description TEXT
);

CREATE TABLE payoffs (
    action_id TEXT,
    state_id TEXT,
    payoff_value REAL,
    PRIMARY KEY (action_id, state_id),
    FOREIGN KEY (action_id) REFERENCES actions(action_id),
    FOREIGN KEY (state_id) REFERENCES states(state_id)
);

CREATE TABLE evidence_posteriors (
    evidence_name TEXT,
    evidence_probability REAL,
    state_id TEXT,
    posterior_probability REAL,
    PRIMARY KEY (evidence_name, state_id),
    FOREIGN KEY (state_id) REFERENCES states(state_id)
);

CREATE TABLE information_costs (
    cost_name TEXT PRIMARY KEY,
    cost_value REAL,
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
