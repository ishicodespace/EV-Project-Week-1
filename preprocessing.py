# data_cleaning.py
import pandas as pd
import pycountry


def clean_and_merge_data():
    print("=== DATA CLEANING PROCESS ===")

    # Load datasets
    charging_df = pd.read_csv('global_ev_charging_stations.csv')
    population_df = pd.read_csv('world_population.csv')

    print(f"Original charging data shape: {charging_df.shape}")
    print(f"Original population data shape: {population_df.shape}")

    # Clean charging data
    charging_clean = charging_df.copy()
    charging_clean = charging_clean.dropna(subset=['country'])

    # Convert country codes to names
    def get_country_name(code):
        try:
            return pycountry.countries.get(alpha_2=code).name
        except:
            return None

    charging_clean['country_name'] = charging_clean['country'].apply(get_country_name)
    charging_clean = charging_clean[charging_clean['country_name'].notna()]

    # Clean population data
    population_clean = population_df[['Country/Territory', '2022 Population']].copy()
    population_clean = population_clean.dropna(subset=['2022 Population'])

    # Merge datasets
    stations_per_country = charging_clean['country_name'].value_counts().reset_index()
    stations_per_country.columns = ['Country/Territory', 'station_count']

    merged_df = stations_per_country.merge(population_clean, on='Country/Territory', how='inner')

    print(f"Successfully merged {len(merged_df)} countries")
    print(f"Final merged data shape: {merged_df.shape}")

    # Save cleaned data
    merged_df.to_csv('cleaned_ev_data.csv', index=False)
    print("Cleaned data saved to 'cleaned_ev_data.csv'")

    return merged_df


if __name__ == "__main__":
    clean_and_merge_data()