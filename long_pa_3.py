'''
File name: long_pa_3.py
Author: Neha Joshi
Course: CSC 120
Description: This program draws a lot of dice across a canvas,
created by importing graphic.py and creating an object. Those
dice are random colors, made by using the random module. At the
end of all of die displaying, the screen gets cleared and displays
the total from all the numbers on the dice.
'''

from graphics import graphics
from random import randint

def draw_dice(win, x_pos, y_pos, side):
    '''
    Based on the number passed in, this function draws that side
    of a dice on the square

    win: a graphics.py canvas object
    x_pos: an integer that represents the top left x coordinate of a square
    y_pos: an integer that represents the top left y coordinate of a square
    side: an integer that represents the side of the dice that is going to
          be drawn
    '''
    #  the number of dots that are going to be drawn
    if side == 1:
        win.ellipse(x_pos + 50, y_pos + 50, 15, 15)
    elif side == 2:
        win.ellipse(x_pos + 20, y_pos + 20, 15, 15)
        win.ellipse(x_pos + 80, y_pos + 80, 15, 15)
    elif side == 3:
        win.ellipse(x_pos + 20, y_pos + 20, 15, 15)
        win.ellipse(x_pos + 50, y_pos + 50, 15, 15)
        win.ellipse(x_pos + 80, y_pos + 80, 15, 15)
    elif side == 4:
        win.ellipse(x_pos + 20, y_pos + 20, 15, 15)
        win.ellipse(x_pos + 20, y_pos + 80, 15, 15)
        win.ellipse(x_pos + 80, y_pos + 20, 15, 15)
        win.ellipse(x_pos + 80, y_pos + 80, 15, 15)
    elif side == 5:
        win.ellipse(x_pos + 20, y_pos + 20, 15, 15)
        win.ellipse(x_pos + 20, y_pos + 80, 15, 15)
        win.ellipse(x_pos + 50, y_pos + 50, 15, 15)
        win.ellipse(x_pos + 80, y_pos + 20, 15, 15)
        win.ellipse(x_pos + 80, y_pos + 80, 15, 15)
    elif side == 6:
        win.ellipse(x_pos + 20, y_pos + 20, 15, 15)
        win.ellipse(x_pos + 20, y_pos + 50, 15, 15)
        win.ellipse(x_pos + 20, y_pos + 80, 15, 15)
        win.ellipse(x_pos + 80, y_pos + 20, 15, 15)
        win.ellipse(x_pos + 80, y_pos + 50, 15, 15)
        win.ellipse(x_pos + 80, y_pos + 80, 15, 15)

def draw_squares(win, x_pos, y_pos, total):
    '''
    This function draws the squares that are going to be representing
    the dice. All the dice are all random colors, picked using randint
    and the get_color_string method from graphic.py. It also keeps a tally
    of the total number displayed by all the dice and returns it.

    total: an integer representing the total number displayed by all the dice
    '''
    side = randint(1, 6)
    #  choose random color and draw a square with it
    red, green, blue = randint(0, 255), randint(0, 255), randint(0, 255)
    color = win.get_color_string(red, green, blue)
    win.rectangle(x_pos, y_pos, 100, 100, "black")
    win.rectangle(x_pos + 5, y_pos + 5, 90, 90, color)
    draw_dice(win, x_pos, y_pos, side)
    total += side
    return total

def main():
    win = graphics(700, 600, "Dice")
    while not win.is_destroyed():
        win.clear()
        total = 0
        #  the dice go across the board
        for y_pos in range(0, 600, 100):
            for x_pos in range(0, 700, 100):
                total = draw_squares(win, x_pos, y_pos, total)
                win.update_frame(10)
        win.update_frame(2)
        #  display the total after holding the dice screen for a bit
        win.clear()
        win.text(200, 250, f"Total: {total}", size=50)
        win.update_frame(0.5)

if __name__ == "__main__":
    main()