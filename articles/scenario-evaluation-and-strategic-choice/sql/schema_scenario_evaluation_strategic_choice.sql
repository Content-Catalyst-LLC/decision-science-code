-- schema_scenario_evaluation_strategic_choice.sql
-- SQLite-compatible schema for scenario evaluation and strategic choice.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS strategies;

CREATE TABLE strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    description TEXT
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
    performance REAL,
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
