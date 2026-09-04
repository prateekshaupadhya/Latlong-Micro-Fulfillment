import pandas as pd

FILE = "outputs/customer_assignments.csv"

print("========================================")
print("FINAL SOLUTION VALIDATION")
print("========================================")

df = pd.read_csv(FILE)

print(f"\nTotal assignment records: {len(df):,}")

# ------------------------------------------------------------
# Check customer count
# ------------------------------------------------------------

customer_count = df["customer_id"].nunique()

print(f"Unique customers: {customer_count:,}")

if customer_count == 10000:
    print("Customer count test: PASSED")
else:
    print("Customer count test: FAILED")


# ------------------------------------------------------------
# Check duplicate customer IDs
# ------------------------------------------------------------

duplicates = df["customer_id"].duplicated().sum()

print(f"\nDuplicate customer assignments: {duplicates}")

if duplicates == 0:
    print("One-assignment-per-customer test: PASSED")
else:
    print("One-assignment-per-customer test: FAILED")


# ------------------------------------------------------------
# Check missing hub assignments
# ------------------------------------------------------------

missing_hubs = df["hub_id"].isna().sum()

print(f"\nCustomers without hub assignment: {missing_hubs}")

if missing_hubs == 0:
    print("Hub assignment completeness test: PASSED")
else:
    print("Hub assignment completeness test: FAILED")


# ------------------------------------------------------------
# Check hub count
# ------------------------------------------------------------

hub_count = df["hub_id"].nunique()

print(f"\nNumber of hubs: {hub_count}")

if hub_count == 8:
    print("Hub count test: PASSED")
else:
    print("Hub count test: FAILED")


# ------------------------------------------------------------
# Check capacity
# ------------------------------------------------------------

hub_counts = df.groupby("hub_id").size()

max_customers = hub_counts.max()

print(f"\nMaximum customers in one hub: {max_customers}")
print("Capacity limit: 2,500")

if max_customers <= 2500:
    print("Capacity test: PASSED")
else:
    print("Capacity test: FAILED")


# ------------------------------------------------------------
# FINAL RESULT
# ------------------------------------------------------------

all_passed = (
    customer_count == 10000
    and duplicates == 0
    and missing_hubs == 0
    and hub_count == 8
    and max_customers <= 2500
)

print("\n========================================")

if all_passed:
    print("FINAL VALIDATION: PASSED")
else:
    print("FINAL VALIDATION: FAILED")

print("========================================")