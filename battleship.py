'''
File name: battleship.py 
Author: Neha Joshi
Course: CSC 120
Description: This program replicates half of the classic board game,
             Battleship. In this game, two people play against each other;
             each arranges their ships on a grid, and then take turns
             “shooting” at each other’s board; one player announces a target,
             and the other player announces wherethat lands on their board: 
             it may be a hit on one of the ships (perhaps sinking it), or a
             miss. There are two classes, Ship and Board, that each represent
             a part of the game.
'''

class Board:
    '''
    This class represents the actual board the ships are placed on.
    
    The constructor initializes a bunch of variables for the class to use,
    like the size of the board, since it's always a square, and the all the
    ship information.

    add_ship(): adds ships to the board
    print(): prints the board in its current state
    has_been_used(): checks if the position has already been attempted
    attempt_move(): attempts to execute a move on the board
    '''
    def __init__(self, size):
        # making sure the size of the board is valid
        assert size > 0

        self.size = size
        self._ships = {} # each key is a coordinate which maps to a ship object
        self._been_used = [] # keeps track of all the used positions

    def add_ship(self, ship, position):
        '''
        This method adds the passed-in ship to the board. It also creates a
        reference from ship to board for later use.

        ship: a reference to a Ship object that's going to be added
        position: a tuple that's the position at which the ship is to be added 
        '''
        # reference to board from ship
        ship.board = self
        for coord in ship._shape:
            # since each ship is orginally positioned off of the origin,
            # the proper position needs to be adjusted
            new_pos = (position[0] + coord[0], position[1] + coord[1])
            
            # making sure the ship is still on the actual board
            assert 0 <= new_pos[0] < self.size and 0 <= new_pos[1] < self.size
            assert new_pos not in self._ships

            # adding the ship in two places for later use
            ship._coords.append(new_pos)
            self._ships[new_pos] = ship
    
    def print(self):
        '''
        This method prints the board in its current state

        - A 'o' represents a place, in deep water, which was shot at, but it
          was a miss
        - An asterisk (*) represents a place on a ship which has been Hit, but
          where the ship has not been sunk
        - An 'X' represents if a ship has been sunk
        - Parts of ships that have not been hit yet are shown by the first
          letter of their name
        '''
        # the code runs two ways depending on the size of the board
        if self.size < 11:
            print("  +" + "-" * (2 * self.size) + "-+") # border string
            # code runs y coord backwards and x coord forward
            for j in range(self.size-1, -1, -1):
                print(f"{j} |", end='')
                for i in range(self.size):
                    # if there isn't a ship at the position, then it can only
                    # be that it was either a miss or empty water
                    if (i, j) not in self._ships:
                        if (i, j) not in self._been_used:
                            print(" .", end='')
                        else:
                            print(" o", end='')
                    else:
                        # if the ship exists, then it's sunk, hit, or still there
                        if (i, j) not in self._been_used:
                            print(f" {self._ships[(i, j)]._name[0]}", end='')
                        else:
                            if self._ships[(i, j)].is_sunk():
                                print(" X", end='')
                            else:
                                print(" *", end='')
                print(" |")
            print("  +" + "-" * (2 * self.size) + "-+") # border string
            print("   ", end='')
            for k in range(self.size):
                print(f" {k}", end='')
            print()
        else:
            print("   +" + "-" * (2 * self.size) + "-+") # border string
            for j in range(self.size-1, -1, -1):
                # a little variation based on whether it's double digits
                if j >= 10:
                    print(f"{j} |", end='')
                else:
                    print(f" {j} |", end='')
                
                # same reasoning as before
                for i in range(self.size):
                    if (i, j) not in self._ships:
                        if (i, j) not in self._been_used:
                            print(" .", end='')
                        else:
                            print(" o", end='')
                    else:
                        if (i, j) not in self._been_used:
                            print(f" {self._ships[(i, j)]._name[0]}", end='')
                        else:
                            if self._ships[(i, j)].is_sunk():
                                print(" X", end='')
                            else:
                                print(" *", end='')
                print(" |")
            print("   +" + "-" * (2 * self.size) + "-+") # border string
            print(" " * 24, end='')
            
            # the horizontal axis had to be adjusted for double digits
            # to account for extra spacing
            for k in range(10, self.size):
                print(f" {str(k)[0]}", end='')
            print()
            print("    ", end='')
            l = 0
            # loops the single digits as many times as needed based on size
            while l < self.size:
                for m in range(10):
                    print(f" {str(m)}", end='')
                    l += 1
            print()

    def has_been_used(self, position):
        '''
        This function returns a boolean based on whether the position being
        asked for has been used already or not

        position: a tuple that represents the coordinates being checked
        '''
        # checking whether the position is even on the board
        assert 0 <= position[0] < self.size and 0 <= position[1] < self.size

        return position in self._been_used

    def attempt_move(self, position):
        '''
        This function attempts to hit a ship and returns a string based on
        what happened.

        position: a tuple that represents the coordinates being attempted
        '''
        # checking whether the position exists and hasn't already been used
        assert 0 <= position[0] < self.size and 0 <= position[1] < self.size
        assert position not in self._been_used

        # if it goes through, then it gets added to been_used
        self._been_used.append(position)
        if position in self._ships:
            if self._ships[position].is_sunk():
                return f"Sunk ({self._ships[position]._name})"
            else:
                return "Hit"
        else:
            return "Miss"

class Ship:
    '''
    This class represents a ship on the board

    The constructor initializes a lot of variables for the ship to use

    print(): prints the state of a ship
    is_sunk(): returns whether a ship has been completely sunk
    initial_rotate(): executes a single rotation
    rotate(): calls the initial_rotate method as many times as needed
    '''
    def __init__(self, name, shape):
        self._name = name # name of the ship shape
        self._shape = shape # an array of original coordinates representing the shape of the ship
        self.board = None
        self._coords = [] # actual coords of the ship

    def print(self):
        '''
        This method prints the state of the ship itself down by the ship info
        area
        '''
        i = 0
        for coord in self._coords:
            if coord in self.board._been_used:
                # if a part of the ship has been hit
                print("*", end='')
            else:
                print(f"{self._name[0]}", end='')
            i += 1
        print(" " * (10-i) + self._name)

    def is_sunk(self):
        '''
        This function returns a boolean based on whether a ship has been sunk
        '''
        # if the ship has any part that has been hit, it's immediately not
        # been sunk
        for coord in self._coords:
            if coord not in self.board._been_used:
                return False    
        return True

    def initial_rotate(self):
        '''
        This function is a helper function for the rotate method, where it
        performs a single rotation
        '''
        new_shape = []
        # each coordinate in a ship gets rotated and appended onto
        # a new shape array
        for coord in self._shape:
            copy = list(coord[:])
            copy[0], copy[1] = copy[1], -copy[0]
            new_shape.append(tuple(copy))
        self._shape = new_shape

    def rotate(self, amount):
        '''
        This method calls the initial_rotate method as many times as needed

        amount: an integer that represents the amount of times the ship's
                going to be rotated
        '''
        for i in range(amount):
            self.initial_rotate()