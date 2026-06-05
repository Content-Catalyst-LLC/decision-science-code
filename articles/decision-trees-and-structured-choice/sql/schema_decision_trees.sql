-- schema_decision_trees.sql
-- SQLite-compatible schema for decision trees and structured choice.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS model_runs;
DROP TABLE IF EXISTS outcomes;
DROP TABLE IF EXISTS probabilities;
DROP TABLE IF EXISTS branches;
DROP TABLE IF EXISTS nodes;
DROP TABLE IF EXISTS decisions;

CREATE TABLE decisions (
    decision_id INTEGER PRIMARY KEY,
    decision_name TEXT NOT NULL,
    decision_context TEXT,
    decision_owner TEXT
);

CREATE TABLE nodes (
    node_id TEXT PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    node_type TEXT NOT NULL CHECK (node_type IN ('decision', 'chance', 'terminal')),
    label TEXT NOT NULL,
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id)
);

CREATE TABLE branches (
    branch_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    from_node TEXT NOT NULL,
    to_node TEXT NOT NULL,
    branch_label TEXT NOT NULL,
    branch_type TEXT NOT NULL CHECK (branch_type IN ('decision', 'chance')),
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id),
    FOREIGN KEY (from_node) REFERENCES nodes(node_id),
    FOREIGN KEY (to_node) REFERENCES nodes(node_id)
);

CREATE TABLE probabilities (
    probability_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    strategy TEXT NOT NULL,
    outcome_state TEXT NOT NULL,
    probability REAL NOT NULL CHECK (probability >= 0 AND probability <= 1),
    quality TEXT CHECK (quality IN ('low', 'medium', 'high')),
    source_type TEXT,
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id)
);

CREATE TABLE outcomes (
    outcome_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    strategy TEXT NOT NULL,
    outcome_state TEXT NOT NULL,
    terminal_value REAL NOT NULL,
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id)
);

CREATE TABLE model_runs (
    run_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    workflow_name TEXT NOT NULL,
    language TEXT NOT NULL,
    status TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id)
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    selected_strategy TEXT,
    rollback_summary TEXT,
    sensitivity_notes TEXT,
    value_of_information_notes TEXT,
    regret_notes TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id)
);
