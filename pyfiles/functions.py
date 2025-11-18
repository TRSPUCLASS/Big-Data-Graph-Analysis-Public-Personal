import networkx
import sys
#For loop, iterates through each line in file and adds edge to graph
def importfile(graph : networkx.DiGraph, file) -> None:
    for pair in file:
        #Handles comments
        if pair[0] == "#":
            continue
        #Split into two strings based on whitespace
        edge = pair.split()
        #Double checks valid input
        if len(edge) != 2 or not edge[0].isdigit() or not edge[1].isdigit():
            print("Invalid input file")
            sys.exit()
        #Adds edge to graph
        graph.add_edge(int(edge[0]), int(edge[1]))

#Attempts at assessing centrality
def centralityassess(pathDict : dict) -> []:
    #Number of nodes, N
    arrayLen = len(pathDict)
    #Stores values
    closenessDict = {}
    for key, row in pathDict.items():
        #Number of Reachable nodes, n
        nodeCount = 0.0
        #Total distance for the row
        rowTotal = 0.0
        for column in row.values():
            #Excludes self loops
            if len(column) != 1:
                nodeCount += 1
                rowTotal += len(column)-1
        #No dividing by zero for exterior nodes
        if rowTotal != 0:
            #Already skipped 1 self loop, so n here is n-1 in proper equation
            #(n/(N-1)) * (n/(Summation of distances of reachable nodes))
            closenessDict.update({key :(nodeCount /(arrayLen-1))*(nodeCount / rowTotal)
})
        #Handles exterior nodes
        else:
            closenessDict.update({key : 0.0})
            
    return closenessDict
#Original attempt, became hard to manage
'''
#Creates a new graph as a subgraph of the original, of degree two. Scalability issues
def twodegsubgraph(index, origGraph):
    newgraph=networkx.DiGraph()
    # root node connections
    for i in origGraph.neighbors(index):
        newgraph.add_edge(index, i)
        #Connection's connections
        for j in origGraph.neighbors(i):
            newgraph.add_edge(i,j)
            #Connection's connection's connections, unless it's the root again
            if not newgraph.has_node(j):
                for k in origGraph.neighbors(j):
                    newgraph.add_edge(j,k)
    return newgraph
'''
#Recursive implementation, easily modifiable but worse space
def degsubgraph(origGraph : networkx.DiGraph, index : int, depth : int) -> networkx.DiGraph:
    newgraph = networkx.DiGraph()
    visited = dict() # Holds all visited nodes
    #Handles leaf nodes
    try:
        #dict only works if neighbors is empty in this specific case
        #It serves as a check for if there are neighbors
        dict(origGraph.neighbors(index))
        newgraph.add_node(index)
        return newgraph
    #Handles everything else
    except:
        #Recursive definition inside base definition to prevent explicit calls
        def recursive(index : int, count : int, graph : networkx.DiGraph):
            #Base case for maximum depth
            if count == depth:
                return
            #Implicit base case of not having neighbors
            for i in origGraph.neighbors(index):
                graph.add_edge(index, i)
                if (i not in visited) or visited[i] > count:
                    visited.update({i:count})
                    recursive(i, count + 1, graph)
                    
        recursive(index, 0, newgraph)
        return newgraph
#Finds longest path
def longestpath(inDict : dict) -> []:
    #Stores index - assumes non null input
    mostIndex = [0,0]
    most = 0
    #Key:value for dictionary
    for key, i in inDict.items():
        for key2, j in i.items():
            if len(j) > most:
                most = len(j)
                mostIndex = [key,key2]
    return inDict[mostIndex[0]][mostIndex[1]]
def shortestpath(graph : networkx.DiGraph, node1 : int, node2 : int) -> []:
    try:
        return networkx.shortest_path(graph, node1, node2)
    except:
        return "Invalid nodes"
