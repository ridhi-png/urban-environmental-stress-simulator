"""
Stress Engine Module

This module provides core calculation functions for the Urban Environmental Stress Simulator.
It handles data normalization, stress score calculation, and risk classification.
"""

import pandas as pd


def normalize(series: pd.Series) -> pd.Series:
    """
    Apply Min-Max normalization to scale values to the range [0, 1].
    
    Formula: (value - min) / (max - min)
    
    This normalization technique scales all values proportionally to fit within
    the [0, 1] range, preserving the relative distances between values.
    
    Edge Cases:
    - When max == min (all values are identical), returns a series of zeros
      to avoid division by zero. This is appropriate because identical values
      have no variance and should all map to the same normalized value.
    
    Args:
        series (pd.Series): A pandas Series containing numeric values to normalize
        
    Returns:
        pd.Series: A new Series with values normalized to the range [0, 1]
        
    Examples:
        >>> normalize(pd.Series([0, 50, 100]))
        0    0.0
        1    0.5
        2    1.0
        dtype: float64
        
        >>> normalize(pd.Series([5, 5, 5]))  # Edge case: all identical
        0    0.0
        1    0.0
        2    0.0
        dtype: float64
    """
    min_val = series.min()
    max_val = series.max()
    
    # Handle edge case: when all values are identical (max == min)
    if max_val == min_val:
        return pd.Series([0.0] * len(series), index=series.index)
    
    # Apply Min-Max normalization formula
    normalized = (series - min_val) / (max_val - min_val)
    
    return normalized


def calculate_stress_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate composite environmental stress scores for urban zones.
    
    This function computes a weighted stress score based on three environmental
    factors: Air Quality Index (AQI), waste management index, and temperature.
    Each factor is first normalized to [0, 1] range, then combined using weights
    that reflect their relative importance to environmental stress.
    
    Weighting Rationale:
    - AQI (50%): Air quality is the primary stress factor as it directly impacts
      respiratory health and overall quality of life for residents.
    - Waste Index (30%): Waste management is a significant secondary factor
      affecting sanitation, disease vectors, and environmental degradation.
    - Temperature (20%): Temperature contributes to thermal stress but is
      weighted lower as it's often seasonal and more predictable.
    
    Formula:
        stress_score = 0.5 × AQI_normalized + 0.3 × waste_normalized + 0.2 × temp_normalized
    
    Args:
        df (pd.DataFrame): DataFrame containing at minimum the columns:
            - AQI: Air Quality Index values
            - waste_index: Waste management metric values
            - temperature: Temperature values in Celsius
            
    Returns:
        pd.DataFrame: The input dataframe with an added 'stress_score' column
                     containing values in the range [0, 1]. All original columns
                     are preserved unchanged.
                     
    Examples:
        >>> df = pd.DataFrame({
        ...     'zone': ['Zone A', 'Zone B'],
        ...     'AQI': [100, 200],
        ...     'waste_index': [30, 60],
        ...     'temperature': [20, 30]
        ... })
        >>> result = calculate_stress_score(df)
        >>> 'stress_score' in result.columns
        True
        >>> 0 <= result['stress_score'].min() <= result['stress_score'].max() <= 1
        True
    """
    # Create a copy to avoid modifying the original dataframe
    df_copy = df.copy()
    
    # Normalize each environmental factor to [0, 1] range
    aqi_normalized = normalize(df_copy['AQI'])
    waste_normalized = normalize(df_copy['waste_index'])
    temp_normalized = normalize(df_copy['temperature'])
    
    # Apply weighted formula to calculate composite stress score
    # Weights: AQI (50%), waste (30%), temperature (20%)
    df_copy['stress_score'] = (
        0.5 * aqi_normalized +
        0.3 * waste_normalized +
        0.2 * temp_normalized
    )
    
    return df_copy


def classify_risk(score: float) -> str:
    """
    Classify environmental stress risk level based on stress score.
    
    This function categorizes stress scores into three risk levels to help
    policy makers prioritize interventions. The thresholds are designed to
    create a balanced distribution that identifies zones requiring immediate
    attention (High), monitoring (Moderate), or minimal intervention (Low).
    
    Risk Level Thresholds:
    - Low Risk (score < 0.4): Environmental conditions are acceptable with
      minimal stress factors. Routine monitoring is sufficient.
    - Moderate Risk (0.4 ≤ score ≤ 0.7): Environmental stress is noticeable
      and may require targeted interventions. Increased monitoring recommended.
    - High Risk (score > 0.7): Significant environmental stress requiring
      immediate policy intervention and resource allocation.
    
    Args:
        score (float): Stress score value in the range [0, 1]
        
    Returns:
        str: Risk classification as "Low", "Moderate", or "High"
        
    Examples:
        >>> classify_risk(0.2)
        'Low'
        >>> classify_risk(0.4)
        'Moderate'
        >>> classify_risk(0.7)
        'Moderate'
        >>> classify_risk(0.8)
        'High'
    """
    if score < 0.4:
        return "Low"
    elif score <= 0.7:
        return "Moderate"
    else:
        return "High"
