from math import *

def get_input():
    x1 = float(input("Please enter the first x-coord: "))
    z1 = float(input("Please enter the first z-coord: "))
    angle_b = abs(float(input("Please enter the first angle: ")))
    print()
    x2 = float(input("Please enter the second x-coord: "))
    z2 = float(input("Please enter the second z-coord: "))
    angle_c = abs(float(input("Please enter the second angle: ")))
    print()

    return (x1, z1, angle_b), (x2, z2, angle_c)

def calculate_location(info_set_1, info_set_2):
    x1, z1, angle_b = info_set_1[0], info_set_1[1], info_set_1[2]
    x2, z2, angle_c = info_set_2[0], info_set_2[1], info_set_2[2]

    '''
    if angle_b is <90, stronghold is to the right
    elif angle_b is >90, stronghold is to the left
    else, account for this
    '''

    if angle_b > 90:
        # stronghold is to the left of the initial throw
        if angle_c > angle_b:
            angle_c = 180 - angle_c
        else:
            angle_b = 180 - angle_b
    elif angle_b < 90:
        # stronghold is to the right of the initial throw
        if angle_b < angle_c:
            angle_c = 180 - angle_c
        else:
            angle_b = 180 - angle_b
    else:
        if z2 > z1:
            angle_c = 180 - angle_c

    # calculating the length of the one side we know for sure
    # if x1 == x2:
    side_a = abs(z2 - z1)
    '''elif z1 == z2:
        side_a = abs(x2 - x1)
    else:
        side_a = math.sqrt(((z2 - z1)**2) + ((x2 - x1)**2))'''

    angle_a = 180 - angle_b - angle_c # third angle in triangulation
    
    # implementing law of sines to get side c and b
    side_c = (side_a * sin(radians(angle_c))) / (sin(radians(angle_a)))
    side_b = (side_a * sin(radians(angle_b))) / (sin(radians(angle_a)))

    # now for the x and z distances to get to stronghold
    z3 = (side_c**2 - z1**2 + z2**2 - side_b**2) / ((2 * z2) - (2 * z1))
    x3 = sqrt(side_c**2 - (z3-z1)**2) + x1

    print("Stronghold is at x = " + str(int(x3)) + " and z = " + str(int(z3)))

    '''z_dist = math.sin(angle_b) * side_c
    x_dist = math.sin(90 - angle_b) * side_c

    if x1 == x2:
        if angle_b < 90:
            new_x = x1 - x_dist
        else:
            new_x = x1 + x_dist
        
        new_z = z1 + z_dist
    elif z1 == z2: # fix this
        if angle_b < 90:
            new_x = x1 - x_dist
        else:
            new_x = x1 + x_dist
        
        new_z = z1 + z_dist'''


def main():
    print("\nInstructions:")
    print("To accurately use this locator, please enter the angle with as many " + 
    "decimal places as possible. Enter the x and z coords of the first location " + 
    "you threw the eye of ender from along with the angle, all listed in the F3 " + 
    "menu. Make sure to throw the second one from a good 200-300 blocks away.\n")
    
    info_set_1, info_set_2 = get_input()
    calculate_location(info_set_1, info_set_2)

if __name__ == "__main__":
    main()