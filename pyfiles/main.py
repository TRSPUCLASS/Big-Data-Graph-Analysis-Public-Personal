# Testing push...
#Indeed, there is pushing
import networkx, matplotlib, functions, getopt, sys

#Default variables - args excludes path to file being run
args = sys.argv[1:]
filename = "" #Holds name of input file
subGraph = bool #Boolean for which function to execute
arg1 = int #Either the start node for creating a subgraph or the start node for a shortest path
arg2 = int #Either the depth for creating a subgraph or the end node for a shortest path
#Setup variables from arguments, verifies variable correctness:
if len(args) == 4 and (".txt" in args[0]) and (args[1] == "-g" or args[1] == "-p") and args[2].isdigit() and args[3].isdigit():
    filename = args[0]
    if args[1] == "-p":
        subGraph = False
    if args[1] == "-g":
        subGraph = True
    arg1 = int(args[2])
    arg2 = int(args[3])
#Handles wrong variables
else:
    print("Incorrect argument count or arguments")
    sys.exit()
#Create base graph
graph = networkx.DiGraph()
#Read from file-if it fails, exit
try:
    inputFile = open(filename, "r")
except:
    print("Invalid input file")
    sys.exit()
functions.importfile(graph, inputFile)
inputFile.close()
#Used for generating filenames, truncates ".txt"
filename = filename[:filename.find('.txt')]
if subGraph:
    if arg1 not in graph:
        print("Invalid integer arguments, exiting")
        sys.exit()
    #Subgraph of given degree from a given node
    newgraph = functions.degsubgraph(graph, arg1, arg2)
    #Loading path pairs into dictionary-sorted for later CSV file
    shortDict = dict(sorted(networkx.all_pairs_shortest_path(newgraph)))
    #Opens CSV file for all pairs shortest path
    outputCSV = open(filename + "-" + str(arg1) + "-" + str(arg2) + "-apsp.csv", "w")
    #shortDict to CSV:
    for i in shortDict.values():
        for j in shortDict.keys():
            if j in i:
                #Checks if final value for row
                if j != next(reversed(shortDict.keys())):
                    print(len(i[j]) - 1, file = outputCSV, end = ',')
                else:
                    print(len(i[j]) - 1, file = outputCSV)
            else:
                if j != next(reversed(shortDict.keys())):
                    print(-1, file = outputCSV, end = ',')
                else:
                    print(-1, file = outputCSV)
    #Closes CSV
    outputCSV.close()
    #Opens CSV for closeness centrality value
    outputCSV = open(filename + "-" + str(arg1) + "-" + str(arg2) + "-closeness.csv", "w")
    #Centrality calculations
    closeDict = functions.centralityassess(shortDict)
    #Output to file
    for i in closeDict.values():
        print(i, file = outputCSV, end = ',')
    outputCSV.close()
    #Prints most central node
    print("Most central node: ", end = '')
    print(max(closeDict, key = closeDict.get))
    #Prints longest path
    print("Longest path: ", end = '')
    print(functions.longestpath(shortDict))
    #Draws subgraph
    networkx.draw_networkx(newgraph)
    matplotlib.pyplot.show()

else:
    #Trivial, but returns path to node from node
    print("Shortest path: ", end = '')
    print(functions.shortestpath(graph, arg1, arg2))
