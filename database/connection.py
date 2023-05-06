from neo4j import GraphDatabase
from neo4j.exceptions import AuthError
import networkx as nx
from logging import getLogger, StreamHandler, DEBUG

handler = StreamHandler()
handler.setLevel(DEBUG)

logger = getLogger("neo4j")
logger.addHandler(handler)


class Neo4jConnection:
    """
    Neo4j Connection class.
    """
    def __init__(self, uri, username, pw):
        self._uri = uri
        self._userName = username
        self._password = pw

        # Connect to the neo4j database server
        try:
            self.driver = GraphDatabase.driver(self._uri, auth=(self._userName, self._password))
            print(f"Successfully connected to Neo4j database (server: {self._uri}.)")
        except AuthError:
            logger.error("Connection to the db couldn't be established. Please check your credentials.")
        logger.info(f"Successfully connected to Neo4j database (server: {self._uri}.)")
        logger.info(self.driver)

    def close(self):
        self.driver.close()

    @staticmethod
    def query(tx, query):
        res = tx.run(query)

        #[print(record["n"].properties) for record in res]

        return [record for record in res]

    def get_data(self):

        graph = nx.Graph()

        with self.driver.session() as session:
            # add nodes to graph
            result = session.read_transaction(self.query, "MATCH (n:RoadPoint) RETURN n;")
            for res in result:
                graph.add_node(res["n"].id, x=res['n'].get("x"), y=res['n'].get("y"), lat=res['n'].get("lat"), lon=res['n'].get("lon"))

            # add edges to graph
            result = session.read_transaction(self.query, "MATCH (n)-[r:ROAD_SEGMENT]-(m)  RETURN r;")
            for res in result:
                graph.add_edge(res["r"].nodes[0].id, res["r"].nodes[1].id, key=res["r"].id, weight=res["r"].get("distance"), attr_dict={'id': res["r"].nodes[1].id})

        return graph
