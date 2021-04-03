 ## Building and Running 

Run ```python main.py ``` on the src folder.

After this the following menu will appear:

```
***************************************
What do you want to do: 

1. Choose an input file
2. See the best score for each file
3. Exit

***************************************
Insert a number from the menu: 1

```
Where the user must choose either one of the options.

When choosing option 1:

 ```
 ***************************************
Choose an input file:

1. a_example.txt
2. b_read_on.txt
3. c_incunabula.txt
4. d_tough_choices.txt
5. e_so_many_books.txt
6. f_libraries_of_the_world.txt
7. Return to main menu

***************************************
```
The user must choose the input file to apply the algorithm and then the algorithm:
```
***************************************
 Choose the algorithm to apply to c_incunabula.txt:

1. Greedy
2. Local Search - First Neighbour
3. Local Search - Best Neighbour
4. Local Search - Random Neighbour
5. Simulated Annealing
6. Genetic
7. Choose another file

***************************************
 ```
When the option is not the greedy algorithm, another menu to choose to either to use greedy as the initial solution or a random will appear:
```
***************************************
What do you want to do?

1. Use greedy solution
2. Use random solution

***************************************
```

If, in the initial menu, the user chooses option 2, the following appears:

```
***************************************
 Best Scores

 File                         | Score     | Algorithm
-------------------------------------------------------------------
 a_example.txt                |        21 | Greedy
 b_read_on.txt                | 5 822 900 | Greedy
 c_incunabula.txt             | 5 690 054 | Random Neighbour
 d_tough_choices.txt          | 5 028 530 | Greedy
 e_so_many_books.txt          | 5 037 291 | Genetic
 f_libraries_of_the_world.txt | 5 329 948 | Simulated Annealing

***************************************
Press enter to return to main menu...
```

 This project was developed using Python 3.