from library import Library
import copy

def score(books, scores):
    return sum([scores[b] for b in books])

def choose_best_score(days, libraries, scores):
    lib_scores = dict()
    for library in libraries:
        lib_scores[library.id] = score(library.get_books(days), scores)/library.signup_days
    maximum = max(lib_scores.values())

    return list(lib_scores.keys())[list(lib_scores.values()).index(maximum)]


def read_libraries(lines, n_libraries, scores):
    libraries = []
    for i in range(0, n_libraries):
        info = lines[i*2].split()
        books = sorted([int(n) for n in lines[i*2+1].split()], key=lambda x: scores[x], reverse=True)
        libraries.append(Library(i, books, int(info[1]), int(info[2])))
        
    return libraries

def calculate_total_score(books_dict, scores):
    total_score = 0
    for id in books_dict:
        total_score += score(books_dict[id], scores)
    return total_score

def find_better_neighbour(choosen_libraries, choosen_books, libraries, scores, n_days):
    found_score = calculate_total_score(choosen_books, scores) 
    ordered_libs = sorted(choosen_libraries, key=lambda x: x.signup_days)
    longest_time_lib = ordered_libs[0]

    day = 0
    new_list = []
    scanned_books_dict = dict()
    all_libraries = copy.deepcopy(libraries)
    for lib in choosen_libraries:
        if lib == longest_time_lib:
            all_libraries.remove(lib)
            break
        else:
            new_list.append(lib)
            scanned_books_dict[lib.id] = lib.get_books(n_days-day)
            all_libraries.remove(lib)
            day += lib.signup_days

    
    while day < n_days and len(all_libraries) > 0:
        id = choose_best_score(n_days - day, all_libraries, scores)
        for lib in all_libraries:
            if lib.id == id:
                scanned_books_dict[lib.id] = lib.get_books(n_days-day)
                new_list.append(lib)
                day += lib.signup_days
                all_libraries.remove(lib)

    new_score = calculate_total_score(scanned_books_dict, scores)
    if new_score > found_score:
        return True, new_list, scanned_books_dict, new_score
    else:
        return False, choosen_libraries, choosen_books, found_score
