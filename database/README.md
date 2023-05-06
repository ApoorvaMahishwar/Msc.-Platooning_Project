# Database Setup

The steps to follow to setup the database to work in a python environement.

## Setup Python

1. Install the `neo4j` package from `PiPy` (this includes the noe4j driver):

```sh
$ pip install neo4j
```

## Setup Neo4j

1. Download [Neo4j Desktop](https://neo4j.com/download-center/) for a GUI management of your neo4j database instances.

2. Create the database by running this query:

```
query = "WITH 50.0*1000 as width, 50.0*1000 as height, 10 as x_num, 10 as y_num, 10 as depot_num UNWIND range(0, x_num-1) AS x UNWIND range(0, y_num-1) AS y WITH *, x * width / 110574.0 AS lat WITH *, y * height / (111320.0 * cos(lat/360.0)) AS lon CREATE (n:RoadPoint {lat: lat, lon: lon, x: x, y: y}) WITH DISTINCT x_num, y_num, depot_num UNWIND range(0, x_num-1) AS x UNWIND range(0, y_num-2) AS y MATCH (n:RoadPoint) WHERE n.x = x AND n.y = y MATCH (m:RoadPoint) WHERE m.x = x AND m.y = y+1 WITH *, distance(point({latitude: n.lat, longitude: n.lon}), point({latitude: m.lat, longitude: m.lon})) AS d CREATE (n)-[:ROAD_SEGMENT {distance_meter: d, distance: d/1000.0}]->(m)<-[:ROAD_SEGMENT {distance_meter: d, distance: d/1000.0}]-(n) WITH DISTINCT x_num, y_num, depot_num UNWIND range(0, x_num-2) AS x UNWIND range(0, y_num-1) AS y MATCH (n:RoadPoint) WHERE n.x = x AND n.y = y MATCH (m:RoadPoint) WHERE m.x = x+1 AND m.y = y WITH *, distance(point({latitude: n.lat, longitude: n.lon}), point({latitude: m.lat, longitude: m.lon})) AS d CREATE (n)-[:ROAD_SEGMENT {distance_meter: d, distance: d/1000.0}]->(m)-[:ROAD_SEGMENT {distance_meter: d, distance: d/1000.0}]->(n) WITH DISTINCT depot_num MATCH (n:RoadPoint) WITH depot_num, n, rand() AS r ORDER BY r DESC WITH COLLECT(n)[0..depot_num] AS depot_roads UNWIND depot_roads AS depot_road CREATE (:Depot)-[:LOCATED_AT]->(depot_road);"
```

3. Currently the database is setup and should be kept active. We can now connect to the database instance from python and run queries as we like using the uri, username and password provided while creating and running the database.

