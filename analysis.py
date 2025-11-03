# analysis.py
import pandas as pd
import matplotlib.pyplot as plt


def perform_analysis():
    print("=== EV CHARGING INFRASTRUCTURE ANALYSIS ===")

    # Load cleaned data
    df = pd.read_csv('cleaned_ev_data.csv')

    # Calculate key metric
    df['stations_per_million'] = (df['station_count'] / df['2022 Population']) * 1000000
    df = df.sort_values('stations_per_million', ascending=False)

    print(f"Analyzed {len(df)} countries")

    # Top 5 leaders
    print("\n TOP 5 COUNTRIES (Best Coverage):")
    top_5 = df.head(5)
    for i, row in top_5.iterrows():
        print(f"  {row['Country/Territory']}: {row['stations_per_million']:.1f} stations/million")

    # Bottom 5 (most needed)
    print("\n TOP 5 COUNTRIES (Most Needed):")
    bottom_5 = df.tail(5)
    for i, row in bottom_5.iterrows():
        print(f"  {row['Country/Territory']}: {row['stations_per_million']:.2f} stations/million")

    # Visualization
    plt.figure(figsize=(10, 6))
    top_10 = df.head(10)
    plt.barh(top_10['Country/Territory'], top_10['stations_per_million'], color='skyblue')
    plt.xlabel('Charging Stations per Million People')
    plt.title('Top 10 Countries by EV Charging Infrastructure')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('charging_infrastructure.png')  # Save for report
    plt.show()

    # Key insights
    print(f"\n KEY INSIGHTS:")
    print(f"• Leader: {df.iloc[0]['Country/Territory']} ({df.iloc[0]['stations_per_million']:.1f}/million)")
    print(f"• Most needed: {df.iloc[-1]['Country/Territory']} ({df.iloc[-1]['stations_per_million']:.2f}/million)")
    print(f"• Global average: {df['stations_per_million'].mean():.2f} stations/million")
    print(f"• Total stations analyzed: {df['station_count'].sum():,}")

    # Save analysis results
    df.to_csv('final_analysis_results.csv', index=False)
    print("Analysis results saved to 'final_analysis_results.csv'")


if __name__ == "__main__":
    perform_analysis()