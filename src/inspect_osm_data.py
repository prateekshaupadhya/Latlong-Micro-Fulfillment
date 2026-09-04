import pandas as pd

FILE = "data/bangalore_osm_points.csv"

print("========================================")
print("OSM DATA INSPECTION")
print("========================================")

# Read the CSV
df = pd.read_csv(FILE)

print("\nTotal rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 10 rows:")
print(df.head(10))

print("\nMissing values:")
print(df.isnull().sum())

print("\nNamed places:")
print((df["name"].notna() & (df["name"] != "")).sum())

print("\nAmenities:")
print((df["amenity"].notna() & (df["amenity"] != "")).sum())

print("\nShops:")
print((df["shop"].notna() & (df["shop"] != "")).sum())

print("\nTop amenities:")
print(df["amenity"].value_counts().head(15))

print("\nTop shops:")
print(df["shop"].value_counts().head(15))