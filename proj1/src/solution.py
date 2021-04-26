import functools


class Solution:
    def __init__(self, libraries_list, score: int, books2lib: dict):
        self.libraries_list = libraries_list  # list of libraries
        self.score = score  # final score
        self.books2lib = books2lib

    def print_solution(self, elapsed_time):
        print("\n-----------------------------")
        print("         Solution")
        print("-----------------------------")

        print("Score:", self.score)  # prints total score
        print("Elapsed Time:", str(elapsed_time))  # prints elapsed time

    def __eq__(self, obj):
        return self.score == obj.score and functools.reduce(lambda x, y: x and y,
                                                            map(lambda p, q: p == q, self.libraries_list,
                                                                obj.libraries_list), True)

    def __str__(self):
        return self.books2lib
