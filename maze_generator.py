import random

def generate_maze(width=41, height=41):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # these are directions for moving down, right, up, left like in videogames lol.
        random.shuffle(directions) # this randomizes the directions so that there is no specific pattern.
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2 # we basiaclly move 2 steps in the direction we want to carve. both steps are carved if conditions are met.
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1: # checks if nx and ny are still within bounds, and if the cell is a wall, if it's a wall, we carve it.
                maze[y + dy][x + dx] = 0 # we carve the wall between the cell we were at and the nx, ny cell.
                maze[ny][nx] = 0 # we carve the nx, ny cell itself.
                carve(nx, ny) # we keep recursively carving until the condition above is not met anymore.

    # Ensure odd dimensions (so walls don't block everything and to avoid going out of bounds when jumping +2 from an odd cell) 
    # it also makes walls be in even positions while paths be in odd position naturally.
    if width % 2 == 0: width += 1
    if height % 2 == 0: height += 1

    # Set entrance and exit manually (very obvious..)
    maze[0][1] = 0
    maze[height - 1][width - 2] = 0

    # Start from (1,1) and begin carving (also very obvious)
    maze[1][1] = 0
    carve(1, 1)

    # Add loops (multiple solutions)
    extra_openings = (width * height) // 10 # so for example, 41x41 = 1681, 1681 // 10 = 168, so we will add 168 extra openings, this obviously adds multiple solutions..
    for _ in range(extra_openings):
        # this keeps the x,y coordinates within bounds, we use -2 because pythons indexing starts at 0 and so we need to be less than 4, not only 5.
        x = random.randint(1, width - 2) 
        y = random.randint(1, height - 2)
        if maze[y][x] == 1:
            maze[y][x] = 0

    return maze # it's returned as a 2D List, Path = 0, Wall = 1
