import sys
from bookscanning import bookScanning

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
    files = { "1" :"a_example.txt", "2": "b_read_on.txt", "3":"c_incunabula.txt", "4":"d_tough_choices.txt", "5":"e_so_many_books.txt", "6":"f_libraries_of_the_world"}
    print("****************************")
    print("Choose the input file: \n")
    for key,value in files.items():
        print(key + ". " + value)
    print("\n*****************************")
    choice = str(choice_input(1,6))
    return files[choice]

def algorithm_menu():
    print("****************************")
    print("Choose the algorithm to apply: \n")
    print("1. greedy")
    print("2. local search - first neighbour")
    print("3. local search - best neighbour")
    print("*****************************")
    choice = choice_input


# List of arguments contains file.py
if __name__ == "__main__":
    file = file_menu()
    bookScanning(file)