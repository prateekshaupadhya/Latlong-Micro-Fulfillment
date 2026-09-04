import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# FILES
# ============================================================

SUMMARY_FILE = "outputs/hub_summary.csv"

CUSTOMER_GRAPH = "graphs/customers_per_hub_final.png"
VOLUME_GRAPH = "graphs/order_volume_per_hub.png"
DISTANCE_GRAPH = "graphs/distance_per_hub.png"


print("========================================")
print("FINAL SOLUTION ANALYSIS")
print("========================================")

# Load hub summary
df = pd.read_csv(SUMMARY_FILE)

print("\nHub summary:")
print(df.to_string(index=False))


# ============================================================
# 1. CUSTOMERS PER HUB
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    df["hub_id"].astype(str),
    df["customer_count"]
)

plt.axhline(
    y=2500,
    linestyle="--",
    label="Capacity limit (2,500)"
)

plt.xlabel("Hub ID")
plt.ylabel("Number of customers")

plt.title("Customer Distribution Across 8 Hubs")

plt.legend()

plt.tight_layout()

plt.savefig(
    CUSTOMER_GRAPH,
    dpi=300
)

plt.close()

print(f"\nSaved: {CUSTOMER_GRAPH}")


# ============================================================
# 2. ORDER VOLUME PER HUB
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    df["hub_id"].astype(str),
    df["total_order_volume"]
)

plt.xlabel("Hub ID")
plt.ylabel("Total order volume")

plt.title("Order Volume Served by Each Hub")

plt.tight_layout()

plt.savefig(
    VOLUME_GRAPH,
    dpi=300
)

plt.close()

print(f"Saved: {VOLUME_GRAPH}")


# ============================================================
# 3. AVERAGE DISTANCE PER HUB
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    df["hub_id"].astype(str),
    df["average_distance_km"]
)

plt.xlabel("Hub ID")
plt.ylabel("Average distance (km)")

plt.title("Average Customer-to-Hub Distance")

plt.tight_layout()

plt.savefig(
    DISTANCE_GRAPH,
    dpi=300
)

plt.close()

print(f"Saved: {DISTANCE_GRAPH}")


# ============================================================
# FINAL METRICS
# ============================================================

total_customers = df["customer_count"].sum()
total_volume = df["total_order_volume"].sum()

max_customers = df["customer_count"].max()

print("\n========================================")
print("FINAL METRICS")
print("========================================")

print(f"Total customers       : {total_customers:,}")
print(f"Total order volume    : {total_volume:,}")
print(f"Maximum customers/hub: {max_customers:,}")
print("Capacity limit        : 2,500")

if max_customers <= 2500:
    print("Capacity constraint   : PASSED")
else:
    print("Capacity constraint   : FAILED")

print("\n========================================")
print("FINAL ANALYSIS COMPLETED")
print("========================================")