# Urban Environmental Stress Simulator

An AI-powered system that analyzes environmental stress levels across urban zones and simulates the impact of policy interventions through an interactive web dashboard.

## Overview

The Urban Environmental Stress Simulator helps policy makers and environmental analysts understand and address environmental challenges in urban areas. The system:

- Analyzes environmental data (air quality, waste management, temperature, humidity) across 10 urban zones
- Calculates composite stress scores using a weighted normalization algorithm
- Classifies zones by risk level (Low, Moderate, High) to prioritize interventions
- Simulates policy interventions (waste reduction, emission control) to predict their impact
- Provides AI-powered explanations of environmental conditions
- Visualizes stress metrics through an interactive Streamlit dashboard

## Methodology

### Stress Scoring Formula

The system calculates environmental stress using a weighted composite score based on three key factors:

**1. Normalization (Min-Max Scaling)**

Each environmental metric is normalized to a [0, 1] range using:

```
normalized_value = (value - min_value) / (max_value - min_value)
```

Special case: When all values are identical (max = min), the normalized value is 0.

**2. Weighted Stress Score**

The composite stress score combines normalized metrics with weights reflecting their relative importance:

```
stress_score = 0.5 × AQI_normalized + 0.3 × waste_normalized + 0.2 × temperature_normalized
```

**Weighting Rationale:**
- **Air Quality Index (50%)**: Primary stress factor directly impacting respiratory health and quality of life
- **Waste Management (30%)**: Secondary factor affecting sanitation and environmental degradation
- **Temperature (20%)**: Contributing factor for thermal stress, weighted lower due to seasonal predictability

**3. Risk Classification**

Stress scores are classified into three risk levels:

| Stress Score | Risk Level | Description |
|--------------|------------|-------------|
| < 0.4 | Low | Acceptable conditions, routine monitoring sufficient |
| 0.4 - 0.7 | Moderate | Noticeable stress, targeted interventions may be needed |
| > 0.7 | High | Significant stress requiring immediate policy intervention |

### Policy Simulation

The system models two types of interventions:

**Waste Reduction:**
```
new_waste_index = original_waste_index × (1 - reduction_percentage / 100)
```

**Emission Control:**
```
new_AQI = original_AQI × (1 - reduction_percentage / 100)
```

After applying interventions, stress scores are recalculated to show the predicted impact.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

The required packages are:
- `pandas` - Data manipulation and analysis
- `streamlit` - Interactive web dashboard
- `matplotlib` - Data visualization
- `hypothesis` - Property-based testing
- `python-dotenv` - Environment variable management
- `google-generativeai` - Google Gemini API integration (optional)
- `openai` - OpenAI API integration (optional)

## Usage

### 1. Generate Synthetic Data

First, generate the environmental dataset:

```bash
python generate_data.py
```

This creates `data/city_environment.csv` with synthetic data for 10 urban zones (Zone A through Zone J).

### 2. Run the Dashboard

Launch the interactive Streamlit dashboard:

```bash
streamlit run app.py
```

The dashboard will open in your web browser (typically at `http://localhost:8501`).

### 3. Explore the Dashboard

**Controls (Sidebar):**
- **Zone Selector**: Choose a zone to view detailed metrics
- **Waste Reduction Slider**: Simulate waste reduction policies (0-100%)
- **Emission Control Slider**: Simulate emission control policies (0-100%)

**Main Panel:**
- **Zone Metrics**: View AQI, waste index, temperature, and humidity
- **Stress Assessment**: See the calculated stress score and risk level
- **Visualizations**: 
  - Bar chart showing stress scores across all zones
  - Bar chart showing risk level distribution
- **AI Explanation**: Get natural language analysis of environmental conditions

### 4. Configure LLM API Keys (Optional)

For AI-powered explanations, you can configure an LLM API key:

**Option 1: Google Gemini API**

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option 2: OpenAI API**

1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set the environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Note**: If no API key is configured, the system will use template-based explanations as a fallback.

## Project Structure

```
urban-environmental-stress-simulator/
├── data/
│   └── city_environment.csv      # Generated environmental data
├── tests/
│   ├── test_stress_engine.py     # Unit and property tests for stress calculations
│   ├── test_simulation.py        # Tests for policy simulations
│   └── test_llm_explainer.py     # Tests for AI explanation generation
├── stress_engine.py              # Core calculation module (normalization, scoring, classification)
├── simulation.py                 # Policy intervention simulation functions
├── llm_explainer.py              # AI-powered explanation generation
├── app.py                        # Streamlit dashboard application
├── generate_data.py              # Synthetic data generation script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Example Output

After running the dashboard, you'll see:

- **Stress scores** ranging from 0 to 1 for each zone
- **Risk levels** color-coded (green for Low, orange for Moderate, red for High)
- **Interactive simulations** showing how policy interventions affect stress levels
- **Visual comparisons** across all zones to identify priority areas
- **AI explanations** providing context and recommendations

## Development

### Running Tests

The project includes comprehensive unit and property-based tests:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_stress_engine.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Code Quality

The codebase follows these principles:
- Modular design with clear separation of concerns
- Comprehensive docstrings explaining formulas and rationale
- Property-based testing for universal correctness guarantees
- Beginner-friendly code without advanced ML frameworks
- No hardcoded API keys (environment variables only)

## License

This project is provided as-is for educational and demonstration purposes.

## Acknowledgments

Built with Python, Streamlit, and modern data science tools to demonstrate environmental policy simulation and AI-powered analysis.
