def score(books, scores):
    return sum([scores[b] for b in books])

def choose_best_score(days, libraries, books):
    scores = dict()
    for library in libraries:
        scores[library.id] = library.get_score(days, books)
        print(library.get_score(days, books))
    print(scores)
    maximum = max(scores.values())

    return list(scores.keys())[list(scores.values()).index(maximum)]