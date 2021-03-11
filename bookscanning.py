import sys
from library import Library
from funcs import choose_best_score
from io_funcs import scan_file, write_output
import datetime

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
    total_score = 0
    while day < n_days and len(libraries)>0:
        id, score = choose_best_score(n_days - day, libraries, scores)
        total_score += score
        for lib in libraries:
            if lib.id == id:
                lib.send_books(n_days - day)
                libraries_list.append(lib)
                day += lib.signup_days
                libraries.remove(lib)

    elapsed_time = datetime.datetime.now() - t
    print("Elapsed Time:", elapsed_time.total_seconds())
    print("Total score: ", total_score)

    write_output(inputfile, libraries_list)

# List of arguments contains file.py
if __name__ == "__main__":
    main(sys.argv[1:])