-- Decision Science SQL schema
-- Educational schema for decisions, alternatives, criteria, weights, scenarios, outcomes, assumptions, and decision records.

CREATE TABLE IF NOT EXISTS decisions (
    decision_id INTEGER PRIMARY KEY,
    decision_name TEXT NOT NULL,
    decision_context TEXT NOT NULL,
    decision_owner TEXT,
    framing_note TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alternatives (
    alternative_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    alternative_name TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id)
);

CREATE TABLE IF NOT EXISTS criteria (
    criterion_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    criterion_name TEXT NOT NULL,
    description TEXT NOT NULL,
    weight REAL NOT NULL,
    direction TEXT NOT NULL,
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id)
);

CREATE TABLE IF NOT EXISTS alternative_scores (
    score_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    criterion_id INTEGER NOT NULL,
    score_value REAL NOT NULL,
    evidence_note TEXT,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (criterion_id) REFERENCES criteria(criterion_id)
);

CREATE TABLE IF NOT EXISTS scenarios (
    scenario_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    scenario_name TEXT NOT NULL,
    description TEXT NOT NULL,
    plausibility_note TEXT,
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id)
);

CREATE TABLE IF NOT EXISTS scenario_outcomes (
    outcome_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    outcome_value REAL NOT NULL,
    interpretation_note TEXT,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE IF NOT EXISTS assumptions (
    assumption_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    assumption_text TEXT NOT NULL,
    confidence REAL NOT NULL,
    impact_if_wrong REAL NOT NULL,
    testing_method TEXT,
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id)
);

CREATE TABLE IF NOT EXISTS decision_records (
    record_id INTEGER PRIMARY KEY,
    decision_id INTEGER NOT NULL,
    selected_alternative_id INTEGER,
    rationale TEXT NOT NULL,
    uncertainty_note TEXT,
    tradeoff_note TEXT,
    review_date TEXT,
    FOREIGN KEY (decision_id) REFERENCES decisions(decision_id),
    FOREIGN KEY (selected_alternative_id) REFERENCES alternatives(alternative_id)
);

INSERT INTO decisions
(decision_id, decision_name, decision_context, decision_owner, framing_note, status)
VALUES
(1, 'Synthetic Decision Science Example', 'Public policy and resilience planning', 'example', 'Compare alternatives under uncertainty, trade-offs, and implementation risk.', 'draft');

INSERT INTO criteria
(criterion_id, decision_id, criterion_name, description, weight, direction)
VALUES
(1, 1, 'Cost Efficiency', 'Relative cost performance.', 0.16, 'maximize'),
(2, 1, 'Effectiveness', 'Expected ability to achieve the stated objective.', 0.22, 'maximize'),
(3, 1, 'Equity', 'Distributional fairness and protection of vulnerable groups.', 0.18, 'maximize'),
(4, 1, 'Feasibility', 'Implementation practicality under current conditions.', 0.16, 'maximize'),
(5, 1, 'Resilience', 'Ability to remain viable under disruption.', 0.20, 'maximize'),
(6, 1, 'Implementation Risk', 'Risk of execution failure or harmful side effects.', -0.08, 'minimize');
