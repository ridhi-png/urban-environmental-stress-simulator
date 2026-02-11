# Design Document: Urban Environmental Stress Simulator

## Overview

The Urban Environmental Stress Simulator is a Python-based web application that analyzes environmental stress across urban zones and simulates policy interventions. The system architecture follows a modular design with four core components:

1. **Stress Engine**: Core calculation module for normalization and stress scoring
2. **Simulation Layer**: Policy intervention modeling (waste reduction, emission control)
3. **LLM Explainer**: AI-powered natural language explanation generation
4. **Streamlit Dashboard**: Interactive web interface for visualization and user interaction

The system processes synthetic environmental data (AQI, waste index, temperature, humidity) through a weighted scoring algorithm to produce actionable stress assessments and risk classifications.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard (app.py)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Zone Selector│  │   Sliders    │  │  Visualizations│     │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────┬────────────────┬────────────────┬──────────────┘
             │                │                │
             ▼                ▼                ▼
┌────────────────────┐ ┌──────────────┐ ┌──────────────────┐
│  Stress Engine     │ │  Simulation  │ │  LLM Explainer   │
│  (stress_engine.py)│ │(simulation.py)│ │(llm_explainer.py)│
│                    │ │              │ │                  │
│ • normalize()      │ │ • simulate_  │ │ • generate_      │
│ • calculate_stress │ │   waste_     │ │   explanation()  │
│ • classify_risk()  │ │   reduction()│ │                  │
│                    │ │ • simulate_  │ │ • LLM API        │
│                    │ │   emission_  │ │   integration    │
│                    │ │   control()  │ │                  │
│                    │ │ • recalculate│ │                  │
│                    │ │   _stress()  │ │                  │
└────────────────────┘ └──────────────┘ └──────────────────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  Data Layer      │
                    │ city_environment │
                    │     .csv         │
                    └──────────────────┘
```

**Data Flow:**
1. Dashboard loads CSV data on startup
2. User selects zone and adjusts policy sliders
3. Simulation layer applies interventions to data
4. Stress engine recalculates scores and risk levels
5. LLM explainer generates contextual explanations
6. Dashboard updates visualizations and displays results

## Components and Interfaces

### 1. Data Layer (data/city_environment.csv)

**Structure:**
```csv
zone,AQI,waste_index,temperature,humidity
Zone A,150,45,28,65
Zone B,220,75,35,50
...
```

**Schema:**
- `zone` (string): Zone identifier (Zone A - Zone J)
- `AQI` (int): Air Quality Index (50-300)
- `waste_index` (int): Waste management metric (20-90)
- `temperature` (float): Temperature in Celsius (15-40)
- `humidity` (int): Relative humidity percentage (30-90)

**Generation Logic:**
- Use Python's random module with appropriate ranges
- Ensure varied distribution across zones
- Store as CSV for easy inspection and modification

### 2. Stress Engine Module (stress_engine.py)

**Function: normalize(series: pd.Series) -> pd.Series**
```python
# Min-Max normalization: (value - min) / (max - min)
# Returns: Series with values scaled to [0, 1]
# Edge case: If max == min, return series of zeros
```

**Function: calculate_stress_score(df: pd.DataFrame) -> pd.DataFrame**
```python
# Input: DataFrame with AQI, waste_index, temperature columns
# Process:
#   1. Normalize AQI, waste_index, temperature
#   2. Apply weighted formula: 0.5*AQI_norm + 0.3*waste_norm + 0.2*temp_norm
#   3. Add 'stress_score' column to dataframe
# Returns: DataFrame with added stress_score column
```

**Function: classify_risk(score: float) -> str**
```python
# Input: Stress score (0-1 range)
# Returns: "Low" if score < 0.4
#          "Moderate" if 0.4 <= score <= 0.7
#          "High" if score > 0.7
```

**Design Rationale:**
- Weighted formula prioritizes air quality (50%) as primary stress factor
- Waste management (30%) and temperature (20%) are secondary factors
- Normalization ensures fair comparison across different measurement scales
- Risk thresholds chosen to create balanced distribution across categories

### 3. Simulation Layer (simulation.py)

**Function: simulate_waste_reduction(df: pd.DataFrame, percent: float) -> pd.DataFrame**
```python
# Input: DataFrame, reduction percentage (0-100)
# Process:
#   1. Calculate reduction factor: (100 - percent) / 100
#   2. Apply to waste_index: waste_index * reduction_factor
#   3. Ensure non-negative values
# Returns: DataFrame with modified waste_index
```

**Function: simulate_emission_control(df: pd.DataFrame, percent: float) -> pd.DataFrame**
```python
# Input: DataFrame, reduction percentage (0-100)
# Process:
#   1. Calculate reduction factor: (100 - percent) / 100
#   2. Apply to AQI: AQI * reduction_factor
#   3. Ensure non-negative values
# Returns: DataFrame with modified AQI
```

**Function: recalculate_stress(df: pd.DataFrame) -> pd.DataFrame**
```python
# Input: DataFrame (possibly with modified AQI/waste_index)
# Process:
#   1. Call calculate_stress_score() from stress_engine
#   2. Apply classify_risk() to each stress score
#   3. Add 'risk_level' column
# Returns: DataFrame with updated stress_score and risk_level
```

**Design Rationale:**
- Percentage-based reductions are intuitive for policy makers
- Functions return new dataframes (immutable approach) for clarity
- Recalculation uses same engine logic to ensure consistency

### 4. LLM Explainer Module (llm_explainer.py)

**Function: generate_explanation(zone: str, aqi: float, waste: float, stress_score: float, risk_level: str) -> str**
```python
# Input: Zone metrics and calculated stress indicators
# Process:
#   1. Check for API key in environment variables
#   2. If available, call LLM API (Gemini or OpenAI) with structured prompt
#   3. If unavailable, use fallback template
# Returns: Formatted explanation string
```

**LLM Prompt Template:**
```
Analyze the environmental stress for {zone}:
- Air Quality Index: {aqi}
- Waste Index: {waste}
- Stress Score: {stress_score:.2f}
- Risk Level: {risk_level}

