-- schema_heuristics_biases.sql
-- SQLite-compatible schema for heuristic judgment and cognitive-bias diagnostics.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS debiasing_reviews;
DROP TABLE IF EXISTS calibration_scores;
DROP TABLE IF EXISTS judgment_cases;
DROP TABLE IF EXISTS bias_profiles;

CREATE TABLE bias_profiles (
    bias_profile_id INTEGER PRIMARY KEY,
    bias_profile TEXT NOT NULL UNIQUE,
    primary_mechanism TEXT,
    typical_distortion TEXT,
    review_priority TEXT
);

CREATE TABLE judgment_cases (
    case_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    bias_profile TEXT NOT NULL,
    base_rate REAL CHECK (base_rate >= 0 AND base_rate <= 1),
    evidence_signal REAL,
    anchor REAL CHECK (anchor >= 0 AND anchor <= 1),
    salience_multiplier REAL,
    confirming_evidence REAL,
    disconfirming_evidence REAL,
    judged_probability REAL CHECK (judged_probability >= 0 AND judged_probability <= 1),
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    outcome INTEGER CHECK (outcome IN (0, 1)),
    FOREIGN KEY (bias_profile) REFERENCES bias_profiles(bias_profile)
);

CREATE TABLE calibration_scores (
    score_id INTEGER PRIMARY KEY,
    case_id INTEGER NOT NULL,
    brier_score REAL,
    bias_magnitude REAL,
    confidence_gap REAL,
    calibration_gap REAL,
    review_flag TEXT,
    scored_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES judgment_cases(case_id)
);

CREATE TABLE debiasing_reviews (
    review_id INTEGER PRIMARY KEY,
    case_id INTEGER,
    bias_profile TEXT,
    review_method TEXT,
    review_owner TEXT,
    review_status TEXT,
    FOREIGN KEY (case_id) REFERENCES judgment_cases(case_id)
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    decision_context TEXT NOT NULL,
    bias_profile TEXT,
    base_rate REAL,
    judged_probability REAL,
    confidence REAL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
