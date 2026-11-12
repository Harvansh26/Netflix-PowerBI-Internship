
import pandas as pd
from pathlib import Path

# ==================================================
# 1. PROJECT SETUP AND DATA IMPORT
# ==================================================

# Locate project folder
project_folder = Path(__file__).resolve().parent

# Define input file path
file_path = project_folder / "data" / "Dataset.csv"

# Load dataset
df = pd.read_csv(file_path)

print("\n========== NETFLIX DATA CLEANING PROJECT ==========")

print("\nDataset loaded successfully!")

# Store original dataset information
original_rows = len(df)
original_columns = len(df.columns)


# ==================================================
# 2. INITIAL DATA INSPECTION
# ==================================================

print("\n========== INITIAL DATA INSPECTION ==========")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst Five Records:")
print(df.head())

print("\nColumn Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe(include="all"))


# ==================================================
# 3. STANDARDIZE COLUMN NAMES
# ==================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
)

print("\nStandardized Column Names:")
print(df.columns.tolist())


# ==================================================
# 4. REMOVE UNWANTED SPACES FROM TEXT
# ==================================================

text_columns = df.select_dtypes(include="object").columns

for col in text_columns:
    df[col] = df[col].str.strip()

print("\nText spaces cleaned successfully!")


# ==================================================
# 5. CHECK AND HANDLE MISSING VALUES
# ==================================================

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

total_missing = df.isnull().sum().sum()

if total_missing > 0:

    print("\nMissing values detected.")
    print("Investigate column-specific handling before removal.")

else:

    print("\nNo missing values found.")


# ==================================================
# 6. REMOVE DUPLICATE RECORDS
# ==================================================

duplicates = df.duplicated().sum()

print("\nDuplicate Records Found:", duplicates)

df = df.drop_duplicates()

print("Remaining Records:", len(df))


# ==================================================
# 7. CHECK DUPLICATE SHOW IDs
# ==================================================

duplicate_ids = df["show_id"].duplicated().sum()

print("\nDuplicate Show IDs:", duplicate_ids)

if duplicate_ids > 0:
    print("Warning: Duplicate Netflix IDs detected.")
else:
    print("All Netflix IDs are unique.")


# ==================================================
# 8. CONVERT DATE COLUMN
# ==================================================

df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

invalid_dates = df["date_added"].isna().sum()

print("\nDate Conversion Completed!")

print("Invalid or Missing Dates:", invalid_dates)


# ==================================================
# 9. FEATURE ENGINEERING - DATE FEATURES
# ==================================================

df["year_added"] = df["date_added"].dt.year

df["month_added"] = df["date_added"].dt.month

df["month_name"] = df["date_added"].dt.month_name()

print("\nDate Features Created Successfully!")


# ==================================================
# 10. FEATURE ENGINEERING - PRIMARY GENRE
# ==================================================

df["primary_genre"] = (
    df["listed_in"]
    .str.split(",")
    .str[0]
    .str.strip()
)

print("\nPrimary Genre Created Successfully!")


# ==================================================
# 11. FEATURE ENGINEERING - DURATION
# ==================================================

df["duration_value"] = pd.to_numeric(
    df["duration"].str.extract(r"(\d+)")[0],
    errors="coerce"
)

df["duration_unit"] = (
    df["duration"].str.extract(r"([A-Za-z]+)")[0]
)

print("\nDuration Features Created Successfully!")


# ==================================================
# 12. FINAL DATA VALIDATION
# ==================================================

print("\n========== FINAL DATA VALIDATION ==========")

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFinal Column Names:")
print(df.columns.tolist())

print("\nRemaining Missing Values:")
print(df.isnull().sum())

print("\nRemaining Duplicate Rows:")
print(df.duplicated().sum())

print("\nFinal Dataset Preview:")
print(df.head())


# ==================================================
# 13. GENERATE DATA QUALITY REPORT
# ==================================================

quality_report = pd.DataFrame({
    "Metric": [
        "Original Rows",
        "Original Columns",
        "Final Rows",
        "Final Columns",
        "Duplicate Rows Removed",
        "Duplicate Show IDs",
        "Missing Values After Cleaning",
        "Invalid or Missing Dates"
    ],

    "Value": [
        original_rows,
        original_columns,
        len(df),
        len(df.columns),
        duplicates,
        duplicate_ids,
        df.isnull().sum().sum(),
        invalid_dates
    ]
})

report_path = project_folder / "reports" / "data_quality_report.csv"

report_path.parent.mkdir(parents=True, exist_ok=True)

quality_report.to_csv(report_path, index=False)


# ==================================================
# 14. EXPORT FINAL CLEANED DATASET
# ==================================================

output_path = project_folder / "data" / "netflix_cleaned.csv"

df.to_csv(output_path, index=False)

print("\n========== EXPORT SUCCESSFUL ==========")

print("Cleaned Dataset:", output_path)

print("Quality Report:", report_path)

print("\nFinal Records:", len(df))

print("Final Columns:", len(df.columns))

print("\nNETFLIX DATA CLEANING COMPLETED!")
