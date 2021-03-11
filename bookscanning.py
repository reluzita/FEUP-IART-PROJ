import sys
from library import Library 
from utils import choose_best_score, score, find_better_neighbour
from io_funcs import scan_file, write_output
import datetime
import copy

def main(argv):
    if len(argv) != 1:
        print("Usage: bookscanning.py <inputfile>")
        sys.exit()
    
    inputfile = argv[0]
        
    n_books, n_libraries, n_days, scores, libraries = scan_file("input/" + inputfile)

    print("***", inputfile, "***")
    t = datetime.datetime.now()

    day = 0
    libraries_list = []
    scanned_books_dict = dict()
    all_libraries = copy.deepcopy(libraries)
    while day < n_days and len(all_libraries)>0:
        id = choose_best_score(n_days - day, all_libraries, scores)
        for lib in all_libraries:
            if lib.id == id:
                scanned_books_dict[lib.id] = lib.get_books(n_days-day)
                libraries_list.append(lib)
                day += lib.signup_days
                all_libraries.remove(lib)

    found_better = True
    while found_better:
        found_better, libraries_list, scanned_books_dict, total_score = find_better_neighbour(libraries_list, scanned_books_dict, libraries, scores, n_days)
   
    
    elapsed_time = datetime.datetime.now() - t
    print("Elapsed Time:", elapsed_time.total_seconds())
    print("Total score: ", total_score)

    write_output(inputfile, libraries_list, scanned_books_dict)

# List of arguments contains file.py
if __name__ == "__main__":
    main(sys.argv[1:])