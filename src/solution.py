import functools

class Solution:
    def __init__(self, libraries_list, score:int, books2lib:dict):
        self.libraries_list = libraries_list #list of libraries
        self.score = score # final score
        self.books2lib = books2lib
        
    def printSol(self, printLibraries, elapsed_time):
        print("\n\n--------------------------")
        print("Solution")
        print("--------------------------")
        
        if printLibraries:
            line = "Choosen Libraries: " 
            for b in self.libraries_list: line += str(b) +" "
            print(line)
        print("Score: ", self.score)
        print("Elapsed Time: ",elapsed_time)
        print("\n\n")

    def __eq__(self, obj):
        return self.score == obj.score and functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q, self.libraries_list ,obj.libraries_list), True)

    def __str__(self):
        return self.books2lib
           