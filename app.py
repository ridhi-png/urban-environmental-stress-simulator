"""
Streamlit Dashboard Application

This is the main entry point for the Urban Environmental Stress Simulator web dashboard.
It provides an interactive interface for exploring environmental data and simulating
policy interventions.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from stress_engine import calculate_stress_score, classify_risk


@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Load environmental data from CSV and calculate initial stress metrics.
    
    This function loads the city environmental data from the CSV file, calculates
    stress scores using the weighted formula, and classifies risk levels for each zone.
    The @st.cache_data decorator ensures the data is loaded only once and cached
    for performance, avoiding redundant calculations on every user interaction.
    
    Data Processing Steps:
    1. Load CSV file from data/city_environment.csv
    2. Calculate stress scores using the stress engine (weighted normalization)
    3. Classify risk levels (Low, Moderate, High) based on stress scores
    
    Returns:
        pd.DataFrame: DataFrame with columns:
            - zone: Zone identifier (Zone A through Zone J)
            - AQI: Air Quality Index
            - waste_index: Waste management metric
            - temperature: Temperature in Celsius
            - humidity: Relative humidity percentage
            - stress_score: Calculated composite stress score (0-1 range)
            - risk_level: Risk classification (Low, Moderate, High)
            
    Raises:
        FileNotFoundError: If data/city_environment.csv does not exist
        pd.errors.EmptyDataError: If the CSV file is empty
        KeyError: If required columns are missing from the CSV
        
    Examples:
        >>> df = load_data()
        >>> len(df)
        10
        >>> 'stress_score' in df.columns and 'risk_level' in df.columns
        True
    """
    # Define the path to the CSV file
    csv_path = Path("data/city_environment.csv")
    
    # Check if the file exists and provide helpful error message
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Data file not found at {csv_path}. "
            "Please run the data generation script first: python generate_data.py"
        )
    
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_path)
        
        # Validate that the dataframe is not empty
        if df.empty:
            raise pd.errors.EmptyDataError("The CSV file is empty. Please regenerate the data.")
        
        # Validate that required columns exist
        required_columns = ['zone', 'AQI', 'waste_index', 'temperature', 'humidity']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise KeyError(
                f"Missing required columns: {missing_columns}. "
                "Please ensure the CSV has all required columns."
            )
        
        # Calculate initial stress scores using the stress engine
        # This applies normalization and weighted formula to AQI, waste_index, and temperature
        df = calculate_stress_score(df)
        
        # Classify risk levels for each zone based on stress scores
        df['risk_level'] = df['stress_score'].apply(classify_risk)
        
        return df
        
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError(f"Error reading CSV file: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error loading data: {e}")


