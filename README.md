# Polycrystalline Aluminium: Microstructure Generation and FEM Analysis

## Project Overview

This project focuses on the computational generation of a synthetic polycrystalline aluminium microstructure and its preliminary mechanical investigation using the Finite Element Method (FEM).

A two-dimensional Voronoi tessellation approach is implemented in Python to generate individual grain regions. The resulting geometry is exported in STEP format and imported into ANSYS Workbench for structural analysis under tensile displacement loading.

The broader research objective is to investigate how grain geometry and grain-boundary properties influence mechanical response and, ultimately, crack propagation in polycrystalline materials.

## Research Objectives

- Generate a synthetic polycrystalline microstructure using Voronoi tessellation.
- Create individual grain geometries and export them in STEP format.
- Develop a finite element model in ANSYS Workbench.
- Evaluate deformation and von Mises stress distributions under tensile loading.
- Investigate mesh sensitivity and the influence of grain interfaces.
- Develop a framework for future grain-boundary fracture modelling.

## Methodology

**1. Microstructure Generation**

A synthetic 2D microstructure containing 50 Voronoi grains is generated using Python.

**2. Geometry Development**

Individual grain regions are constructed using Shapely and Gmsh and exported as a STEP geometry.

**3. Finite Element Modelling**

The geometry is imported into ANSYS Workbench, where meshing, material assignment, contact definitions and tensile boundary conditions are established.

**4. Structural Analysis**

A preliminary static structural analysis is performed to evaluate total deformation and equivalent von Mises stress.

**5. Mesh Sensitivity**

Additional mesh refinements are performed to examine the sensitivity of maximum stress predictions.

## Software and Tools

- Python
- NumPy
- SciPy
- Matplotlib
- Shapely
- Gmsh
- ANSYS Workbench 2026 R1

## Preliminary Simulation Results

| Parameter | Result |
|---|---:|
| Synthetic grain count | 50 |
| Maximum applied displacement | 0.01 mm |
| Maximum total deformation | 0.010034 mm |
| Initial maximum von Mises stress | 148.05 MPa |
| First refined model maximum stress | 174.99 MPa |
| Second refined model maximum stress | 185.84 MPa |

The increase in maximum stress with mesh refinement indicates that further mesh convergence assessment is required.

## Limitations

- The microstructure is synthetically generated and is not an experimentally measured aluminium microstructure.
- All grains currently use identical isotropic elastic properties.
- The current bonded grain interfaces do not permit grain-boundary separation.
- The present analysis does not yet simulate crack initiation or propagation.
- Mesh convergence and contact behaviour require further verification.

## Future Work

- Mesh convergence and validation.
- Incorporation of crystallographic orientation-dependent properties.
- Grain-boundary cohesive-zone modelling.
- Investigation of crack initiation and propagation.
- Quantitative analysis of grain size and grain-boundary fracture resistance.

## Author

**Harshit Anand**

M.Tech Candidate, Materials Science and Engineering

Indian Institute of Technology Indore

**Research Interests:** Computational Materials Science, Finite Element Analysis, Fracture Mechanics and Advanced Materials.
