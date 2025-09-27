# flight_analysis.py
"""
IS 362 Project 1 - Airline Delay Analysis
This script performs comprehensive analysis comparing arrival delays for ALASKA vs AM WEST airlines.
"""

import pandas as pd
import numpy as np


class FlightAnalyzer:
    """Class to analyze flight delay data"""

    def __init__(self, csv_file='flight_data.csv'):
        self.csv_file = csv_file
        self.df = None
        self.load_data()

    def load_data(self):
        """Load data from CSV file"""
        try:
            self.df = pd.read_csv(self.csv_file)
            print(f"✓ Successfully loaded data from {self.csv_file}")
            print(f"✓ Data shape: {self.df.shape}")
        except FileNotFoundError:
            print(f"❌ Error: {self.csv_file} not found. Please run create_flight_data.py first.")
            return False
        return True

    def basic_info(self):
        """Display basic information about the dataset"""
        print("\n" + "=" * 60)
        print("DATASET OVERVIEW")
        print("=" * 60)

        print(f"\nAirlines: {', '.join(self.df['airline'].unique())}")
        print(f"Cities: {', '.join(self.df['city'].unique())}")
        print(f"Status types: {', '.join(self.df['status'].unique())}")

        print("\nFirst 10 rows of data:")
        print(self.df.head(10))

        print("\nDataset summary:")
        print(self.df.describe())

    def create_pivot_view(self):
        """Create a pivot table similar to the original PDF format"""
        print("\n" + "=" * 60)
        print("PIVOT TABLE VIEW (Matching PDF Format)")
        print("=" * 60)

        pivot_df = self.df.pivot_table(
            index=['airline', 'status'],
            columns='city',
            values='flights',
            aggfunc='sum',
            fill_value=0
        )

        # Reorder columns to match PDF
        city_order = ['Los Angeles', 'Phoenix', 'San Diego', 'San Francisco', 'Seattle']
        pivot_df = pivot_df[city_order]

        print(pivot_df)
        return pivot_df

    def calculate_airline_performance(self):
        """Calculate overall performance metrics for each airline"""
        print("\n" + "=" * 60)
        print("OVERALL AIRLINE PERFORMANCE")
        print("=" * 60)

        # Calculate totals and percentages
        performance = self.df.pivot_table(
            index='airline',
            columns='status',
            values='flights',
            aggfunc='sum'
        )

        performance['total_flights'] = performance.sum(axis=1)
        performance['on_time_percentage'] = (performance['on time'] / performance['total_flights'] * 100).round(2)
        performance['delayed_percentage'] = (performance['delayed'] / performance['total_flights'] * 100).round(2)

        print(performance)
        return performance

    def analyze_city_performance(self):
        """Analyze performance by city for each airline"""
        print("\n" + "=" * 60)
        print("PERFORMANCE ANALYSIS BY CITY")
        print("=" * 60)

        results = {}

        for airline in self.df['airline'].unique():
            print(f"\n{airline} AIRLINES:")
            print("-" * 40)

            airline_data = self.df[self.df['airline'] == airline]
            city_stats = []

            for city in self.df['city'].unique():
                city_data = airline_data[airline_data['city'] == city]
                total = city_data['flights'].sum()
                delayed = city_data[city_data['status'] == 'delayed']['flights'].sum()
                on_time = city_data[city_data['status'] == 'on time']['flights'].sum()
                delay_rate = (delayed / total * 100).round(2) if total > 0 else 0

                city_stats.append({
                    'city': city,
                    'total_flights': total,
                    'on_time': on_time,
                    'delayed': delayed,
                    'delay_rate': delay_rate,
                    'on_time_rate': (100 - delay_rate).round(2)
                })

                print(f"  {city}: {on_time}/{total} on-time ({100 - delay_rate}%)")

            results[airline] = pd.DataFrame(city_stats)

        return results

    def comparative_analysis(self):
        """Perform comparative analysis between the two airlines"""
        print("\n" + "=" * 60)
        print("COMPARATIVE ANALYSIS")
        print("=" * 60)

        performance = self.calculate_airline_performance()
        city_results = self.analyze_city_performance()

        alaska_on_time = performance.loc['ALASKA', 'on_time_percentage']
        amwest_on_time = performance.loc['AM WEST', 'on_time_percentage']

        print(f"\nON-TIME PERFORMANCE COMPARISON:")
        print(f"ALASKA Airlines: {alaska_on_time}%")
        print(f"AM WEST Airlines: {amwest_on_time}%")

        if alaska_on_time > amwest_on_time:
            winner = "ALASKA"
            difference = alaska_on_time - amwest_on_time
        else:
            winner = "AM WEST"
            difference = amwest_on_time - alaska_on_time

        print(f"\nCONCLUSION: {winner} has better overall on-time performance.")
        print(f"Difference: {difference:.2f} percentage points")

        # Additional insights
        print("\nADDITIONAL INSIGHTS:")
        print("-" * 40)

        # Best and worst cities for each airline
        for airline in ['ALASKA', 'AM WEST']:
            df_city = city_results[airline]
            best_city = df_city.loc[df_city['on_time_rate'].idxmax()]
            worst_city = df_city.loc[df_city['on_time_rate'].idxmin()]

            print(f"\n{airline}:")
            print(f"  Best performance: {best_city['city']} ({best_city['on_time_rate']}% on-time)")
            print(f"  Worst performance: {worst_city['city']} ({worst_city['on_time_rate']}% on-time)")

        return winner, difference

    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print("\n" + "=" * 60)
        print("SUMMARY REPORT")
        print("=" * 60)

        performance = self.calculate_airline_performance()
        winner, difference = self.comparative_analysis()

        summary_text = f"""
IS 362 PROJECT 1 - AIRLINE DELAY ANALYSIS SUMMARY
=================================================

OVERALL PERFORMANCE:
-------------------
- ALASKA Airlines: {performance.loc['ALASKA', 'on_time_percentage']}% on-time
- AM WEST Airlines: {performance.loc['AM WEST', 'on_time_percentage']}% on-time

CONCLUSION:
----------
{winner} has better overall on-time performance by {difference:.2f} percentage points.

DETAILED STATISTICS:
-------------------
Total flights analyzed: {performance['total_flights'].sum():,}

ALASKA Airlines:
- On-time flights: {performance.loc['ALASKA', 'on time']:,}
- Delayed flights: {performance.loc['ALASKA', 'delayed']:,}
- Total flights: {performance.loc['ALASKA', 'total_flights']:,}

AM WEST Airlines:
- On-time flights: {performance.loc['AM WEST', 'on time']:,}
- Delayed flights: {performance.loc['AM WEST', 'delayed']:,}
- Total flights: {performance.loc['AM WEST', 'total_flights']:,}
"""
        print(summary_text)

        # Save summary to file
        with open('analysis_summary.txt', 'w') as f:
            f.write(summary_text)
        print("✓ Summary report saved to 'analysis_summary.txt'")

        return summary_text


def main():
    """Main function to run the complete analysis"""
    print("IS 362 PROJECT 1 - AIRLINE DELAY ANALYSIS")
    print("=" * 60)

    # Initialize analyzer
    analyzer = FlightAnalyzer()

    if not analyzer.df.empty:
        # Run all analyses
        analyzer.basic_info()
        analyzer.create_pivot_view()
        analyzer.calculate_airline_performance()
        analyzer.analyze_city_performance()
        analyzer.comparative_analysis()
        analyzer.generate_summary_report()

        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE!")
        print("=" * 60)
        print("\nGenerated files:")
        print("✓ flight_data.csv - Raw flight data")
        print("✓ analysis_summary.txt - Comprehensive analysis summary")
        print("\nThank you for using the Flight Delay Analyzer!")


if __name__ == "__main__":
    main()