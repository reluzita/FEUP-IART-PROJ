import sys
import os
from library import Library

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