import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# SETTINGS
# ============================================================

INPUT_FILE = "data/customers.csv"
GRAPH_FILE = "graphs/customer_distribution.png"

print("========================================")
print("CUSTOMER DATA VALIDATION")
print("========================================")

# Load customer data
df = pd.read_csv(INPUT_FILE)

# ============================================================
# BASIC INFORMATION
# ============================================================

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 customers:")
print(df.head())

# ============================================================
# VALIDATION
# ============================================================

print("\n========================================")
print("VALIDATION RESULTS")
print("========================================")

# Customer count
print(f"\nNumber of customers: {len(df):,}")

if len(df) >= 10000:
    print("Customer count test: PASSED")
else:
    print("Customer count test: FAILED")

# Missing values
missing = df.isnull().sum()

print("\nMissing values:")
print(missing)

if missing.sum() == 0:
    print("Missing value test: PASSED")
else:
    print("Missing value test: FAILED")

# Duplicate customer IDs
duplicate_ids = df["customer_id"].duplicated().sum()

print(f"\nDuplicate customer IDs: {duplicate_ids}")

if duplicate_ids == 0:
    print("Duplicate ID test: PASSED")
else:
    print("Duplicate ID test: FAILED")

# Latitude validation
valid_lat = df["latitude"].between(12.80, 13.20).all()

print(f"\nLatitude range valid: {valid_lat}")

# Longitude validation
valid_lon = df["longitude"].between(77.40, 77.80).all()

print(f"Longitude range valid: {valid_lon}")

# Volume validation
valid_volume = (df["volume"] > 0).all()

print(f"\nAll order volumes positive: {valid_volume}")

# ============================================================
# SUMMARY STATISTICS
# ============================================================

print("\n========================================")
print("ORDER VOLUME STATISTICS")
print("========================================")

print(f"Total order volume : {df['volume'].sum():,}")
print(f"Average volume     : {df['volume'].mean():.2f}")
print(f"Minimum volume     : {df['volume'].min()}")
print(f"Maximum volume     : {df['volume'].max()}")

# ============================================================
# CREATE CUSTOMER DISTRIBUTION GRAPH
# ============================================================

print("\nCreating customer distribution graph...")

plt.figure(figsize=(10, 8))

plt.scatter(
    df["longitude"],
    df["latitude"],
    s=3,
    alpha=0.5
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Bangalore Customer Distribution")

plt.grid(True, alpha=0.2)

plt.tight_layout()

plt.savefig(
    GRAPH_FILE,
    dpi=300
)

plt.show()

print(f"\nGraph saved to: {GRAPH_FILE}")

print("\n========================================")
print("VALIDATION COMPLETED")
print("========================================")