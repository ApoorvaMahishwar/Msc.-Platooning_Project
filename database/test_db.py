#./database/test_db.py

from connection import Neo4jConnection
import db_credentials as dbc


def main():

    app   = Neo4jConnection(dbc.DB_URL, dbc.DB_USERNAME, dbc.DB_PW)
    graph = app.get_data()

    print(graph.nodes())
    print(graph.edges())

if __name__ == "__main__":
    main()

