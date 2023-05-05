'''
File name: twine.py
Author: Neha Joshi
Course: CSC 120
Description: This program is a small interactive game where the player
is wandering through a forest, unravelling a ball of "twine" to keep track
of their way. This program replicates that functionality and provides several
functions for the user to do so. It always prompts the user with their current
position, the places they've been (their history), and what they want to do.
It can even read in obstacles that user has to avoid.
'''

def directions(new_dir, positions, obstacles_coords):
    '''
    This function moves the player one step in the direction passed
    into the function and appends the new position to the overall
    array and returns it.

    new_dir: a string that determines the direction the user wants to
             move in
    positions: an array of tuples that are a history of where the player
               has been
    obstacles_coords: a set of tuples that contain the coordinates of where
                      there are obstacles that the user can't go on 
    '''
    #  create a copy of the last position to use to create new one
    new_copy = positions.copy()
    new_pos = list(new_copy[-1])
    #  based on the direction the user inputs, the position gets adjusted
    if new_dir == "n":
        new_element = new_pos[1] + 1
        new_pos[1] = new_element
    elif new_dir == "s":
        new_element = new_pos[1] - 1
        new_pos[1] = new_element
    elif new_dir == "e":
        new_element = new_pos[0] + 1
        new_pos[0] = new_element
    elif new_dir == "w":
        new_element = new_pos[0] - 1
        new_pos[0] = new_element
    new_pos = tuple(new_pos)
    #  checking for whether or not the new position goes onto an obstacle
    #  if it does, an error message is printed and the position is ignored
    if new_pos not in obstacles_coords:
        positions.append(new_pos)
    else:
        print("You could not move in that direction, because there is an obstacle in the way.")
        print("You stay where you are.")
    return positions

def go_back(positions):
    '''
    This function moves the user back one position by deleting the last
    position from the history and returning the new version
    '''
    #  error checking for whether the user is at the start
    #  in that case, they can't go back any further, and an error message
    #  is printed
    if len(positions) == 1:
        print("Cannot move back, as you're at the start!")
    else:
        print("You retrace your steps by one space")
        del positions[-1]
    return positions

def crossings(positions):
    '''
    This function counts and prints how many times the player crossed over the
    particular last position
    '''
    pos_count = positions.count(positions[-1])
    print(f"There have been {pos_count} times in the history when you were at this point.")

def print_map(positions, obstacles_coords):
    '''
    This function prints a map of where the player has been so far.
        - "X" means that there is an obstacle there
        - "*" means that that is the origin point
        - "+" means that this is the player's current location
        - "." means that this is a position the player has been to
    '''
    #  map prints left to right, top to bottom
    print("+-----------+")
    for y in range(5, -6, -1):
        print("|", end="")
        for x in range(-5, 6, 1):
            #  all the tuples in positions are like this, but the first
            #  element in each tuple is the x coordinate and the second
            #  one is the y coordinate
            cur_pos = (x, y)
            if cur_pos in obstacles_coords:
                print("X", end="")
                continue
            if cur_pos not in positions:
                print(" ", end="")
            else:
                if cur_pos == (0, 0) and cur_pos != positions[-1]:
                    print("*", end="")
                elif cur_pos == positions[-1]:
                    print("+", end="")
                else:
                    print(".", end="")
        print("|")
    print("+-----------+")

def show_ranges(positions):
    '''
    This function prints out the range of the positions the user has been
    to. That is, how far the user has been in all four directions.
    '''
    #  initialize the ranges by setting them equal to the first coordinates
    furthest_e, furthest_w = positions[0][0], positions[0][0]
    furthest_n, furthest_s = positions[0][1], positions[0][1]
    #  loop through and every time a greater or smaller range is found,
    #  replace the old with the new one
    for pos in positions:
        if pos[0] > furthest_e:
            furthest_e = pos[0]
        elif pos[0] < furthest_w:
            furthest_w = pos[0]
        
        if pos[1] > furthest_n:
            furthest_n = pos[1]
        elif pos[1] < furthest_s:
            furthest_s = pos[1]
    #  printing out the results
    print(f"The furthest West your twine goes is {furthest_w}")
    print(f"The furthest East your twine goes is {furthest_e}")
    print(f"The furthest South your twine goes is {furthest_s}")
    print(f"The furthest North your twine goes is {furthest_n}")

def read_obstacles_file(open_file, obstacles_coords):
    '''
    This function takes in an opened file object and an empty set to represent
    the coordinates of the obstacles. It then reads through the file and
    populates the obstacles_coords set and returns it.

    open_file: an opened file object that contains all the data for the
               obstacles
    obstacles_coords: an empty set when passed in, but a set that contains the
                      coordinates of the obstacles when returned
    '''
    for line in open_file:
        line = line.strip()
        #  checking for blank lines in the file
        if line == "":
            continue
        else:
            line = line.split()
            #  checking to make sure each line only has two elements
            if len(line) == 2:
                try:
                    obstacle = (int(line[0]), int(line[1]))
                    obstacles_coords.add(obstacle)
                #  if this except gets triggered, it means that the data in
                #  the line wasn't an integer. an error message is printed
                #  to show this.
                except ValueError:
                    print("ERROR: Obstacles file has invalid data inside it." + \
                          "The coordinates in the obstacles file are not integers.")
            else:
                print("ERROR: Obstacles file has invalid data inside it.")
    return obstacles_coords 

def main():
    #  initialize both the positions array and the obstacles_coords set
    positions = [(0, 0)]
    obstacles_coords = set()
    print("Please give the name of the obstacles filename, or - for none:")
    user_file = input()
    print()
    #  error checking to make sure file is valid
    #  if an error is tripped, a message is printed and the user is prompted
    #  to enter the name of the file again
    if user_file.endswith(".txt"):
        try:
            open_file = open(user_file, "r")
            obstacles_coords = read_obstacles_file(open_file, obstacles_coords)
        except FileNotFoundError:
            print("ERROR: Please enter the name of a file that exists.")
            print()
            print("Please give the name of the obstacles filename, or - for none:")
            user_file = input()
            print()
    elif user_file.strip() == "":
        print("ERROR: Obstacles filename is blank")
        print()
        print("Please give the name of the obstacles filename, or - for none:")
        user_file = input()
        print()
    #  entering - means that there is no obstacle file the user wanted to use
    elif user_file == "-":
        pass
    #  user is constantly prompted to provide a command
    while True:
        print(f"Current position: {positions[-1]}")
        print(f"Your history:     {positions}")
        try:
            print("What is your next command?")
            user_cmd = input()
        except EOFError:
            break
        
        #  only valid commands are allowed to run
        #  rest are error messaged
        if user_cmd.strip() == "":
            print()
            print("You do nothing.")
            print()
        elif user_cmd in ["n", "s", "e", "w"]:
            positions = directions(user_cmd, positions, obstacles_coords)
            print()
        elif user_cmd == "back":
            positions = go_back(positions)
            print()
        elif user_cmd == "crossings":
            crossings(positions)
            print()
        elif user_cmd == "map":
            print_map(positions, obstacles_coords)
            print()
        elif user_cmd == "ranges":
            show_ranges(positions)
            print()
        else:
            if len(user_cmd.split()) > 1:
                print("ERROR: You have typed more than one word for a command." + \
                      "Commands are only one word long!")
                print()
            else:
                print("ERROR: Command was not recognized. Please enter a valid command.")
                print()

if __name__ == "__main__":
    main()