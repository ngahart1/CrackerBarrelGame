import sys
import random

"""
A Python game of Jump-All-But-One, the game
found at Cracker Barrel Restaurants!

User inputs the amount of rows in the triangular
game board!

The encoding of the holes is as follows:

                0
              1   2
            3   4   5
           6  7   8   9
        10  11  12  13  14
etc.
"""

num_rows = 0

"""
'x' indicates hole is full
'o' indicates hole is empty
"""
def print_board(vec):

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


def makeMove(board):
    jumper = getJump(board, 'x', 'jumping peg')
    jumpTo = getJump(board, 'x', 'hole to jump to')
    board[inBetween(board, jumper, jumpTo)] = 'o'
    board[jumper] = 'o'
    board[jumpTo] = 'x'

"""
Returns the index of the hole in between the given
x and y on the given game board.
"""
def inBetween(board, x, y):
    global num_rows


"""
A function to get an input related to a jump. Goes
through all possible user failures to ensure eventually
a correct input is given.
@param board the game board
@param char the character the user's space on game board must contain
@param seeking a string describing what the function of input is
"""
def getJump(board, char, seeking):
    haveValue = False
    while not haveValue:
        try:
            print('Location of ', seeking, ': ', sep = '', end = '')
            value = int(input())
        except ValueError:
            print('Must give integer location')
        if value >= len(board) or value < 0 or board[value] != char:
            print('Input can not be used for this')
        else:
            haveValue = True
    return value


def getNumRows():
    try:
        num_rows = int(input('Enter number of rows: '))
    except ValueError:
        print('Must Enter Integer')
        num_rows = getNumRows()
    return num_rows


"""
A function to determine whether or not the game
is over. Returns true if there are no possible moves,
returns false if move is possible
"""
def finished(board):
    return False


def setupBoard():
    getNumHoles = lambda x: int(x * (x + 1) / 2)
    global num_rows
    num_rows = getNumRows()
    num_holes = getNumHoles(num_rows)
    board = ['x'] * num_holes

    # one empty location to start, randomly chosen
    board[random.randint(0, num_holes - 1)] = 'o'

    return board


def main(num_rows = 5):
    board = setupBoard()
    print_board(board)
    while not finished(board):
        board = makeMove(board)
        print_board(board)

if __name__ == "__main__":
    main()



