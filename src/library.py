class Library:
    def __init__(self, id, books, signup_days, books_per_day):
        self.id = id
        self.books = books
        self.signup_days = signup_days
        self.books_per_day = books_per_day
        self.scannedBooks = []

    def __str__(self):
        return str(self.id)

    def get_books(self, days):
        remaining = days - self.signup_days
        n_books = self.books_per_day * remaining
        return self.books[:n_books]

    def send_books(self, days):
        remaining = days - self.signup_days
        n_books = self.books_per_day * remaining
        self.scannedBooks = self.books[:n_books]
  
    def __eq__(self, other):
        return(self.__class__ == other.__class__ and self.id == other.id)
