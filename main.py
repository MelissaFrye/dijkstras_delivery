import csv


# This class creates a chaining hash table to store all packages. Contains a hash table constructor, with methods to
# add, remove, and search methods. If a collision occurs, the newly added item will be added to the bucket's list (
# chaining) and when a search is performed the bucket will be found and the list iterated through.
# O(n) time complexity (for i in range(initial_buckets)).
class ChainHashTable:
    # hash table constructor, with optional initial capacity, assigns each bucket an empty list. 39 was chosen in this
    # case as the default initial bucket number because that's the number of packages assigned but also accommodates
    # similar and growing business needs for versatility.
    def __init__(self, initial_buckets=39):
        self.table = []
        for i in range(initial_buckets):
            self.table.append([])

    # Inserts new item into hash table by unique key. Value is updated if key found to exist in table already.
    # O(n) time complexity, for kv in bucket_list:, line 24
    def insert(self, key, item):
        # The hash function below calculates which bucket the new item will belong to.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # If key is new, then insert item to the end of bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Search hash table using 'key' as search parameter. If found, the item is returned. If not, None is returned.
    # O(n) time complexity, for kv in bucket_list:
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]  # the value that belongs to the key
        return None  # When key is not found

    # To remove an item with matching key from the table.
    # O(n) time complexity, for kv in bucket_list:, line 52
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])


# This class allows the creation of package objects, each has fields to store package data such as address,
# time of delivery deadline, and special notes.
# O(1) run-time complexity, since one package is created each time init is called, line 61
class Package:
    def __init__(self, p_id, address, city, state, zipcode, deadline, mass_k, note, truck, status, time_mod):
        self.p_id = p_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.mass_k = mass_k
        self.note = note
        self.truck = truck
        self.status = status
        self.time_mod = time_mod

    def __str__(self):  # print data items not reference.
        return "%s | %s | %s | %s | %s | Deadline %s | Kg %s | %s" % (
            self.p_id, self.address, self.city, self.state, self.zipcode, self.deadline, self.mass_k, self.note)

    def __repr__(self):
        return f'Package({self.p_id})'  # ,"{self.address}",{self.status})'


# Takes data from a csv file and reads each row into a new package object.
# O(n) run-time complexity, for package in packageData:, line 87.
def loadPackageData(fileName):
    with open(fileName) as allPackages:
        packageData = csv.reader(allPackages, delimiter=',')
        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline = package[5]
            pMass_k = package[6]
            pNote = package[7]
            pTruck = None
            pStatus = "at the hub"
            pTime = '08:00'

            # Creation of each Package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline, pMass_k, pNote, pTruck, pStatus, pTime)

            # Insert the new Package into table.
            packageHash.insert(pID, p)


# Creating the Hash Table instance
packageHash = ChainHashTable()

# Load packages to Hash Table
loadPackageData('packages.csv')


# Class for creating a Vertex object, to represent an address to visit. Contains constructor for new vertex
# object, initialized with distance infinity and a preceding vertex initialized to None to be used in conjunction
# with Dijkstra's algorithm.
# O(1) since one Vertex is created each time init is called, line 120
class Vertex:
    def __init__(self, label):
        self.label = label
        self.distance = float('inf')
        self.pred_vertex = None

    def __str__(self):  # print the data not references
        return "%s, %f, %s" % (self.label, self.distance, self.pred_vertex)

    def __repr__(self):
        return f'Vertex({self.label})'  # ,"{self.distance}",{self.pred_vertex})'


