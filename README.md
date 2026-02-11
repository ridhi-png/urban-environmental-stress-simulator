# 🌆 Urban Environmental Stress Simulator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://urban-environmental-stress-simulator-kdrkgmb4napexfpkn8cezg.streamlit.app/)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> **An interactive web dashboard for simulating and analyzing urban environmental stress across city zones**

Empower city planners and environmental officials with data-driven insights into air quality, waste management, and policy interventions through intuitive visualizations and AI-powered explanations.

---

## ✨ Features

### 🎯 Core Capabilities

- **📊 Real-time Environmental Dashboard**: Interactive visualization of environmental metrics across 10 urban zones
- **🧮 Composite Stress Scoring**: Weighted calculation combining AQI, waste index, and temperature
- **🚦 Risk Classification**: Automatic categorization into Low, Moderate, and High risk levels
- **🎮 Policy Simulation**: Test "what-if" scenarios for waste reduction and emission control interventions
- **🤖 AI-Powered Insights**: Natural language explanations powered by Gemini or OpenAI (optional)
- **📈 Dynamic Charts**: Compare current conditions with simulated policy outcomes

### 🔬 Technical Highlights

- Min-Max normalization for fair metric comparison
- Weighted stress formula (AQI: 50%, Waste: 30%, Temperature: 20%)
- Synthetic data generation for testing and demonstrations
- Comprehensive unit tests with pytest and hypothesis

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ridhi-png/urban-environmental-stress-simulator.git
   cd urban-environmental-stress-simulator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data**
   ```bash
   python generate_data.py
   ```

4. **Launch the dashboard**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

---

## 🌐 Live Demo

Experience the app in action: **[Launch Simulator](https://urban-environmental-stress-simulator-kdrkgmb4napexfpkn8cezg.streamlit.app/)**

---

## 📖 How It Works

### Data Flow

```
Environmental Data → Normalization → Weighted Scoring → Risk Classification → Visualization
                                            ↓
                                  Policy Simulation
                                            ↓
                                  Comparative Analysis
```

### Stress Score Formula

```
stress_score = (0.5 × AQI_normalized) + (0.3 × waste_normalized) + (0.2 × temperature_normalized)
```

### Risk Levels

| Score Range | Classification | Interpretation |
|------------|---------------|----------------|
| 0.0 - 0.4  | 🟢 Low        | Acceptable conditions |
| 0.4 - 0.7  | 🟡 Moderate   | Monitoring advised |
| 0.7 - 1.0  | 🔴 High       | Immediate intervention required |

---

## 🎨 Screenshots

*Dashboard showing environmental metrics across all zones*

*Policy simulation comparison view*

---

## 🔧 Project Structure

```
urba...-environmental-stress-simulator/
├── app.py                  # Main Streamlit dashboard application
├── stress_engine.py        # Core stress calculation and classification
├── simulation.py           # Policy intervention simulation functions
├── llm_explainer.py        # AI-powered explanation generation
├── generate_data.py        # Synthetic data generation script
├── test_*.py              # Comprehensive unit tests
├── data/
│   └── city_environment.csv  # Environmental metrics data
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🧪 Running Tests

```bash
# Run all unit tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run property-based tests
pytest test_llm_explainer.py -v
```

---

## 🤝 Configuration

### Optional: Enable AI Explanations

For natural language insights, set an API key:

**Option 1: Google Gemini**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Option 2: OpenAI**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

*Note: The app falls back to template-based explanations if no API key is provided.*

---

## 📊 Sample Data

The simulator includes a data generator that creates realistic environmental metrics:

- **Zones**: 10 urban zones (Zone A - Zone J)
- **AQI Range**: 50-300 (Moderate to Hazardous)
- **Waste Index**: 20-90 (varied management effectiveness)
- **Temperature**: 15-40°C (temperate to hot climates)
- **Humidity**: 30-90% (dry to humid conditions)

---

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Interactive web dashboard
- **Data Processing**: [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis
- **Visualization**: [Matplotlib](https://matplotlib.org/) - Chart generation
- **Testing**: [pytest](https://pytest.org/) + [Hypothesis](https://hypothesis.readthedocs.io/) - Comprehensive testing
- **AI Integration**: Google Gemini / OpenAI (optional) - Natural language generation

---

## 🎯 Use Cases

### For City Planners
- Identify high-stress zones requiring immediate attention
- Simulate policy impacts before implementation
- Compare intervention strategies across zones

### For Environmental Officials
- Monitor air quality and waste management metrics
- Generate reports with AI-powered insights
- Track policy effectiveness over time

### For Researchers
- Test environmental stress models
- Analyze correlations between metrics
- Develop new intervention strategies

---

## 🌟 Roadmap

- [ ] Real-time data integration with city sensors
- [ ] Historical trend analysis and forecasting
- [ ] Mobile-responsive design
- [ ] Multi-city comparison
- [ ] Export reports as PDF
- [ ] Custom weighting for stress formula
- [ ] Integration with GIS mapping

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Ridhi** - [@ridhi-png](https://github.com/ridhi-png)

**Project Link**: [https://github.com/ridhi-png/urban-environmental-stress-simulator](https://github.com/ridhi-png/urban-environmental-stress-simulator)

**Live Demo**: [https://urban-environmental-stress-simulator-kdrkgmb4napexfpkn8cezg.streamlit.app/](https://urban-environmental-stress-simulator-kdrkgmb4napexfpkn8cezg.streamlit.app/)

---

## 🙏 Acknowledgments

- Inspired by real-world urban environmental challenges
- Built with ❤️ using Streamlit
- Thanks to the open-source community for amazing tools

---

<div align="center">
  <strong>Made with 🌱 for a sustainable future</strong>
</div>