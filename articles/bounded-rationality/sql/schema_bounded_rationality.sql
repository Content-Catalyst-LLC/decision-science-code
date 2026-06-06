-- schema_bounded_rationality.sql
-- SQLite-compatible schema for bounded rationality, search, satisficing, and decision records.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS stopping_rules;
DROP TABLE IF EXISTS aspiration_levels;
DROP TABLE IF EXISTS search_cycles;
DROP TABLE IF EXISTS alternatives;

CREATE TABLE alternatives (
    alternative_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    option_name TEXT NOT NULL,
    raw_utility REAL NOT NULL,
    implementation_risk REAL NOT NULL,
    uncertainty_penalty REAL NOT NULL,
    search_order INTEGER NOT NULL
);

CREATE TABLE search_cycles (
    cycle INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    aspiration REAL NOT NULL,
    search_cost_per_option REAL NOT NULL,
    n_options INTEGER NOT NULL,
    time_limit INTEGER
);

CREATE TABLE aspiration_levels (
    aspiration_id INTEGER PRIMARY KEY,
    period INTEGER NOT NULL,
    domain TEXT NOT NULL,
    aspiration REAL NOT NULL,
    feedback REAL,
    learning_rate REAL
);

CREATE TABLE stopping_rules (
    rule_id TEXT PRIMARY KEY,
    rule_name TEXT NOT NULL,
    description TEXT,
    primary_risk TEXT
);

CREATE TABLE review_triggers (
    trigger_id TEXT PRIMARY KEY,
    indicator TEXT NOT NULL,
    threshold_direction TEXT NOT NULL,
    threshold_value REAL,
    review_owner TEXT
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    aspiration REAL,
    search_rule TEXT,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
