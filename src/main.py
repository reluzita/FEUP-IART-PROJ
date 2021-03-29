import sys
from bookscanning import bookScanning, genetic

def choice_input(min, max):
    user_in = input("Insert a number from the menu: ")
    while(True):
        try:
            val = int(user_in)
            if(val < min or val > max):
                user_in = input("Invalid input, please insert a valid one: ")
            else:
                break
        except ValueError:
            user_in = input("Invalid input, please insert a valid one: ")

    return val


def file_menu():
    files = { "1" :"a_example.txt", "2": "b_read_on.txt", "3":"c_incunabula.txt", "4":"d_tough_choices.txt", "5":"e_so_many_books.txt", "6":"f_libraries_of_the_world.txt"}
    print("****************************")
    print("Choose the input file: \n")
    for key,value in files.items():
        print(key + ". " + value)
    print("\n*****************************")
    choice = str(choice_input(1,6))
    return files[choice]

def algorithm_menu():
    algorithms = {"1": "Greedy", "2": "Local search - first neighbour", "3": "Local search - best neighbour", "4": "Local search - random walk", "5": "Genetic"}
    print("\n\n****************************")
    print("Choose the algorithm to apply: \n")
    for key,value in algorithms.items():
        print(key + ". " + value)
    print("\n*****************************")
    choice = choice_input(1,5)

    return choice


# List of arguments contains file.py
if __name__ == "__main__":
    file = file_menu()
    algorithm = algorithm_menu()
    if algorithm >= 1 and algorithm <= 4: bookScanning(file, algorithm)
    else:  genetic(file)