Provide a brief explanation (2-3 sentences) of the environmental conditions 
and their implications for residents.
```

**Fallback Template:**
```
{zone} has a {risk_level} risk level with a stress score of {stress_score:.2f}.
The Air Quality Index is {aqi} and waste management index is {waste}.
[Additional context based on risk level]
```

**API Integration:**
- Support for Google Gemini API (google-generativeai library)
- Support for OpenAI API (openai library)
- API keys loaded from environment variables (GEMINI_API_KEY or OPENAI_API_KEY)
- Graceful degradation to template-based explanations

### 5. Streamlit Dashboard (app.py)

**Layout Structure:**
```
┌─────────────────────────────────────────────────┐
│  Title: Urban Environmental Stress Simulator    │
├─────────────────────────────────────────────────┤
│  Sidebar:                                       │
│    • Zone Selector (dropdown)                   │
│    • Waste Reduction Slider (0-100%)            │
│    • Emission Control Slider (0-100%)           │
├─────────────────────────────────────────────────┤
│  Main Panel:                                    │
│    • Selected Zone Metrics (cards)              │
│    • Stress Score & Risk Level (highlighted)    │
│    • Bar Chart: Stress Scores by Zone          │
│    • Bar Chart: Risk Distribution               │
│    • AI Explanation (text box)                  │
└─────────────────────────────────────────────────┘
```

**Key Functions:**
```python
def load_data() -> pd.DataFrame:
    # Load CSV, calculate initial stress scores
    # Cache with @st.cache_data decorator

def apply_simulations(df, waste_pct, emission_pct) -> pd.DataFrame:
    # Apply both simulations, recalculate stress
    
def render_zone_metrics(zone_data):
    # Display metrics in columns using st.metric()
    
def render_charts(df):
    # Create matplotlib bar charts
    # Display with st.pyplot()
```

**Interactivity:**
- Sliders trigger automatic recalculation
- Zone selector updates displayed metrics and explanation
- Charts update to reflect simulated changes
- Color coding for risk levels (green/yellow/red)

## Data Models

### Environmental Data Record
```python
{
    'zone': str,           # "Zone A" through "Zone J"
    'AQI': int,            # 50-300
    'waste_index': int,    # 20-90
    'temperature': float,  # 15-40
    'humidity': int,       # 30-90
    'stress_score': float, # 0-1 (calculated)
    'risk_level': str      # "Low", "Moderate", "High" (calculated)
}
```

### Normalization Formula
```
normalized_value = (value - min_value) / (max_value - min_value)

