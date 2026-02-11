# Implementation Plan: Urban Environmental Stress Simulator

## Overview

This implementation plan breaks down the Urban Environmental Stress Simulator into discrete coding tasks. The approach follows a bottom-up strategy: build core calculation modules first, add simulation capabilities, integrate AI explanations, and finally create the interactive dashboard. Each task builds incrementally with testing integrated throughout.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create directory structure: `data/`, `tests/`
  - Create empty Python files: `stress_engine.py`, `simulation.py`, `llm_explainer.py`, `app.py`
  - Create `requirements.txt` with dependencies: pandas, streamlit, matplotlib, hypothesis, python-dotenv, google-generativeai, openai
  - Create `.env.example` file showing required environment variables
  - _Requirements: 10.1, 10.2_

- [ ] 2. Implement data generation
  - [x] 2.1 Create data generation script
    - Write function to generate 10 zones with random environmental data
    - Ensure AQI (50-300), waste_index (20-90), temperature (15-40), humidity (30-90)
    - Save to `data/city_environment.csv` with proper headers
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_
  
  - [ ]* 2.2 Write property test for data generation bounds
    - **Property 1: Data Generation Bounds**
    - **Validates: Requirements 1.4, 1.5, 1.6, 1.7**
  
  - [ ]* 2.3 Write unit tests for data generation
    - Test CSV structure (10 rows, correct columns)
    - Test zone naming (Zone A through Zone J)
    - _Requirements: 1.1, 1.2, 1.3_

- [ ] 3. Implement stress engine core functions
  - [x] 3.1 Implement normalize() function
    - Apply Min-Max normalization: (value - min) / (max - min)
    - Handle edge case when max == min (return zeros)
    - Add docstring explaining formula and edge cases
    - _Requirements: 2.1, 2.3_
  
  - [ ]* 3.2 Write property tests for normalization
    - **Property 2: Normalization Formula Correctness**
    - **Validates: Requirements 2.1**
    - **Property 3: Normalization Output Range**
    - **Validates: Requirements 2.2**
    - **Property 4: Normalization Preserves Ordering**
    - **Validates: Requirements 2.4**
  
  - [x] 3.3 Implement calculate_stress_score() function
    - Normalize AQI, waste_index, temperature columns
    - Apply weighted formula: 0.5*AQI + 0.3*waste + 0.2*temp
    - Add stress_score column to dataframe
    - Add docstring explaining weighting rationale
    - _Requirements: 3.1, 3.2, 3.4, 3.5_
  
  - [ ]* 3.4 Write property tests for stress calculation
    - **Property 5: Stress Score Weighted Formula**
    - **Validates: Requirements 3.2**
    - **Property 6: Stress Calculation Preserves Original Data**
    - **Validates: Requirements 3.5**
  
  - [x] 3.5 Implement classify_risk() function
    - Return "Low" for score < 0.4
    - Return "Moderate" for 0.4 ≤ score ≤ 0.7
    - Return "High" for score > 0.7
    - Add docstring explaining thresholds
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  
  - [ ]* 3.6 Write property tests for risk classification
    - **Property 7: Risk Classification Correctness**
    - **Validates: Requirements 4.1, 4.2, 4.3**
    - **Property 8: Risk Classification Returns String**
    - **Validates: Requirements 4.4**

- [x] 4. Checkpoint - Ensure stress engine tests pass
  - Run all stress_engine tests
  - Verify property tests run 100+ iterations
  - Ask user if questions arise

- [ ] 5. Implement simulation layer
  - [x] 5.1 Implement simulate_waste_reduction() function
    - Accept dataframe and percentage (0-100)
    - Calculate reduction: waste_index * (1 - percent/100)
    - Ensure non-negative values
    - Return modified dataframe
    - Add docstring explaining policy simulation
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [x] 5.2 Implement simulate_emission_control() function
    - Accept dataframe and percentage (0-100)
    - Calculate reduction: AQI * (1 - percent/100)
    - Ensure non-negative values
    - Return modified dataframe
    - Add docstring explaining policy simulation
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ]* 5.3 Write property tests for simulations
    - **Property 9: Percentage Reduction Formula**
    - **Validates: Requirements 5.2, 6.2**
    - **Property 10: Simulation Maintains Non-Negative Values**
    - **Validates: Requirements 5.3, 6.3**
    - **Property 11: Simulation Preserves Unrelated Columns**
    - **Validates: Requirements 5.5, 6.5**
  
  - [x] 5.4 Implement recalculate_stress() function
    - Call calculate_stress_score() on current dataframe
    - Apply classify_risk() to each stress score
    - Add risk_level column
    - Return dataframe with updated stress metrics
    - _Requirements: 7.1, 7.2, 7.3, 7.4_
  
  - [ ]* 5.5 Write property tests for stress recalculation
    - **Property 12: Stress Recalculation Consistency**
    - **Validates: Requirements 7.1**
    - **Property 13: Recalculation Uses Current Values**
    - **Validates: Requirements 7.3**
  
  - [ ]* 5.6 Write unit tests for simulation edge cases
    - Test 0% reduction (no change)
    - Test 100% reduction (values become 0)
    - Test with single-row dataframe
    - _Requirements: 5.1, 5.2, 5.3, 6.1, 6.2, 6.3_

