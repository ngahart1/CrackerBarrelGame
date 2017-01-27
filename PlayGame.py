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
    print('linex:', linex, 'liney:', liney)
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



