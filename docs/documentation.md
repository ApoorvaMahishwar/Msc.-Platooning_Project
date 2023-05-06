# Documentation of the project
This markdown includes the documentations of our project. This will include any steps performed during the setup of the dev environments and implementation of the project.
## Configuration & Preparation
This chapter handles the used configurations and the steps needed for setting up the environements.
### GitLab & GitKraken
We will use GitLab TU-Clausthal internal-managed server (`gitlab.tu-clausthal.de`) to track the development of our master's project.
GitKraken GLO Board is used to keep track of the requirements and tasks of the project.
GitLab URL: `https://gitlab.tu-clausthal.de/mbe19/msc-platooning-project.git`
GitKraken GLO Board: `https://app.gitkraken.com/glo/board/YXk7XbLwZwBH-ip5`
### Initial Setup
- Intialise a new repository to held the `Msc. Platooning Project`.
- This repository includes the progress made concerning the implementations.
- extract the ILP solution for the VP problem into the local repos as `~/msc-platooning-project/ILP_VPP`.
- add `~/msc-platooning-project/GNNVPP` to include the Graph Neural Network (GNN) proposed solution for the VP problem.
- add a `~/msc-platooning-project/docs/` directory for documentation.
### Environements & Requirements
- Setting up a virtual environment using `mkvirtualenv` and activate it using `workon`:
```
$ mkvirtualenv --python=/usr/bin/python3.6 project_venv
$ workon project_venv
```
This will create a virtual environment based on python *version 3.6.9* (as mentioned in a meeting with Gerrit, `gurobipy` has problems with version 3.7).
To deactivate `project_venv` we can use `(project_venv)$ deactivate`.
- Installation of `gurobipy`:
`gurobi` is an optimization framework and package that focuses on offering fast mathematical optimization solvers. More information can be found [here](https://www.gurobi.com/company/about-gurobi/).
These are the steps followed to setup `gurobi` both as a cl utility and a python package.
  - Download the *gurobi optimizer* sources and the README file from here: [Download Page of Gurobi](https://www.gurobi.com/downloads/gurobi-software/) (A register account is needed).
  - Follow the instructions from the README file to install the sources and set up some environmental variables properly.
  - Generate a [Free Academic License](https://www.gurobi.com/academia/academic-program-and-licenses).
  - Use the `grbgetkey` command to pull the key: `$ grbgetkey ae36ac20-16e6-acd2-f242-4da6e765fa0a`.
  - Copy the downloaded license to a safe directory (preferably in e.g: /opt/gurobi912), if another directory is used then the `GRB_LICENSE_FILE` variable needs to be set up in `.bashrc`, by adding: `export GRB_LICENSE_FILE='/home/user/path_to_license/gurobi.lic'`
  - `$ source .bashrc` can be used to refresh the current bash session to take the new configurations into account.
  - We can test that the license is installed by running `gurobi_cl`, sample output:
```
Academic license - for non-commercial use only - expires 2022-10-22
Using license file /home/user/.gurobi_lic/gurobi.lic
```
- To install the `gurobipy` package we can use the `pip` python installer:
  - Run `(project_venv)$ python -m pip install -i https://pypi.gurobi.com gurobipy` from our `project_venv` virtual environment for installation.
  - We can check the installation by running `(project_venv)$ pip list`, sample output:
  
```
Package       Version
------------- -------
gurobipy      9.1.2
...
```

- We can run this `(project_venv)$ python -c "from gurobipy import Model; model=Model()"` to check whether everything is setup correctly, this command should have similar output to this:
```
Academic license - for non-commercial use only - expires 2022-10-22
Using license file /home/user/.gurobi_lic/gurobi.lic
```
Now everything is setup for using `gurobipy` with `python3.6.9` in our `project_venv` environment.
- Installation of other dependencies:
Only `networkx` and `neo4j` packages are left to install, this can be done with:
```
(project_venv)$ pip install networkx neo4j
```
- A `requirements.txt` file is provided under `~/msc-platooning.project/pkgs/` containing all the required packages for using the scripts. This comes handy when installing packages from scratch. This can be done with `(project_venv)$ pip install -r requirements.txt`.
- Setting up the Neo4j database:
A [Neo4j graph database](https://neo4j.com/) is required to hold the road network, vehicles and their defined model. Therefore setting up `neo4j` in our case is a must. This is performed by following one of the following approaches:
  - Setting up `Neo4j Desktop`:
Which can hold one or more local databases, and can be managed by and viewed purely in a GUI.
The following link: [how to set up Neo4j Desktop](https://neo4j.com/download-thanks-desktop/?edition=desktop&flavour=unix&release=1.4.8&offline=true), provides a downloadable image with some simple steps to get your Neo4j Desktop experience going.
  - Setting up `Neo4j v3.5.14` to run from the commmand line on `Ubuntu 18.04.6 LTS`. This is the recommended approach, since it offers more flexibility of controlling our `neo4j` environement and launching our database server without the need to have an open GUI all the time.
    - To do so we can simply add the *Neo4j repository* to the *apt package manager database* and installing neo4j by running:
	```
	$ wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
	$ echo 'deb https://debian.neo4j.com stable 3.5' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
	$ sudo apt-get update
	$ sudo apt install neo4j=1:3.5.14
	```
    - Now that we installed `neo4j`, we can simply check if it's correctly installed by runningand installing neo4j :
	```
	$ neo4j version
	```
	You should get a simillar output to this:
	```
	neo4j 3.5.14
	```
    - Before continuing any further we need to change a default setting, namely, altering the privileges for `/var/lib/neo4j/data/databases/store_lock`, by running:
	```
	$ sudo chmod 776 /var/lib/neo4j/data/databases/store_lock
	```
	This will allow `neo4j` to have *read/write* privileges over this file, which let us avoid a related error when running our `neo4j` database server .
 - Setting up our `platooning.db` database:
 
     We need to modify our `neo4j` default active database situated in `/etc/neo4j/neo4j.conf`.\
     We should set up the value of `dbms.active_database` to `platooning.db`. Save changes.\
     This will let the `neo4j` to point to this database as active every time we run our db server.
 - Finally, running our `neo4j` database server:
     - we can start the server either in the background by running the following:
     ```
     $ sudo neo4j start
     ```
     Sample output:
     ```
     Active database: platooning.db
     Directories in use:
       home:         /var/lib/neo4j
       config:       /etc/neo4j
       logs:         /var/log/neo4j
       plugins:      /var/lib/neo4j/plugins
       import:       /var/lib/neo4j/import
       data:         /var/lib/neo4j/data
       certificates: /var/lib/neo4j/certificates
       run:          /var/run/neo4j
     Starting Neo4j.
     WARNING: Max 1024 open files allowed, minimum of 40000 recommended. See the Neo4j manual.
     Started neo4j (pid 16081). It is available at http://localhost:7474/
     There may be a short delay until the server is ready.
     See /var/log/neo4j/neo4j.log for current status.
     ```
     - The second approach to run our server in *console mode*, by running:
     ```
     $ sudo neo4j console
     ```
     Sample output:
     ```
     Active database: platooning.db
     Directories in use:
       home:         /var/lib/neo4j
       config:       /etc/neo4j
       logs:         /var/log/neo4j
       plugins:      /var/lib/neo4j/plugins
       import:       /var/lib/neo4j/import
       data:         /var/lib/neo4j/data
       certificates: /var/lib/neo4j/certificates
       run:          /var/run/neo4j
     Starting Neo4j.
     WARNING: Max 1024 open files allowed, minimum of 40000 recommended. See the Neo4j manual.
     2021-10-28 10:57:35.264+0000 WARN  dbms.active_database is deprecated.
     2021-10-28 10:57:35.276+0000 INFO  ======== Neo4j 3.5.14 ========
     2021-10-28 10:57:35.283+0000 INFO  Starting...
     2021-10-28 10:57:35.863+0000 INFO  Initiating metrics...
     2021-10-28 10:57:36.611+0000 INFO  Sending metrics to CSV file at /var/lib/neo4j/metrics
     2021-10-28 10:57:36.942+0000 INFO  Bolt enabled on 127.0.0.1:7687.
     2021-10-28 10:57:37.944+0000 INFO  Started.
     2021-10-28 10:57:38.074+0000 INFO  Mounted REST API at: /db/manage
     2021-10-28 10:57:38.122+0000 INFO  Server thread metrics have been registered successfully
     2021-10-28 10:57:38.625+0000 INFO  Remote interface available at http://localhost:7474/
     ```
     
     This mode is nicer when a live debugging session is required, since any output will be shown directly on the terminal output.
     
   - We can then visit `http://localhost:7474/` in our browser to have a GUI view of our database.\
    Note! The default credentials are:
    ```
    username: neo4j
    password: neo4j
    ```
        

*Side-Note: the `sudo` here in most of the command is required since we are installing `neo4j` in root owned directories (i.e: `/var/lib`, `/var/run` and `/etc`).*

### Populating the database

*Under Construction...*

### Running the example:
In this section we will try to run the `main.py` script, but first we need to make sure that Neo4j configurations in `db_credentials.py` are correct:
* We should change the following variables:

```
DB_URL = ""
DB_USERNAME = ""
DB_PW = ""

```

Where: `DB_URL` is the database uri; `DB_USERNAME` is the database admin user; `DB_PW` is the user password.
In our case this should be set to:

```
DB_URL = "bolt://localhost:7687"
DB_USERNAME = "neo4j"
DB_PW = "mydb12345"
```

Now we can test, (make sure that your database server is started):

```
(project_venv)$ python main.py

```
Sample output:

```
Academic license - for non-commercial use only - expires 2022-10-22
Using license file /home/mohamed/.gurobi_lic/gurobi.lic
Gurobi Optimizer version 9.1.2 build v9.1.2rc0 (linux64)
Thread count: 6 physical cores, 12 logical processors, using up to 12 threads
Optimize a model with 18 rows, 15 columns and 40 nonzeros
Model fingerprint: 0xd0543416
Variable types: 0 continuous, 15 integer (15 binary)
Coefficient statistics:
  Matrix range     [1e+00, 1e+00]
  Objective range  [1e+00, 9e+01]
  Bounds range     [1e+00, 1e+00]
  RHS range        [1e+00, 1e+00]
Found heuristic solution: objective 140.0000000
Presolve removed 18 rows and 15 columns
Presolve time: 0.00s
Presolve: All rows and columns removed

Explored 0 nodes (0 simplex iterations) in 0.00 seconds
Thread count was 1 (of 12 available processors)

Solution count 2: 116 140

Optimal solution found (tolerance 1.00e-04)
Best objective 1.160000000000e+02, best bound 1.160000000000e+02, gap 0.0000%
Optimal solution value: 116.0
edge (1, 4) has value: 1.0
vehicle 1 on the edge (1, 4) has : 1.0
vehicle 2 on the edge (1, 4) has : 0.0
edge (4, 3) has value: 1.0
vehicle 1 on the edge (4, 3) has : 1.0
vehicle 2 on the edge (4, 3) has : 1.0
```

## Starting with ILP

This chapter describes how to start using the ILP solution (situated in `msc-platooning-project/ILP_VPP/main.py`). It will focus on understanding the code, the optimization model and how to build your own data and use it.

### ILP Implementation

The script `msc-platooning-project/ILP_VPP/main.py` includes the implementation of the ILP optimization model. This is defined inside the function `optimization_model(road_network, group, saving_factor)` based on the `gurobipy` optimization package. `msc-platooning-project/ILP_VPP/lp_VPP.png` hold the mathematical model of the ILP for solving the VPP. The model requires a `road_network` directed graph that describes the road structure; places are represented by nodes and the link between them as edges (please see the function `definitions()` of how this is being done).\

### Definition of the Graph

The `graph` data for the road network and other parameters needed by the optimizer (i.e: `saving_factor`, `every_value`, `draw`).\
a simple directed graph can be defined e.g as follow:\
```
import networkx as nx

graph = nx.DiGraph()

graph.add_nodes_from([(1, {"coords": [1, 1]}), (2, {"coords": [1, 2]}), (3, {"coords": [2, 1]}))

graph.add_edges_from([(1, 2, {'weight': 10}), (2, 3, {'weight': 90}), (1, 3, {'weight': 100})])
```

Here we are defining a directed graph by using the `nx.DiGraph()` constructor; 3 nodes in the graph with coordinates `"coords": [x, y]`; after that we should define the edges from a starting node to an end node: `((N1, N2, {'weight': v}))`, the edges contain a certain weight property that define the distance between 2 nodes in the road network.

### Definition of the Vehicles' Plan

The `group` dictionary in the `main()` function holds the vehicles' planned routes, which are defined in this format: `{V_ID: (S_Node, E_Node)}`, an example of a vehicles' plan is: {1: (1, 3), 2: (2, 1), 3: (1, 2)}. More vehicles can of course be added to the plan by taking into account the definition of the road network.

# The GNN Solution

This part is concerning the proposed Graph Neural Network (GNN) solution to the vehicle platooning problem.
For a full documentation of this part please refer to the `README.md` file inside the `GNN_VPP/` directory.