def main():
    """
    Main application function that sets up the dashboard layout and handles user interactions.
    """
    # Set page configuration
    st.set_page_config(
        page_title="Urban Environmental Stress Simulator",
        page_icon="🌆",
        layout="wide"
    )
    
    # Main title
    st.title("Urban Environmental Stress Simulator")
    
    # Load data
    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()
    
    # Sidebar controls
    st.sidebar.header("Controls")
    
    # Zone selector dropdown
    zones = df['zone'].unique().tolist()
    selected_zone = st.sidebar.selectbox(
        "Select Zone",
        options=zones,
        index=0
    )
    
    # Waste reduction slider
    waste_reduction = st.sidebar.slider(
        "Waste Reduction (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        help="Percentage reduction in waste index across all zones"
    )
    
    # Emission control slider
    emission_control = st.sidebar.slider(
        "Emission Control (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        help="Percentage reduction in Air Quality Index (AQI) across all zones"
    )
    
    # Apply simulations based on slider values
    # Import simulation functions
    from simulation import simulate_waste_reduction, simulate_emission_control, recalculate_stress
    from llm_explainer import generate_explanation
    
    # Start with the original loaded data
    simulated_df = df.copy()
    
    # Apply waste reduction if slider is not at 0
    if waste_reduction > 0:
        simulated_df = simulate_waste_reduction(simulated_df, waste_reduction)
    
    # Apply emission control if slider is not at 0
    if emission_control > 0:
        simulated_df = simulate_emission_control(simulated_df, emission_control)
    
    # Recalculate stress scores and risk levels after simulations
    # This ensures the stress metrics reflect the modified environmental values
    if waste_reduction > 0 or emission_control > 0:
        simulated_df = recalculate_stress(simulated_df)
    
    # Display metrics for selected zone
    st.header(f"📊 {selected_zone} Metrics")
    
    # Get the data for the selected zone
    zone_data = simulated_df[simulated_df['zone'] == selected_zone].iloc[0]
    
    # Create columns for metrics layout
    col1, col2, col3, col4 = st.columns(4)
    
    # Display environmental metrics using st.metric()
    with col1:
        st.metric(
            label="Air Quality Index (AQI)",
            value=f"{zone_data['AQI']:.1f}"
        )
    
    with col2:
        st.metric(
            label="Waste Index",
            value=f"{zone_data['waste_index']:.1f}"
        )
    
    with col3:
        st.metric(
            label="Temperature (°C)",
            value=f"{zone_data['temperature']:.1f}"
        )
    
    with col4:
        st.metric(
            label="Humidity (%)",
            value=f"{zone_data['humidity']:.1f}"
        )
    
    # Display stress score and risk level with color coding
    st.subheader("Stress Assessment")
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.metric(
            label="Stress Score",
            value=f"{zone_data['stress_score']:.3f}"
        )
    
    with col6:
        # Color code the risk level
        risk_level = zone_data['risk_level']
        
        # Define color mapping for risk levels
        risk_colors = {
            'Low': 'green',
            'Moderate': 'orange',
            'High': 'red'
        }
        
        # Get the color for the current risk level
        color = risk_colors.get(risk_level, 'gray')
        
        # Display risk level with color coding using markdown
        st.markdown(f"**Risk Level**")
        st.markdown(f":{color}[**{risk_level}**]")
    
    # Visualizations
    st.header("📈 Visualizations")
    
    # Create two columns for the charts
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.subheader("Stress Scores by Zone")
        
        # Create bar chart for stress scores
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        
        # Sort by stress score for better visualization
        sorted_df = simulated_df.sort_values('stress_score', ascending=False)
        
        # Define colors based on risk levels
        colors = []
        for risk in sorted_df['risk_level']:
            if risk == 'Low':
                colors.append('green')
            elif risk == 'Moderate':
                colors.append('orange')
            else:  # High
                colors.append('red')
        
        # Create bar chart
        ax1.bar(sorted_df['zone'], sorted_df['stress_score'], color=colors, alpha=0.7)
        ax1.set_xlabel('Zone', fontsize=10)
        ax1.set_ylabel('Stress Score', fontsize=10)
        ax1.set_ylim(0, 1.0)
        ax1.tick_params(axis='x', rotation=45, labelsize=9)
        ax1.tick_params(axis='y', labelsize=9)
        ax1.grid(axis='y', alpha=0.3)
        
        # Add a horizontal line at risk thresholds
        ax1.axhline(y=0.4, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
        ax1.axhline(y=0.7, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
        
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)
    
    with viz_col2:
        st.subheader("Risk Level Distribution")
        
        # Count risk levels
        risk_counts = simulated_df['risk_level'].value_counts()
        
        # Ensure all risk levels are present (even if count is 0)
        risk_levels = ['Low', 'Moderate', 'High']
        risk_counts = risk_counts.reindex(risk_levels, fill_value=0)
        
        # Create bar chart for risk distribution
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        
        # Define colors for risk levels
        risk_colors_chart = ['green', 'orange', 'red']
        
        # Create bar chart
        ax2.bar(risk_counts.index, risk_counts.values, color=risk_colors_chart, alpha=0.7)
        ax2.set_xlabel('Risk Level', fontsize=10)
        ax2.set_ylabel('Number of Zones', fontsize=10)
        ax2.set_ylim(0, max(10, risk_counts.max() + 1))
        ax2.tick_params(axis='x', labelsize=9)
        ax2.tick_params(axis='y', labelsize=9)
        ax2.grid(axis='y', alpha=0.3)
        
        # Add count labels on top of bars
        for i, (level, count) in enumerate(risk_counts.items()):
            ax2.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)
    
    # AI Explanation Section
    st.header("🤖 AI-Powered Explanation")
    
    # Display explanation in an expandable section
    with st.expander("View Environmental Analysis", expanded=True):
        # Show loading indicator while generating explanation
        with st.spinner("Generating AI explanation..."):
            try:
                # Call generate_explanation for the selected zone
                explanation = generate_explanation(
                    zone=zone_data['zone'],
                    aqi=zone_data['AQI'],
                    waste=zone_data['waste_index'],
                    stress_score=zone_data['stress_score'],
                    risk_level=zone_data['risk_level']
                )
                
                # Display the explanation
                st.write(explanation)
                
            except Exception as e:
                # Handle errors gracefully with fallback message
                st.warning(
                    f"Unable to generate AI explanation. "
                    f"Showing basic analysis instead."
                )
                
                # Provide a simple fallback message
                fallback_msg = (
                    f"{zone_data['zone']} has a {zone_data['risk_level']} risk level "
                    f"with a stress score of {zone_data['stress_score']:.2f}. "
                    f"The Air Quality Index is {zone_data['AQI']:.0f} and "
                    f"waste management index is {zone_data['waste_index']:.0f}."
                )
                st.write(fallback_msg)


if __name__ == "__main__":
    main()
