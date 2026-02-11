"""
Data Generation Script

Generates synthetic environmental data for 10 urban zones.
Creates a CSV file with realistic varied environmental metrics.
"""

import random
import csv
import os


def generate_city_environment_data():
    """
    Generate synthetic environmental data for 10 urban zones.
    
    This function creates realistic synthetic data for testing and demonstrating
    the Urban Environmental Stress Simulator. The data represents environmental
    conditions across 10 urban zones with varied pollution, waste, temperature,
    and humidity levels.
    
    Data Generation Strategy:
    - Uses Python's random module to generate varied values within realistic ranges
    - Each zone gets independent random values to simulate diverse urban conditions
    - Ranges are chosen to represent typical urban environmental conditions:
      * AQI (50-300): Covers "Moderate" to "Hazardous" air quality levels
      * Waste Index (20-90): Represents varying waste management effectiveness
      * Temperature (15-40°C): Covers temperate to hot urban climates
      * Humidity (30-90%): Represents dry to humid conditions
    
    Creates data/city_environment.csv with the following columns:
    - zone: Zone identifier (Zone A through Zone J)
    - AQI: Air Quality Index (50-300)
    - waste_index: Waste management metric (20-90)
    - temperature: Temperature in Celsius (15-40)
    - humidity: Relative humidity percentage (30-90)
    
    Returns:
        str: Path to the generated CSV file
    
    Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7
    """
    # Define zone labels using ASCII character codes
    # chr(65) = 'A', chr(66) = 'B', etc.
    # This generates: ["Zone A", "Zone B", ..., "Zone J"]
    zones = [f"Zone {chr(65 + i)}" for i in range(10)]  # Zone A through Zone J
    
    # Generate random environmental data for each zone
    data = []
    for zone in zones:
        # Create a dictionary for each zone with randomized environmental metrics
        row = {
            'zone': zone,
            # AQI range (50-300): Represents air pollution levels
            # Lower values = better air quality, higher values = worse air quality
            'AQI': random.randint(50, 300),
            
            # Waste index range (20-90): Represents waste management effectiveness
            # Lower values = better waste management, higher values = more waste issues
            'waste_index': random.randint(20, 90),
            
            # Temperature range (15-40°C): Represents ambient temperature
            # Rounded to 1 decimal place for realistic precision
            'temperature': round(random.uniform(15, 40), 1),
            
            # Humidity range (30-90%): Represents relative humidity
            # Integer values are sufficient for humidity measurements
            'humidity': random.randint(30, 90)
        }
        data.append(row)
    
    # Ensure the data directory exists before writing the file
    # exist_ok=True prevents errors if the directory already exists
    os.makedirs('data', exist_ok=True)
    
    # Write the generated data to a CSV file
    csv_path = 'data/city_environment.csv'
    with open(csv_path, 'w', newline='') as csvfile:
        # Define the column order for the CSV file
        fieldnames = ['zone', 'AQI', 'waste_index', 'temperature', 'humidity']
        
        # Create a CSV DictWriter to write dictionaries as CSV rows
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row with column names
        writer.writeheader()
        
        # Write all data rows
        writer.writerows(data)
    
    # Print confirmation messages
    print(f"✓ Generated environmental data for {len(data)} zones")
    print(f"✓ Saved to {csv_path}")
    return csv_path


if __name__ == "__main__":
    generate_city_environment_data()
