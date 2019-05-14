import pyglet
snake_tiles= {}

for path in TILES_DIRECTORY.glob("*.png"):
    snake_tiles[path.stem] = pyglet.image.load(str(path))
print(had)
