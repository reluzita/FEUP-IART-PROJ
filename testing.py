import sys
from library import Library 
from utils import find_best_neighbour, calculate_total_score, choose_best_score
from io_funcs import scan_file, write_output
import datetime
import copy



# List of arguments contains file.py
if __name__ == "__main__":
    n_books, n_libraries, n_days, scores, libraries = scan_file("input/c_incunabula.txt")

    sorted_times = sorted([lib.signup_days for lib in libraries], key=lambda x: x)

    print(sorted_times)
    print(sum(sorted_times))