import numpy as np
cimport numpy as np
from tqdm import tqdm

edge_dtype = np.dtype([
    ("first_node", np.int_),
    ("second_node", np.int_),
    ("distance", np.single)
])

cdef edge_t[::1] transform_graph_pd(G, str length_attribute):
    """ Transforms a pandas DataFrame in a MemoryView of edge_t that
    represents the same graph.

    Parameters
    ----------
        G : pandas DataFrame that represent an edge list.

        length_attribute : name of the weights on edges. By default, for a osmnx network this is 'legnth'.
    """
    cdef int number_of_edges = max(G["source"].max(),G["target"].max())+1
    cdef np.ndarray[ndim =1, dtype = edge_t] edge_array = np.empty(G.shape[0], dtype = edge_dtype, order = "C")
    cdef int i = 0

    edge_array["first_node"] = G["source"]
    edge_array["second_node"] = G["target"]
    edge_array["distance"] = G[length_attribute]

    return edge_array


cdef edge_t[::1] transform_graph_nx(G, str length_attribute):
    """ Transforms a networkx undirected graph in a MemoryView of edge_t that
    represents the same graph.

    Parameters
    ----------
        G : a networkx undirected graph.

        length_attribute : name of the weights on edges. By default, for a osmnx network this is 'legnth'.
    """

    cdef int number_of_edges = G.number_of_edges()
    cdef edge_t[::1] edge_array = np.zeros(number_of_edges, dtype=edge_dtype)
    cdef int i = 0

    for u, v, data in G.edges(data=True):
        edge_array[i].first_node = u
        edge_array[i].second_node = v
        edge_array[i].distance = data[length_attribute]
        i+=1 

    return edge_array




