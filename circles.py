'''
File name: circles.py
Author: Neha Joshi
Course: CSC 120
Description: This program creates a simulation of circles that drop under
             the influence of gravity and whenever one circle hits another,
             the bigger one swallows up the smaller one. It imports
             three_shapes_game.py and the random module.
'''

from three_shapes_game import Game
from random import randint

class Circle:
    '''
    This class creates the circle objects for the simulation. Circles
    follow gravity and get slower as they bounce. They also take in the
    smaller circles.

    The constructor initializes the x and y positions of the center of the
    circles, the radius, and the speed at which they're going to move, which
    is selected at random from a particular range

    get_xy(): This method gets the x and y positions of the circle in the
              form of a tuple
    get_radius(): This method gets the radius of the circle
    nearby(): This method determines whether or not there is another circle
              close to the circle the code is looking at
    edge(): This method describes what's going to happen to the circle when
            it gets close to an edge of the canvas
    move(): This method moves the shape itself
    draw(): This method draws out the circles and randomizes their color
    '''
    def __init__(self, x, y, r):
        self._x = x
        self._y = y
        self._r = r
        self._speed = randint(1, 5)
    
    def get_xy(self):
        '''
        Returns the x and y coordinates of the object, measured from the
        center, in the form of a tuple
        '''
        return (self._x , self._y)

    def get_radius(self):
        '''
        Returns the radius of the object
        '''
        return self._r

    def nearby(self, other, dist, game):
        '''
        Determines, out of the two circles being looked at, which one is
        going to be swallowed

        other: a reference to the other object this particular one is being
               compared to
        dist: an integer that represents the distance from one center to
              the other
        game: a Game object that is an instance of the simulation
        '''
        # returns True if any circles are touching
        if dist <= self.get_radius() + other.get_radius():
            # deciding which circle gets taken in based on size
            obj_to_remove = max(self.get_radius(), other.get_radius())
            if obj_to_remove == other.get_radius():
                self._r += other._r
                game.remove_obj(other)
            else:
                other._r += self._r
                game.remove_obj(self)
            return True
        else:
            return False

    def edge(self, dir, position):
        '''
        Determines what happens to the object when it hits an edge of
        the canvas

        dir: a string that represents what edge of the canvas the object is
             close to: top, bottom, left, or right
        position: an integer that represents the position of the edge
        '''
        # they get slower and slower as they keep bouncing from the bottom
        if dir == "bottom":
            self._speed *= -0.75

    def move(self, game):
        '''
        This function updates the position and moves the object whichever
        way it needs to move

        game: a Game object that is an instance of the simulation
        '''
        # the circles fall down sorta according to gravity and increase
        # in speed as they go down
        self._y += self._speed
        self._speed += 2

    def draw(self, win):
        '''
        Draws the object itself using the graphics.py module, imported
        inside three_shapes_game.py, and assigns it a random color using
        the random module and get_color_string method from graphics.py

        win: a graphics.py object which is an instance of a canvas object
        '''
        # random color is chosen
        red, green, blue = randint(0, 255), randint(0, 255), randint(0, 255)
        color = win.get_color_string(red, green, blue)
        win.ellipse(self._x, self._y, self._r, self._r, color)

def spawn(game, wid, hei):
    '''
    This function spawns in a few circles to start off the simulation. It
    creates them and adds them using the Game class from three_shapes_game.py

    game: a Game object that is an instance of the simulation
    wid: an integer that represents the width of the canvas
    hei: an integer that represents the height of the canvas
    '''
    new_obj = Circle(20, 20, 3)
    game.add_obj(new_obj)

    new_obj = Circle(100, 50, 2)
    game.add_obj(new_obj)

    new_obj = Circle(160, 50, 5)
    game.add_obj(new_obj)

def spawn_more(game, wid, hei):
    '''
    This function spawns in circles, with their x and y coordinates and
    radius random, and adds them using the Game class from
    three_shapes_game.py

    game: a Game object that is an instance of the simulation
    wid: an integer that represents the width of the canvas
    hei: an integer that represents the height of the canvas
    '''
    new_obj = Circle(randint(0, wid), randint(0, hei), randint(3, 20))
    game.add_obj(new_obj)
    

def main():
    # This is the size of the window; feel free to tweak it. However,
    # please don’t make this gigantic (about 800x800 should be max),
    # since your TA may not have a screen with crazy-large resolution.
    wid = 400
    hei = 600

    # This creates the Game object. The first param is the window name;
    # the second is the framerate you want (20 frames per second, in this
    # example); the last two are the window / game space size.
    game = Game("Three Shapes", 20, wid,hei)

    # This affects how the distance calculation in the "nearby" calls
    # works; the default is to measure center-to-center. But if anybody
    # wants to measure edge-to-edge, they can turn on this feature.
    # game.config_set("account_for_radii_in_dist", True)

    # You get to decide what spawn() does. This sets up the initial
    # objects that you want to create, at the beginning of the game (if
    # any). Of course, you can remove this is you want to create objects
    # some other way.
    spawn(game, wid,hei)

    # game loop. Runs forever, unless the game ends.
    while not game.is_over():
        game.do_nearby_calls()
        game.do_move_calls()
        game.do_edge_calls()
        game.draw()
        # You get to decide what spawn_more() does (if anything). This
        # allows you to spawn additional objects over time. It is
        # called once per game tick.
        spawn_more(game, wid,hei)


if __name__ == "__main__":
    main()