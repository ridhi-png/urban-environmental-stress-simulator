"""
Tests for LLM Explainer Module

This module tests the generate_explanation function with both unit tests
and property-based tests.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from hypothesis import given, strategies as st
from llm_explainer import generate_explanation

# Check if optional API libraries are available
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class TestGenerateExplanation:
    """Unit tests for generate_explanation function."""
    
    def test_fallback_explanation_no_api_key(self):
        """Test that fallback template is used when no API key is available."""
        # Ensure no API keys in environment
        with patch.dict(os.environ, {}, clear=True):
            result = generate_explanation("Zone A", 150, 45, 0.55, "Moderate")
            
            assert isinstance(result, str)
            assert "Zone A" in result
            assert "Moderate" in result
            assert "0.55" in result
            assert "150" in result
            assert "45" in result
    
    def test_fallback_high_risk(self):
        """Test fallback template for high risk level."""
        with patch.dict(os.environ, {}, clear=True):
            result = generate_explanation("Zone B", 250, 80, 0.85, "High")
            
            assert "High risk level" in result
            assert "Immediate intervention" in result
    
    def test_fallback_low_risk(self):
        """Test fallback template for low risk level."""
        with patch.dict(os.environ, {}, clear=True):
            result = generate_explanation("Zone C", 80, 25, 0.25, "Low")
            
            assert "Low risk level" in result
            assert "acceptable ranges" in result
    
    def test_fallback_moderate_risk(self):
        """Test fallback template for moderate risk level."""
        with patch.dict(os.environ, {}, clear=True):
            result = generate_explanation("Zone D", 150, 50, 0.50, "Moderate")
            
            assert "Moderate risk level" in result
            assert "Monitoring is advised" in result
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="google-generativeai not installed")
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_gemini_api_success(self, mock_model_class, mock_configure):
        """Test successful Gemini API call."""
        # Mock Gemini API response
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Zone A shows moderate environmental stress with elevated AQI."
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            result = generate_explanation("Zone A", 150, 45, 0.55, "Moderate")
            
            assert result == "Zone A shows moderate environmental stress with elevated AQI."
            mock_configure.assert_called_once_with(api_key='test_key')
    
    @pytest.mark.skipif(not GEMINI_AVAILABLE, reason="google-generativeai not installed")
    @patch('google.generativeai.GenerativeModel')
    def test_gemini_api_failure_fallback(self, mock_model_class):
        """Test that fallback is used when Gemini API fails."""
        # Mock Gemini API to raise exception
        mock_model_class.side_effect = Exception("API Error")
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            result = generate_explanation("Zone A", 150, 45, 0.55, "Moderate")
            
            # Should fall back to template
            assert isinstance(result, str)
            assert "Zone A" in result
            assert "Moderate" in result
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="openai not installed")
    @patch('openai.OpenAI')
    def test_openai_api_success(self, mock_openai_class):
        """Test successful OpenAI API call."""
        # Mock OpenAI API response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Zone B has high pollution levels requiring attention."
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            result = generate_explanation("Zone B", 200, 60, 0.70, "High")
            
            assert result == "Zone B has high pollution levels requiring attention."
    
    @pytest.mark.skipif(not OPENAI_AVAILABLE, reason="openai not installed")
    @patch('openai.OpenAI')
    def test_openai_api_failure_fallback(self, mock_openai_class):
        """Test that fallback is used when OpenAI API fails."""
        # Mock OpenAI API to raise exception
        mock_openai_class.side_effect = Exception("API Error")
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            result = generate_explanation("Zone B", 200, 60, 0.70, "High")
            
            # Should fall back to template
            assert isinstance(result, str)
            assert "Zone B" in result
            assert "High" in result


class TestGenerateExplanationProperties:
    """Property-based tests for generate_explanation function."""
    
    # Feature: urban-environmental-stress-simulator, Property 14: Explanation Returns String
    @given(
        zone=st.text(min_size=1, max_size=20),
        aqi=st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False),
        waste=st.floats(min_value=20, max_value=90, allow_nan=False, allow_infinity=False),
        stress_score=st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        risk_level=st.sampled_from(["Low", "Moderate", "High"])
    )
    def test_explanation_returns_string(self, zone, aqi, waste, stress_score, risk_level):
        """
        For any set of zone metrics, generate_explanation should return a string.
        
        **Validates: Requirements 8.4**
        """
        with patch.dict(os.environ, {}, clear=True):
            result = generate_explanation(zone, aqi, waste, stress_score, risk_level)
            assert isinstance(result, str), f"Expected string, got {type(result)}"
            assert len(result) > 0, "Explanation should not be empty"
