import numpy as np
cimport numpy as np

from NetHDBSCAN.structures._union_find cimport UnionFind
from NetHDBSCAN.structures._graph cimport edge_t, transform_graph_nx, transform_graph_pd
from NetHDBSCAN.structures._graph import edge_dtype

from tqdm import tqdm

cdef  np.ndarray[ndim = 2, dtype = double] percolate_edge_list(edge_t[::1] edge_list, int n_nodes):
    """ Computes the percolation algorithm on the edge list of a given network.
    
    Parameters  
    ----------
        edge_list : a MemoryView of edge_t formated edges that represents a graph
        
        n_node : the number of nodes in the graph
    
    Returns
    -------
        linkage_matrix : the linkage matrix representation of the computed linkage tree
    
    A linkage matrix is a np.ndarray A with 4 columns : 
    - A[i,0] and A[i,1] are the names of the merged clusters at step i
    - A[i,2] contains the length of the link that merged the two clusters
    - A[i,3] contains the size of the new cluster

    NB : The scipy standard for linkage matrix requires that the same cluster can not be merged. 
    Thus one may use the clean_linkage_matrix function to fit this constraint.
    """

    cdef : 
        int n_samples = len(edge_list)
        long current_node_cluster, next_node_cluster
        long current_node, next_node 
        int i
        double distance
        UnionFind U = UnionFind(n_nodes)
        np.ndarray[ndim = 2, dtype = double] linkage_matrix = np.zeros((n_samples,4), dtype = np.double)

    pbar = tqdm(total = n_samples)

    for i in range(n_samples):

        pbar.update(1)
        
        current_node = edge_list[i].first_node
        next_node = edge_list[i].second_node
        distance = edge_list[i].distance

        current_node_cluster = U.fast_find(current_node)
        next_node_cluster = U.fast_find(next_node)
        
        # Standard representation of the linkage tree
        linkage_matrix[i,0] = current_node_cluster
        linkage_matrix[i,1] = next_node_cluster
        linkage_matrix[i,2] = distance
        linkage_matrix[i,3] = U.size_arr[current_node_cluster] + U.size_arr[next_node_cluster]

        U.union(current_node_cluster, next_node_cluster)

    pbar.close()
    return linkage_matrix




cdef np.ndarray[dtype = double, ndim=2] clean_linkage_matrix(np.ndarray[dtype = double, ndim=2] linkage_matrix):
    """ Removes redundant rows in the linkage matrix to fit the constraints of scipy standard.
    The scipy standard for linkage matrix requires that the same cluster can not be merged. 
    
    Parameters  
    ----------
        linkage_matrix : the linkage matrix that is output by the percolation method
    
    Returns 
    -------
        cleaned_linkage_matrix : linkage matrix of the same linkage tree but the 
        redundant merges of the same cluster are deleted
    """

    cdef int i = 0
    linkage_matrix = linkage_matrix[linkage_matrix[:, 0] != linkage_matrix[:, 1]]
    return linkage_matrix



cpdef np.ndarray[dtype = double, ndim=2] percolate_network(G, str length_attribute, str data_type):
    """ Computes the percolation algorithm on the a given network output by a osmnx querry.
    
    Parameters  
    ----------
        G : a networkx MultiDiGraph

        length_attribute : name of the weights on edges. By default, for a osmnx network this is 'legnth'

        data_type : data type for the G. "networkx" by defalt, "pandas" otherwise
    
    Returns
    -------
        linkage_matrix : the linkage matrix representation of the computed linkage tree 
    
    A linkage matrix is a np.ndarray A with 4 columns : 
    - A[i,0] and A[i,1] are the names of the merged clusters at step i
    - A[i,2] contains the length of the link that merged the two clusters
    - A[i,3] contains the size of the new cluster

    """
    
    cdef int number_of_nodes
    cdef edge_t[::1] edge_list 

    if data_type == "networkx":
        edge_list = transform_graph_nx(G, length_attribute)
        number_of_nodes =  G.number_of_nodes()
    elif data_type == "pandas":
        edge_list = transform_graph_pd(G, length_attribute)
        number_of_nodes = max(G["source"].max(), G["target"].max())+1

    #sorting the list of edges
    np_edge_list = np.asarray(edge_list, dtype = edge_dtype)
    np_edge_list = np.sort(np_edge_list, order=('distance', 'first_node', 'second_node'))
    edge_list = np_edge_list

    cdef np.ndarray[ndim= 2, dtype = double] linkage_matrix = percolate_edge_list(edge_list, number_of_nodes)
    
    linkage_matrix = clean_linkage_matrix(linkage_matrix)

    return linkage_matrix