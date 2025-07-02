# algorithms.py
def bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    queue = [start]
    visited = {start: None}
    head = 0  # Acts like deque.popleft()

    while head < len(queue):
        y, x = queue[head]
        head += 1 
        if (y, x) == end: # if we reached the end node, we can stop searching.
            break
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # directions for moving up, down, left, right.
            ny, nx = y + dy, x + dx # this calculates the neighbour coordinates by adding the direction to the current cell coordinates.
            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 0 and (ny, nx) not in visited: # make sure the neighbour is within bounds, and that it's a path(0) and not a wall(1), and that it hasn't been visited yet.
                queue.append((ny, nx)) # add the neighbour to the queue to explore it later.
                visited[(ny, nx)] = (y, x) # store the current cell(y, x) as the previous cell for the neighbour (ny, nx).
    return reconstruct_path(visited, end)


def dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    visited = {start: None} # acts like a dict to store the path

    while stack:
        y, x = stack.pop() 
        if (y, x) == end: # if we reached the end node, we can stop searching.
            break
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #directions for moving up, down, left, right.
            ny, nx = y + dy, x + dx # this calculates the neighbour coordinates by adding the direction to the current cell coordinates.
            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 0 and (ny, nx) not in visited: # make sure the neighbour is within bounds, and that it's a path(0) and not a wall(1), and that it hasn't been visited yet.
                stack.append((ny, nx)) # push the neighbour onto the stack to explore it later.
                visited[(ny, nx)] = (y, x) # store the current cell(y, x) as the previous cell for the neighbour (ny, nx).
    return reconstruct_path(visited, end)


def dijkstra(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    heap = [(0, start)]
    visited = {start: None}
    costs = {start: 0}

    while heap:
        heap.sort()  # sort ascending by cost
        cost, (y, x) = heap.pop(0)
        if (y, x) == end: # if we reached the end node, we can stop searching.
            break
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 0:
                new_cost = cost + 1
                if (ny, nx) not in costs or new_cost < costs[(ny, nx)]: # checks if a newer path to the neighbour is cheaperl
                    costs[(ny, nx)] = new_cost
                    heap.append((new_cost, (ny, nx)))
                    visited[(ny, nx)] = (y, x)
    return reconstruct_path(visited, end)

def astar(maze, start, end):
    from math import dist
    rows, cols = len(maze), len(maze[0])
    open_list = [(heuristic(start, end), 0, start)]  # (f = g + h, g, node)
    visited = {start: None}
    g_score = {start: 0}

    while open_list:
        open_list.sort()  # sort by f = g + h
        _, g, current = open_list.pop(0)
        y, x = current

        if current == end:
            break

        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            neighbor = (ny, nx)
            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 0:
                tentative_g = g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, end)
                    open_list.append((f, tentative_g, neighbor))
                    visited[neighbor] = current
    return reconstruct_path(visited, end)

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(visited, end):
    if end not in visited: # if the end node was never reached in the dictionary, it means there is no path. fa it returns an empty list.
        return []
    path = [] # a list to store the path we will reconstruct.
    current = end # this is the current node we are reconstructing the path from, it starts at the end node.
    while current: # while current is not None: # we keep going back until we reach the start node, which has no previous node.
        path.append(current)
        current = visited[current] # redefines current to the previous node in the path.
    path.reverse() # we reverse the path since we reconstructed it backwards (from end to start).
    return path