import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

from sklearn.cluster import KMeans
from pyproj import Transformer


# ============================================================
# SETTINGS
# ============================================================

INPUT_FILE = "data/customers.csv"

HUB_FILE = "outputs/hub_locations.csv"
ASSIGNMENT_FILE = "outputs/customer_assignments.csv"
SUMMARY_FILE = "outputs/hub_summary.csv"

MAP_FILE = "outputs/bangalore_hub_map.html"
GRAPH_FILE = "graphs/customers_per_hub.png"

K = 8
CAPACITY = 2500
RANDOM_STATE = 42


print("========================================")
print("FINAL 8-HUB SOLUTION")
print("========================================")


# ============================================================
# 1. LOAD CUSTOMER DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print(f"\nCustomers loaded: {len(df):,}")
print(f"Total order volume: {df['volume'].sum():,}")


# ============================================================
# 2. CONVERT LAT/LON TO METERS
# ============================================================

# EPSG:4326 = latitude/longitude
# EPSG:32643 = UTM Zone 43N, suitable for Bangalore

to_utm = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32643",
    always_xy=True
)

to_latlon = Transformer.from_crs(
    "EPSG:32643",
    "EPSG:4326",
    always_xy=True
)


x, y = to_utm.transform(
    df["longitude"].values,
    df["latitude"].values
)

coordinates = np.column_stack((x, y))


# ============================================================
# 3. RUN WEIGHTED K-MEANS
# ============================================================

print(f"\nRunning weighted K-Means with K = {K}...")

model = KMeans(
    n_clusters=K,
    random_state=RANDOM_STATE,
    n_init=10
)

model.fit(
    coordinates,
    sample_weight=df["volume"].values
)


labels = model.labels_

centers = model.cluster_centers_


# ============================================================
# 4. CALCULATE CUSTOMER DISTANCES
# ============================================================

assigned_centers = centers[labels]

distances_m = np.sqrt(
    np.sum(
        (coordinates - assigned_centers) ** 2,
        axis=1
    )
)

distances_km = distances_m / 1000


# ============================================================
# 5. CREATE CUSTOMER ASSIGNMENT DATA
# ============================================================

assignments = df.copy()

assignments["hub_id"] = labels + 1

assignments["distance_km"] = distances_km

assignments["weighted_distance"] = (
    assignments["distance_km"]
    * assignments["volume"]
)


# ============================================================
# 6. CONVERT HUB CENTERS BACK TO LAT/LON
# ============================================================

hub_longitudes = []
hub_latitudes = []

for center_x, center_y in centers:

    lon, lat = to_latlon.transform(
        center_x,
        center_y
    )

    hub_longitudes.append(lon)
    hub_latitudes.append(lat)


# ============================================================
# 7. CREATE HUB SUMMARY
# ============================================================

hub_summary = []

for hub_id in range(1, K + 1):

    hub_customers = assignments[
        assignments["hub_id"] == hub_id
    ]

    customer_count = len(hub_customers)

    total_volume = hub_customers["volume"].sum()

    average_distance = hub_customers[
        "distance_km"
    ].mean()

    weighted_distance = hub_customers[
        "weighted_distance"
    ].sum()

    hub_summary.append({

        "hub_id": hub_id,

        "latitude": hub_latitudes[hub_id - 1],

        "longitude": hub_longitudes[hub_id - 1],

        "customer_count": customer_count,

        "total_order_volume": total_volume,

        "average_distance_km": average_distance,

        "total_weighted_distance": weighted_distance,

        "capacity_limit": CAPACITY,

        "capacity_satisfied": customer_count <= CAPACITY

    })


hub_summary = pd.DataFrame(hub_summary)


# ============================================================
# 8. CALCULATE OVERALL METRICS
# ============================================================

total_weighted_distance = assignments[
    "weighted_distance"
].sum()

total_volume = assignments["volume"].sum()

weighted_average_distance = (
    total_weighted_distance / total_volume
)

maximum_customers = hub_summary[
    "customer_count"
].max()

