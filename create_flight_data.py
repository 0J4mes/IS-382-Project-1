# create_flight_data.py
"""
IS 362 Project 1 - Flight Data CSV Creator
This script creates the flight_data.csv file from the project requirements.
"""

import pandas as pd


def create_flight_csv():
    """Create the CSV file with flight delay data for two airlines"""

    # Create the flight data based on the project PDF
    data = {
        'airline': ['ALASKA', 'ALASKA', 'ALASKA', 'ALASKA', 'ALASKA',
                    'ALASKA', 'ALASKA', 'ALASKA', 'ALASKA', 'ALASKA',
                    'AM WEST', 'AM WEST', 'AM WEST', 'AM WEST', 'AM WEST',
                    'AM WEST', 'AM WEST', 'AM WEST', 'AM WEST', 'AM WEST'],
        'status': ['on time', 'on time', 'on time', 'on time', 'on time',
                   'delayed', 'delayed', 'delayed', 'delayed', 'delayed',
                   'on time', 'on time', 'on time', 'on time', 'on time',
                   'delayed', 'delayed', 'delayed', 'delayed', 'delayed'],
        'city': ['Los Angeles', 'Phoenix', 'San Diego', 'San Francisco', 'Seattle',
                 'Los Angeles', 'Phoenix', 'San Diego', 'San Francisco', 'Seattle',
                 'Los Angeles', 'Phoenix', 'San Diego', 'San Francisco', 'Seattle',
                 'Los Angeles', 'Phoenix', 'San Diego', 'San Francisco', 'Seattle'],
        'flights': [497, 221, 212, 503, 1841,
                    62, 12, 20, 102, 305,
                    694, 4840, 383, 320, 201,
                    117, 415, 65, 129, 61]
    }

    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('flight_data.csv', index=False)
    print("✓ flight_data.csv created successfully!")
    print(f"✓ File contains {len(df)} records")
    print("\nSample of the data:")
    print(df.head(10))

    return df


if __name__ == "__main__":
    create_flight_csv()