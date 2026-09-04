import osmium
import csv

# Approximate Bangalore bounding box
MIN_LAT = 12.80
MAX_LAT = 13.20
MIN_LON = 77.40
MAX_LON = 77.80

INPUT_FILE = "data/southern-zone-260831.osm.pbf"
OUTPUT_FILE = "data/bangalore_osm_points.csv"


class BangalorePointHandler(osmium.SimpleHandler):

    def __init__(self):
        super().__init__()
        self.points = []

    def node(self, n):

        if not n.location.valid():
            return

        lat = n.location.lat
        lon = n.location.lon

        if MIN_LAT <= lat <= MAX_LAT and MIN_LON <= lon <= MAX_LON:

            self.points.append({
                "latitude": lat,
                "longitude": lon,
                "name": n.tags.get("name", ""),
                "amenity": n.tags.get("amenity", ""),
                "shop": n.tags.get("shop", "")
            })


print("========================================")
print("BANGALORE OSM DATA EXTRACTION")
print("========================================")
print("Reading OSM file...")
print("This may take some time...")
print()

handler = BangalorePointHandler()

handler.apply_file(INPUT_FILE, locations=True)

print(f"Total Bangalore OSM points found: {len(handler.points)}")

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "latitude",
            "longitude",
            "name",
            "amenity",
            "shop"
        ]
    )

    writer.writeheader()
    writer.writerows(handler.points)

print()
print(f"Saved to: {OUTPUT_FILE}")
print("Extraction completed successfully!")