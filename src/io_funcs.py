import sys
import os
from library import Library
from utils import read_libraries, score
from solution import Solution



def write_output(inputName, solution):
    outputName = "output/" + inputName
    file = open(outputName, "w")

    libraries = []
    for lib in solution.libraries_list:
        if lib not in libraries and lib != -1:
            libraries.append(lib)

    nLibraries = len(libraries)
    file.write(str(nLibraries) + "\n")

    for lib in libraries:
        file.write(str(lib) + " " + str(len(solution.books2lib[lib])) + "\n")
        for book in solution.books2lib[lib]:
            file.write(str(book) + " ")
        file.write("\n")        

    file.close()

def read_output(file, libraries, scores):
    with open(file, 'r', encoding = 'utf-8') as ifp:
	    lines = ifp.readlines()

    n_libraries = int(lines[0])
    libraries_list = []
    books2lib = dict()
    books = set()
    for i in range(n_libraries):
        line = lines[i*2+1].split()
        lib_id = int(line[0])
        for _ in range(libraries[lib_id].signup_days):
            libraries_list.append(lib_id)
        books2lib[lib_id] = [int(x) for x in lines[i*2+2].split()]
        books.update(books2lib[lib_id])
    
    return Solution(libraries_list, score(books, scores), books2lib)



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
    
    libraries = read_libraries(sections, n_libraries, books)
    
    return n_days, books, libraries



