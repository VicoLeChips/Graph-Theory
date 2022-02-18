"""
This python file contains the class Graph 

Class :
    - Graph : Class that allows to create an oriented and valued graph object and to use 
        its different methods
        
Functions :
    - 
"""

__authors__ = ("BABIN Victor",
               "DEWATRE Pierre",
               "SANDILLON Etienne", 
               "VIEILLEVIGNE Julien")
__date__ = "15/11/2021"

# Library
import string
# Secure importation
try:
    # Data analysis library that allow us to create the adjacency matrices
    import pandas as pd
    import numpy as np
except ImportError:
    np = None
    pd = None
    print('Please import the data analysis library "numpy" and "pandas" with the command : "python -m pip install [name]"')


class Graph:
    """
        A class to represent an oriented and valued graph.


        Attributes
            ----------
            number_V : int 
                number of vertices
            number_E : int
                number of edges
            E : adjacency matrices
                store the edges and their value in a matrices 


        Public Methods
            ----------
            Graph(txt):
                Constructor of a graph
            display_graph()
                Print the adjacency matrices of a graph


        Private Methods
            ----------
            _read_graph_from_txt : Function that creates and returns an adjacency matrice
                by reading a given text file
        """

    def __init__(self, filename):
        """
            Constructs all the necessary attributes for the finite automaton object.

            Parameters
                filename : str
                    filename to open

            Returns : 
                NewGraph : Graph
                    the graph created from the file
        """   
        self.number_V, self.number_E, self.E = self._read_graph_from_txt(filename)

    
    # Displaying the graph info (nbr vertices, nbr edges, adjacency matrices)
    def display_graph(self):
        print("Number of vertices:", self.number_V)
        print("Number of edges:", self.number_E)
        print("\nAdjacency matrices :\n")
        display_matrix(self.E)


    # Main algorithm (Floyd-Warshall)
    def floydWarshall(self):      
        L = [] # Minimum value of all paths from x to y identified so far
        P = [] # Predecessor of y in the path of minimal value from x to y
        for i in range(self.number_V): # For 0 to number_vertices-1
            L.append([]) # Creating a squared matrix (nbr rows) (from the number of vertices)
            P.append([]) # Creating a squared matrix (nbr rows) (from the number of vertices)
            for j in range(self.number_V):
                if self.E[i][j] is None:
                    if i == j: # Fill the diagonal with 0 if None values
                        P[i].append(i)
                        L[i].append(0)
                    else:
                        P[i].append(None)
                        L[i].append(np.inf)
                else:
                    P[i].append(i)
                    if i==j and self.E[i][j]>0: # case when there is an absorbant cycle
                        L[i].append(0)
                    else:
                        L[i].append(self.E[i][j])
        
        x = 0
        # Processing on the basis of "transitive closure on x", performed successively on all vertices
        while(x<self.number_V and not isAbsorbant(L)):
            #Print iteration number
            print("\n-------------------------------\nInteration", x)

            # Display the L matrix (=weight)
            print("\nMatrice L :")
            display_matrix(L)

            # Display the P matrix (=predecessor)
            print("\nMatrice P :")
            display_matrix(P)

            # We take into account all the paths y-x that have been found
            for y in range(self.number_V):
    
                # All paths x-z that have been found are taken into account
                for z in range(self.number_V):
    
                    # To get from y to z, passing through x offers a path of smaller value than what was known before
                    if (L[y][x] + L[x][z] < L[y][z]):
                        L[y][z] = L[y][x] + L[x][z]
                        P[y][z] = P[x][z]
                        
            x += 1 # Incrementing x

        # Printing results
        print("\n-------------------------------\nInteration", x)
        # Display the L matrix (=weight)
        print("\nMatrice L :")
        display_matrix(L) 
        
        # Display the P matrix (=predecessor)
        print("\nMatrice P :")
        display_matrix(P) 

        # Checking if the graph is absorbent
        if isAbsorbant(L):
            print("The algorithm stops at step", x, "due to an absorbent circuit")
        else:
            displayPath(L, P)


    # Reading the file into a graph
    def _read_graph_from_txt(self, filename):
        """
            This function will return the graph parameters from a file.
            It will open the file, read trough it in order to get all the informations,
            then return the information to the right variables.

            Parameters:
                str : filename to open

            Returns : 
                number_V : int 
                    number of vertices
                number_E : int
                    number of edges
                E : double array of int
                    store the edges and their value in a matrix
        """
        # We start by opening the file
        fileGraph = open("tested_graph/" + filename, "r")

        # Read the 2 first lines (number_V (nbr vertices) and number_E (nbr edges))
        # The 'rstrip' method is used to get rid of the '\n' character since it's part of the line that is readed by the 'readLine' method, but we don't want it in the result
        number_V = int(fileGraph.readline().rstrip('\n')) # Number of vertices
        number_E = int(fileGraph.readline().rstrip('\n')) # Number of edges

        # Creating an squared array filled of None (of size number_V)
        E = np.full((number_V, number_V), None)

        # Going through all the lines (=the different edges) of the files and appends it to the adjacency matrix
        for i in range(0, number_E): #For 0 to nbr_edges-1         
            x, y, weight = fileGraph.readline().rstrip('\n').split(' ')  # Reading each line from the given pattern separated with a space (unecessary parameters in the split method, because it's by default with a space, but it's more explicit like this) the different strings
            E[int(x)][int(y)] = int(weight) # Filling the initial adjacency matrix with the weight at the position (init_vertex, final_vertex)
        
        #Returning the number of vertices (number_V), number of edges (number_E) and the adjacency matrix (double array matrix)
        return number_V, number_E, E


#Function to check if a graph is absorbent or not
# Return true if the diagonal contains a negative value (absorbent cycle)
def isAbsorbant(matrix):
    return True in map(lambda x: x < 0, np.diag(matrix))


#Displaying the matrix
def display_matrix(matrix):
    columns = []
    index = []

    # Appending the columns and rows "names" (corresponds to an int from 0 to nbr_vertices-1(=len(matrix)))
    for i in range(len(matrix)): 
        columns.append(i)
        index.append(i)

    # We use dataframe (library pandas) for a better visual understanding when displaying the matrix
    df = pd.DataFrame(matrix, index=index, columns=columns)

    # Checking if the matrix is L (displaying infinite sign) or P (displaying empty cases) and cast the array into int
    for col in range(len(matrix)):
        df[col] = df[col].apply(lambda x: "" if x != x or x == None else("∞" if x == np.inf else int(x)))

    # Printing the matrix
    print(df)


# Function to display the path
def displayPath(L, P):
    Redo = "Y"
    print("\n\nPATHS :")
    while Redo == "Y":

        initial = input("Please give the initial vertex : ")
        #Check if not a number
        while not initial.isnumeric():
            initial = input("This is not a number ! Please give the initial vertex : ")

        final = input("Please give the final vertex : ")
        #Check if not a number
        while not final.isnumeric():
            final = input("This is not a number ! Please give the final vertex : ")

        # Secure input
        initial = int(initial)
        final = int(final)

        predecessor = final
        # Array of all the predecessors (=path)
        path = [predecessor]

        # We use the P matrix to come back until we hit the initial vertex
        while(predecessor != initial):
            predecessor = P[initial][predecessor]
            path.insert(0, predecessor)
            
        print("\nThe shortest path from", initial, "to", final,"is : ", path, "with a cost of", L[initial][final])

        #Ask the user if he wants to continue
        Redo = input("\nDo you want to try anoter path ? [Y for yes]")

    
