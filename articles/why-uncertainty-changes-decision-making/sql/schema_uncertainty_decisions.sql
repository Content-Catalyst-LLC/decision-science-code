-- schema_uncertainty_decisions.sql
-- SQLite-compatible schema for uncertainty-aware decision workflows.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS value_of_information;
DROP TABLE IF EXISTS robustness_results;
DROP TABLE IF EXISTS regret_results;
DROP TABLE IF EXISTS ambiguity_assumptions;
DROP TABLE IF EXISTS scenario_outcomes;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS alternatives;

CREATE TABLE alternatives (
    alternative_id INTEGER PRIMARY KEY,
    alternative_name TEXT NOT NULL UNIQUE,
    ambiguity_exposure REAL CHECK (ambiguity_exposure >= 0),
    reversibility REAL CHECK (reversibility >= 0 AND reversibility <= 1),
    robustness REAL CHECK (robustness >= 0 AND robustness <= 1),
    implementation_capacity REAL CHECK (implementation_capacity >= 0 AND implementation_capacity <= 1),
    evidence_quality REAL CHECK (evidence_quality >= 0 AND evidence_quality <= 1),
    learning_capacity REAL CHECK (learning_capacity >= 0 AND learning_capacity <= 1)
);

CREATE TABLE scenarios (
    scenario_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL UNIQUE,
    probability REAL CHECK (probability >= 0 AND probability <= 1),
    disruption REAL,
    model_shift REAL,
    delay_cost REAL
);

CREATE TABLE scenario_outcomes (
    outcome_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    payoff REAL NOT NULL,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    UNIQUE (alternative_id, scenario_id)
);

CREATE TABLE ambiguity_assumptions (
    ambiguity_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    ambiguity_lambda REAL NOT NULL,
    ambiguity_penalty REAL NOT NULL,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id)
);

CREATE TABLE regret_results (
    regret_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    payoff REAL NOT NULL,
    best_payoff REAL NOT NULL,
    regret REAL NOT NULL,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE robustness_results (
    robustness_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    threshold REAL NOT NULL,
    robustness_share REAL NOT NULL,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id)
);

CREATE TABLE value_of_information (
    voi_id INTEGER PRIMARY KEY,
    decision_context TEXT NOT NULL,
    value_with_information REAL NOT NULL,
    value_without_information REAL NOT NULL,
    delay_cost REAL NOT NULL,
    net_value_of_information REAL NOT NULL
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
