import os
import numpy as np
import matplotlib.pyplot as plt
import gmsh

from scipy.spatial import Voronoi
from shapely.geometry import Polygon, box


# ==========================================================
# 1. PROJECT SETTINGS
# ==========================================================

L = 10.0                 # Specimen length in mm
H = 5.0                  # Specimen height in mm
N_GRAINS = 50            # Approximate number of grains
RANDOM_SEED = 42         # Makes the geometry reproducible

OUTPUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "geometry")
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

IMAGE_FILE = os.path.join(
    OUTPUT_DIR, "polycrystalline_microstructure.png"
)

STEP_FILE = os.path.join(
    OUTPUT_DIR, "polycrystalline_microstructure.step"
)


# ==========================================================
# 2. GENERATE RANDOM GRAIN CENTRES
# ==========================================================

rng = np.random.default_rng(RANDOM_SEED)

# Points inside the specimen
points_inside = np.column_stack((
    rng.uniform(0, L, N_GRAINS),
    rng.uniform(0, H, N_GRAINS)
))

# Extra points outside the specimen help define boundary grains
margin = max(L, H)

outside_points = np.array([
    [-margin, -margin],
    [L / 2, -margin],
    [L + margin, -margin],
    [-margin, H / 2],
    [L + margin, H / 2],
    [-margin, H + margin],
    [L / 2, H + margin],
    [L + margin, H + margin],
])

all_points = np.vstack((points_inside, outside_points))


# ==========================================================
# 3. GENERATE THE VORONOI TESSELLATION
# ==========================================================

vor = Voronoi(all_points)

specimen = box(0, 0, L, H)

grain_polygons = []

for point_index in range(N_GRAINS):

    region_index = vor.point_region[point_index]
    region = vor.regions[region_index]

    # Skip unbounded regions
    if not region or -1 in region:
        continue

    vertices = vor.vertices[region]

    polygon = Polygon(vertices).intersection(specimen)

    if polygon.is_empty:
        continue

    if polygon.geom_type == "Polygon":
        pieces = [polygon]

    elif polygon.geom_type == "MultiPolygon":
        pieces = list(polygon.geoms)

    else:
        continue

    for piece in pieces:
        if piece.area > 1e-8 and piece.is_valid:
            grain_polygons.append(piece)


if not grain_polygons:
    raise RuntimeError(
        "No grains were generated. Check the Python installation."
    )


# ==========================================================
# 4. PLOT AND SAVE THE MICROSTRUCTURE
# ==========================================================

fig, ax = plt.subplots(figsize=(12, 6))

for grain in grain_polygons:

    x, y = grain.exterior.xy

    ax.fill(
        x,
        y,
        facecolor="white",
        edgecolor="black",
        linewidth=0.8
    )

ax.set_xlim(0, L)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")
ax.set_title("Simulated Polycrystalline Microstructure")

plt.tight_layout()
plt.savefig(IMAGE_FILE, dpi=300)
plt.show()
plt.close(fig)

print("Number of polygon pieces:", len(grain_polygons))
print("Microstructure image saved to:", IMAGE_FILE)


# ==========================================================
# 5. CREATE CAD SURFACES IN GMSH
# ==========================================================

gmsh.initialize()

try:
    gmsh.model.add("Polycrystalline_Aluminium")

    # Use OpenCASCADE for CAD geometry
    gmsh.model.setCurrent("Polycrystalline_Aluminium")

    gmsh.option.setString("Geometry.OCCTargetUnit", "MM")

    occ = gmsh.model.occ

    surface_tags = []

    for grain in grain_polygons:

        # This script exports the exterior of each polygon.
        # It is designed for polygons without holes.
        if len(grain.interiors) > 0:
            raise ValueError(
                "A grain contains a hole; special handling is required."
            )

        coords = list(grain.exterior.coords)[:-1]

        point_tags = []

        for x, y in coords:
            point_tags.append(
                occ.addPoint(float(x), float(y), 0.0)
            )

        line_tags = []

        for i in range(len(point_tags)):

            start_tag = point_tags[i]
            end_tag = point_tags[(i + 1) % len(point_tags)]

            line_tags.append(
                occ.addLine(start_tag, end_tag)
            )

        curve_loop = occ.addCurveLoop(line_tags)

        surface_tag = occ.addPlaneSurface([curve_loop])

        surface_tags.append(surface_tag)

    # Fragment surfaces so touching grains share interfaces
    # in the CAD geometry.
    occ.fragment(
        [(2, surface_tags[0])],
        [(2, tag) for tag in surface_tags[1:]],
        removeObject=True,
        removeTool=True
    )

    occ.synchronize()

    # Export the geometry
    gmsh.write(STEP_FILE)

    print("STEP geometry saved to:", STEP_FILE)

finally:
    gmsh.finalize()


print("\nGeometry generation completed.")