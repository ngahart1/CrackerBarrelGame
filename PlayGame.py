import sys
import random

"""
A Python game of Jump-All-But-One, the game
found at Cracker Barrel Restaurants!

The encoding of the holes is as follows:

                1
              2   3
            4   5   6
           7  8   9   10
        11  12  13  14  15
"""

"""
vec should be a 15-length boolean vector,
to enable printing in the standard formation.
true indicates there is a peg in the hole,
false indicates the hole is empty.
"""
def print_board(vec, num_rows):

    for i in vec:
        if i != 'x' and i != 'o':
            print('Illegal Game Vector')
            exit()

    num_printed = 0
    rows_printed= 0
    while num_printed < len(vec):
        print(''.ljust(num_rows - rows_printed - 1), end='')
        for i in list(range(num_printed, num_printed + rows_printed + 1)):
            print(vec[i], end = ' ')
            num_printed += 1
        print('')
        rows_printed += 1


def getNumRows():
    try:
        num_rows = int(input('Enter number of rows: '))
    except ValueError:
        print('Must Enter Integer')
        num_rows = getNumRows()
    return num_rows


def main(num_rows = 5):
    getNumHoles = lambda x: int(x*(x+1)/2)
    num_rows = getNumRows()
    num_holes = getNumHoles(num_rows)
    board = ['x'] * num_holes
    # one empty location to start, randomly chosen
    board[random.randint(0, num_holes - 1)] = 'o'
    print_board(board, num_rows)

if __name__ == "__main__":
    main()



