# Dijkstra's Shortest Path Algorithm is applied to a graph. A self-adjusting hash table stores ‘package’ data. Deliveries are made using Nearest Neighbor heuristics.
 A graph of vertices and edges is created to model the distances between addresses of physical locations, imported from .csv files. Dijkstra's Shortest Path algorithm is used to calculate the shortest route to the next address, recalculating after each vertex is visited. The entire application runs in O(n<sup>2</sup>) time complexity, n being the number of 'packages' to deliver. This app minimizes distance traveled, offering a solution for a variation of the Traveling Salesman Problem.
 
This code is a first draft, but no excuse for the lack of modularity. ***to-do***
