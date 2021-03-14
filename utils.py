from library import Library
import copy

def score(books, scores):
    return sum([scores[b] for b in books])

def choose_best_score(days, libraries, scores, scanned_books):
    lib_scores = dict()
    for library in libraries:
        books = [b for b in library.get_books(days) if b not in scanned_books]
        lib_scores[library.id] = score(books, scores)/library.signup_days
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
    all_books = set()
    for id in books_dict:
        all_books.update(books_dict[id])
    return score(list(all_books), scores)


def find_best_neighbour(choosen_libraries, choosen_books, libraries, scores, n_days):
    best_score = calculate_total_score(choosen_books, scores) 
    best_libraries = copy.deepcopy(choosen_libraries)
    best_books = copy.deepcopy(choosen_books)
    found_better = False

    for current_lib in choosen_libraries:
        day = 0
        new_list = []
        scanned_books_dict = dict()
        scanned_books_set = set()
        all_libraries = copy.deepcopy(libraries)
        for lib in choosen_libraries:
            if lib == current_lib:
                all_libraries.remove(lib)
                break
            else:
                new_list.append(lib)
                scanned_books_dict[lib.id] = lib.get_books(n_days-day)
                scanned_books_set.update(scanned_books_dict[lib.id])
                all_libraries.remove(lib)
                day += lib.signup_days

        
        while day < n_days and len(all_libraries) > 0:
            id = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
            for lib in all_libraries:
                if lib.id == id:
                    scanned_books_dict[lib.id] = lib.get_books(n_days-day)
                    scanned_books_set.update(scanned_books_dict[lib.id])
                    new_list.append(lib)
                    day += lib.signup_days
                    all_libraries.remove(lib)

        new_score = calculate_total_score(scanned_books_dict, scores)
        if new_score > best_score:
            found_better = True
            best_libraries = copy.deepcopy(new_list)
            best_books = copy.deepcopy(scanned_books_dict)
            best_score = new_score
            print("better!")
        else:
            print("not better :(")

    return found_better, best_libraries, best_books, best_score

def find_first_neighbour(choosen_libraries, choosen_books, libraries, scores, n_days):
    best_score = calculate_total_score(choosen_books, scores) 
    best_libraries = copy.deepcopy(choosen_libraries)
    best_books = copy.deepcopy(choosen_books)
    found_better = False

    for current_lib in choosen_libraries:
        day = 0
        new_list = []
        scanned_books_dict = dict()
        scanned_books_set = set()
        all_libraries = copy.deepcopy(libraries)
        for lib in choosen_libraries:
            if lib == current_lib:
                all_libraries.remove(lib)
                break
            else:
                new_list.append(lib)
                scanned_books_dict[lib.id] = lib.get_books(n_days-day)
                scanned_books_set.update(scanned_books_dict[lib.id])
                all_libraries.remove(lib)
                day += lib.signup_days

        
        while day < n_days and len(all_libraries) > 0:
            id = choose_best_score(n_days - day, all_libraries, scores, scanned_books_set)
            for lib in all_libraries:
                if lib.id == id:
                    scanned_books_dict[lib.id] = lib.get_books(n_days-day)
                    scanned_books_set.update(scanned_books_dict[lib.id])
                    new_list.append(lib)
                    day += lib.signup_days
                    all_libraries.remove(lib)

        new_score = calculate_total_score(scanned_books_dict, scores)
        if new_score > best_score:
            found_better = True
            best_libraries = copy.deepcopy(new_list)
            best_books = copy.deepcopy(scanned_books_dict)
            best_score = new_score
            print("better!")
            return found_better, best_libraries, best_books, best_score
        else:
            print("not better :(")

    return found_better, best_libraries, best_books, best_score