from funcs import score

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
  