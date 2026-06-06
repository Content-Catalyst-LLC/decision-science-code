PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS distributional_impacts;
DROP TABLE IF EXISTS alternative_scores;
DROP TABLE IF EXISTS criteria;
DROP TABLE IF EXISTS alternatives;

CREATE TABLE alternatives (
  alternative_id TEXT PRIMARY KEY,
  alternative_name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE criteria (
  criterion_id TEXT PRIMARY KEY,
  criterion_name TEXT NOT NULL,
  weight REAL,
  description TEXT
);

CREATE TABLE alternative_scores (
  alternative_id TEXT PRIMARY KEY,
  expected_value REAL,
  equity_score REAL,
  safety_score REAL,
  legitimacy_score REAL,
  transparency_score REAL,
  contestability_score REAL,
  reversibility_score REAL,
  accountability_score REAL,
  harm_risk REAL,
  opacity_risk REAL,
  exclusion_risk REAL
);

CREATE TABLE distributional_impacts (
  alternative_id TEXT,
  group_name TEXT,
  benefit REAL,
  cost REAL,
  risk REAL,
  net_benefit REAL
);

CREATE TABLE decision_records (
  record_id TEXT PRIMARY KEY,
  decision_context TEXT NOT NULL,
  selected_action TEXT,
  rationale TEXT,
  review_trigger TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
