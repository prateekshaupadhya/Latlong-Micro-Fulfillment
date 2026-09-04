import pandas as pd
import numpy as np

# ============================================================
# SETTINGS
# ============================================================

INPUT_FILE = "data/bangalore_osm_points.csv"
OUTPUT_FILE = "data/customers.csv"

NUMBER_OF_CUSTOMERS = 10000

# Fixed seed makes our results reproducible
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)

print("========================================")
print("CREATING CUSTOMER DATASET")
print("========================================")

# ============================================================
# 1. LOAD OSM DATA
# ============================================================

print("\nLoading OSM data...")

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

print(f"Total OSM points: {len(df):,}")

# ============================================================
# 2. SELECT MEANINGFUL OSM LOCATIONS
# ============================================================

print("\nSelecting meaningful geographic locations...")

# Keep locations that have at least one useful OSM attribute
candidates = df[
    (df["name"].notna() & (df["name"].astype(str).str.strip() != ""))
    |
    (df["amenity"].notna() & (df["amenity"].astype(str).str.strip() != ""))
    |
    (df["shop"].notna() & (df["shop"].astype(str).str.strip() != ""))
].copy()

# Remove duplicate coordinates
candidates = candidates.drop_duplicates(
    subset=["latitude", "longitude"]
)

print(f"Meaningful OSM locations: {len(candidates):,}")

# ============================================================
# 3. CHECK WHETHER WE HAVE ENOUGH LOCATIONS
# ============================================================

if len(candidates) < NUMBER_OF_CUSTOMERS:
    raise ValueError(
        f"Only {len(candidates)} meaningful locations found. "
        f"We need at least {NUMBER_OF_CUSTOMERS}."
    )

# ============================================================
# 4. SAMPLE 10,000 CUSTOMER LOCATIONS
# ============================================================

print(f"\nSelecting {NUMBER_OF_CUSTOMERS:,} customer locations...")

customers = candidates.sample(
    n=NUMBER_OF_CUSTOMERS,
    random_state=RANDOM_SEED
).copy()

customers = customers.reset_index(drop=True)

# ============================================================
# 5. CREATE CUSTOMER IDs
# ============================================================

customers["customer_id"] = [
    f"C{i:05d}"
    for i in range(1, len(customers) + 1)
]

# ============================================================
# 6. GENERATE ORDER VOLUME
# ============================================================

# Synthetic order volume.
# Most customers have relatively small volume,
# while some customers have higher order volume.

customers["volume"] = np.random.lognormal(
    mean=1.2,
    sigma=0.7,
    size=len(customers)
)

# Convert to positive integer order volume
customers["volume"] = (
    customers["volume"]
    .round()
    .astype(int)
    .clip(lower=1, upper=50)
)

# ============================================================
# 7. KEEP ONLY REQUIRED COLUMNS
# ============================================================

customers = customers[
    [
        "customer_id",
        "latitude",
        "longitude",
        "volume"
    ]
]

# ============================================================
# 8. SAVE DATASET
# ============================================================

customers.to_csv(
    OUTPUT_FILE,
    index=False
)

# ============================================================
# 9. DISPLAY SUMMARY
# ============================================================

print("\n========================================")
print("CUSTOMER DATASET CREATED")
print("========================================")

print(f"Number of customers : {len(customers):,}")
print(f"Total order volume  : {customers['volume'].sum():,}")
print(f"Minimum volume      : {customers['volume'].min()}")
print(f"Maximum volume      : {customers['volume'].max()}")
print(f"Average volume      : {customers['volume'].mean():.2f}")

print("\nFirst 10 customers:")
print(customers.head(10))

print("\nSaved to:")
print(OUTPUT_FILE)

print("\nDataset creation completed successfully!")