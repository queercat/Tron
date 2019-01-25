# tron.py -- a curses version of Tron!
import curses

# init_curses ... Initalizes the curses library.
def init_curses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak() # instanteous keys.
    
    stdscr.keypad(True) # enable special keys.

    return stdscr

# Entity ... A generic entity class.
class Entity():
    def __init__(self, x, y, speed, char):
        self.x = x
        self.y = y
        self.speed = speed
        self.char = char # character representation of that entity.

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def get_char(self):
        return self.char

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

# Player ... the player class, inherits Entity.
class Player(Entity):
    def __init__(self, x, y, speed):
        Entity.__init__(self, x, y, speed, '@')

# Enemy ... the enemy class, inherits Entity.
class Enemey(Entity):
    def __init__(self, x, y, speed):
        Entity.__init__(self, x, y, speed, '#')

# loop ... Setup some curses stuff and then loop game.
def loop(scr):
    # scr.nodelay()

    player_start_x = round(scr.getmaxyx()[1] * 1/2) # set the starting player x to the middle of the screen.
    player_start_y = round(scr.getmaxyx()[0] * 3/4) # set the ending player y to the 1/4 from the bottom of the screen.
    player_start_speed = 1

    player = Player(player_start_x, player_start_y, player_start_speed)

    scr.clear() # clear the screen.
    scr.border()

    scr.addstr(player.get_y(), player.get_x(), player.get_char())

    scr.getch()
    close_curses(scr)

# close curses ... Close curses.
def close_curses(scr):
    curses.nocbreak()
    scr.keypad(False)
    curses.endwin()

def main():
    scr = init_curses()
    loop(scr) # go into game loop.

if __name__ == '__main__':
    main()