"""
LLM Explainer Module

This module provides AI-powered natural language explanation generation for environmental
stress conditions. It integrates with external LLM APIs (Gemini or OpenAI) with fallback
to template-based explanations.
"""

import os


def generate_explanation(zone: str, aqi: float, waste: float, stress_score: float, risk_level: str) -> str:
    """
    Generate a natural language explanation of environmental stress conditions.
    
    This function integrates with external LLM APIs (Google Gemini or OpenAI) to generate
    contextual explanations of environmental conditions. If no API key is available or if
    the API call fails, it falls back to a template-based explanation.
    
    Args:
        zone: Zone identifier (e.g., "Zone A")
        aqi: Air Quality Index value
        waste: Waste management index value
        stress_score: Calculated stress score (0-1 range)
        risk_level: Risk classification ("Low", "Moderate", or "High")
    
    Returns:
        A formatted string explaining the environmental conditions
    
    API Integration:
        - Checks for GEMINI_API_KEY or OPENAI_API_KEY in environment variables
        - Uses 10-second timeout for API calls
        - Gracefully falls back to template if API is unavailable or fails
    """
    # Check for API keys in environment
    gemini_key = os.environ.get('GEMINI_API_KEY')
    openai_key = os.environ.get('OPENAI_API_KEY')
    
    # Try LLM API if key is available
    if gemini_key:
        try:
            explanation = _call_gemini_api(zone, aqi, waste, stress_score, risk_level, gemini_key)
            return explanation
        except Exception:
            # Fall through to fallback template
            pass
    elif openai_key:
        try:
            explanation = _call_openai_api(zone, aqi, waste, stress_score, risk_level, openai_key)
            return explanation
        except Exception:
            # Fall through to fallback template
            pass
    
    # Fallback template when API is unavailable or fails
    return _generate_fallback_explanation(zone, aqi, waste, stress_score, risk_level)


def _call_gemini_api(zone: str, aqi: float, waste: float, stress_score: float, risk_level: str, api_key: str) -> str:
    """Call Google Gemini API to generate explanation."""
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""Analyze the environmental stress for {zone}:
- Air Quality Index: {aqi}
- Waste Index: {waste}
- Stress Score: {stress_score:.2f}
- Risk Level: {risk_level}

Provide a brief explanation (2-3 sentences) of the environmental conditions and their implications for residents."""
    
    # Generate with 10-second timeout
    response = model.generate_content(prompt, request_options={'timeout': 10})

if hasattr(response, "text") and response.text:
    return response.text
else:
    return _generate_fallback_explanation(zone, aqi, waste, stress_score, risk_level)



def _call_openai_api(zone: str, aqi: float, waste: float, stress_score: float, risk_level: str, api_key: str) -> str:
    """Call OpenAI API to generate explanation."""
    from openai import OpenAI
    
    client = OpenAI(api_key=api_key, timeout=10.0)
    
    prompt = f"""Analyze the environmental stress for {zone}:
- Air Quality Index: {aqi}
- Waste Index: {waste}
- Stress Score: {stress_score:.2f}
- Risk Level: {risk_level}

Provide a brief explanation (2-3 sentences) of the environmental conditions and their implications for residents."""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    
    return response.choices[0].message.content


def _generate_fallback_explanation(zone: str, aqi: float, waste: float, stress_score: float, risk_level: str) -> str:
    """Generate template-based explanation when API is unavailable."""
    base = f"{zone} has a {risk_level} risk level with a stress score of {stress_score:.2f}. "
    base += f"The Air Quality Index is {aqi:.0f} and waste management index is {waste:.0f}. "
    
    # Add context based on risk level
    if risk_level == "High":
        base += "Immediate intervention is recommended to address elevated pollution and waste levels."
    elif risk_level == "Moderate":
        base += "Monitoring is advised, with consideration for preventive measures to avoid escalation."
    else:  # Low
        base += "Current conditions are within acceptable ranges, but continued monitoring is recommended."
    
    return base

