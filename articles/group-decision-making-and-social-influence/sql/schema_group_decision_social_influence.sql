-- schema_group_decision_social_influence.sql
-- SQLite-compatible schema for group decision-making and social influence.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS influence_weights;
DROP TABLE IF EXISTS evidence_items;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS groups_table;

CREATE TABLE groups_table (
    group_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    true_value REAL,
    authority_concentration REAL,
    consensus_pressure REAL,
    shared_information INTEGER,
    unique_information INTEGER,
    decision_rule TEXT
);

CREATE TABLE members (
    member_id INTEGER,
    group_id INTEGER,
    role_name TEXT,
    expertise REAL,
    status REAL,
    independent_estimate REAL,
    influenced_estimate REAL,
    PRIMARY KEY (group_id, member_id),
    FOREIGN KEY (group_id) REFERENCES groups_table(group_id)
);

CREATE TABLE evidence_items (
    evidence_id TEXT PRIMARY KEY,
    group_id INTEGER,
    evidence_type TEXT,
    shared_status TEXT,
    quality TEXT,
    description TEXT,
    FOREIGN KEY (group_id) REFERENCES groups_table(group_id)
);

CREATE TABLE influence_weights (
    group_id INTEGER,
    member_id INTEGER,
    influence_weight REAL,
    influence_basis TEXT,
    PRIMARY KEY (group_id, member_id),
    FOREIGN KEY (group_id, member_id) REFERENCES members(group_id, member_id)
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
    decision_rule TEXT,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
