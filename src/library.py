class Library:
    def __init__(self, id, books, signup_days, books_per_day):
        self.id = id  # id of the library
        self.books = books  # set of books in the library
        self.signup_days = signup_days  # time in days that it takes to sign the library up for scanning
        self.books_per_day = books_per_day  # the number of books that can be scanned each day from the library once the library is signed up
        self.scannedBooks = []  # books already scanned

    def __str__(self):
        return str(self.id)

    # get books that need to be scanned
    def get_books(self, days, scanned_books):
        remaining = days - self.signup_days
        n_books = self.books_per_day * remaining
        to_send = [book for book in self.books if
                   book not in scanned_books]  # if not in scanned_books, book needs to be scanned

        # return only books that can actually be scanned according to the remaining days and the number of books that can be scanned each day
        if len(to_send) > n_books:
            return to_send[:n_books]
        else:
            return to_send

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def __hash__(self):
        return self.id
