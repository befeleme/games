import pyglet, math, random
from pyglet import gl

def draw_circle(x, y, radius):
    iterations = 20
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dy = radius, 0

    gl.glBegin(gl.GL_LINE_STRIP)
    for i in range(iterations+1):
        gl.glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    gl.glEnd()
    
def distance(a, b, wrap_size):
    """Distance in one direction (x or y)"""
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result

def overlaps(a, b):
    """Returns true iff two space objects overlap"""
    distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared
    
def load_image(path):
    image = pyglet.image.load(path)
    # set center of rotation to image center
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2 
    return image

asteroid_image = load_image('meteorBrown_med1.png')
image = load_image('playerShip2_blue.png')

# set of codes of all pressed keys
pressed_keys = set()

# constants
ROTATION_SPEED = 6  # rad/s
ACCELERATION = 20  # px/s^2


class SpaceObject:
    def __init__(self):
        # Set position to the center of window
        self.x = window.width / 2
        self.y = window.height / 2
        self.rotation = 0
        self.x_speed = 0  
        self.y_speed = 0
    
    def draw(self):
        #Copy position to the sprite
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = 90 - math.degrees(self.rotation)
        self.sprite.draw() 
        
    def tick(self, dt):
         # Update position based on speed
        self.x = self.x + self.x_speed * dt
        self.y = self.y + self.y_speed * dt 
        
         # Return to the window if it flies out 
        self.x = self.x % window.width
        self.y = self.y % window.height 
        
    def hit_by_spaceship(self, spaceship):
        pass

class Spaceship(SpaceObject):
    radius = 25
    
    def __init__(self):
        super().__init__()
        self.sprite = pyglet.sprite.Sprite(image)
        
    def tick(self, dt):
        # Rotate if relf/right arrows are pressed
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation = self.rotation + ROTATION_SPEED * dt
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation = self.rotation - ROTATION_SPEED * dt
            
        # Accelerate if up arrow is pressed
        if pyglet.window.key.UP in pressed_keys:
            self.x_speed = self.x_speed + ACCELERATION * math.cos(self.rotation)
            self.y_speed = self.y_speed + ACCELERATION * math.sin(self.rotation)
        
        super().tick(dt)
        #self.x_speed = self.x_speed * 0.98
        #self.y_speed = self.y_speed * 0.98
        
        # Handle collisions
        for obj in objects:
            if overlaps(self, obj) and self != obj:
                obj.hit_by_spaceship(self)
                
          

class Asteroid(SpaceObject):
    radius = 25
    def __init__(self):
        super().__init__()
        self.sprite = pyglet.sprite.Sprite(asteroid_image)
        
        # Start at the edge of window
        if random.randrange(0, 2) == 0:
            # Bottom edge
            self.y = 0
            self.x = random.randrange(0, window.width)
        else:
            # Left edge
            self.x = 0
            self.y = random.randrange(0, window.width)
        
        self.x_speed = random.randrange(-100, 100)
        self.y_speed = random.randrange(-100, 100) 
        
    def hit_by_spaceship(self, spaceship):
        if spaceship in objects:
            objects.remove(spaceship)
                  
    """def draw(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = 90 - math.degrees(self.rotation)
        self.sprite.draw()"""
           

window = pyglet.window.Window()
objects = []

# Create 1 spaceship and add it to the list of objects
spaceship = Spaceship()
objects.append(spaceship)

# Create asteroid
for i in range(2):
    asteroid = Asteroid()
    objects.append(asteroid)

def draw():
    """Draw all objects in the game"""
    window.clear()
    for obj in objects:
        obj.draw()
        draw_circle(obj.x, obj.y, obj.radius)

def tick(dt):
    """Update all objects in the game"""
    for obj in objects:
        obj.tick(dt)
    
def key_press(key, mod):
    """Add a key code to the set of pressed keys"""
    pressed_keys.add(key)
  
def key_release(key, mod):
    """Remove a key code from the set of pressed keys"""
    pressed_keys.discard(key)

# Register functions Pyglet should call on various events
window.push_handlers(
    on_draw=draw,
    on_key_press=key_press,
    on_key_release=key_release,
    )
    
pyglet.clock.schedule_interval(tick, 1/30)

# Run it all!
pyglet.app.run()
