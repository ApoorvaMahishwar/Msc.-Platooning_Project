# Search Algorithms

This is the impelementation of the suggested search algorithms for the given network.

*Authors: Apoorva Mahishwar (519795) & Mohamed Benchat (516589)*

## Method 1: Permute & Search

This approach takes the permutation order of a certain truck and applies it to all the nodes in the given network graph. The resulting structure is then used for creating the route starting from an origin and ending in a destination.

## Method 2: Embed & Search

The permutation order is embedded into the network's nodes. The search algorithm starts from the origin and visits the adjacent node with the minimum weight (i.e: order) until it reachs the destination.


## Query to build database

Run this query to setup the database for the stress-test.

```
query = "WITH 50.0*1000 as width, 50.0*1000 as height, 10 as x_num, 10 as y_num, 10 as depot_num UNWIND range(0, x_num-1) AS x UNWIND range(0, y_num-1) AS y WITH *, x * width / 110574.0 AS lat WITH *, y * height / (111320.0 * cos(lat/360.0)) AS lon CREATE (n:RoadPoint {lat: lat, lon: lon, x: x, y: y}) WITH DISTINCT x_num, y_num, depot_num UNWIND range(0, x_num-1) AS x UNWIND range(0, y_num-2) AS y MATCH (n:RoadPoint) WHERE n.x = x AND n.y = y MATCH (m:RoadPoint) WHERE m.x = x AND m.y = y+1 WITH *, distance(point({latitude: n.lat, longitude: n.lon}), point({latitude: m.lat, longitude: m.lon})) AS d CREATE (n)-[:ROAD_SEGMENT {distance_meter: d, distance: d/1000.0}]->(m)<-[:ROAD_SEGMENT {distance_meter: d, distance: d/1000.0}]-(n) WITH DISTINCT x_num, y_num, depot_num UNWIND range(0, x_num-2) AS x UNWIND range(0, y_num-1) AS y MATCH (n:RoadPoint) WHERE n.x = x AND n.y = y MATCH (m:RoadPoint) WHERE m.x = x+1 AND m.y = y WITH *, distance(point({latitude: n.lat, longitude: n.lon}), point({latitude: m.lat, longitude: m.lon})) AS d CREATE (n)-[:ROAD_SEGMENT {distance_meter: d, distance: d/1000.0}]->(m)-[:ROAD_SEGMENT {distance_meter: d, distance: d/1000.0}]->(n) WITH DISTINCT depot_num MATCH (n:RoadPoint) WITH depot_num, n, rand() AS r ORDER BY r DESC WITH COLLECT(n)[0..depot_num] AS depot_roads UNWIND depot_roads AS depot_road CREATE (:Depot)-[:LOCATED_AT]->(depot_road);"
```

## Clarifications

* depot  = potential destination/origin.

1. Setup database.
2. Naive solution.
3. Stress test.


## Writing Procedure

I. Literature review

II. Modeling: Point of the problem definition

III. Solution Methodology

IV. Experimental Results (Computantional Experiments)

V. Conclusion

VI. References


Number of pages: 12 - 14.
