import sys
import random
import Error as e

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

from enum import Enum

class GameStates(Enum):
    WINNER = 1
    LOSER = 2
    KEEP_GOING = 3

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
    while True:
        jumper = getJump(board, 'x', 'jumping peg')
        jumpTo = getJump(board, 'o', 'hole to jump to')
        try:
            board[inBetween(jumper, jumpTo)] = 'o'
            break
        except e.InvalidJumpError:
            print('Invalid jump!')
    board[jumper] = 'o'
    board[jumpTo] = 'x'
    return board

"""
Returns the index of the hole in between the given
x and y on the given game board.
"""
def inBetween(x, y):
    if x > y:
        temp = x
        x = y
        y = temp
    linex = getLineOfHole(x)
    liney = getLineOfHole(y)
    # first condition: if on same line, then
    # must be exactly two away for valid jump
    if liney == linex:
        if y - x == 2:
            return y - 1
        else:
            raise e.InvalidJumpError()
    # second condition: if on different lines, those
    # lines must be two apart, leaving room for a piece
    # to be jumped but not too far of a jump
    elif liney - linex != 2:
        raise e.InvalidJumpError()
    # lastly, if on lines 2 apart must follow the rule:
    # going up 2 lines to the left, as would be required for a
    # legal jump, requires a difference of (2*line_no) + 1
    # going up 2 lines to the right, as would be required for a
    # legal jump in that direction, requires difference of
    # (2*line_no) - 1, where line_no is the greater of the line
    # numbers of the two holes
    else:
        if x == y - (2*liney + 1):
            # going up left
            return y - (liney + 1)
        elif x == y - (2*liney - 1):
            # going up right
            return y - liney
        else:
            raise e.InvalidJumpError()


"""
Finds the line of the board on which the given hole
resides.
Line            Picture
0                   0
1                  1 2
2                 3 4 5
3                6 7 8 9
    etc.
"""
def getLineOfHole(num):
    # triangular numbers are 0, 1, 3, 6,...
    # line starts at line 0
    triangular = lambda x: x*(x+1)/2
    line = 0
    beginningOfLine = 0
    while num > beginningOfLine:
        line += 1
        beginningOfLine = triangular(line)
    if beginningOfLine > num:
        line -= 1
    return line



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
            inp = input()
            if inp == 'q':
                print('You have entered q, so the game is over')
                exiter(board)
            value = int(inp)
        except ValueError:
            print('Must give integer location')
        if value >= len(board) or value < 0 or board[value] != char:
            print('Input can not be used for this')
        else:
            haveValue = True
    return value

def exiter(board):
    numLeft = sum([hole == 'x' for hole in board])
    res = resultName(numLeft)
    print('There are ', numLeft, ' pegs remaining, so ', res, '!', sep = '')
    exit()

def resultName(num):
    if num == 1:
        return 'you are a genius'
    elif num == 2:
        return 'you are pretty smart'
    elif num == 3:
        return 'you are just average'
    elif num == 4:
        return 'you are just plain dumb'
    else:
        return 'you are an eg-no-ra-mus'


def getNumRows():
    try:
        num_rows = int(input('Enter number of rows: '))
    except ValueError:
        print('Must Enter Integer')
        num_rows = getNumRows()
    return num_rows


"""
A function to determine current game board status.
Returns from the enum defined globally, with options
for win, loss, or keep going.
"""
def status(board):
    # first, check if only one more peg
    if sum([hole == 'x' for hole in board]) == 1:
        exiter(board)
    #elif lost(board):
    #    return GameStates.LOSER
    return GameStates.KEEP_GOING

"""
returns true if the board situation indicates the game is
over, false if there are still possible jumps
"""
'''def lost(board):
    # i is a hole that might contain the jumping peg
    # j is a hole that might contain the hole to be
    # jumped into
    for i in range(len(board)):
        if board[i] == 'x':
            for j in range(len(board)):
                if board[j] == 'o':
                    try:
                        between = inBetween(i, j)
                        if board[between] == 'x':
                            return False
                    except e.InvalidJumpError:
                        break

   return True
'''

def setupBoard():
    getNumHoles = lambda x: int(x * (x + 1) / 2)
    global num_rows
    num_rows = getNumRows()
    num_holes = getNumHoles(num_rows)
    board = ['x'] * num_holes

    # one empty location to start, randomly chosen
    board[random.randint(0, num_holes - 1)] = 'o'

    return board


def main():
    board = setupBoard()
    print_board(board)
    while status(board) == GameStates.KEEP_GOING:
        board = makeMove(board)
        print_board(board)
    if status(board) == GameStates.WINNER:
        print('Congratulations, you have won!!!')
    elif status(board) == GameStates.LOSER:
        print('Sorry, you have lost')

if __name__ == "__main__":
    main()



