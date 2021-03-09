import sys
from library import Library
from funcs import choose_best_score
from io_funcs import scan_file, write_output

def main(argv):
    if len(argv) != 1:
        print("Usage: bookscanning.py <inputfile>")
        sys.exit()
    
    inputfile = argv[0]
        
    n_books, n_libraries, n_days, books, libraries = scan_file("input/" + inputfile)

    day = 0
    libraries_list = []
    while day < n_days and len(libraries)>0:
        id = choose_best_score(n_days - day, libraries, books)
        for lib in libraries:
            if lib.id == id:
                lib.send_books(n_days - day, books)
                libraries_list.append(lib)
                day += lib.signup_days
                libraries.remove(lib)
    
    write_output(inputfile, libraries_list)

# List of arguments contains file.py
if __name__ == "__main__":
    main(sys.argv[1:])