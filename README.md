# Dijkstra's Shortest Path Algorithm is applied to a graph. A self-adjusting hash table stores ‘package’ data. Deliveries are made using nearest neighbor heuristics.
 A graph of edges and vertices is created to model distances between addresses of physical locations, imported from .csv files. Dijkstra's Shortest Path algorithm is used to calculate the shortest route to the next vertex, recalculating after each vertex is visited. The entire application runs in O(n<sup>2</sup>) time complexity, n being the number of graph vertices to visit. This app minimizes distance traveled, offering a solution for a variation of the Traveling Salesman Problem.
 
 ###  *to-do*
1. This code is a first draft, but that's still no excuse for the lack of modularity. Make it modular. 
2. Currently a command line user interface. Make a GUI. 
