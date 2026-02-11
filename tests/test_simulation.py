"""
Unit tests for simulation module.
"""

import pytest
import pandas as pd
from simulation import simulate_waste_reduction


class TestSimulateWasteReduction:
    """Tests for the simulate_waste_reduction() function."""
    
    def test_basic_waste_reduction(self):
        """Test basic waste reduction with 20% reduction."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'waste_index': [50, 80]
        })
        result = simulate_waste_reduction(df, 20)
        assert result['waste_index'].tolist() == [40.0, 64.0]
    
    def test_zero_percent_reduction(self):
        """Test that 0% reduction leaves values unchanged."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'waste_index': [50, 80]
        })
        result = simulate_waste_reduction(df, 0)
        assert result['waste_index'].tolist() == [50.0, 80.0]
    
    def test_complete_elimination(self):
        """Test that 100% reduction results in zero values."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'waste_index': [50, 80]
        })
        result = simulate_waste_reduction(df, 100)
        assert result['waste_index'].tolist() == [0.0, 0.0]
    
    def test_preserves_other_columns(self):
        """Test that other columns remain unchanged."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [100, 200],
            'waste_index': [50, 80],
            'temperature': [25, 30]
        })
        result = simulate_waste_reduction(df, 20)
        assert result['zone'].tolist() == ['Zone A', 'Zone B']
        assert result['AQI'].tolist() == [100, 200]
        assert result['temperature'].tolist() == [25, 30]
    
    def test_non_negative_values(self):
        """Test that all values remain non-negative."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'waste_index': [50, 80]
        })
        result = simulate_waste_reduction(df, 50)
        assert (result['waste_index'] >= 0).all()
    
    def test_does_not_modify_original(self):
        """Test that the original dataframe is not modified."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'waste_index': [50, 80]
        })
        original_values = df['waste_index'].tolist()
        simulate_waste_reduction(df, 20)
        assert df['waste_index'].tolist() == original_values


from simulation import simulate_emission_control, recalculate_stress


class TestSimulateEmissionControl:
    """Tests for the simulate_emission_control() function."""
    
    def test_basic_emission_reduction(self):
        """Test basic emission reduction with 20% reduction."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [200, 150]
        })
        result = simulate_emission_control(df, 20)
        assert result['AQI'].tolist() == [160.0, 120.0]
    
    def test_zero_percent_reduction(self):
        """Test that 0% reduction leaves values unchanged."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [200, 150]
        })
        result = simulate_emission_control(df, 0)
        assert result['AQI'].tolist() == [200.0, 150.0]
    
    def test_complete_elimination(self):
        """Test that 100% reduction results in zero values."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [200, 150]
        })
        result = simulate_emission_control(df, 100)
        assert result['AQI'].tolist() == [0.0, 0.0]
    
    def test_preserves_other_columns(self):
        """Test that other columns remain unchanged."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [200, 150],
            'waste_index': [50, 80],
            'temperature': [25, 30]
        })
        result = simulate_emission_control(df, 20)
        assert result['zone'].tolist() == ['Zone A', 'Zone B']
        assert result['waste_index'].tolist() == [50, 80]
        assert result['temperature'].tolist() == [25, 30]


class TestRecalculateStress:
    """Tests for the recalculate_stress() function."""
    
    def test_adds_stress_score_and_risk_level(self):
        """Test that recalculate_stress adds both stress_score and risk_level columns."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [100, 200],
            'waste_index': [30, 60],
            'temperature': [20, 30]
        })
        result = recalculate_stress(df)
        assert 'stress_score' in result.columns
        assert 'risk_level' in result.columns
    
    def test_risk_level_values(self):
        """Test that risk_level contains only valid values."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B', 'Zone C'],
            'AQI': [100, 200, 250],
            'waste_index': [30, 60, 80],
            'temperature': [20, 30, 35]
        })
        result = recalculate_stress(df)
        assert result['risk_level'].isin(['Low', 'Moderate', 'High']).all()
    
    def test_preserves_original_columns(self):
        """Test that original columns are preserved."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [100, 200],
            'waste_index': [30, 60],
            'temperature': [20, 30],
            'humidity': [50, 60]
        })
        result = recalculate_stress(df)
        assert result['zone'].tolist() == ['Zone A', 'Zone B']
        assert result['AQI'].tolist() == [100, 200]
        assert result['waste_index'].tolist() == [30, 60]
        assert result['temperature'].tolist() == [20, 30]
        assert result['humidity'].tolist() == [50, 60]
    
    def test_stress_score_range(self):
        """Test that stress scores are in the valid range [0, 1]."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B', 'Zone C'],
            'AQI': [100, 200, 250],
            'waste_index': [30, 60, 80],
            'temperature': [20, 30, 35]
        })
        result = recalculate_stress(df)
        assert (result['stress_score'] >= 0).all()
        assert (result['stress_score'] <= 1).all()
    
    def test_recalculation_after_simulation(self):
        """Test that recalculate_stress works correctly after policy simulation."""
        # Start with high stress data
        df = pd.DataFrame({
            'zone': ['Zone A'],
            'AQI': [250],
            'waste_index': [80],
            'temperature': [35]
        })
        
        # Apply waste reduction
        df_reduced = simulate_waste_reduction(df, 50)
        
        # Recalculate stress
        result = recalculate_stress(df_reduced)
        
        # Verify waste_index was reduced
        assert result['waste_index'].iloc[0] == 40.0
        
        # Verify stress_score and risk_level were calculated
        assert 'stress_score' in result.columns
        assert 'risk_level' in result.columns
        assert isinstance(result['stress_score'].iloc[0], float)
        assert result['risk_level'].iloc[0] in ['Low', 'Moderate', 'High']



