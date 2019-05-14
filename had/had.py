import pyglet
import random
from pathlib import Path

TILE_SIZE = 64
TILES_DIRECTORY = Path('snake-tiles')

class State:
    def __init__(self):
        self.food = []
        self.snake = [(0, 0), (1, 0)]
        self.snake_direction = 0, 1
        self.width = 10
        self.height = 10
        self.add_food()
        self.add_food()
        self.add_food()
        self.snake_alive = True

    def move(self):
        if not self.snake_alive:
            return
        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y
        new_head = new_x, new_y
              
        """kus kodu Pavla
        x = 0
        y = 1
        self.snake[-1], self.snake_direction = last_head, s_dir
        new_head = last_head[x]+s_dir[x], last_head[y]+s_dir[y]
        
        if not (0 < new_head[x] <= self.width):
            self.snake_alive = False             
        """
        
        if new_x < 0:
            self.snake_alive = False
        if new_y < 0:
            self.snake_alive = False
        if new_x >= self.width:
            self.snake_alive = False
        if new_y > self.height:
            self.snake_alive = False

        if new_head in self.snake:
            self.snake_alive = False

        self.snake.append(new_head)
        if new_head in self.food:
            self.food.remove(new_head)
            self.add_food()
        else:
            del self.snake[0]

    def add_food(self):
        for nu in range(100):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            if (position not in self.snake) and (position not in self.food):
                self.food.append(position)
                return

window = pyglet.window.Window()
state = State()

state.width = window.width // TILE_SIZE
state.height = window.height // TILE_SIZE

apple_image = pyglet.image.load("apple.png")
snake_tiles= {}
for path in TILES_DIRECTORY.glob("*.png"):
    snake_tiles[path.stem] = pyglet.image.load(str(path))

def direction(a, b):
    if a == "nic":
        return "end"
    if b[0] - a[0] == 1:
        return "left"
    if b[0] - a[0] == -1:
        return "right"
    if b[1] - a[1] == 1:
        return "bottom"
    if b[1] - a[1] == -1:
        return "top"
    return "end"

@window.event
def on_draw():
    window.clear()
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    for a, b, c in zip((["nic"] + state.snake[:-1]), state.snake, (state.snake[1:] + ["nic"])):
        x, y = b
        source = direction(a, b)
        dest = direction(c, b)
        if dest == 'end' and not state.snake_alive:
            dest = 'dead'
        snake_tiles[source + "-" + dest].blit(x * TILE_SIZE,
                         y * TILE_SIZE,
                         width=TILE_SIZE,
                         height=TILE_SIZE)
    for x, y in state.food:
        apple_image.blit(x * TILE_SIZE,
                         y * TILE_SIZE,
                         width=TILE_SIZE,
                         height=TILE_SIZE)

def move(dt):
    state.move()

@window.event
def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.LEFT:
        state.snake_direction = -1, 0
    if key_code == pyglet.window.key.RIGHT:
        state.snake_direction = 1, 0
    if key_code == pyglet.window.key.UP:
        state.snake_direction = 0, 1
    if key_code == pyglet.window.key.DOWN:
        state.snake_direction = 0, -1

pyglet.clock.schedule_interval(move, 1/6)

pyglet.app.run()