# Class for creating a graph from a set of Vertices. Contains a dictionary to hold a list of vertices adjacent to
# each vertex, and another dictionary to hold 'edge-weights' which represent distances between vertices.
# O(1) since one Vertex is created each time init is called, line 135.
class Graph:
    def __init__(self):
        self.adjacency_list = {}  # vertex dictionary {key:value}
        self.edge_weights = {}  # edge dictionary {key:value}
        self.vertex_list = []

    # This method adds a Vertex to the Graph by adding it as a key to adjacency_list dict with value
    # initialized to an empty list, and the Vertex is also appended to the vertex_list.
    # O(1) run-time complexity, adding to a dictionary and a list.
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []  # {vertex_1: [], vertex_2: [], ...}
        self.vertex_list.append(new_vertex)

    # This method takes two Vertex objects along with the distance between them and records it in edge_weights.
    # O(n) run-time complexity, if to_vertex not in self.adjacency_list[from_vertex]:, line 152.
    def add_directed_edge(self, from_vertex, to_vertex, distance=1.0):
        self.edge_weights[(from_vertex.label, to_vertex.label)] = distance
        if to_vertex not in self.adjacency_list[from_vertex]:
            self.adjacency_list[from_vertex].append(to_vertex)

    # This method takes two Vertex objects along with the distance between them, calling add_directed_edge twice but
    # switching the to and from vertices, adding both directions with the same distance.
    # O(n) run-time complexity, since add_directed_edge is called twice.
    def add_undirected_edge(self, vertex_a, vertex_b, distance=1.0):
        # these two directed edges together make up the undirected edge
        self.add_directed_edge(vertex_a, vertex_b, distance)
        self.add_directed_edge(vertex_b, vertex_a, distance)

    def __str__(self):  # print the data not references
        return "%s, %s" % (self.adjacency_list, self.edge_weights)


#  Creating a Graph instance
g = Graph()

#  Blank list to conveniently hold distances from csv file, to be used in the creation of Vertices
distances = []


# This method reads each row from csv file and appends to distances list, creates a Vertex using its index in the list
# as the label, which is added to the graph. Then for each vertex, the vertex list is iterated through to get each
# combination for the add_undirected_edge method and using the distances from the list just created.
# O(n^2) run-time complexity, for vert_a in g.vertex_list: for vert_b in g.vertex_list:, lines 189 and 190.
def loadDistanceData(fileName):
    with open(fileName) as allDistances:
        distanceData = csv.reader(allDistances, delimiter=',')

        for distance in distanceData:
            distances.append(distance)

        for d in distances:
            d = Vertex(distances.index(d))
            g.add_vertex(d)

    for vert_a in g.vertex_list:
        for vert_b in g.vertex_list:
            g.add_undirected_edge(vert_a, vert_b, float(distances[vert_a.label][vert_b.label]))


loadDistanceData('distance.csv')


