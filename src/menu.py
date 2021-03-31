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

def print_menu(options, message):
    print("\n***************************************")
    print(message, '\n')
    
    for key, value in options.items():
        print(key + ". " + value)
    print("\n***************************************")

    return choice_input(1, len(options))

###############################################################################################################################################################################

def best_scores():
    
    print("\n***************************************")
    input("Press any key to return to main menu...")
    return 0

###############################################################################################################################################################################

def main_menu():
    options = { "1" :"Choose an input file", "2": "See the best score for each file", "3": "Exit"}
    message = "What do you want to do:"
    choice = print_menu(options, message)

    if choice == 3: return -1
    return choice

def file_menu():
    files = { "1" :"a_example.txt", "2": "b_read_on.txt", "3":"c_incunabula.txt", "4":"d_tough_choices.txt", "5":"e_so_many_books.txt", "6":"f_libraries_of_the_world.txt", "7":"Return to main menu"}
    message = "Choose an input file:"
    choice = print_menu(files, message)

    if choice == 7: return 0
    return files[str(choice)]

def algorithm_menu(file):

    algorithms = {"1": "Greedy", "2": "Local Search - First Neighbour", "3": "Local Search - Best Neighbour", "4": "Local search - random neighbour", "5":"Simulated Annealing", "6": "Genetic", "7": "Choose another file"}
    message = "Choose the algorithm to apply to " + file + ": "

    while True:
        algorithm = print_menu(algorithms, message)
        if algorithm == 7: break

        print("\n***************************************")
        print("Applying " + algorithms[str(algorithm)] + " to " + file, '\n')

        if algorithm >= 1 and algorithm <= 5: bookScanning(file, algorithm)
        else:  genetic(file)

        print("\n***************************************")
        input("Press any key to return to algorithms menu...")

    return 1

###############################################################################################################################################################################

def menu():

    current_menu = 0
    file = "a_example.txt"

    while current_menu != -1 :
        if current_menu == 0: # main menu
            current_menu = main_menu()
        
        elif current_menu == 1: #files menu
            file = file_menu()
            if file == 0: current_menu = 0
            else: current_menu = 3

        elif current_menu == 2: #best scores
            current_menu = best_scores()

        elif current_menu == 3: #algorithm menu
            current_menu = algorithm_menu(file)

        

