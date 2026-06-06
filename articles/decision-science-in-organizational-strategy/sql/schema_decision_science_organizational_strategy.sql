-- schema_decision_science_organizational_strategy.sql
-- SQLite-compatible schema for decision science in organizational strategy.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS strategy_scores;
DROP TABLE IF EXISTS strategies;
DROP TABLE IF EXISTS scenarios;

CREATE TABLE strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE strategy_scores (
    strategy_id TEXT PRIMARY KEY,
    low_growth REAL,
    base_case REAL,
    high_growth REAL,
    disruption REAL,
    adaptability REAL,
    capability_fit REAL,
    governance_feasibility REAL,
    reversibility REAL,
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id)
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    probability REAL,
    description TEXT
);

CREATE TABLE scenario_performance (
    strategy_id TEXT,
    scenario_id TEXT,
    value REAL,
    PRIMARY KEY (strategy_id, scenario_id),
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id),
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