# Dijkstra's Shortest Path Algorithm to find how to deliver based on distances and addresses to visit.
# O(n) run-time complexity, iterating through the vertex_list or adjacency_list or len(unvisited_q).
def dijkstras_short(g, start_vertex):
    for tex in g.vertex_list:
        tex.distance = float('inf')
        tex.pred_vertex = None

    # All vertices appended to unvisited_q list, by iterating through g.adjacency_list.
    unvisited_q = []
    for current_vertex in g.adjacency_list:
        unvisited_q.append(current_vertex)

    # start_vertex has a distance of 0 from itself
    start_vertex.distance = 0

    # one vertex is removed with each iteration; repeat until the list is empty.
    while len(unvisited_q) > 0:

        # Visit vertex with min distance from the start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_q)):
            if unvisited_q[i].distance < unvisited_q[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_q.pop(smallest_index)

        # check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in g.adjacency_list[current_vertex]:  # values from dictionary
            edge_weight = g.edge_weights[(current_vertex.label, adj_vertex.label)]  # values from dictionary
            alternative_path_distance = current_vertex.distance + edge_weight

            # if shorter path from start_vertex to adj_vertex is found, update
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex.label


# This method builds a shortest path starting with end_vertex, using the Vertex attribute pred_vertex to find the path
# back to start_vertex. The path is returned.
# O(n) run-time complexity, depending on how many vertices are between start_vertex and end-vertex.
def get_shortest_path(start_vertex, end_vertex):
    path = ""
    current_v = end_vertex
    while current_v is not start_vertex:
        path = " -> " + str(current_v.label) + path
        current_v = g.vertex_list[current_v.pred_vertex]
    path = str(start_vertex.label) + path
    # print("path", path)
    return path


# calling Dijkstra's Shortest Path with starting Vertex(0), which is the WGUPS hub.
dijkstras_short(g, g.vertex_list[0])


# This method accepts a Truck object containing a list of packages to deliver, and returns the number of miles for a
# round-trip to complete all deliveries.Question about run-time....is addresses n (I think this is yes)? ...is
# verts_to_visit n (I think this is NO)?  since the list doesn't change over this particular program.
# O(n^2) run-time complexity, 1st time: for i in truck.loaded_packages_list: for a in addresses (lines 260/ 276),
# 2nd time: for ve in verts_to_visit:get_shortest_path(nxt_vert, ve) (lines 295, 303).
def get_best_route(truck):
    # verts_to_visit list will be made from the package addresses.
    global return_dist
    verts_to_visit = []
    # for every package on the Truck:
    for i in truck.loaded_packages_list:  # O(n)
        # change package status from "at hub" to "en route". *I don't think this has much effect and could be removed*
        i.status = "en route"
        # set the Truck number as a package attribute for later use in displaying results.
        if truck == my_Truck1:
            i.truck = 1
        elif truck == my_Truck1_a:
            i.truck = 4
        elif truck == my_Truck2:
            i.truck = 2
        elif truck == my_Truck2_a:
            i.truck = 3
        else:
            i.truck = "unknown"

        # for each address, a, in the addresses list,
        for a in addresses:
            # if the package (i) address matches the address, a, then variable, vert_dex, is assigned with the index of
            # a in the addresses list.
            if i.address == a:
                vert_dex = addresses.index(a)
                # if vert_dex, representing a Vertex, is not already in the verts_to visit list then append it.
                # ******** does this make it O(n^3?)
                if vert_dex not in verts_to_visit:
                    verts_to_visit.append(vert_dex)
                    # print("Package ID:", i.p_id, "to be delivered to:", addresses[vert_dex], "by:, ", i.deadline)
                    break
    # initialize nxt_vert to Vertex(0), since the Truck's journey begins at the hub, and total_distance to 0.
    nxt_vert = g.vertex_list[0]
    total_distance = 0
    # while verts_to_visit is not empty:
    while len(verts_to_visit) > 0:
        # smlst_dist is initialized to an arbitrary high number.
        smlst_dist = 50
        this_ve = ''

        # for each vertex in verts_to_visit:
        for ve in verts_to_visit:
            # get the Vertex object.
            ve = g.vertex_list[ve]
            # path may not exist if....
            if ve.pred_vertex is None and ve is not nxt_vert:
                print(nxt_vert, " to %s ==> no path exists" % ve.label)
            # get_shortest_path is called with nxt_vert as start_vertex and ve as end_vertex.
            else:
                get_shortest_path(nxt_vert, ve)
                # print(nxt_vert.label, "to %s ==> %s (total distance: %g)" % (
                # ve.label, get_shortest_path(nxt_vert, ve), ve.distance))

            # keep track of smallest distance from start. ve.distance represents distance from start_vertex to ve.
            if ve.distance < smlst_dist:
                smlst_dist = ve.distance
                # assign this_ve with ve, for some reason? (maybe don't need this)
                this_ve = ve

        # once all verts_to_visit have been visited add the smallest distance to running total.
        total_distance = total_distance + smlst_dist

        # find total minutes.
        total_minutes = (total_distance / 18) * 60
        # This for loop checks each package loaded to see if it belongs at present address, since multiple packages may
        # be going to the same address.
        for pack in truck.loaded_packages_list:
            # if addresses match, mark package as 'Delivered' and with time and distance.
            if pack.address == addresses[this_ve.label]:
                pack.status = 'Delivered'
                pack.time_mod = get_time(total_minutes, truck)

                # add a message to the truck.
        truck.message[get_time(total_minutes, truck)] = total_distance
        # nxt_vert is now assigned with the vertex found to have the shortest distance from present vertex. It is the
        # vertex to be visited next, popped from the verts_to_visit list and will be used as the starting vertex next
        # time dijkstras_short is called.
        nxt_vert = verts_to_visit.pop(verts_to_visit.index(this_ve.label))
        # if all the vertices have been popped from vert_to_vist, then call dijkstras_short for the last vertex to get
        # the shortest path back to Vertex(0), return trip to the hub.
        if len(verts_to_visit) == 0:
            dijkstras_short(g, g.vertex_list[nxt_vert])
            get_shortest_path(g.vertex_list[nxt_vert], g.vertex_list[0])
            return_dist = g.vertex_list[0].distance
            # print("total return trip distance: ", return_dist, ". Minutes:", (return_dist / 18) * 60)
            dijkstras_short(g, g.vertex_list[0])
        # else there are still more vertices in the list verts_to_visit. Call dijkstras_short, same as in if branch,
        # *****maybe we don't need this inside the if-else, above instead*****
        else:
            dijkstras_short(g, g.vertex_list[nxt_vert])
        # nxt_vert gets reassigned with the actual Vertex object instead of the int that it was.
        nxt_vert = g.vertex_list[nxt_vert]
        # print("next Address:", addresses[nxt_vert.label])
    # keeps track of all distance
    new_total_of_all_distance = total_distance + return_dist
    # return the sum of the path and the return trip.
    return new_total_of_all_distance


# This Truck class holds a list of loaded packages, a truck_id, and a message about distance.
# O(1), since once Truck instance is created each time init is called.
class Truck:
    def __init__(self, truck_id, load_id):
        # self.message = []  # list of "message here"
        self.message = {}  # list of "message here"

        if truck_id == 1 or 2:
            self.truck_id = truck_id
        else:
            print("Truck ", truck_id, " is not in service today.")

        self.loaded_packages_list = []
        self.load_id = load_id

        if load_id == 1:
            # First load for Truck 1
            self.loaded_packages_list = [packageHash.search(13), packageHash.search(14), packageHash.search(15),
                                         packageHash.search(16), packageHash.search(19), packageHash.search(20),
                                         packageHash.search(21), packageHash.search(27), packageHash.search(34),
                                         packageHash.search(35), packageHash.search(39)]
        elif load_id == 2:
            # First load for Truck 2
            self.loaded_packages_list = [packageHash.search(1), packageHash.search(5), packageHash.search(8),
                                         packageHash.search(29), packageHash.search(30), packageHash.search(31),
                                         packageHash.search(37), packageHash.search(38), packageHash.search(40)]
        elif load_id == 3:
            # Second Load for Truck 2
            self.loaded_packages_list = [packageHash.search(3), packageHash.search(6), packageHash.search(9),
                                         packageHash.search(10), packageHash.search(11), packageHash.search(18),
                                         packageHash.search(23), packageHash.search(25), packageHash.search(32),
                                         packageHash.search(36)]
        elif load_id == 4:
            # Second Load for Truck 1
            self.loaded_packages_list = [packageHash.search(2), packageHash.search(4), packageHash.search(7),
                                         packageHash.search(12), packageHash.search(17), packageHash.search(22),
                                         packageHash.search(26), packageHash.search(24), packageHash.search(28),
                                         packageHash.search(33)]
        else:
            print("error not a valid package list ID number")

    def __repr__(self):
        return f'Truck({self.truck_id})'  # ,"{self.load_id}",{self.loaded_packages_list})'


# creating Truck instances.
my_Truck2 = Truck(2, 2)
my_Truck2_a = Truck(2, 3)
my_Truck1_a = Truck(1, 4)
my_Truck1 = Truck(1, 1)

addresses = []  # address list


# This method reads the addresses from a csv file into the addresses list.
# O(n) run-time complexity, depending on the number of rows in the csv file.
def loadAddressData(fileName):
    with open(fileName) as allAddresses:
        addressData = csv.reader(allAddresses, delimiter=',')
        for addrezz in addressData:
            addresses.append(str(addrezz)[2:-2])


# loading addresses.csv into the program.
loadAddressData('addresses.csv')


# This method accepts a number of minutes and truck number, then based on the start time of 08:00, returns a formatted
# time of day. If minutes > 60, 60 minutes are subtracted and 1 added to hour.
# O(n) run-time complexity since, while minutes >= 60: (lines 433, 442, 452) as written, minutes could be any number
def get_time(minutes, truck):
    hour = 8
    my_time = '00:00'
    if (truck == my_Truck1) or (truck == my_Truck2):
        if minutes < 60:
            my_time = '{:02d}:{:02d}'.format(hour, int(minutes))
        while minutes >= 60:
            minutes = minutes - 60
            hour = hour + 1
        my_time = '{:02d}:{:02d}'.format(hour, int(minutes))
    if truck == my_Truck1_a:
        minutes = (((truck1_total_distance / 18) * 60) + minutes)
        if minutes < 60:
            my_time = '{:02d}:{:02d}'.format(hour, int(minutes))
        else:
            while minutes >= 60:
                minutes = minutes - 60
                hour = hour + 1
        my_time = '{:02d}:{:02d}'.format(hour, int(minutes))

    if truck == my_Truck2_a:
        minutes = (((truck2_total_distance / 18) * 60) + minutes)
        if minutes < 60:
            my_time = '{:02d}:{:02d}'.format(hour, int(minutes))
        else:
            while minutes >= 60:
                minutes = int(minutes - 60)
                hour = int(hour + 1)
        my_time = '{:02d}:{:02d}'.format(hour, int(minutes))
    return my_time


truck1_total_distance = get_best_route(my_Truck1)
truck2_total_distance = get_best_route(my_Truck2)
truck1_trip2_total_distance = get_best_route(my_Truck1_a)
truck2_trip2_total_distance = get_best_route(my_Truck2_a)
print("\n                                                           --------------------------------")
print("                                                            WGUPS Package Delivery Service   ")
print("                                                          ----------------------------------")


'''print("Truck 1_a returns to the hub, All Packages Delivered, at " + get_time(((truck1_trip2_total_distance / 18) * 60),
                                                                             my_Truck1_a))
print("Truck 2_a returns to the hub, All Packages Delivered, at " + get_time(((truck2_trip2_total_distance / 18) * 60),
                                                                             my_Truck2_a))'''


# This method accepts a usertime and prints the status of all packages.
# **** THIS WOULD NEED TO BE rewritten/or table initial_buckets increased?? if more packages were added to the table****
# What happens when more packages are added????
# O(1) run-time complexity, since the packageHash table length is iterated through but it is a constant, 39 ??????
def search_allpackages_by_usertime(usertime):
    h_m = usertime.split(':')
    uhour = h_m[0]
    uminute = h_m[1]
    if int(uhour) < 8:
        print("Business hours begin at 08:00, please enter a later time.")
    else:
        print('\n                                              ************************STATUS  OF ALL PACKAGES AT',
              usertime, '************************')
        for yuh in range(1, len(packageHash.table) + 2):
            p_m = (packageHash.search(yuh)).time_mod.split(':')
            phour = p_m[0]
            pminute = p_m[1]
            if packageHash.search(yuh).truck == 3:
                #  MUST change if any of the packages switch trucks, maybe can code in the time
                if int(uhour) < 9 or (int(uhour) == 9 and int(uminute) < 20):
                    print("Package", packageHash.search(yuh), "| STATUS: at hub | scheduled departure 09:20")
                    continue
            elif packageHash.search(yuh).truck == 4:
                #  MUST change if any of the packages switch trucks, maybe can code in the time
                if int(uhour) < 9 or (int(uhour) == 9 and int(uminute) < 26):
                    print("Package", packageHash.search(yuh), "| STATUS: at hub | scheduled departure 09:26")
                    continue

            if int(uhour) < int(phour):
                print("Package", packageHash.search(yuh), "| STATUS: en route | est. delivery time:",
                      packageHash.search(yuh).time_mod)
            elif int(uhour) == int(phour):
                if int(uminute) < int(pminute):
                    print("Package", packageHash.search(yuh), "| STATUS: en route | est. delivery time:",
                          packageHash.search(yuh).time_mod)
                elif int(uminute) >= int(pminute):
                    print("Package", packageHash.search(yuh), "| STATUS:", packageHash.search(yuh).status, "|",
                          packageHash.search(yuh).time_mod)
            elif int(uhour) > int(phour):
                print("Package", packageHash.search(yuh), "| STATUS:", packageHash.search(yuh).status, "|",
                      packageHash.search(yuh).time_mod)


# This method accepts a time and a package ID and prints the status of the package at that time.
# O(n) run-time complexity, because packageHash.search was called, which is O(n).
def search_a_package_by_usertime(usertime, p_id):
    pkg = packageHash.search(p_id)
    h_m = usertime.split(':')
    uhour = h_m[0]
    uminute = h_m[1]
    if int(uhour) < 8:
        print("Business hours begin at 08:00, please enter a later time.")
    else:
        print('\n                                              ************************STATUS OF PACKAGE', p_id, 'AT',
              usertime, '************************')
        p_m = pkg.time_mod.split(':')
        phour = p_m[0]
        pminute = p_m[1]
        if pkg.truck == 3 and (int(uhour) < 9 or (int(uhour) == 9 and int(uminute) < 20)):
            #  MUST change if any of the packages switch trucks, maybe can code in a time variable
            print("Package", pkg, "| STATUS: at hub | scheduled departure 09:20")

        elif pkg.truck == 4 and int(uhour) < 9 or (int(uhour) == 9 and int(uminute) < 26):
            #  MUST change if any of the packages switch trucks, maybe can code in a time variable
            print("Package", pkg, "| STATUS: at hub | scheduled departure 09:26")

        elif int(uhour) < int(phour):  # elif from if
            print("Package", pkg, "| STATUS: en route  | est. delivery time:", pkg.time_mod)
        elif int(uhour) == int(phour):
            if int(uminute) < int(pminute):
                print("Package", pkg, "| STATUS: en route  | est. delivery time:", pkg.time_mod)
            elif int(uminute) >= int(pminute):
                print("Package", pkg, "| STATUS: ", pkg.status, "|", pkg.time_mod)
        elif int(uhour) > int(phour):
            print("Package", pkg, "| STATUS: ", pkg.status, "|", pkg.time_mod)


# print(search_a_package_by_usertime('9:45', 13))


def search_a_truck_by_time(usertime, truck):  # user can choose truck 1 or 2, but will run twice with 3 or 4 used the
    # second time. where is the truck at the given time, and what is the status of its packages?  we'll go thru the
    # list of packages on the truck and their delivered times then compare to query time
    # other method to search for any attribute of the package: first do write a method where the search parameter of the
    # package is found and get those package id's, then use the existing search package by pid.
    h_m = usertime.split(':')
    uhour = int(h_m[0])
    uminute = int(h_m[1])
    umin_ttl = 0
    trk = ''
    th_uhour = 0
    if uhour < 8:
        print("Business hours begin at 08:00.")
    elif uhour == 8:
        umin_ttl = uminute
    else:
        th_uhour = uhour
        while th_uhour > 8:
            umin_ttl = umin_ttl + 60
            th_uhour = th_uhour - 1
        umin_ttl = umin_ttl + uminute

    miles_trav = 0
    if truck == 1:
        trk = my_Truck1
        # usertime - truck's starttime(08:00) = ((number of minutes since truck left hub/60)*18)
        truck1_max_mins = (truck1_total_distance / 18) * 60
        if uhour < 8:
            print("Zero miles traveled.")
        elif umin_ttl < truck1_max_mins:
            miles_trav = (umin_ttl / 60) * 18
            # print('{:.2f}'.format(miles_trav))
            print("                                                  ------- Status of Truck", truck, "at",
                  usertime, '---',
                  '{:.2f}'.format(miles_trav),
                  "miles traveled, first trip-------\n")
        else:
            print("                                                  ------- Status of Truck", truck, "at",
                  usertime, '---',
                  '{:.2f}'.format(truck1_total_distance),
                  "miles traveled, first trip-------\n")

    elif truck == 2:
        trk = my_Truck2
        # usertime - truck's starttime(08:00) = ((number of minutes since truck left hub/60)*18)
        truck2_max_mins = (truck2_trip2_total_distance / 18) * 60
        if uhour < 8:
            print("Zero miles traveled.")
        elif umin_ttl < truck2_max_mins:
            miles_trav = (umin_ttl / 60) * 18
            # print('{:.2f}'.format(miles_trav))
            print("\n                                                  ------- Status of Truck", truck, "at",
                  usertime, '---',
                  '{:.2f}'.format(miles_trav),
                  " miles traveled, first trip-------\n")
        else:
            print("\n                                                  ------- Status of Truck", truck, "at",
                  usertime, '---',
                  '{:.2f}'.format(truck2_trip2_total_distance),
                  " miles traveled, first trip-------\n")

    elif truck == 4:  # truck1 2nd trip
        trk = my_Truck1_a
        truck4_min_mins = (truck1_total_distance / 18) * 60
        truck4_max_mins = ((truck1_trip2_total_distance + truck1_total_distance) / 18) * 60
        # case when usertime is less than truck4 start
        if umin_ttl < truck4_min_mins:
            search_a_truck_by_time(usertime, 1)
        # case when usertime is >= truck 4 start
        elif truck4_min_mins <= umin_ttl <= truck4_max_mins:
            search_a_truck_by_time(usertime, 1)
            miles_trav = ((umin_ttl - truck4_min_mins) / 60) * 18
            # print('{:.2f}'.format(miles_trav))
            print("\n                                                  ------- Status of Truck #1, Second Run, at",
                  usertime, '---',
                  '{:.2f}'.format(miles_trav + truck1_total_distance),
                  "total miles traveled by Truck #1-------\n")
        else:
            search_a_truck_by_time(usertime, 1)
            print("\n                                                  ------- Status of Truck #1, Second Run, at",
                  usertime, '---',
                  '{:.2f}'.format(truck1_trip2_total_distance + truck1_total_distance),
                  "total miles traveled by Truck #1-------\n")

    elif truck == 3:
        trk = my_Truck2_a  # truck 2 2nd trip
        truck3_min_mins = (truck2_total_distance / 18) * 60
        truck3_max_mins = ((truck2_trip2_total_distance + truck2_total_distance) / 18) * 60
        # case when usertime is less than truck4 start
        if umin_ttl < truck3_min_mins:
            search_a_truck_by_time(usertime, 2)
        # case when usertime is >= truck 4 start
        elif truck3_min_mins <= umin_ttl <= truck3_max_mins:
            search_a_truck_by_time(usertime, 2)
            miles_trav = ((umin_ttl - truck3_min_mins) / 60) * 18
            # print('{:.2f}'.format(miles_trav))
            print("\n                                                  ------- Status of Truck #2, Load 2, at",
                  usertime, '---',
                  '{:.2f}'.format(miles_trav + truck2_total_distance),
                  "total miles traveled by Truck #2-------\n")
        else:
            search_a_truck_by_time(usertime, 2)
            print("\n                                                  ------- Status of Truck #2, Load 2, at",
                  usertime, '---',
                  '{:.2f}'.format(truck2_trip2_total_distance + truck2_total_distance),
                  "total miles traveled by Truck #2-------\n")

    # normal printing of packages
    if int(uhour) < 8:
        print("Business hours begin at 08:00, please enter a later time.")
    else:
        # to do: print miles traveled at user time
        # print(trk.message)
        for pkg in trk.loaded_packages_list:
            p_m = pkg.time_mod.split(':')
            phour = p_m[0]
            pminute = p_m[1]
            if pkg.truck == 3:
                if int(uhour) < 9 or (int(uhour) == 9 and int(uminute) < 20):
                    #  MUST change if any of the packages switch trucks, maybe can code in the time
                    print("Package", pkg, "| at hub | scheduled departure 09:20")
                    continue
            elif pkg.truck == 4:
                if int(uhour) < 9 or (int(uhour) == 9 and int(uminute) < 26):
                    #  MUST change if any of the packages switch trucks, maybe can code in the time
                    print("Package", pkg, "| at hub | scheduled departure 09:26")
                    continue

            if int(uhour) < int(phour):
                print("Package", pkg, "| en route  | est. delivery time:", pkg.time_mod)
            elif int(uhour) == int(phour):
                if int(uminute) < int(pminute):
                    print("Package", pkg, "| en route  | est. delivery time:", pkg.time_mod)

                elif int(uminute) >= int(pminute):
                    print("Package", pkg, "|", pkg.status, "|", pkg.time_mod)
            elif int(uhour) > int(phour):
                print("Package", pkg, "|", pkg.status, "|", pkg.time_mod)


user_selection = input("Please make a selection by typing the number and then Enter. \nFor package information: "
                       "1\nFor truck information: 2\nTo quit: 3\nYour Selection:")
if user_selection == '1':
    pak_select = input("Please make a selection by typing the number and then Enter. \nFor all packages: "
                       "1\nFor a single package: 2\nTo quit: 3\nYour Selection:")
    if pak_select == '1':
        tyme = input('To search status of all Packages, enter a time in the form HH:MM')
        while tyme == '':
            tyme = input('Enter a valid time HH:MM')
        search_allpackages_by_usertime(tyme)
    elif pak_select == '2':
        tyme = input('Enter a time in the form HH:MM')
        while tyme == '':
            tyme = input('Enter a valid time HH:MM')
        pak_id = input('To search a specific package, enter the Package ID')
        while pak_id == '':
            pak_id = input('To search a specific package, enter the Package ID')
        while int(pak_id) > 40:
            pak_id = input("try again, 40 packages today")
        search_a_package_by_usertime(tyme, int(pak_id))
    elif pak_select == '3':
        exit()
    else:
        print("invalid selection")

elif user_selection == '2':
    trk_select = input("Please make a selection by typing the number and then Enter. \nFor all trucks: "
                       "1\nFor a single truck: 2\nTo quit: 3\nYour Selection:")
    if trk_select == '1':
        tyme = input("To search all trucks by a time, please enter a time in the form HH:MM")
        search_a_truck_by_time(tyme, 4)
        search_a_truck_by_time(tyme, 3)
    elif trk_select == '2':
        tyme = input("To search a specific truck by a time, please enter a time in the form HH:MM")
        truk_id = input('Choose a truck:\n 4:  Truck #1 \n 3:  Truck #2 ')
        search_a_truck_by_time(tyme, int(truk_id))
    elif trk_select == '3':
        exit()
    else:
        print("invalid selection")
elif user_selection == '3':
    exit()
else:
    print("Invalid Selection, choose again")

form_trk1 = "{:.2f}".format(truck1_total_distance + truck1_trip2_total_distance)
form_trk2 = "{:.2f}".format(truck2_total_distance + truck2_trip2_total_distance)

total_mega_dist = truck1_total_distance + truck1_trip2_total_distance + truck2_total_distance + truck2_trip2_total_distance
total_mega_dist = "{:.2f}".format(total_mega_dist)
print("\n\n                                                 **************************************************")
print("                                                 **   All Deliveries Completed in", total_mega_dist,
      "Miles   **")
print("                                                 **************************************************\n")

print("Truck #1 miles traveled:", form_trk1,
      "  |  departed the hub at 08:00  |  reloaded at " + get_time(((truck1_total_distance / 18) * 60), my_Truck1),
      " |  all packages delivered, Truck #1 returned to the hub at " + get_time(
          ((truck1_trip2_total_distance / 18) * 60),
          my_Truck1_a))
print("Truck #2 miles traveled:", form_trk2,
      "  |  departed the hub at 08:00  |  reloaded at " + get_time(((truck2_total_distance / 18) * 60), my_Truck1),
      " |  all packages delivered, Truck #2 returned to the hub at " + get_time(
          ((truck2_trip2_total_distance / 18) * 60),
          my_Truck2_a))