capacity_satisfied = (
    maximum_customers <= CAPACITY
)


# ============================================================
# 9. SAVE HUB LOCATIONS
# ============================================================

hub_locations = hub_summary[
    [
        "hub_id",
        "latitude",
        "longitude"
    ]
]

hub_locations.to_csv(
    HUB_FILE,
    index=False
)


# ============================================================
# 10. SAVE CUSTOMER ASSIGNMENTS
# ============================================================

assignments.to_csv(
    ASSIGNMENT_FILE,
    index=False
)


# ============================================================
# 11. SAVE HUB SUMMARY
# ============================================================

hub_summary.to_csv(
    SUMMARY_FILE,
    index=False
)


# ============================================================
# 12. PRINT FINAL RESULTS
# ============================================================

print("\n========================================")
print("FINAL HUB RESULTS")
print("========================================")

print(
    f"\nNumber of hubs: {K}"
)

print(
    f"Total customers: {len(assignments):,}"
)

print(
    f"Total order volume: {total_volume:,}"
)

print(
    f"Weighted average distance: "
    f"{weighted_average_distance:.3f} km"
)

print(
    f"Maximum customers in one hub: "
    f"{maximum_customers:,}"
)

print(
    f"Capacity limit: {CAPACITY:,}"
)

print(
    f"Capacity constraint satisfied: "
    f"{capacity_satisfied}"
)


print("\n========================================")
print("HUB SUMMARY")
print("========================================")

print(
    hub_summary[
        [
            "hub_id",
            "latitude",
            "longitude",
            "customer_count",
            "total_order_volume",
            "average_distance_km",
            "capacity_satisfied"
        ]
    ].to_string(index=False)
)


# ============================================================
# 13. CREATE CUSTOMERS PER HUB GRAPH
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    hub_summary["hub_id"].astype(str),
    hub_summary["customer_count"]
)

plt.axhline(
    y=CAPACITY,
    linestyle="--",
    label="Capacity limit"
)

plt.xlabel("Hub ID")
plt.ylabel("Number of customers")

plt.title(
    "Customers Assigned to Each Hub"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    GRAPH_FILE,
    dpi=300
)

plt.close()

print(
    f"\nGraph saved to: {GRAPH_FILE}"
)


# ============================================================
# 14. CREATE INTERACTIVE MAP
# ============================================================

center_lat = df["latitude"].mean()
center_lon = df["longitude"].mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11
)


# ------------------------------------------------------------
# Add customers
# ------------------------------------------------------------

for _, row in assignments.iterrows():

    folium.CircleMarker(
        location=[
            row["latitude"],
            row["longitude"]
        ],
        radius=2,
        popup=(
            f"Customer: {row['customer_id']}<br>"
            f"Hub: {row['hub_id']}<br>"
            f"Volume: {row['volume']}<br>"
            f"Distance: {row['distance_km']:.2f} km"
        ),
        fill=True
    ).add_to(m)


# ------------------------------------------------------------
# Add hubs
# ------------------------------------------------------------

for _, row in hub_summary.iterrows():

    folium.Marker(
        location=[
            row["latitude"],
            row["longitude"]
        ],
        popup=(
            f"<b>Hub {int(row['hub_id'])}</b><br>"
            f"Customers: {int(row['customer_count'])}<br>"
            f"Order volume: {int(row['total_order_volume'])}<br>"
            f"Average distance: "
            f"{row['average_distance_km']:.2f} km"
        ),
        tooltip=f"Hub {int(row['hub_id'])}"
    ).add_to(m)


# ============================================================
# SAVE MAP
# ============================================================

m.save(MAP_FILE)

print(
    f"Map saved to: {MAP_FILE}"
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n========================================")
print("FINAL SOLUTION COMPLETED")
print("========================================")

print("\nFiles created:")

print(f"1. {HUB_FILE}")
print(f"2. {ASSIGNMENT_FILE}")
print(f"3. {SUMMARY_FILE}")
print(f"4. {GRAPH_FILE}")
print(f"5. {MAP_FILE}")

print("\n========================================")