import sys
import os

class Library:
    def __init__(self, id, books, signup_days, books_per_day):
        self.id = id
        self.books = books
        self.signup_days = signup_days
        self.books_per_day = books_per_day
        self.scannedBooks = []

    def get_score(self, days, scores):
        remaining = days - self.signup_days
        n_books = self.books_per_day * remaining
        ordered_books = sorted(self.books, key=lambda x: scores[x], reverse=True)
        return score(ordered_books[:n_books],scores)

    def send_books(self, days, scores):
        remaining = days - self.signup_days
        n_books = self.books_per_day * remaining
        self.scannedBooks = sorted(self.books, key=lambda x: scores[x], reverse=True)[:n_books]
    
    
def score(books, scores):
    return sum([scores[b] for b in books])
    

def write_output(inputName, libraries):
    outputName = "output/" + inputName
    file = open(outputName, "w")

    nLibraries = len(libraries)
    file.write(str(nLibraries) + "\n")

    for lib in libraries:
        file.write(str(lib.id) + " " + str(len(lib.scannedBooks)) + "\n")
        for book in lib.scannedBooks:
            file.write(str(book) + " ")
        file.write("\n")        

    file.close()


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
        books[i] = int(scores[i])
    sections = lines[2:]
    
    libraries = read_libraries(sections, n_libraries)
    
    return n_books, n_libraries, n_days, books, libraries



def read_libraries(lines, n_libraries):
    libraries = []
    for i in range(0, n_libraries):
        info = lines[i*2].split()
        books = [int(n) for n in lines[i*2+1].split()]
        libraries.append(Library(i, books, int(info[1]), int(info[2])))
        
    return libraries



def choose_best_score(days, libraries, books):
    scores = dict()
    for library in libraries:
        scores[library.id] = library.get_score(days, books)
        print(library.get_score(days, books))
    print(scores)
    maximum = max(scores.values())

    return list(scores.keys())[list(scores.values()).index(maximum)]

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