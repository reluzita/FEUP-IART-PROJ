import sys
import os

class Library:
    def __init__(self, id, books, signup_days, books_per_day):
        self.id = id
        self.books = books
        self.signup_days = signup_days
        self.books_per_day = books_per_day


def scan_file(file):
    if os.stat(file).st_size == 0:
        print("File is empty!")
        sys.exit()
    
    with open(file, 'r', encoding = 'utf-8') as ifp:
	    lines = ifp.readlines()

    if (len(lines) % 2) != 0:
        print("Input file has incomplete information!")
        sys.exit()

    first_line = lines[0]

    general_info = first_line.split()

    n_books = int(general_info[0])
    n_libraries = int(general_info[1])
    n_days = int(general_info[2])

    scores = lines[1].split()
    books = dict()
    for i in range(n_books):
        books[i] = scores[i]
    sections = lines[1:]
    
    libraries = read_libraries(sections, n_libraries)
    
    return n_books, n_libraries, n_days, books, libraries
        
def read_libraries(lines, n_libraries):
    libraries = []
    for i in range(0, n_libraries):
        info = lines[i*2].split()
        books = [int(n) for n in lines[i*2+1].split()]
        libraries.append(Library(i, books, int(info[1]), int(info[2])))
        
    return libraries

def main(argv):
    if len(argv) != 1:
        print("Usage: bookscanning.py <inputfile>")
        sys.exit()
    n_books, n_libraries, n_days, books, libraries = scan_file("input/" + argv[0])
    print(n_books)
    print(n_libraries)
    print(n_days)
    print(books)
    for lib in libraries:
        print(lib)
    

# List of arguments contains file.py
if __name__ == "__main__":
    main(sys.argv[1:])