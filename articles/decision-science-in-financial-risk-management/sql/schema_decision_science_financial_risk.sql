-- schema_decision_science_financial_risk.sql
-- SQLite-compatible schema for decision science in financial risk management.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS portfolio_scores;
DROP TABLE IF EXISTS portfolios;
DROP TABLE IF EXISTS scenarios;

CREATE TABLE portfolios (
    portfolio_id TEXT PRIMARY KEY,
    portfolio_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE portfolio_scores (
    portfolio_id TEXT PRIMARY KEY,
    normal REAL,
    recession REAL,
    liquidity_shock REAL,
    systemic_stress REAL,
    liquidity_score REAL,
    governance_score REAL,
    model_confidence REAL,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id)
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    probability REAL,
    description TEXT
);

CREATE TABLE scenario_performance (
    portfolio_id TEXT,
    scenario_id TEXT,
    loss_pct REAL,
    PRIMARY KEY (portfolio_id, scenario_id),
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
