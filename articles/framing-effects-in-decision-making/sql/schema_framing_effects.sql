-- schema_framing_effects.sql
-- SQLite-compatible schema for framing effects and decision architecture.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS frame_scores;
DROP TABLE IF EXISTS framing_cases;
DROP TABLE IF EXISTS reference_points;

CREATE TABLE reference_points (
    reference_point_id INTEGER PRIMARY KEY,
    reference_point_type TEXT NOT NULL,
    value REAL NOT NULL,
    description TEXT
);

CREATE TABLE framing_cases (
    case_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    reference_point REAL NOT NULL,
    sure_outcome REAL NOT NULL,
    risky_high_outcome REAL NOT NULL,
    risky_high_probability REAL NOT NULL CHECK (risky_high_probability >= 0 AND risky_high_probability <= 1),
    loss_aversion REAL NOT NULL,
    alpha REAL NOT NULL,
    beta REAL NOT NULL
);

CREATE TABLE frame_scores (
    score_id INTEGER PRIMARY KEY,
    case_id INTEGER NOT NULL,
    gain_frame_choice TEXT,
    loss_frame_choice TEXT,
    frame_reversal INTEGER CHECK (frame_reversal IN (0, 1)),
    gain_risk_premium REAL,
    loss_risk_premium REAL,
    frame_sensitivity_index REAL,
    review_flag TEXT,
    scored_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES framing_cases(case_id)
);

CREATE TABLE review_triggers (
    trigger_id INTEGER PRIMARY KEY,
    indicator TEXT NOT NULL,
    threshold_direction TEXT NOT NULL,
    threshold_value REAL,
    review_owner TEXT
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    decision_context TEXT NOT NULL,
    current_frame TEXT,
    reference_point TEXT,
    equivalent_frames_tested TEXT,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
