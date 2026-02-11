"""
Simulation Layer Module

This module provides policy intervention simulation functions for the Urban Environmental
Stress Simulator. It models waste reduction and emission control interventions.
"""

import pandas as pd


def simulate_waste_reduction(df: pd.DataFrame, percent: float) -> pd.DataFrame:
    """
    Simulate the impact of a waste reduction policy intervention.
    
    This function models a policy scenario where waste management improvements
    reduce the waste_index across all urban zones by a specified percentage.
    The reduction is applied uniformly to demonstrate the potential impact of
    city-wide waste reduction initiatives (e.g., recycling programs, waste
    processing improvements, or behavioral campaigns).
    
    Policy Simulation Formula:
        new_waste_index = original_waste_index × (1 - percent/100)
    
    For example, a 20% reduction on a waste_index of 50 results in:
        new_waste_index = 50 × (1 - 20/100) = 50 × 0.8 = 40
    
    Args:
        df (pd.DataFrame): DataFrame containing at minimum a 'waste_index' column
                          with waste management metric values
        percent (float): Reduction percentage in the range [0, 100]
                        - 0% means no reduction (no change)
                        - 100% means complete elimination (values become 0)
                        
    Returns:
        pd.DataFrame: A new dataframe with modified waste_index values.
                     All other columns are preserved unchanged.
                     All waste_index values are guaranteed to be non-negative.
                     
    Examples:
        >>> df = pd.DataFrame({
        ...     'zone': ['Zone A', 'Zone B'],
        ...     'waste_index': [50, 80]
        ... })
        >>> result = simulate_waste_reduction(df, 20)
        >>> result['waste_index'].tolist()
        [40.0, 64.0]
        
        >>> result = simulate_waste_reduction(df, 100)  # Complete elimination
        >>> result['waste_index'].tolist()
        [0.0, 0.0]
    """
    # Create a copy to avoid modifying the original dataframe
    df_copy = df.copy()
    
    # Calculate the reduction factor: (1 - percent/100)
    # This converts percentage to a multiplier (e.g., 20% reduction → 0.8 multiplier)
    reduction_factor = 1 - (percent / 100)
    
    # Apply the reduction to waste_index values
    df_copy['waste_index'] = df_copy['waste_index'] * reduction_factor
    
    # Ensure non-negative values (though mathematically guaranteed with valid inputs)
    # This is a safety measure for edge cases or floating-point precision issues
    df_copy['waste_index'] = df_copy['waste_index'].clip(lower=0)
    
    return df_copy


def simulate_emission_control(df: pd.DataFrame, percent: float) -> pd.DataFrame:
    """
    Simulate the impact of an emission control policy intervention.
    
    This function models a policy scenario where emission control measures
    reduce the Air Quality Index (AQI) across all urban zones by a specified
    percentage. The reduction is applied uniformly to demonstrate the potential
    impact of city-wide emission control initiatives (e.g., vehicle restrictions,
    industrial emission standards, clean energy transitions, or public transit
    improvements).
    
    Policy Simulation Formula:
        new_AQI = original_AQI × (1 - percent/100)
    
    For example, a 20% reduction on an AQI of 200 results in:
        new_AQI = 200 × (1 - 20/100) = 200 × 0.8 = 160
    
    Args:
        df (pd.DataFrame): DataFrame containing at minimum an 'AQI' column
                          with Air Quality Index values
        percent (float): Reduction percentage in the range [0, 100]
                        - 0% means no reduction (no change)
                        - 100% means complete elimination (values become 0)
                        
    Returns:
        pd.DataFrame: A new dataframe with modified AQI values.
                     All other columns are preserved unchanged.
                     All AQI values are guaranteed to be non-negative.
                     
    Examples:
        >>> df = pd.DataFrame({
        ...     'zone': ['Zone A', 'Zone B'],
        ...     'AQI': [200, 150]
        ... })
        >>> result = simulate_emission_control(df, 20)
        >>> result['AQI'].tolist()
        [160.0, 120.0]
        
        >>> result = simulate_emission_control(df, 100)  # Complete elimination
        >>> result['AQI'].tolist()
        [0.0, 0.0]
    """
    # Create a copy to avoid modifying the original dataframe
    df_copy = df.copy()
    
    # Calculate the reduction factor: (1 - percent/100)
    # This converts percentage to a multiplier (e.g., 20% reduction → 0.8 multiplier)
    reduction_factor = 1 - (percent / 100)
    
    # Apply the reduction to AQI values
    df_copy['AQI'] = df_copy['AQI'] * reduction_factor
    
    # Ensure non-negative values (though mathematically guaranteed with valid inputs)
    # This is a safety measure for edge cases or floating-point precision issues
    df_copy['AQI'] = df_copy['AQI'].clip(lower=0)
    
    return df_copy


def recalculate_stress(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recalculate stress scores and risk levels for modified environmental data.
    
    This function is used after policy simulations to update stress metrics
    based on the current (possibly modified) values of AQI, waste_index, and
    temperature. It ensures consistency by using the same calculation logic
    as the initial stress score computation.
    
    The function performs two operations:
    1. Recalculates stress_score using the same weighted formula as calculate_stress_score()
    2. Classifies each stress score into a risk_level (Low, Moderate, High)
    
    This is essential for the simulation workflow:
    - User adjusts policy sliders (waste reduction, emission control)
    - Simulation functions modify AQI or waste_index values
    - recalculate_stress() updates stress_score and risk_level to reflect changes
    - Dashboard displays updated metrics and visualizations
    
    Args:
        df (pd.DataFrame): DataFrame containing at minimum the columns:
            - AQI: Air Quality Index values (possibly modified by simulation)
            - waste_index: Waste management metric values (possibly modified)
            - temperature: Temperature values in Celsius
            
    Returns:
        pd.DataFrame: The input dataframe with updated 'stress_score' and
                     'risk_level' columns. All original columns are preserved.
                     
    Examples:
        >>> df = pd.DataFrame({
        ...     'zone': ['Zone A', 'Zone B'],
        ...     'AQI': [100, 200],
        ...     'waste_index': [30, 60],
        ...     'temperature': [20, 30]
        ... })
        >>> result = recalculate_stress(df)
        >>> 'stress_score' in result.columns and 'risk_level' in result.columns
        True
        >>> result['risk_level'].isin(['Low', 'Moderate', 'High']).all()
        True
    """
    # Import stress_engine functions
    from stress_engine import calculate_stress_score, classify_risk
    
    # Recalculate stress scores using current environmental values
    # This uses the same normalization and weighting formula as initial calculation
    df_with_scores = calculate_stress_score(df)
    
    # Apply risk classification to each stress score
    # This categorizes zones into Low, Moderate, or High risk levels
    df_with_scores['risk_level'] = df_with_scores['stress_score'].apply(classify_risk)
    
    return df_with_scores
