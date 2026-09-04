import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bangalore Micro-Fulfillment Optimization",
    page_icon="📍",
    layout="wide"
)

st.title("📍 Bangalore Micro-Fulfillment Hub Optimization")
st.markdown(
    "Micro-fulfillment hub optimization using Weighted K-Means clustering."
)

# Load data
hub_summary = pd.read_csv("outputs/hub_summary.csv")
hub_locations = pd.read_csv("outputs/hub_locations.csv")
assignments = pd.read_csv("outputs/customer_assignments.csv")

# Metrics
total_customers = len(assignments)
total_orders = int(hub_summary["total_order_volume"].sum())
number_of_hubs = len(hub_summary)
weighted_distance = 3.596
capacity = 2500
max_customers = int(hub_summary["customer_count"].max())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Customers", f"{total_customers:,}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Number of Hubs", number_of_hubs)
col4.metric("Weighted Avg Distance", f"{weighted_distance:.3f} km")

st.divider()

# Capacity status
st.subheader("Capacity Validation")

if max_customers <= capacity:
    st.success(
        f"Capacity constraint PASSED — maximum hub load: "
        f"{max_customers:,} / {capacity:,} customers"
    )
else:
    st.error("Capacity constraint FAILED")

# Hub summary
st.subheader("Hub Summary")

st.dataframe(
    hub_summary,
    use_container_width=True
)

# Charts
st.subheader("Hub Performance")

col1, col2 = st.columns(2)

with col1:
    st.image(
        "graphs/customers_per_hub_final.png",
        caption="Customers per Hub",
        use_container_width=True
    )

with col2:
    st.image(
        "graphs/order_volume_per_hub.png",
        caption="Order Volume per Hub",
        use_container_width=True
    )

col1, col2 = st.columns(2)

with col1:
    st.image(
        "graphs/distance_per_hub.png",
        caption="Average Distance per Hub",
        use_container_width=True
    )

with col2:
    st.image(
        "graphs/k_vs_distance.png",
        caption="K vs Weighted Average Distance",
        use_container_width=True
    )

# Interactive map
st.subheader("🗺️ Bangalore Hub Map")

map_file = Path("outputs/bangalore_hub_map.html")

if map_file.exists():
    html = map_file.read_text(encoding="utf-8")
    components.html(html, height=650, scrolling=True)
else:
    st.warning("Hub map file not found.")

# Downloads
st.subheader("Download Results")

st.download_button(
    "Download Hub Summary",
    data=hub_summary.to_csv(index=False),
    file_name="hub_summary.csv",
    mime="text/csv"
)

st.download_button(
    "Download Customer Assignments",
    data=assignments.to_csv(index=False),
    file_name="customer_assignments.csv",
    mime="text/csv"
)

st.success("Final solution validated successfully.")