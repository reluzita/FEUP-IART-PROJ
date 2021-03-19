import sys
from library import Library 
from solution import Solution
from utils import find_best_neighbour, calculate_total_score, choose_best_score, find_first_neighbour
from io_funcs import scan_file, write_output
import datetime
import copy

def getElapsedTime(t):
    return datetime.datetime.now() - t

def main(argv):
    if len(argv) != 1:
        print("Usage: bookscanning.py <inputfile>")
        sys.exit()
    
    inputfile = argv[0]
        
    n_books, n_libraries, n_days, scores, libraries, printLibraries = scan_file("input/" + inputfile)

    print("\n***", inputfile, "***")
    t = datetime.datetime.now()

    day = 0
    libraries_list = []
    scanned_books_dict = dict()
    scanned_books_set = set()
    all_libraries = copy.deepcopy(libraries)
    while day < n_days and len(all_libraries)>0:
        id = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
        #print(day, "-" , id)
        if id == -1:
            break
        for lib in all_libraries:
            if lib.id == id:
                scanned_books_dict[lib.id] = lib.get_books(n_days-day)
                scanned_books_set.update(scanned_books_dict[lib.id])
                libraries_list.append(lib)
                day += lib.signup_days
                all_libraries.remove(lib)


    print("\n--------------------------")
    print("All done, optimizing now!")
    print("-------------------------- ")

    found_better = True
    while found_better:
        found_better, libraries_list, scanned_books_dict, total_score = find_best_neighbour(libraries_list, scanned_books_dict, libraries, scores, n_days)
   

    total_score = calculate_total_score(scanned_books_dict, scores) 
    solution = Solution(libraries_list, total_score,  getElapsedTime(t).total_seconds(), printLibraries) #prints the solution

    write_output(inputfile, libraries_list, scanned_books_dict)

# List of arguments contains file.py
if __name__ == "__main__":
    main(sys.argv[1:])