import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from pyproj import Transformer

# ============================================================
# SETTINGS
# ============================================================

INPUT_FILE = "data/customers.csv"
RESULT_FILE = "outputs/k_comparison.csv"
GRAPH_FILE = "graphs/k_vs_distance.png"

K_VALUES = range(4, 9)

RANDOM_STATE = 42

print("========================================")
print("MICRO-FULFILLMENT HUB OPTIMIZATION")
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
# Bangalore is represented using UTM Zone 43N.
# This allows distance calculations in meters.

transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32643",
    always_xy=True
)

x, y = transformer.transform(
    df["longitude"].values,
    df["latitude"].values
)

coordinates = np.column_stack((x, y))

# ============================================================
# 3. TEST DIFFERENT VALUES OF K
# ============================================================

results = []

for k in K_VALUES:

    print("\n----------------------------------------")
    print(f"Testing K = {k}")
    print("----------------------------------------")

    # Weighted K-Means
    model = KMeans(
        n_clusters=k,
        random_state=RANDOM_STATE,
        n_init=10
    )

    model.fit(
        coordinates,
        sample_weight=df["volume"].values
    )

    labels = model.labels_

    # --------------------------------------------------------
    # Calculate distance from every customer to assigned hub
    # --------------------------------------------------------

    centers = model.cluster_centers_

    assigned_centers = centers[labels]

    distances_m = np.sqrt(
        np.sum(
            (coordinates - assigned_centers) ** 2,
            axis=1
        )
    )

    distances_km = distances_m / 1000

    # --------------------------------------------------------
    # Weighted average distance
    # --------------------------------------------------------

    weighted_average_distance = np.average(
        distances_km,
        weights=df["volume"]
    )

    # --------------------------------------------------------
    # Customer count per hub
    # --------------------------------------------------------

    customer_counts = np.bincount(
        labels,
        minlength=k
    )

    max_customers = customer_counts.max()

    capacity_ok = max_customers <= 2500

    # --------------------------------------------------------
    # Total weighted distance
    # --------------------------------------------------------

    total_weighted_distance = np.sum(
        distances_km * df["volume"].values
    )

    # --------------------------------------------------------
    # Store result
    # --------------------------------------------------------

    results.append({
        "k": k,
        "weighted_average_distance_km":
            weighted_average_distance,
        "total_weighted_distance":
            total_weighted_distance,
        "max_customers_per_hub":
            max_customers,
        "capacity_constraint_satisfied":
            capacity_ok
    })

    print(
        f"Weighted average distance: "
        f"{weighted_average_distance:.3f} km"
    )

    print(
        f"Maximum customers in a hub: "
        f"{max_customers}"
    )

    print(
        f"Capacity constraint satisfied: "
        f"{capacity_ok}"
    )

# ============================================================
# 4. SAVE COMPARISON RESULTS
# ============================================================

results_df = pd.DataFrame(results)

results_df.to_csv(
    RESULT_FILE,
    index=False
)

print("\n========================================")
print("K COMPARISON RESULTS")
print("========================================")

print(
    results_df.to_string(index=False)
)

# ============================================================
# 5. SELECT BEST FEASIBLE K
# ============================================================

feasible = results_df[
    results_df["capacity_constraint_satisfied"] == True
]

if len(feasible) == 0:

    print(
        "\nNo tested K satisfies the 2,500 "
        "customer capacity constraint."
    )

else:

    best_row = feasible.loc[
        feasible["weighted_average_distance_km"].idxmin()
    ]

    best_k = int(best_row["k"])
    best_distance = best_row[
        "weighted_average_distance_km"
    ]

    print("\n========================================")
    print("BEST FEASIBLE SOLUTION")
    print("========================================")

    print(f"Best number of hubs: {best_k}")

    print(
        f"Weighted average distance: "
        f"{best_distance:.3f} km"
    )

    print(
        f"Maximum customers per hub: "
        f"{int(best_row['max_customers_per_hub'])}"
    )

# ============================================================
# 6. CREATE K VS DISTANCE GRAPH
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    results_df["k"],
    results_df["weighted_average_distance_km"],
    marker="o"
)

plt.xlabel("Number of hubs (K)")
plt.ylabel("Weighted average distance (km)")
plt.title(
    "Number of Hubs vs "
    "Order-Volume-Weighted Average Distance"
)

plt.xticks(list(K_VALUES))
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    GRAPH_FILE,
    dpi=300
)

plt.close()

print(
    f"\nGraph saved to: {GRAPH_FILE}"
)

print("\n========================================")
print("OPTIMIZATION COMPLETED")
print("========================================")