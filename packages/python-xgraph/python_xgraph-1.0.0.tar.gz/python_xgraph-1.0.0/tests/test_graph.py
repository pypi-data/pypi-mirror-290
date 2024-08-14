import unittest
from python_xgraph import Graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        """Set up a basic graph for testing."""
        self.graph = Graph(directed=True)
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")

    def test_add_vertex(self):
        """Test adding a vertex."""
        self.graph.add_vertex("D")
        self.assertTrue(self.graph.has_vertex("D"))
        self.assertRaises(ValueError, self.graph.add_vertex, "A")

    def test_add_edge(self):
        """Test adding an edge."""
        self.graph.add_edge("C", "A")
        self.assertTrue(self.graph.has_edge("C", "A"))
        self.assertRaises(ValueError, self.graph.add_edge, "A", "B")

    def test_remove_vertex(self):
        """Test removing a vertex."""
        self.graph.remove_vertex("B")
        self.assertFalse(self.graph.has_vertex("B"))
        self.assertFalse(self.graph.has_edge("A", "B"))
        self.assertRaises(ValueError, self.graph.remove_vertex, "Z")

    def test_remove_edge(self):
        """Test removing an edge."""
        self.graph.remove_edge("A", "B")
        self.assertFalse(self.graph.has_edge("A", "B"))
        self.assertRaises(ValueError, self.graph.remove_edge, "A", "B")

    def test_dfs(self):
        """Test DFS traversal."""
        result = self.graph.dfs("A")
        self.assertEqual(result, ["A", "B", "C"])

    def test_bfs(self):
        """Test BFS traversal."""
        result = self.graph.bfs("A")
        self.assertEqual(result, ["A", "B", "C"])

    def test_has_cycle(self):
        """Test cycle detection."""
        self.assertFalse(self.graph.has_cycle())
        self.graph.add_edge("C", "A")
        self.assertTrue(self.graph.has_cycle())

    def test_topological_sort(self):
        """Test topological sort."""
        result = self.graph.topological_sort()
        self.assertEqual(result, ["A", "B", "C"])
        self.graph.add_edge("C", "A")
        self.assertRaises(ValueError, self.graph.topological_sort)

if __name__ == "__main__":
    unittest.main()
