-- schema_bayesian_decision_making.sql
-- SQLite-compatible schema for Bayesian decision-making workflows.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS model_runs;
DROP TABLE IF EXISTS utilities;
DROP TABLE IF EXISTS posteriors;
DROP TABLE IF EXISTS likelihoods;
DROP TABLE IF EXISTS evidence;
DROP TABLE IF EXISTS priors;
DROP TABLE IF EXISTS hypotheses;

CREATE TABLE hypotheses (
    hypothesis_id INTEGER PRIMARY KEY,
    case_name TEXT NOT NULL,
    hypothesis_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE priors (
    prior_id INTEGER PRIMARY KEY,
    hypothesis_id INTEGER NOT NULL,
    prior_probability REAL NOT NULL CHECK (prior_probability >= 0 AND prior_probability <= 1),
    prior_type TEXT,
    source TEXT,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    FOREIGN KEY (hypothesis_id) REFERENCES hypotheses(hypothesis_id)
);

CREATE TABLE evidence (
    evidence_id INTEGER PRIMARY KEY,
    case_name TEXT NOT NULL,
    evidence_name TEXT NOT NULL,
    evidence_value TEXT,
    evidence_quality TEXT CHECK (evidence_quality IN ('low', 'medium', 'high')),
    observed_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE likelihoods (
    likelihood_id INTEGER PRIMARY KEY,
    hypothesis_id INTEGER NOT NULL,
    evidence_id INTEGER NOT NULL,
    sensitivity REAL CHECK (sensitivity >= 0 AND sensitivity <= 1),
    false_positive_rate REAL CHECK (false_positive_rate >= 0 AND false_positive_rate <= 1),
    likelihood_notes TEXT,
    FOREIGN KEY (hypothesis_id) REFERENCES hypotheses(hypothesis_id),
    FOREIGN KEY (evidence_id) REFERENCES evidence(evidence_id)
);

CREATE TABLE posteriors (
    posterior_id INTEGER PRIMARY KEY,
    hypothesis_id INTEGER NOT NULL,
    evidence_id INTEGER NOT NULL,
    posterior_probability REAL NOT NULL CHECK (posterior_probability >= 0 AND posterior_probability <= 1),
    posterior_odds REAL,
    bayes_factor REAL,
    calculated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hypothesis_id) REFERENCES hypotheses(hypothesis_id),
    FOREIGN KEY (evidence_id) REFERENCES evidence(evidence_id)
);

CREATE TABLE utilities (
    utility_id INTEGER PRIMARY KEY,
    case_name TEXT NOT NULL,
    action_name TEXT NOT NULL,
    state_name TEXT NOT NULL,
    utility_value REAL NOT NULL
);

CREATE TABLE model_runs (
    run_id INTEGER PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    language TEXT NOT NULL,
    status TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    case_name TEXT NOT NULL,
    selected_action TEXT,
    prior_notes TEXT,
    evidence_notes TEXT,
    likelihood_notes TEXT,
    posterior_summary TEXT,
    utility_summary TEXT,
    sensitivity_notes TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
