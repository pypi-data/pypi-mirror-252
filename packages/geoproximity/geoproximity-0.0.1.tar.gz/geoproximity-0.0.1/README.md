### GeoProximity Package Usage Guide

#### Introduction

GeoProximity is a Python package designed to facilitate geospatial distance calculations, point projections, and related operations. It includes functions for both Haversine distance (great-circle distance) and Euclidean distance calculations. GeoProximity is suitable for applications that require proximity analysis, spatial operations, and basic geospatial functionality.

#### Installation

Ensure Python is installed on your system, then install the `geoproximity` package using `pip`:

```sh
pip install geoproximity
```

#### Calculate harversine distance
```python
import geoproximity
geoproximity.haversine_distance(coord1, coord2)
```
