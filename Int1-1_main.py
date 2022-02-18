from Graph import *
import os
import sys

def main(): 
    print("""\n  
 _____                 _       _   _                           
|  __ \               | |     | | | |                          
| |  \/_ __ __ _ _ __ | |__   | |_| |__   ___  ___  _ __ _   _ 
| | __| '__/ _` | '_ \| '_ \  | __| '_ \ / _ \/ _ \| '__| | | |
| |_\ \ | | (_| | |_) | | | | | |_| | | |  __/ (_) | |  | |_| |
 \____/_|  \__,_| .__/|_| |_|  \__|_| |_|\___|\___/|_|   \__, |
                | |                                       __/ |
                |_|                                      |___/""")

    #Emulating a do... while loop in python
    chooseContinue= "Y"
    while (chooseContinue == 'Y'):
        print("\n\nList of all available graphs 🠗\n")

        #Declaring the graph's folder
        filesArray = sorted(os.listdir('tested_graph'))

        #Initializing first position
        filePosition = 1

        #Printing all files from filesArray (tested_graph directory)
        for file in filesArray:
            print(filePosition, ":",file)
            filePosition += 1

        #Emulating a do... while loop in python + secure INTEGER input
        isInvalid = True
        while isInvalid:
            isInvalid = False
            filePositionChosen = -1

            #Asking the user for the index of the chosen graph
            filePositionChosen = input("\nPlease Select a File (enter its position) : ")

            #If not a number
            if (not filePositionChosen.isnumeric()):
                print("This is not a number !")
                isInvalid = True
            else:
                #If a number, we force it to be an integer
                filePositionChosen = int(filePositionChosen)
                
                #Checking if the number is out of bound of the number of graph
                if (filePositionChosen < 1 or filePositionChosen > len(filesArray)):
                    isInvalid = True
                    print("Your number does not correspond to any file !")
        

        #Reading the chosen graph and displaying it before computation
        chosenGraph = Graph(filesArray[filePositionChosen-1]) #-1 because it starts at 0 and not 1 (as shown to the user for its comfort)
        
        #Display the graph, compute Floyd-Warshall and show the shortest 
        print("\n\nYou have chosen the following graph :")
        chosenGraph.display_graph()
        chosenGraph.floydWarshall()

        #Ask the user if he wants to continue
        chooseContinue = input("\n\n\nDo you want to try another graph ? [Y for yes]")

if __name__ == '__main__':
    main()
