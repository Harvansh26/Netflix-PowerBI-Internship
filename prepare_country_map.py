
import pandas as pd
from pathlib import Path

# Locate project folder
project_folder = Path(__file__).resolve().parent

# Load cleaned Netflix dataset
df = pd.read_csv(
    project_folder / "data" / "netflix_cleaned.csv"
)

# Keep only required columns
country_df = df[["show_id", "country"]].copy()

# Remove missing countries
country_df = country_df.dropna(subset=["country"])

# Split multiple countries into separate rows
country_df["country"] = country_df["country"].str.split(",")

country_df = country_df.explode("country")

# Remove unwanted spaces
country_df["country"] = country_df["country"].str.strip()

# Remove blank country values
country_df = country_df[
    country_df["country"] != ""
]

# Remove duplicate title-country combinations
country_df = country_df.drop_duplicates(
    subset=["show_id", "country"]
)

# Export country dataset
output_path = (
    project_folder / "data" / "netflix_country_map.csv"
)

country_df.to_csv(output_path, index=False)

print("Country dataset created successfully!")
print("Total country records:", len(country_df))
print("Unique countries:", country_df["country"].nunique())
print("Saved at:", output_path)
