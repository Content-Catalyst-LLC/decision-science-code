-- historical_traditions.sql

INSERT INTO historical_traditions (tradition_name, period, core_contribution, decision_question)
VALUES
('Probability foundations', '17th-18th century', 'Chance can be measured and compared', 'What is the probability-weighted payoff?'),
('Expected utility', '18th-20th century', 'Outcomes should be evaluated by utility not payoff alone', 'What is the probability-weighted utility?'),
('Subjective probability', '20th century', 'Beliefs can be formalized when frequencies are unavailable', 'What should be chosen given coherent belief?'),
('Operations research', '20th century', 'Mathematical models can improve organizational decisions', 'How should scarce resources be allocated?'),
('Bounded rationality', '20th century', 'Real decision-makers search and satisfice under constraints', 'What is good enough under limited information?'),
('Robust decision-making', 'late 20th-21st century', 'Strategies should perform acceptably across plausible futures', 'What remains viable under deep uncertainty?');
