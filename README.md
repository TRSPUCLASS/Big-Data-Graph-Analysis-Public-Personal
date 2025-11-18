# Big Data Graph Analysis
Processing a BigData Graph with a third party library.

Read the PowerPoint on Canvas.
*You may use the Graph Library Shortest Paths functions*
*You **may not** use the Graph Library Closeness Centrality functions*
* You will work with the data available [here](https://www.kaggle.com/datasets/pappukrjha/google-web-graph/code).

**DO NOT COPY, DO THE PROJECT 100% YOURSELVES**

**USE AI AT YOUR OWN RISK**
> It is probable that I ask in the test about how you did something on this assignment, so learn very well!



## Introduction	
This program aims to find the node most suited to propagate changes through a sub-network of a network. It accomplishes this by modelling the network (Provided as a file with a set of edges) as a graph, calculating a requested subgraph, and finding the most central vertex of that subgraph. The most central vertex is well suited to propagate changes due to being the node with the average shortest distance to the other nodes, requiring fewer nodes on average to propagate the change.\
This program also provides a tool to find the shortest path between any two given nodes in a network.
## Description
In order to calculate centrality, the program first computes the shortest paths from each node to each other node. This is done using networkx's built in all_pairs_shortest_paths function. 
This data is then stored in a dictionary for internal access and a CSV file in case of manual review.\
![image](https://github.com/user-attachments/assets/ff9e9e55-bbfa-4662-aded-59a7e54d5c73)\
  A dictionary, used for internal access\
![image](https://github.com/user-attachments/assets/bfd63c27-fb82-42e1-9440-f4274bf9b5b9)\
  A sorted CSV file, used for manual review \
The computer then calculates closeness centrality for each node. Closeness centrality is a measure of how central a node is in the graph. This is done by taking the reciprocal of the sum of the distances from that node to each other node, with the additional convention that ∞ = 0 and skipping the calculation of 1/0 (a case in which no other nodes are reachable from that node-this results in the result being multiplied by 0 later). This value is then multiplied by the number of  nodes reachable divided by the total number of nodes, to account for the high chance of a graph not being completely connected. Neither of the latter two values count the node being analyzed itself.\
$`\frac{n-1}{N-1} * \frac{1}{\sum_{y=1}^n dist(x,y)} `$
```
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
```
From here, finding the most central node is simply a matter of finding the maximum value in the resulting dictionary. The dictionary is also stored as a CSV file, for manual review.
## Requirements	
Python version 3.13 or higher\
An amount of RAM proportionate to the size of the input graph. The google web graph requires > 8GB. (Exact numbers unavailable at present, owing to communication issues) \
At least 73627 KB available storage, excluding required libraries. If excluding the google web graph this is greatly decreased, down to 13KB. Additional storage will be required for the actual running of the application, in an amount proportionate to the size of the input graph. 
## User Manual
**Installation**\
From command line, run `python -m pip install -r requirements.txt` in the pyfiles directory to acquire necessary libraries.\
**USAGE**\
Run main.py from the command line with arguments for which file to assess, what program to execute (-p for shortest path, -g for subgraph generation and assessement), and two integers.\
Example command, starting in project directory:
```
python pyfiles\main.py data\smalltests.txt -g 3 2
```
For the shortest path, the first integer indicates the start node and the second the end node.\
For the subgraph, the first integer indicates the starting node and the second the intended depth of the subgraph.\
When reading (filename)-(start)-(depth)-apsp.txt a value of -1 indicates a lack of path between the nodes.\
**IMPORTANT**\
Incorrect argument format will result in failure to run.\
Variables **must** follow the format of `(something).txt (-p *or* -g) (int) (int)`\
If the requested starting node is not in the graph when creating a subgraph the subgraph will not be able to be created, so it exits.
Generated CSV files can be found in the same folder as the source data.
## Reflection
Overall, the "centralityassess" algorithm should have a time complexity of O(n^2). This is primarily due to the need to traverse a 2D dictionary with equally long "sides". While dictionaries are well-optimized for look-ups, such optimization is not possible for traversals. Unfortunately, centralityassess is only the most time consuming algorithm I wrote, not the most time consuming algorithm used. That honour goes to the "All Pairs Shortest Path" algorithm, which usually has O(n^3) time complexity. Because of this, the overall time complexity for main.py can be said to be O(n^3), not O(n^2). \
There have been quite a few difficulties in this assignment. One such difficulty was figuring out how to calculate closeness centrality. Originally, I was attempting to calculate using an equation I got from wikipedia that was designed for a different set of cases. Bavelas's equation works well for strongly connected graphs, but less strongly connected graphs run into issues with infinite distances-that is to say, unreachable nodes. After several attempts at calculating centrality using that algorithm, I restarted my research with a greater focus on equations used for cases bearing a stronger resemblance to my own. Eventually, I found an equation that was ideal for my situation: what seems to be the standard algorithm used in the underlying library we were using for the graph: Wasserman and Faust's formula. Using my own implementation of (a slightly modified version of-outgoing instead of incoming) this formula as an algorithm has consistently yielded an accurate assessement of closeness centrality, and so is the one currently in use.\
Another difficulty encountered during this assignment was figuring out how to sync GitHub across both browser edits and desktop edits. While working on the assignment, I would often forget to sync GitHub Desktop with its browser equivalent. This unfortunate habit resulted in many conflicting files and even a few conflicting file structures, requiring me to resolve them. During this time, I found GitHub's stash function to be of great use. It permitted me to sync my project files across platforms without deleting either one of them, instead holding one in escrow until I was able to look at it. This permitted me to manually review the competing edits and copy the desired changes over.\
Yet another troublesome portion of the assignment was found midway through, when I realized I would have to use dictionaries instead of arrays for much of the assignment. I have little to no prior experience with doing anything python's dictionaries, let alone managing ones that were pre-generated by someone elses code. In order to learn how to use them, I set a day or so of time I had allocated to this project aside for research. Eventually, I came to realize that you could iterate through both keys and values using `for key, value in dict.items()`. This easy access to both permitted me to easily store access keys for both sides of a 2D (Technically it was 3D, but the third dimension was an array storing a path and the actual content was mostly irrelevant) dictionary when finding the longest of the shortest paths in the dictionary.\
![Video](https://github.com/csc3430-winter2025/graph-the-gitclub/blob/main/Running%20Graph.mp4)\
The video cannot show the program being executed on web-google.txt due to communication issues and processing power constraints.
## Results
No screenshots of the graph resulting from web-google.txt will be available due to communication issues.\
![image](https://github.com/user-attachments/assets/497fba7c-26d9-4e3c-bb39-36e3f55f3cf9)\
Command line input\
![image](https://github.com/user-attachments/assets/e2207437-c384-48f4-9d22-9515d47d9013)\
Command line output\
![image](https://github.com/user-attachments/assets/e79fd568-fbe3-46df-bd62-a980d755f21d)\
Graph visual output\
![image](https://github.com/user-attachments/assets/e279b19d-4863-45e3-a280-d2237d8e9efc)\
Command line input for finding the shortest path between two points\
![image](https://github.com/user-attachments/assets/454b6e24-8873-4ac6-b5ea-ffc4ed0442e3)\
Command line output for finding the shortest path between two points
