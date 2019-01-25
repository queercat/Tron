# tron.py -- a curses version of Tron!
import curses
import time

# Entity ... A generic entity class.
class Entity():
    def __init__(self, x, y, speed, char):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.old_positions = []
        self.speed = speed
        self.char = char # character representation of that entity.
        self.direction_x = 0 # 1 represents positive (right) -1 represents negative (left)
        self.direction_y = 0 # 1 represents positive (up / ascending) -1 represents negative (down / descending)

    # update_position ... Updates the x and y coordinates of the entity.
    def update_position(self, x, y):

        if (self.x, self.y) != (x, y):
            self.old_x = self.x
            self.old_y = self.y
            self.old_positions.append((self.old_x, self.old_y))

        self.x = x
        self.y = y

    # get_old_positions ... Returns an array of old position tuples.
    def get_old_positions(self):
        return self.old_positions

    # get_position ... Returns the position of the entity in a tuple of (x, y).
    def get_position(self):
        return (self.x, self.y)

    # get_speed ... Returns the speed of the entity.
    def get_speed(self):
        return self.speed

    # update_direction ... Updates the horizontal or vertical direction of the entity.
    def update_direction(self, x, y):
        self.direction_x = x
        self.direction_y = y

    # get_direction ... returns the direction as tuple of (direction_x, direction_y)
    def get_direction(self):
        return (self.direction_x, self.direction_y)

    # get_char ... Returns the character representation of the entity.
    def get_char(self):
        return self.char

# Player ... The player class, inherits Entity.
class Player(Entity):
    def __init__(self, x, y, speed):
        Entity.__init__(self, x, y, speed, '@')
        
    def get_input(self, scr):
        return(scr.getch())
    
    def game_over(self, scr):
        game_over(scr)

# Enemy ... The enemy class, inherits Entity.
class Enemey(Entity):
    def __init__(self, x, y, speed):
        Entity.__init__(self, x, y, speed, '#')

    def game_over(self, scr):
        player_win(scr)

def main():
    scr = init_curses()
    loop(scr) # go into game loop.

# init_curses ... Initalizes the curses library.
def init_curses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak() # instanteous keys.
    
    stdscr.keypad(True) # enable special keys.

    return stdscr

# close curses ... Close curses.
def close_curses(scr):
    curses.nocbreak()
    scr.keypad(False)
    curses.endwin()

# loop ... Setup some curses stuff and then loop game.
def loop(scr):
    scr.clear() # clear the screen.
    curses.curs_set(0) # set the cursor invisible.
    scr.nodelay(True)

    player_start_x = round(scr.getmaxyx()[1] * 1/2) # set the starting player x to the middle of the screen.
    player_start_y = round(scr.getmaxyx()[0] * 3/4) # set the ending player y to the 1/4 from the bottom of the screen.
    player_start_speed = 1

    player = Player(player_start_x, player_start_y, player_start_speed)

    entities = [player]

    while True:
        if update(player, entities, scr):
            break
        draw(entities, scr)

    close_curses(scr)

# draw ... Draws the entities on the screen.
def draw(entities, scr):
    scr.clear()
    scr.border()

    for entity in entities:
        position = entity.get_position()
        trail = entity.get_old_positions()
        tail = len(trail) - 1
        
        while tail > 0:
            horizontal = trail[tail][0] is not trail[tail - 1][0]
            char = '│'
            if horizontal:
                char = '─'

            tail -= 1

            scr.addstr(trail[tail][1], trail[tail][0], char)
            scr.addstr(1, 1, str(entities[0].get_position()[0]) + ', ' + str(entities[0].get_position()[1]))

        scr.addstr(position[1], position[0], entity.get_char())

    scr.refresh()
    time.sleep(.04)

# player_win ... The player wins!
def player_win(scr):
    scr.clear()
    scr.nodelay(False)

    msg = 'YOU WIN!'

    scr.addstr(round(scr.getmaxyx()[0] * 1/2), round(scr.getmaxyx()[1] * 1/2) - round(len(msg) * 1/2), msg)
    scr.refresh()

    scr.getch()

# game_over ... Does game over stuff.
def game_over(scr):
    scr.clear()
    scr.nodelay(False)

    msg = 'GAME OVER!'

    scr.addstr(round(scr.getmaxyx()[0] * 1/2), round(scr.getmaxyx()[1] * 1/2) - round(len(msg) * 1/2), msg)
    scr.refresh()

    scr.getch()

# update ... Update the game using the list of current entities.
def update(player, entities, scr):
    key = player.get_input(scr)
    scr.addstr(0, 0, str(key))

    if key != -1:
        if key == ord('w') or key == curses.KEY_UP:
            player.update_direction(0, -1)
        elif key == ord('a') or key == curses.KEY_LEFT:
            player.update_direction(-1, 0)
        elif key == ord('s') or key == curses.KEY_DOWN:
            player.update_direction(0, 1)
        elif key == ord('d') or key == curses.KEY_RIGHT:
            player.update_direction(1, 0)
        elif key == ord('q') or key == curses.KEY_CLOSE:
            game_over(scr)
            return True

    for entity in entities:
        position = entity.get_position()
        direction = entity.get_direction()
        speed = entity.get_speed()

        new_position = (position[0] + round(direction[0] * speed), position[1] + round(direction[1] * speed))
        
        if not in_bounds(new_position, scr.getmaxyx()):
            entity.game_over(scr)
            return True

        if hit_light_trail(new_position, entities):
            entity.game_over(scr)
            return True

        entity.update_position(new_position[0], new_position[1])

# hit_light_trail ... Checks to see if an entity's position would be in that of a light trail.
def hit_light_trail(position, entities):
    light_trails = []

    for entity in entities:
        for light_trail in entity.get_old_positions():
            light_trails.append(light_trail)

    if position in light_trails:
        return True

    return False

# in_bounds ... Checks if a tuple (x, y) are in bounds of the tuple bounds.
def in_bounds(position, bounds):
    if position[0] <= 0 or position[0] >= bounds[1]:
        return False

    if position[1] <= 0 or position[1] >= bounds[0]:
        return False

    return True

if __name__ == '__main__':
    main()