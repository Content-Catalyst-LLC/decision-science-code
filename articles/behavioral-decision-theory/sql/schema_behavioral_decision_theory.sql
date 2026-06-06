-- schema_behavioral_decision_theory.sql
-- SQLite-compatible schema for behavioral decision theory.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS framing_cases;
DROP TABLE IF EXISTS behavioral_scores;
DROP TABLE IF EXISTS prospects;
DROP TABLE IF EXISTS alternatives;

CREATE TABLE alternatives (
    alternative_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    option_name TEXT NOT NULL,
    reference_point REAL NOT NULL,
    description TEXT
);

CREATE TABLE prospects (
    prospect_id TEXT PRIMARY KEY,
    alternative_id TEXT,
    outcome_1 REAL NOT NULL,
    probability_1 REAL CHECK (probability_1 >= 0 AND probability_1 <= 1),
    outcome_2 REAL NOT NULL,
    probability_2 REAL CHECK (probability_2 >= 0 AND probability_2 <= 1),
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id)
);

CREATE TABLE behavioral_scores (
    score_id TEXT PRIMARY KEY,
    alternative_id TEXT,
    expected_value REAL,
    expected_utility REAL,
    prospect_score REAL,
    probability_weight_distortion REAL,
    frame_sensitivity_index REAL,
    rank_divergence REAL,
    review_flag TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id)
);

CREATE TABLE framing_cases (
    frame_id TEXT PRIMARY KEY,
    frame_type TEXT NOT NULL,
    positive_frame TEXT,
    negative_frame TEXT,
    positive_value REAL,
    negative_value REAL,
    domain TEXT
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
    current_frame TEXT,
    reference_point TEXT,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
