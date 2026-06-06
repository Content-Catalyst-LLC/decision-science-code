-- schema_cascading_risk_systemic_failure.sql
-- SQLite-compatible schema for cascading risk and systemic decision failure.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS system_scores;
DROP TABLE IF EXISTS systems;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS network_dependencies;

CREATE TABLE systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE system_scores (
    system_id TEXT PRIMARY KEY,
    exposure REAL,
    dependency_centrality REAL,
    buffer_weakness REAL,
    common_mode_risk REAL,
    monitoring_quality REAL,
    response_capacity REAL,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE scenario_performance (
    system_id TEXT,
    scenario_id TEXT,
    service_continuity REAL,
    PRIMARY KEY (system_id, scenario_id),
    FOREIGN KEY (system_id) REFERENCES systems(system_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE network_dependencies (
    target_node TEXT,
    source_node TEXT,
    dependency_weight REAL
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
