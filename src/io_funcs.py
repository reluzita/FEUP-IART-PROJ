import os
import sys

from solution import Solution
from utils import read_libraries, score


def write_output(input_name, solution):
    output_name = "output/" + input_name
    file = open(output_name, "w")

    libraries = []
    for lib in solution.libraries_list:
        if lib not in libraries and lib != -1:
            libraries.append(lib)

    n_libraries = len(libraries)
    file.write(str(n_libraries) + "\n")

    for lib in libraries:
        file.write(str(lib) + " " + str(len(solution.books2lib[lib])) + "\n")
        for book in solution.books2lib[lib]:
            file.write(str(book) + " ")
        file.write("\n")

    file.close()


def read_output(file, libraries, scores, n_days):
    with open(file, 'r', encoding='utf-8') as ifp:
        lines = ifp.readlines()

    n_libraries = int(lines[0])
    libraries_list = []
    books2lib = dict()
    books = set()
    for i in range(n_libraries):
        line = lines[i * 2 + 1].split()
        lib_id = int(line[0])
        for _ in range(libraries[lib_id].signup_days):
            libraries_list.append(lib_id)
        books2lib[lib_id] = [int(x) for x in lines[i * 2 + 2].split()]
        books.update(books2lib[lib_id])
        
    while len(libraries_list) < n_days:
        libraries_list.append(-1)

    return Solution(libraries_list, score(books, scores), books2lib)


def scan_file(file):
    if os.stat(file).st_size == 0:
        print("File is empty!")
        sys.exit()

    with open(file, 'r', encoding='utf-8') as ifp:
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
