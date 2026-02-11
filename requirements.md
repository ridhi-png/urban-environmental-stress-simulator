# Requirements Document

## Introduction

The Urban Environmental Stress Simulator is an AI-powered system that analyzes environmental stress levels across urban zones and simulates the impact of policy interventions. The system combines data analysis, stress scoring algorithms, policy simulation, and AI-powered explanations through an interactive web dashboard.

## Glossary

- **System**: The Urban Environmental Stress Simulator application
- **Zone**: A geographic urban area being monitored (Zone A through Zone J)
- **AQI**: Air Quality Index, measuring air pollution levels (50-300 range)
- **Waste_Index**: Metric measuring waste management effectiveness (20-90 range)
- **Stress_Score**: Composite normalized score representing overall environmental stress (0-1 range)
- **Risk_Level**: Classification of stress severity (Low, Moderate, High)
- **Normalization**: Min-Max scaling transformation to 0-1 range
- **Policy_Simulation**: Hypothetical intervention modeling waste or emission reduction
- **Dashboard**: Streamlit web interface for user interaction
- **Stress_Engine**: Core calculation module for stress scoring
- **LLM_Explainer**: AI-powered explanation generation component

## Requirements

### Requirement 1: Synthetic Dataset Generation

**User Story:** As a developer, I want to generate realistic synthetic environmental data for urban zones, so that I can test and demonstrate the simulation system.

#### Acceptance Criteria

1. THE System SHALL create a CSV file at data/city_environment.csv with exactly 10 rows
2. THE System SHALL include columns: zone, AQI, waste_index, temperature, humidity
3. WHEN generating zone identifiers, THE System SHALL use labels "Zone A" through "Zone J"
4. THE System SHALL generate AQI values within the range 50-300
5. THE System SHALL generate waste_index values within the range 20-90
6. THE System SHALL generate temperature values within the range 15-40
7. THE System SHALL generate humidity values within the range 30-90
8. THE System SHALL ensure all generated values are realistic and varied across zones

### Requirement 2: Data Normalization

**User Story:** As a data analyst, I want to normalize environmental metrics to a common scale, so that I can compare and combine different measurements fairly.

#### Acceptance Criteria

1. WHEN provided with a numeric series, THE Stress_Engine SHALL apply Min-Max normalization using the formula (value - min) / (max - min)
2. THE Stress_Engine SHALL return normalized values in the range 0 to 1
3. WHEN all values in a series are identical, THE Stress_Engine SHALL handle the division by zero case gracefully
4. THE Stress_Engine SHALL preserve the relative ordering of values after normalization

### Requirement 3: Stress Score Calculation

**User Story:** As an environmental analyst, I want to calculate composite stress scores for urban zones, so that I can identify areas requiring intervention.

#### Acceptance Criteria

1. WHEN calculating stress scores, THE Stress_Engine SHALL normalize AQI, waste_index, and temperature values
2. THE Stress_Engine SHALL compute the composite score using the weighted formula: 0.5 × AQI_normalized + 0.3 × waste_normalized + 0.2 × temperature_normalized
3. THE Stress_Engine SHALL return stress scores in the range 0 to 1
4. THE Stress_Engine SHALL add a stress_score column to the dataframe
5. THE Stress_Engine SHALL preserve all original columns when adding stress scores

### Requirement 4: Risk Classification

**User Story:** As a policy maker, I want to classify zones by risk level, so that I can prioritize interventions appropriately.

#### Acceptance Criteria

1. WHEN a stress score is less than 0.4, THE Stress_Engine SHALL classify the risk as "Low"
2. WHEN a stress score is between 0.4 and 0.7 (inclusive), THE Stress_Engine SHALL classify the risk as "Moderate"
3. WHEN a stress score is greater than 0.7, THE Stress_Engine SHALL classify the risk as "High"
4. THE Stress_Engine SHALL return the risk classification as a string

