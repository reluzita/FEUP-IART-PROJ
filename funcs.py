def score(books, scores):
    return sum([scores[b] for b in books])

def choose_best_score(days, libraries, scores):
    lib_scores = dict()
    for library in libraries:
        lib_scores[library.id] = score(library.get_books(days), scores)
    maximum = max(lib_scores.values())

    return list(lib_scores.keys())[list(lib_scores.values()).index(maximum)], maximum