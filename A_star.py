import heapq


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def A_star(app):
    # print("A_STAR_START")
    start = app.start_node
    end = app.end_node
    came_from = {}

    pq = []
    g_cost, h_cost, f_cost = {}, {}, {}  # (start -> cur), (cur -> end), (sum of both)
    g_cost[start] = 0
    h_cost[start] = heuristic(start, end)
    f_cost[start] = g_cost[start] + h_cost[start]
    heapq.heappush(pq, (f_cost[start], start))

    def step():
        if not pq:
            return

        _, current = heapq.heappop(pq)

        if current != start:
            app.canvas.itemconfig(app.grid[current[0]][current[1]], fill="yellow")
            app.canvas.update_idletasks()  # Force update canvas

        if current == end:
            reconstruct_path(app, came_from, current)
            return True

        for neighbor in get_neighbors(app, current):
            tentative_g_cost = g_cost[current] + 1
            if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g_cost
                h_cost[neighbor] = heuristic(neighbor, end)
                f_cost[neighbor] = g_cost[neighbor] + h_cost[neighbor]
                heapq.heappush(pq, (f_cost[neighbor], neighbor))

        app.root.after(20, step)

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