- [x] 6. Checkpoint - Ensure simulation tests pass
  - Run all simulation tests
  - Verify integration between stress_engine and simulation modules
  - Ask user if questions arise

- [ ] 7. Implement LLM explainer
  - [x] 7.1 Create generate_explanation() function
    - Accept zone, AQI, waste, stress_score, risk_level parameters
    - Check for GEMINI_API_KEY or OPENAI_API_KEY in environment
    - If API key exists, construct prompt and call LLM API
    - Implement fallback template for when API unavailable
    - Add error handling with timeout (10 seconds)
    - Return formatted explanation string
    - Add docstring explaining API integration and fallback
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  
  - [ ]* 7.2 Write property test for explanation output
    - **Property 14: Explanation Returns String**
    - **Validates: Requirements 8.4**
  
  - [ ]* 7.3 Write unit tests for LLM explainer
    - Test with mocked Gemini API (successful response)
    - Test with mocked OpenAI API (successful response)
    - Test fallback when no API key present
    - Test fallback on API timeout
    - Test fallback on API error
    - _Requirements: 8.2, 8.3_

- [ ] 8. Implement Streamlit dashboard
  - [x] 8.1 Create data loading function
    - Load CSV with pandas
    - Calculate initial stress scores and risk levels
    - Use @st.cache_data decorator for performance
    - Add error handling for missing file
    - _Requirements: 9.8_
  
  - [x] 8.2 Create dashboard layout and sidebar
    - Add title: "Urban Environmental Stress Simulator"
    - Create sidebar with zone selector (dropdown for Zone A-J)
    - Add waste reduction slider (0-100%, default 0)
    - Add emission control slider (0-100%, default 0)
    - _Requirements: 9.1, 9.2, 9.3_
  
  - [x] 8.3 Implement simulation application logic
    - Apply waste reduction based on slider value
    - Apply emission control based on slider value
    - Recalculate stress scores after simulations
    - Update dataframe reactively when sliders change
    - _Requirements: 9.4_
  
  - [x] 8.4 Create metrics display for selected zone
    - Display zone name as header
    - Show AQI, waste_index, temperature, humidity using st.metric()
    - Highlight stress_score and risk_level with color coding
    - Use green for Low, yellow for Moderate, red for High
    - _Requirements: 9.5_
  
  - [x] 8.5 Create visualization charts
    - Bar chart: Stress scores by zone (matplotlib)
    - Bar chart: Risk level distribution (count of Low/Moderate/High)
    - Use color coding consistent with risk levels
    - Display charts with st.pyplot()
    - _Requirements: 9.6_
  
  - [x] 8.6 Integrate AI explanations
    - Call generate_explanation() for selected zone
    - Display explanation in expandable text box
    - Show loading indicator while generating
    - Handle errors gracefully with fallback message
    - _Requirements: 9.7_
  
  - [ ]* 8.7 Write integration tests for dashboard components
    - Test data loading with valid CSV
    - Test data loading with missing CSV
    - Test simulation application logic
    - _Requirements: 9.8_

- [ ] 9. Create documentation
  - [x] 9.1 Write README.md
    - Project overview and purpose
    - Methodology section explaining stress scoring formula
    - Mathematical formulas for normalization and weighting
    - Installation instructions (pip install -r requirements.txt)
    - Data generation instructions
    - How to run the dashboard (streamlit run app.py)
    - Optional: How to configure LLM API keys
    - Screenshots or example output (optional)
    - _Requirements: 10.3_
  
  - [x] 9.2 Add inline code comments
    - Explain normalization formula in normalize()
    - Explain weighted sum in calculate_stress_score()
    - Explain policy impact calculations in simulation functions
    - Add module-level docstrings to each file
    - _Requirements: 10.4_

- [ ] 10. Final integration and testing
  - [x] 10.1 Generate sample dataset
    - Run data generation to create city_environment.csv
    - Verify CSV has realistic varied values
    - _Requirements: 1.8_
  
  - [x] 10.2 Run complete test suite
    - Execute all unit tests
    - Execute all property tests (verify 100+ iterations)
    - Check test coverage (aim for 80%+ on core modules)
    - Fix any failing tests
  
  - [-] 10.3 Manual dashboard testing
    - Start Streamlit app
    - Test zone selection
    - Test slider interactions
    - Verify charts update correctly
    - Test with and without API keys
    - Verify error handling for edge cases
  
  - [ ] 10.4 Code quality review
    - Verify modular structure (no merged files)
    - Check that code is beginner-friendly
    - Ensure no hardcoded API keys
    - Verify all files have proper docstrings
    - _Requirements: 10.4, 10.5, 10.6, 8.5_

- [ ] 11. Final checkpoint - Project complete
  - Ensure all tests pass
  - Verify README is complete and accurate
  - Confirm dashboard runs without errors
  - Ask user if any final adjustments needed

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties with 100+ iterations
- Unit tests validate specific examples and edge cases
- The implementation follows a bottom-up approach: core logic → simulation → AI → dashboard
- Checkpoints ensure incremental validation at key milestones
