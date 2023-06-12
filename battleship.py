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
