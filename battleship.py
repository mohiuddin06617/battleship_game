"""
Battleship Single Player Game Against Computer

Step 1 - Create two 10x10 boards. One board is Hidden and other is visible to the user.
Step 2 - Place the ships on the grid. The hidden board holds the locations of the ships marked with X. Guess board will hold '.' value.
Step 3 - Before placing each ships ensure that it does not overlap with other ships. They can touch but can not overlap. Additionallu, ensure that they are placed within the grid.
Step 5 - Display the guess board to the user.
Step 6 - Prompt the user to enter coordinates in the format "A5" to target a square on the grid. Validate inputted coordiates.
Step 7 - If user entered "show" command then display the hidden board to user alongside with guess board
Step 8 - Update the guess board according to the users inputted value.
    Step 8.1 -> If the target square is miss (marked as "-") or hit (marked as "X"), then inform the player that it is already guessed.
    Step 8.2 -> If the target square is empty (marked as '.'), update it to a miss marker '-' and inform the player.
    Step 8.3 -> If the target square in hidden board contains a ship, update the guess board marker to 'X'. After each hit, check if all the squares of a ship is hit mark. If it is, then mark it as sunk and inform the player accordingly.
Step 9 - Keep count of number of shots. Increase number of shots after each iteration.
Step 10 - Check if game is over. When the total number of ships is equal to sunked ships end the game and notify user that he has won after X number of shots.
"""

import random
import time

ROW_SIZE = 10
COLUMN_SIZE = 10

"""
Ensures different sequence of random numbers
"""
random.seed(time.time())


class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.hits = 0

    def is_sunk(self):
        return self.hits == self.size


class Board:
    def __init__(self):
        self.ships = []
        self.hidden_board = [["." for _ in range(ROW_SIZE)] for _ in range(COLUMN_SIZE)]
        self.guess_board = [["." for _ in range(ROW_SIZE)] for _ in range(COLUMN_SIZE)]
        self.ship_coordinates = []
        self.total_ship_sunk = 0
        self.num_of_ships_placed = 0
        self.game_over = False
        self.shots = 0

    def validate_ship_placement_grid(self, ship, row, column, orientation):
        """
        This method validate that it does not overlap with other ships and its in range
        """
        if orientation == 'horizontal':
            column_size = column + ship.size
            if column_size > 10:
                return False
            for j in range(column, column_size):
                if self.hidden_board[row][j] != '.':
                    return False
        else:
            row_size = row + ship.size
            if row_size > 10:
                return False
            for i in range(row, row_size):
                if self.hidden_board[i][column] != '.':
                    return False
        return True

    def place_ship(self, ship, row, column, orientation):
        """Place ship value by orientation"""
        if orientation == "horizontal":
            end_col = 0
            for j in range(column, column + ship.size):
                self.hidden_board[row][j] = "X"
                end_col = j
            self.ship_coordinates.append([column, end_col, row, orientation])
        else:
            end_row = 0
            for i in range(row, row + ship.size):
                self.hidden_board[i][column] = "X"
                end_row = i
            self.ship_coordinates.append([row, end_row, column, orientation])

        self.ships.append(ship)
        self.num_of_ships_placed += 1

    def ship_placement_process(self, ship):
        """Place random generated ship value in the hidden board"""
        while True:
            row = random.randint(0, (ROW_SIZE - 1))
            column = random.randint(0, (COLUMN_SIZE - 1))
            orientation = random.choice(["horizontal", "vertical"])
            if self.validate_ship_placement_grid(ship, row, column, orientation):
                self.place_ship(ship, row, column, orientation)
                break

    def show_hidden_board(self):
        print("Hidden Board : ")
        self.show_board(board=self.hidden_board)

    def show_guess_board(self):
        print("Guess Board : ")
        self.show_board(board=self.guess_board)

    def show_board(self, board):
        print("  1 2 3 4 5 6 7 8 9 10")
        for i, row in enumerate(board):
            print(chr(ord('A') + i) + ' ' + ' '.join(row))

    def check_for_game_over(self):
        if self.num_of_ships_placed == self.total_ship_sunk:
            self.game_over = True
            print(f"Well Done! You completed the game in {self.shots} shots")

    def get_array_values_by_range(self, start_row, start_col, end_row, end_col):
        array_slice = []
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                array_slice.append(self.guess_board[row][col])
        return array_slice

    def check_for_ship_sunk(self, row, col):
        """check all consecutive rows/columns are hit or not. if all are hit then mark the ship as sunk"""
        for position in self.ship_coordinates:
            orientation = position[3]
            if orientation == "horizontal":
                start_column = position[0]
                end_column = position[1]
                horizontal_row = position[2]
                if horizontal_row == row:
                    hit_ships_list = self.get_array_values_by_range(horizontal_row, start_column, horizontal_row,
                                                                    end_column)
                    return hit_ships_list.count("X") == len(hit_ships_list)

            elif orientation == "vertical":
                start_row = position[0]
                end_row = position[1]
                vertical_column = position[2]
                if vertical_column == col:
                    hit_ships_list = self.get_array_values_by_range(start_row, vertical_column, end_row,
                                                                    vertical_column)
                    return hit_ships_list.count("X") == len(hit_ships_list)
        return True

    def shot_to_ship(self, row, column):
        """"""
        if self.guess_board[row][column] == "-" or self.guess_board[row][column] == "X":
            print("Already Guessed")
        elif self.hidden_board[row][column] == ".":
            print("**Miss**")
            self.guess_board[row][column] = "-"
        elif self.hidden_board[row][column] == "X":
            print("**Hit**")
            self.guess_board[row][column] = "X"
            if self.check_for_ship_sunk(row, column):
                self.total_ship_sunk += 1
                print("** A Ship Completely Sunk")


def get_coordinates():
    while True:
        input_coordinates = input("Enter coordinates (row, col), e.g. A5 = ").strip().upper()
        if input_coordinates == "SHOW":
            return "SHOW"
        try:
            row_val = ord(input_coordinates[0]) - ord("A")  # Converting string into ordinal number
            col_val = int(input_coordinates[1:]) - 1

            if 0 <= row_val <= (ROW_SIZE - 1) and 0 <= col_val <= (COLUMN_SIZE - 1):
                return row_val, col_val
            print("Invalid Coordinates. Please provide valid coordinates.")
        except ValueError:
            print("Invalid Input. Please recheck and try again")


if __name__ == "__main__":
    board = Board()

    battleship = Ship(name="Battleship", size=5)
    destroyer_one = Ship(name="Destroyers", size=4)
    destroyer_two = Ship(name="Destroyers", size=4)

    board.ship_placement_process(battleship)
    board.ship_placement_process(destroyer_one)
    board.ship_placement_process(destroyer_two)

    while not board.game_over:
        board.show_guess_board()
        coordinates = get_coordinates()
        if coordinates == "SHOW":
            board.show_hidden_board()
            continue

        row, column = coordinates
        board.shot_to_ship(row, column)
        board.shots += 1
        board.check_for_game_over()

    board.show_guess_board()
