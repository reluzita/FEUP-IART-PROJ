class Solution:
    def __init__(self, sol, score, elapsed_time, printLibraries):
        self.sol = sol #list of libraries
        self.score = score # final score
        self.elapsed_time = elapsed_time
        self.printLibraries = printLibraries
        self.printSol()
        
    def printSol(self):
        print("\n\n--------------------------")
        print("Solution")
        print("--------------------------")
        
        if self.printLibraries:
            line = "Choosen Libraries: " 
            for b in self.sol: line += str(b) +" "
            print(line)
        print("Score:", self.score)
        print("Elapsed Time:",self.elapsed_time)
        print("\n\n")
           