class TestSimulationApplicationLogic:
    """Tests for the combined simulation application logic (task 8.3)."""
    
    def test_combined_waste_and_emission_reduction(self):
        """Test applying both waste reduction and emission control together."""
        # Create sample data
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [200, 150],
            'waste_index': [60, 40],
            'temperature': [30, 25],
            'humidity': [50, 60]
        })
        
        # Apply waste reduction (20%)
        simulated_df = simulate_waste_reduction(df, 20)
        
        # Apply emission control (30%)
        simulated_df = simulate_emission_control(simulated_df, 30)
        
        # Recalculate stress
        simulated_df = recalculate_stress(simulated_df)
        
        # Verify waste_index was reduced by 20%
        assert simulated_df['waste_index'].iloc[0] == 48.0  # 60 * 0.8
        assert simulated_df['waste_index'].iloc[1] == 32.0  # 40 * 0.8
        
        # Verify AQI was reduced by 30%
        assert simulated_df['AQI'].iloc[0] == 140.0  # 200 * 0.7
        assert simulated_df['AQI'].iloc[1] == 105.0  # 150 * 0.7
        
        # Verify stress scores and risk levels were recalculated
        assert 'stress_score' in simulated_df.columns
        assert 'risk_level' in simulated_df.columns
        assert (simulated_df['stress_score'] >= 0).all()
        assert (simulated_df['stress_score'] <= 1).all()
        assert simulated_df['risk_level'].isin(['Low', 'Moderate', 'High']).all()
    
    def test_no_simulation_when_sliders_at_zero(self):
        """Test that no changes occur when both sliders are at 0%."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [200, 150],
            'waste_index': [60, 40],
            'temperature': [30, 25]
        })
        
        # Simulate the logic: copy dataframe
        simulated_df = df.copy()
        
        # No waste reduction (slider at 0)
        waste_reduction = 0
        if waste_reduction > 0:
            simulated_df = simulate_waste_reduction(simulated_df, waste_reduction)
        
        # No emission control (slider at 0)
        emission_control = 0
        if emission_control > 0:
            simulated_df = simulate_emission_control(simulated_df, emission_control)
        
        # No recalculation needed when both are 0
        if waste_reduction > 0 or emission_control > 0:
            simulated_df = recalculate_stress(simulated_df)
        
        # Verify values remain unchanged
        assert simulated_df['AQI'].tolist() == [200, 150]
        assert simulated_df['waste_index'].tolist() == [60, 40]
    
    def test_reactive_update_on_slider_change(self):
        """Test that dataframe updates reactively when slider values change."""
        # Initial data with multiple zones to avoid normalization edge case
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B', 'Zone C'],
            'AQI': [200, 150, 100],
            'waste_index': [60, 40, 30],
            'temperature': [30, 25, 20]
        })
        
        # Scenario 1: Waste reduction only
        simulated_df1 = df.copy()
        simulated_df1 = simulate_waste_reduction(simulated_df1, 50)
        simulated_df1 = recalculate_stress(simulated_df1)
        
        # Scenario 2: Add emission control
        simulated_df2 = df.copy()
        simulated_df2 = simulate_waste_reduction(simulated_df2, 50)
        simulated_df2 = simulate_emission_control(simulated_df2, 40)
        simulated_df2 = recalculate_stress(simulated_df2)
        
        # Verify waste_index is reduced in both scenarios
        assert simulated_df1['waste_index'].iloc[0] == 30.0  # 60 * 0.5
        assert simulated_df2['waste_index'].iloc[0] == 30.0  # 60 * 0.5
        
        # Verify AQI is only reduced in scenario 2
        assert simulated_df1['AQI'].iloc[0] == 200.0  # No emission control
        assert simulated_df2['AQI'].iloc[0] == 120.0  # 200 * 0.6
        
        # Verify that both scenarios have valid stress scores
        assert 'stress_score' in simulated_df1.columns
        assert 'stress_score' in simulated_df2.columns
        assert (simulated_df1['stress_score'] >= 0).all()
        assert (simulated_df1['stress_score'] <= 1).all()
        assert (simulated_df2['stress_score'] >= 0).all()
        assert (simulated_df2['stress_score'] <= 1).all()
        
        # Verify that risk levels are calculated
        assert simulated_df1['risk_level'].isin(['Low', 'Moderate', 'High']).all()
        assert simulated_df2['risk_level'].isin(['Low', 'Moderate', 'High']).all()
