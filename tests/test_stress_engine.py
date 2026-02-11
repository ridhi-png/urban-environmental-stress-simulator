"""
Unit tests for stress_engine module.
"""

import pytest
import pandas as pd
from stress_engine import normalize, calculate_stress_score, classify_risk


class TestClassifyRisk:
    """Tests for the classify_risk() function."""
    
    def test_low_risk_classification(self):
        """Test that scores below 0.4 are classified as Low."""
        assert classify_risk(0.0) == "Low"
        assert classify_risk(0.2) == "Low"
        assert classify_risk(0.39) == "Low"
    
    def test_moderate_risk_classification(self):
        """Test that scores between 0.4 and 0.7 (inclusive) are classified as Moderate."""
        assert classify_risk(0.4) == "Moderate"
        assert classify_risk(0.5) == "Moderate"
        assert classify_risk(0.7) == "Moderate"
    
    def test_high_risk_classification(self):
        """Test that scores above 0.7 are classified as High."""
        assert classify_risk(0.71) == "High"
        assert classify_risk(0.9) == "High"
        assert classify_risk(1.0) == "High"
    
    def test_boundary_values(self):
        """Test exact boundary values for risk classification."""
        # Just below 0.4 should be Low
        assert classify_risk(0.3999) == "Low"
        # Exactly 0.4 should be Moderate
        assert classify_risk(0.4) == "Moderate"
        # Exactly 0.7 should be Moderate
        assert classify_risk(0.7) == "Moderate"
        # Just above 0.7 should be High
        assert classify_risk(0.7001) == "High"
    
    def test_returns_string(self):
        """Test that classify_risk always returns a string."""
        assert isinstance(classify_risk(0.2), str)
        assert isinstance(classify_risk(0.5), str)
        assert isinstance(classify_risk(0.9), str)


class TestNormalize:
    """Tests for the normalize() function."""
    
    def test_basic_normalization(self):
        """Test normalization with simple values."""
        series = pd.Series([0, 50, 100])
        result = normalize(series)
        expected = pd.Series([0.0, 0.5, 1.0])
        pd.testing.assert_series_equal(result, expected)
    
    def test_identical_values(self):
        """Test edge case when all values are identical."""
        series = pd.Series([5, 5, 5])
        result = normalize(series)
        expected = pd.Series([0.0, 0.0, 0.0])
        pd.testing.assert_series_equal(result, expected)


class TestCalculateStressScore:
    """Tests for the calculate_stress_score() function."""
    
    def test_adds_stress_score_column(self):
        """Test that stress_score column is added to dataframe."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [100, 200],
            'waste_index': [30, 60],
            'temperature': [20, 30]
        })
        result = calculate_stress_score(df)
        assert 'stress_score' in result.columns
    
    def test_preserves_original_columns(self):
        """Test that original columns are preserved."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B'],
            'AQI': [100, 200],
            'waste_index': [30, 60],
            'temperature': [20, 30]
        })
        result = calculate_stress_score(df)
        assert list(df.columns) == ['zone', 'AQI', 'waste_index', 'temperature']
        assert all(col in result.columns for col in df.columns)
    
    def test_stress_score_in_valid_range(self):
        """Test that stress scores are in [0, 1] range."""
        df = pd.DataFrame({
            'zone': ['Zone A', 'Zone B', 'Zone C'],
            'AQI': [100, 200, 150],
            'waste_index': [30, 60, 45],
            'temperature': [20, 30, 25]
        })
        result = calculate_stress_score(df)
        assert (result['stress_score'] >= 0).all()
        assert (result['stress_score'] <= 1).all()
