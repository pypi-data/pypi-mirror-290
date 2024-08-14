cimport numpy as np

from NetHDBSCAN.structures._union_find cimport UnionFind
from NetHDBSCAN.structures._graph cimport edge_t


cdef np.ndarray[dtype = double, ndim=2] clean_linkage_matrix(np.ndarray[dtype = double, ndim=2] linkage_matrix)
cdef np.ndarray[ndim=2, dtype = double] percolate_edge_list(edge_t[::1] edge_list, int n_nodes)
cpdef np.ndarray[dtype = double, ndim=2] percolate_network(G, str length_attribute, str data_type)