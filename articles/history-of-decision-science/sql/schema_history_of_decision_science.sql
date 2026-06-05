-- schema_history_of_decision_science.sql
-- SQLite-compatible schema for historical decision-science workflows.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS robustness_results;
DROP TABLE IF EXISTS regret_results;
DROP TABLE IF EXISTS payoffs;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS paradigms;
DROP TABLE IF EXISTS historical_traditions;

CREATE TABLE historical_traditions (
    tradition_id INTEGER PRIMARY KEY,
    tradition_name TEXT NOT NULL UNIQUE,
    period TEXT,
    core_contribution TEXT,
    decision_question TEXT
);

CREATE TABLE paradigms (
    paradigm_id INTEGER PRIMARY KEY,
    paradigm_name TEXT NOT NULL UNIQUE,
    decision_rule TEXT,
    historical_note TEXT
);

CREATE TABLE scenarios (
    scenario_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL UNIQUE,
    objective_probability REAL CHECK (objective_probability >= 0 AND objective_probability <= 1),
    subjective_probability REAL CHECK (subjective_probability >= 0 AND subjective_probability <= 1)
);

CREATE TABLE payoffs (
    payoff_id INTEGER PRIMARY KEY,
    paradigm_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    payoff REAL NOT NULL,
    FOREIGN KEY (paradigm_id) REFERENCES paradigms(paradigm_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    UNIQUE (paradigm_id, scenario_id)
);

CREATE TABLE regret_results (
    regret_id INTEGER PRIMARY KEY,
    paradigm_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    payoff REAL NOT NULL,
    best_payoff REAL NOT NULL,
    regret REAL NOT NULL,
    FOREIGN KEY (paradigm_id) REFERENCES paradigms(paradigm_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE robustness_results (
    robustness_id INTEGER PRIMARY KEY,
    paradigm_id INTEGER NOT NULL,
    threshold REAL NOT NULL,
    robustness_share REAL NOT NULL,
    FOREIGN KEY (paradigm_id) REFERENCES paradigms(paradigm_id)
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
