# Chris Tomaskovic chrtomas@uat.edu
# CSC235 Final Project

import random
import re
import matplotlib.pyplot as plt


def save_game():
    # Saves the users inputs
    # Writes data to a text file
    # If it does not exist it creates a file
    f = open("gamelog.txt", "a")
    # Write some stuff to the file
    # Use the file object, not the file name to handle the file
    f.write("Saved Info: \n")
    # Close the file right away
    f.close()


def read_data():
    # Reads data from a text file
    # If it does not exist it will error
    f = open("gamelog.txt", "r")
    # Read contents of the file and display them
    print(f.read())
    # Close file
    f.close()


def display_intro():
    # Displays the intro for the user
    print("\n\n\t*** Welcome to Minesweeper ***\n")
    print("\nThis application lets you play Minesweeper in the CLI (Command Line Interface).")
    print("\nThe main objective of Minesweeper is to dig up all the spaces except for the 10 hidden mines.")
    print("\nThe rules for Minesweeper are simple:")
    print("\n1. Enter the row (left side) and the column (top) you would like to dig in with a , separating them.")
    print("\n2. The number on a space represents how many bombs are bordering that space.")
    print("\n3. Dig away until all the spaces without mines are discovered.")
    print("\n4. Have fun!\n")


class gameBoard:
    def __init__(self, dim_size, num_bombs):
        # keeps track of parameters
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # creates board
        self.board = self.make_board()
        self.assign_values_to_board()

        self.dug = set()

    def make_board(self):
        # makes a new board based on the dimension size

        # generates a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # creates the array

        # plants bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)  # return a random integer N so that a <= N <= b
            row = loc // self.dim_size  # we want the number of times dim_size goes into loc to tell us what row to look at
            col = loc % self.dim_size  # we want the remainder to tell us what index in that row to look at

            if board[row][col] == '*':
                # this means a bomb has already been planted
                continue

            board[row][col] = '*'  # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # represents number of neighboring bombs
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # doesn't calculate anything if there's already a bomb
                    continue
                self.board[r][c] = self.neighboring_bombs(r, c)

    # checks if there is a bomb in a square around the location
    def neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    # original location
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at that location
        # return True if successful dig, False if bomb dug recursively until bombs surround* the cells

        self.dug.add((row, col))  # keeps track of dig sites

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue  # don't dig where you've already dug
                self.dig(r, c)
        return True

    def __str__(self):
        # prints board

        # array
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # puts array together in a string
        string_rep = ''
        # gets widths for printing
        widths = []
        for index in range(self.dim_size):
            # lambda creates a random function, that cannot contain statements
            columns = map(lambda x: x[index], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [x for x in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for x in range(len(visible_board)):
            row = visible_board[x]
            string_rep += f'{x} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep


# function that allows the user to play the game
def play(dim_size=10, num_bombs=10):
    save_game()

    display_save = input("Would you like to display saved data? (y/n): ")
    if display_save == "y":
        read_data()
    else:
        print("\nYou choose not to display saved data.")

    display_intro()

    play_again = True

    while play_again == True:

        boardShow = gameBoard(dim_size, num_bombs)

        safe = True

        while len(boardShow.dug) < boardShow.dim_size ** 2 - num_bombs:
            print(boardShow)

            # regular expression allows for any input as long as it is in range and has a comma
            user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
            row, col = int(user_input[0]), int(user_input[-1])
            if row < 0 or row >= boardShow.dim_size or col < 0 or col >= dim_size:
                print("Invalid location. Try again.")
                continue

            # if location is valid, a hole is dug
            safe = boardShow.dig(row, col)
            if not safe:
                break  # game over

        if safe:
            print("CONGRATULATIONS! YOU WON!")
            # creates file with final board
            gamelog = input('What is your name: ')
            f = open('gamelog.txt', 'a')
            f.write(str(boardShow))
            f.write("\n" + gamelog + "'s won game\n\n")
            f.close()
            # graphs a check mark
            grty = [.5, 0, .5, 1, 1.5]
            grtx = [0, 0, .5, 1, 1.5]
            plt.plot(grtx, 'g')
            plt.plot(grty, 'g')
            plt.title('YOU WON!')
            plt.show()
        else:
            print("GAME OVER")
            # reveals whole board
            boardShow.dug = [(r, c) for r in range(boardShow.dim_size) for c in range(boardShow.dim_size)]
            print(boardShow)
            # creates file with final board
            gamelog = input('What is your name: ')
            f = open('gamelog.txt', 'a')
            f.write(str(boardShow))
            f.write("\n" + gamelog + "'s lost game\n\n")
            f.close()
            # graphs and X
            grty = [3, 2, 1, 0]
            grtx = [0, 1, 2, 3]
            plt.plot(grtx, 'r')
            plt.plot(grty, 'r')
            plt.title('YOU LOST')
            plt.show()

        # Ask the player if they would like to play again
        player_choice = input("\nWould you like to play again? (y/n): ")
        # Evaluate the player choice
        if player_choice == "y":
            play_again = True
        else:
            print("\nSee you later!")
            play_again = False


if __name__ == '__main__':
    # This checks if there is a main function and then runs it if there is
    play()