Special case: If max_value == min_value, return 0
```

### Stress Score Formula
```
stress_score = (0.5 × AQI_normalized) + 
               (0.3 × waste_normalized) + 
               (0.2 × temperature_normalized)

Where each component is normalized to [0, 1] range
```

### Risk Classification Thresholds
```
score < 0.4:           "Low"
0.4 ≤ score ≤ 0.7:     "Moderate"
score > 0.7:           "High"
```

### Policy Simulation Formula
```
new_value = original_value × (1 - reduction_percentage / 100)

Example: 20% reduction on AQI of 200
new_AQI = 200 × (1 - 20/100) = 200 × 0.8 = 160
```


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Data Generation Bounds

*For any* generated environmental dataset, all AQI values should be within [50, 300], all waste_index values within [20, 90], all temperature values within [15, 40], and all humidity values within [30, 90].

**Validates: Requirements 1.4, 1.5, 1.6, 1.7**

### Property 2: Normalization Formula Correctness

*For any* numeric series with at least one value, applying Min-Max normalization should produce values where each normalized value equals (original_value - min) / (max - min), except when max equals min, in which case all values should be 0.

**Validates: Requirements 2.1**

### Property 3: Normalization Output Range

*For any* numeric series, all normalized values should be within the range [0, 1].

**Validates: Requirements 2.2**

### Property 4: Normalization Preserves Ordering

*For any* numeric series, if value A is greater than value B in the original series, then normalized A should be greater than normalized B (relative ordering is preserved).

**Validates: Requirements 2.4**

### Property 5: Stress Score Weighted Formula

*For any* dataframe with AQI, waste_index, and temperature columns, the calculated stress_score should equal exactly 0.5 × normalized_AQI + 0.3 × normalized_waste + 0.2 × normalized_temperature.

**Validates: Requirements 3.2**

### Property 6: Stress Calculation Preserves Original Data

*For any* dataframe, after calculating stress scores, all original columns (zone, AQI, waste_index, temperature, humidity) should remain unchanged.

**Validates: Requirements 3.5**

### Property 7: Risk Classification Correctness

*For any* stress score value, the risk classification should be "Low" when score < 0.4, "Moderate" when 0.4 ≤ score ≤ 0.7, and "High" when score > 0.7.

**Validates: Requirements 4.1, 4.2, 4.3**

### Property 8: Risk Classification Returns String

*For any* stress score value, the classify_risk function should return a string type.

**Validates: Requirements 4.4**

### Property 9: Percentage Reduction Formula

*For any* dataframe and reduction percentage in [0, 100], applying waste reduction or emission control should multiply the target column values by (1 - percentage/100).

**Validates: Requirements 5.2, 6.2**

### Property 10: Simulation Maintains Non-Negative Values

*For any* dataframe and reduction percentage in [0, 100], after applying waste reduction or emission control, all values in the modified column should be non-negative.

**Validates: Requirements 5.3, 6.3**

### Property 11: Simulation Preserves Unrelated Columns

*For any* dataframe, after applying waste reduction, all columns except waste_index should remain unchanged; after applying emission control, all columns except AQI should remain unchanged.

**Validates: Requirements 5.5, 6.5**

### Property 12: Stress Recalculation Consistency

*For any* dataframe, recalculating stress scores should produce the same stress_score values as calling calculate_stress_score on the same data.

**Validates: Requirements 7.1**

### Property 13: Recalculation Uses Current Values

*For any* dataframe, if AQI or waste_index values are modified and stress is recalculated, the new stress scores should reflect the modified values, not the original values.

**Validates: Requirements 7.3**

### Property 14: Explanation Returns String

*For any* set of zone metrics (zone name, AQI, waste_index, stress_score, risk_level), the generate_explanation function should return a string type.

**Validates: Requirements 8.4**

## Error Handling

### Data Loading Errors
- **Missing CSV file**: Display clear error message indicating file path and suggest running data generation
- **Malformed CSV**: Validate column names and data types, provide specific error about what's wrong
- **Empty dataset**: Check for minimum 1 row, display error if empty

### Calculation Errors
- **Division by zero in normalization**: When max == min, return series of zeros (handled in normalize function)
- **Invalid stress score range**: Add assertion to verify 0 ≤ stress_score ≤ 1, log warning if violated
- **Missing columns**: Validate required columns exist before calculations, raise ValueError with missing column names

### Simulation Errors
- **Invalid percentage**: Validate 0 ≤ percentage ≤ 100, raise ValueError if out of range
- **Negative values after reduction**: Use max(0, reduced_value) to ensure non-negative results
- **Empty dataframe**: Check for empty dataframe before simulation, return empty dataframe with warning

### LLM API Errors
- **Missing API key**: Check environment variables, fall back to template if not found
- **API timeout**: Set 10-second timeout, fall back to template on timeout
- **API error response**: Catch exceptions, log error, use template fallback
- **Rate limiting**: Implement exponential backoff (1s, 2s, 4s), max 3 retries, then fallback

### Dashboard Errors
- **File not found on startup**: Display error page with instructions to generate data
- **Invalid zone selection**: Validate zone exists in dataframe, default to first zone if invalid
- **Chart rendering errors**: Wrap matplotlib calls in try-except, display error message instead of chart
- **Slider value errors**: Streamlit handles slider bounds, but validate before passing to simulation functions

## Testing Strategy

### Dual Testing Approach

The system will use both unit testing and property-based testing to ensure comprehensive coverage:

- **Unit tests**: Verify specific examples, edge cases, and error conditions
- **Property tests**: Verify universal properties across all inputs

These approaches are complementary—unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing Configuration

**Library Selection**: Use `hypothesis` for Python property-based testing

**Test Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Each property test must reference its design document property
- Tag format: `# Feature: urban-environmental-stress-simulator, Property {number}: {property_text}`

