# Bangalore Micro-Fulfillment Hub Optimization

## 1. Project Overview

This project solves a micro-fulfillment hub placement problem for Bangalore.

The objective is to determine suitable hub locations that minimize
order-volume-weighted customer-to-hub distance while respecting the
approximate capacity constraint of 2,500 customers per hub.

OpenStreetMap (OSM) geographic data is used as the geographic basis
for constructing the customer-location dataset.

---

## 2. Dataset

The provided Southern Zone OpenStreetMap data was processed to extract
locations within the Bangalore study area.

The extracted OSM data contained:

- 4,888,752 OSM points
- 46,122 meaningful locations

Meaningful locations were identified using OSM name, amenity, and shop
information.

A reproducible sample of 10,000 locations was selected for the
customer dataset.

The final customer dataset contains:

- Customer ID
- Latitude
- Longitude
- Order volume

The order-volume values are synthetic because OSM does not provide
private customer order information.

---

## 3. Customer Dataset

File:

`data/customers.csv`

Columns:

- `customer_id`
- `latitude`
- `longitude`
- `volume`

Statistics:

- Customers: 10,000
- Total order volume: 42,511
- Average order volume: 4.25
- Minimum volume: 1
- Maximum volume: 50

---

## 4. Methodology

### Step 1: OSM Data Extraction

PyOsmium was used to process the OSM PBF file.

A Bangalore geographic bounding box was used to identify relevant
locations.

### Step 2: Customer Dataset Creation

Meaningful OSM locations containing a name, amenity, or shop attribute
were selected.

10,000 locations were sampled using a fixed random seed of 42.

Synthetic order volumes were generated for the selected locations.

### Step 3: Coordinate Transformation

Latitude and longitude coordinates were transformed from EPSG:4326
to UTM Zone 43N (EPSG:32643).

This allows distances to be calculated in meters.

### Step 4: Hub Optimization

Weighted K-Means clustering was used for hub placement.

Order volume was used as the sample weight so higher-volume customers
have greater influence on hub locations.

K values from 4 to 8 were tested.

### Step 5: Capacity Validation

Each solution was checked against the approximate capacity of
2,500 customers per hub.

---

## 5. K Comparison

| Hubs | Weighted Average Distance | Maximum Customers/Hub | Capacity |
|---:|---:|---:|---|
| 4 | 4.935 km | 3,683 | Failed |
| 5 | 4.330 km | 2,636 | Failed |
| 6 | 4.010 km | 2,667 | Failed |
| 7 | 3.762 km | 2,384 | Passed |
| 8 | 3.596 km | 2,340 | Passed |

Among the tested feasible solutions, 8 hubs produced the lowest
order-volume-weighted average distance.

---

## 6. Final Solution

**Number of hubs:** 8

**Total customers:** 10,000

**Total order volume:** 42,511

**Weighted average distance:** 3.596 km

**Maximum customers per hub:** 2,340

**Capacity limit:** 2,500 customers

**Capacity constraint:** PASSED

---

## 7. Hub Summary

| Hub | Customers | Order Volume | Average Distance |
|---:|---:|---:|---:|
| 1 | 2,340 | 10,011 | 3.00 km |
| 2 | 1,023 | 4,199 | 4.56 km |
| 3 | 483 | 2,112 | 5.09 km |
| 4 | 910 | 3,762 | 4.15 km |
| 5 | 1,981 | 8,756 | 3.20 km |
| 6 | 135 | 566 | 6.13 km |
| 7 | 1,234 | 5,118 | 3.71 km |
| 8 | 1,894 | 7,987 | 3.33 km |

---

## 8. Project Outputs

### Data

- `data/customers.csv`
- `data/bangalore_osm_points.csv`

### Hub Results

- `outputs/hub_locations.csv`
- `outputs/customer_assignments.csv`
- `outputs/hub_summary.csv`
- `outputs/k_comparison.csv`

### Visualizations

- `graphs/customer_distribution.png`
- `graphs/k_vs_distance.png`
- `graphs/customers_per_hub.png`
- `graphs/customers_per_hub_final.png`
- `graphs/order_volume_per_hub.png`
- `graphs/distance_per_hub.png`

### Interactive Map

- `outputs/bangalore_hub_map.html`

---

## 9. How to Run

Create the virtual environment:

```bash
python -m venv venv