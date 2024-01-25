import numpy as np # for doing math easily in python
import matplotlib.pyplot as plt # for plotting in python

def test_bipartite_graph(bipartite_graph_student):
    bipartite_graph = np.array([[1, 0, 0],
                                [0, 1, 0],
                                [1, 0, 1],
                                [0, 1, 0]])

    equal = np.array_equal(bipartite_graph, bipartite_graph_student)

    if equal is True:
        print("Your adjancency matrix is correct!")
    else:
        print("Your adjancency matrix is incorrect. Check for mistakes.")