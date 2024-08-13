# python-xgraph

`python-xgraph` is a simple Python library for working with graphs. It provides basic functionalities like adding vertices and edges, performing DFS and BFS, detecting cycles, and more.

## Installation

You can install the package via pip:

```bash
pip install python-xgraph
```

## Usage

```
from python_xgraph import Graph

g = Graph(directed=True)
g.add_vertex("A")
g.add_edge("A", "B")
print(g.dfs("A"))

```