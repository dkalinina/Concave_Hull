from scipy.spatial import Delaunay
import networkx as nx
import numpy as np
from libc.math cimport sqrt

cpdef area_of_polygon_crd(object cordinates):
    N = len(cordinates)
    cdef object a = cordinates[N-1], b = cordinates[0], c = cordinates[1]
    cdef double area = a[0] * (b[1] - cordinates[-2][1]) + b[0] * (c[1] - a[1])
    for i in range(2, N):    
        a = b
        b = c
        c = cordinates[i]
        area += b[0] * (c[1] - a[1])
    area /= 2.0
    return area

cpdef shapeToSomePolygons(shape):
    G = nx.Graph()
    allnodes = set()
    for line in shape:
        G.add_nodes_from(line)
        G.add_edge(line[0], line[1])
        allnodes.add(line[0])
        allnodes.add(line[1])

    result = []

    while allnodes:
        node = allnodes.pop()
        new_node = next(iter(G[node]), None)
        if not new_node: continue

        G.remove_edge(node, new_node)
        temp = nx.shortest_path(G, node, new_node)
        for t in temp:
            if t in allnodes:
                allnodes.remove(t)
                
        result.append(temp)
    return result

cpdef getAlfaShapes(pts,alfas=1):
    tri = Delaunay(pts)
    triangles = [s for s in tri.simplices]
    for s in triangles:
        s.sort()
    lengths = lengths_dict(pts, triangles, len(triangles))

    mean_length = np.mean(list(lengths.values()))
    ls = sorted([l for l in lengths.values() if l >= mean_length])
    magic_numbers = [l for l in ls]
    magic_numbers_func(magic_numbers, len(magic_numbers))

    rez = []

    for alfa in alfas:
        av_length = get_min_length(magic_numbers, ls, alfa, len(ls))
        good_lines = get_good_lines(av_length, lengths, triangles, pts, len(triangles))
        
        result = shapeToSomePolygons(good_lines) # разделение на отдельные кластеры
        result.sort(key=area_of_polygon_crd, reverse=True)
        rez.append(result)
    return rez

cpdef get_good_lines(double l, object lengths, object tri, object pts, int N):
    good_lines = set()
    cdef object s, line1, line2, line3, line
    for i in range(0, N):
        s = tri[i]
        line1 = (s[0], s[1])
        if lengths[line1] > l: continue
        line2 = (s[1], s[2])
        if lengths[line2] > l: continue
        line3 = (s[0], s[2])
        if lengths[line3] > l: continue
        
        for line in [line1, line2, line3]:
            line = (pts[line[0]], pts[line[1]])
            if line in good_lines:
                good_lines.remove(line)
            else:
                good_lines.add(line)
    return good_lines    

cpdef magic_numbers_func(object a, int N):
    cdef double sum = 0
    a[0] = 0
    for i in range(1, N):
        sum += a[i]
        a[i] += a[i-1]
    for i in range(1, N):
        a[i] /= sum
    return a
    
cpdef get_min_length(object a, object b, double alfa, int N):
    cdef int i = 0
    for i in range(0, N):
        if a[i] >= alfa:
            return b[i]
    return b[N-1]  
    
cpdef lengths_dict(object pts, object tri, int N):
    cpdef tri_ind = [(0,1),(1,2),(0,2)]
    cdef int x = -1, y = -1
    cdef object s, line
    lengths = {}
    for i in range(0, N):
        s = tri[i]
        for ind in tri_ind:
            x = s[ind[0]]
            y = s[ind[1]]
            line = (x, y)
            if line not in lengths:
                lengths[line] = dist(pts[x], pts[y])
    return lengths  

cpdef dist(object a, object b):
    return dist_inner(a[0]-b[0], a[1]-b[1])

cdef dist_inner(object a, object b):
    return sqrt(a*a + b*b)