**Property Test Implementation**:
- Each correctness property listed above must be implemented as a single property-based test
- Use Hypothesis strategies to generate random test data:
  - `st.floats()` for numeric values with appropriate bounds
  - `st.integers()` for discrete values
  - `st.lists()` for generating dataframes with multiple rows
  - Custom strategies for dataframe generation with required columns

### Unit Testing Focus

Unit tests should focus on:
- **Specific examples**: Test known input-output pairs (e.g., normalize([0, 50, 100]) → [0.0, 0.5, 1.0])
- **Edge cases**: Empty dataframes, single-row dataframes, identical values
- **Error conditions**: Invalid percentages, missing columns, malformed data
- **Integration points**: CSV loading, API mocking, dataframe transformations

**Avoid excessive unit tests**: Property-based tests handle covering lots of inputs, so unit tests should be selective and focus on scenarios that demonstrate specific behaviors or edge cases.

### Test Organization

```
tests/
├── test_stress_engine.py
│   ├── Unit tests for normalize, calculate_stress_score, classify_risk
│   └── Property tests for Properties 2-8
├── test_simulation.py
│   ├── Unit tests for simulation functions
│   └── Property tests for Properties 9-13
├── test_llm_explainer.py
│   ├── Unit tests with mocked APIs
│   └── Property test for Property 14
├── test_integration.py
│   └── End-to-end tests combining multiple components
└── test_data_generation.py
    ├── Unit test for CSV structure
    └── Property test for Property 1
```

### Example Property Test

```python
from hypothesis import given, strategies as st
import pandas as pd
from stress_engine import normalize

# Feature: urban-environmental-stress-simulator, Property 3: Normalization Output Range
@given(st.lists(st.floats(min_value=-1000, max_value=1000, allow_nan=False), min_size=1))
def test_normalization_output_range(values):
    """For any numeric series, all normalized values should be within [0, 1]"""
    series = pd.Series(values)
    normalized = normalize(series)
    assert all(0 <= val <= 1 for val in normalized), \
        f"Normalized values outside [0,1]: {normalized.tolist()}"
```

### Coverage Goals

- **Line coverage**: Minimum 80% for core modules (stress_engine, simulation)
- **Branch coverage**: Minimum 70% for conditional logic
- **Property coverage**: 100% of correctness properties must have corresponding tests
- **Edge case coverage**: All identified edge cases must have unit tests