### Requirement 5: Waste Reduction Simulation

**User Story:** As a policy maker, I want to simulate waste reduction interventions, so that I can predict their impact on environmental stress.

#### Acceptance Criteria

1. WHEN simulating waste reduction, THE Simulation SHALL accept a percentage parameter between 0 and 100
2. THE Simulation SHALL reduce the waste_index for all zones by the specified percentage
3. THE Simulation SHALL ensure waste_index values remain non-negative after reduction
4. THE Simulation SHALL return a modified dataframe with updated waste_index values
5. THE Simulation SHALL preserve all other columns unchanged

### Requirement 6: Emission Control Simulation

**User Story:** As a policy maker, I want to simulate emission control interventions, so that I can predict their impact on air quality and stress levels.

#### Acceptance Criteria

1. WHEN simulating emission control, THE Simulation SHALL accept a percentage parameter between 0 and 100
2. THE Simulation SHALL reduce the AQI for all zones by the specified percentage
3. THE Simulation SHALL ensure AQI values remain non-negative after reduction
4. THE Simulation SHALL return a modified dataframe with updated AQI values
5. THE Simulation SHALL preserve all other columns unchanged

### Requirement 7: Stress Recalculation

**User Story:** As a system user, I want stress scores to be recalculated after policy simulations, so that I can see the updated environmental impact.

#### Acceptance Criteria

1. WHEN recalculating stress, THE Simulation SHALL apply the same normalization and weighting formula as initial calculation
2. THE Simulation SHALL update both stress_score and risk_level columns
3. THE Simulation SHALL use the current (possibly modified) values of AQI, waste_index, and temperature
4. THE Simulation SHALL return a dataframe with updated stress metrics

### Requirement 8: AI Explanation Generation

**User Story:** As a dashboard user, I want AI-generated explanations of environmental conditions, so that I can understand the stress factors in plain language.

#### Acceptance Criteria

1. WHEN generating explanations, THE LLM_Explainer SHALL accept zone name, AQI, waste_index, stress_score, and risk_level as inputs
2. THE LLM_Explainer SHALL integrate with external LLM APIs (Gemini or OpenAI)
3. WHEN API integration is unavailable, THE LLM_Explainer SHALL provide a fallback explanation template
4. THE LLM_Explainer SHALL return explanations as formatted text strings
5. THE LLM_Explainer SHALL NOT contain hardcoded API keys in the source code

### Requirement 9: Interactive Dashboard

**User Story:** As a user, I want an interactive web dashboard, so that I can explore environmental data and simulate policy interventions visually.

#### Acceptance Criteria

1. THE Dashboard SHALL display a zone selector allowing users to choose from Zone A through Zone J
2. THE Dashboard SHALL provide a slider for waste reduction percentage (0-100%)
3. THE Dashboard SHALL provide a slider for emission reduction percentage (0-100%)
4. WHEN slider values change, THE Dashboard SHALL update stress scores and risk levels in real-time
5. THE Dashboard SHALL display current stress scores and risk levels for the selected zone
6. THE Dashboard SHALL render bar charts visualizing stress metrics across zones
7. THE Dashboard SHALL display AI-generated explanations for the selected zone
8. THE Dashboard SHALL load data from data/city_environment.csv on startup

### Requirement 10: Project Structure and Documentation

**User Story:** As a developer, I want clear project structure and documentation, so that I can understand, run, and extend the system easily.

#### Acceptance Criteria

1. THE System SHALL organize code into separate modules: stress_engine.py, simulation.py, llm_explainer.py, app.py
2. THE System SHALL include a requirements.txt file listing all Python dependencies
3. THE System SHALL include a README.md file with project overview, methodology, formulas, and execution instructions
4. THE System SHALL include clear code comments explaining normalization, weighted calculations, and policy impacts
5. THE System SHALL use beginner-friendly, readable code without advanced ML frameworks
6. THE System SHALL maintain modular structure with no file merging
