def DFS(app):
    # print("DFS_START")
    start = app.start_node
    end = app.end_node
    came_from = {}

    stack = [start]
    visited = set()
    visited.add(start)

    def step():
        if not stack:
            return

        current = stack.pop()

        if current != start:
            app.canvas.itemconfig(app.grid[current[0]][current[1]], fill="yellow")
            app.canvas.update_idletasks()

        if current == end:
            reconstruct_path(app, came_from, current)
            return True

        for neighbor in get_neighbors(app, current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)

        app.root.after(20, step)
        return False

    app.root.after(20, step)
    return False


def reconstruct_path(app, came_from, current):
    while current in came_from:
        app.canvas.itemconfig(app.grid[current[0]][current[1]], fill="green")
        current = came_from[current]
    app.canvas.itemconfig(app.grid[current[0]][current[1]], fill="green")
    app.canvas.update_idletasks()


def get_neighbors(app, node):
    row, col = node
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r, c in directions:
        new_r, new_c = row + r, col + c
        if 0 <= new_r < app.n and 0 <= new_c < app.n:
            if app.canvas.itemcget(app.grid[new_r][new_c], "fill") != "black":
                neighbors.append((new_r, new_c))

    return neighbors
