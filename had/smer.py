snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]
snake_old = ["nic"] + snake[:-1]
snake_new = snake[1:] + ["nic"]

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


for a, b, c in zip((["nic"] + snake[:-1]), snake, (snake[1:] + ["nic"])):
    x, y = b
    odkud = direction(a, b)
    kam = direction(c, b)
    print(x, y, odkud, kam)


#for x, y in snake:
 #   print(x, y)


#print(snake_old)
#print(snake)
#print(snake_new)