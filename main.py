
import pygame
import heapq
import time
from collections import deque

pygame.init()

WIDTH, HEIGHT = 800, 760
CELL_SIZE = 30
COLS = WIDTH // CELL_SIZE
ROWS = 600 // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RescueRoute | Algorithm Comparison")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 20, bold=True)
small_font = pygame.font.SysFont("arial", 16)
title_font = pygame.font.SysFont("arial", 24, bold=True)

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
GRID = (205, 210, 215)
WALL = (80, 80, 80)
GREEN = (40, 180, 80)
RED = (230, 60, 60)
BLUE = (40, 100, 240)
PURPLE = (145, 65, 220)
YELLOW = (255, 220, 70)
BG = (235, 240, 245)
DARK_BG = (30, 35, 45)
MUTED = (190, 200, 215)

START = (1, 1)
END = (24, 17)

walls = set()
explored = []
path = []
algorithm_name = "BFS"
path_color = BLUE
animation_index = 0
animation_delay = 0
animating = False
search_finished = False

message = "Left-click: wall | 1: BFS | 2: A* | C: clear"

stats = {
    "BFS": {"steps": None, "explored": None, "time": None},
    "A*": {"steps": None, "explored": None, "time": None}
}


def get_neighbors(cell):
    x, y = cell

    options = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    ]

    return [
        (nx, ny)
        for nx, ny in options
        if 0 <= nx < COLS
        and 0 <= ny < ROWS
        and (nx, ny) not in walls
    ]


def reconstruct_path(parent, current):
    result = []

    while current is not None:
        result.append(current)
        current = parent[current]

    result.reverse()
    return result


def bfs():
    queue = deque([START])
    parent = {START: None}
    visited = {START}
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)

        if current == END:
            return reconstruct_path(parent, END), order

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return [], order


def heuristic(cell):
    return abs(cell[0] - END[0]) + abs(cell[1] - END[1])


def astar():
    counter = 0
    queue = [(heuristic(START), counter, START)]
    parent = {START: None}
    cost = {START: 0}
    closed = set()
    order = []

    while queue:
        _, _, current = heapq.heappop(queue)

        if current in closed:
            continue

        closed.add(current)
        order.append(current)

        if current == END:
            return reconstruct_path(parent, END), order

        for neighbor in get_neighbors(current):
            new_cost = cost[current] + 1

            if new_cost < cost.get(neighbor, float("inf")):
                cost[neighbor] = new_cost
                parent[neighbor] = current
                counter += 1

                priority = new_cost + heuristic(neighbor)
                heapq.heappush(
                    queue,
                    (priority, counter, neighbor)
                )

    return [], order


def timed_search(function):
    start_time = time.perf_counter()
    result_path, result_explored = function()
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return result_path, result_explored, elapsed_ms


def run_search(use_astar):
    global explored, path, algorithm_name
    global path_color, animation_index, animation_delay
    global animating, search_finished, message, stats

    # Run both algorithms on the same grid for comparison.
    bfs_path, bfs_explored, bfs_time = timed_search(bfs)
    astar_path, astar_explored, astar_time = timed_search(astar)

    stats["BFS"] = {
        "steps": len(bfs_path) - 1 if bfs_path else None,
        "explored": len(bfs_explored),
        "time": bfs_time
    }

    stats["A*"] = {
        "steps": len(astar_path) - 1 if astar_path else None,
        "explored": len(astar_explored),
        "time": astar_time
    }

    if use_astar:
        path = astar_path
        explored = astar_explored
        algorithm_name = "A*"
        path_color = PURPLE
    else:
        path = bfs_path
        explored = bfs_explored
        algorithm_name = "BFS"
        path_color = BLUE

    animation_index = 0
    animation_delay = 0
    animating = True
    search_finished = False

    if path:
        message = f"{algorithm_name}: Exploring cells..."
    else:
        message = f"{algorithm_name}: No route found!"


def clear_all():
    global walls, explored, path, animation_index
    global animating, search_finished, algorithm_name, message, stats

    walls.clear()
    explored = []
    path = []
    animation_index = 0
    animating = False
    search_finished = False
    algorithm_name = "BFS"
    message = "Left-click: wall | 1: BFS | 2: A* | C: clear"

    stats = {
        "BFS": {"steps": None, "explored": None, "time": None},
        "A*": {"steps": None, "explored": None, "time": None}
    }


def draw_dashboard():
    pygame.draw.rect(screen, DARK_BG, (0, 600, WIDTH, 160))

    heading = title_font.render(
        "BFS vs A* | Live Comparison",
        True,
        WHITE
    )
    screen.blit(heading, (18, 608))

    # Two comparison columns.
    pygame.draw.line(screen, MUTED, (400, 645), (400, 725), 1)

    bfs_title = font.render("BFS", True, (100, 160, 255))
    astar_title = font.render("A*", True, (195, 135, 255))

    screen.blit(bfs_title, (22, 645))
    screen.blit(astar_title, (422, 645))

    for name, x in [("BFS", 22), ("A*", 422)]:
        data = stats[name]

        if data["explored"] is None:
            lines = [
                "Path steps: --",
                "Explored cells: --",
                "Search time: --"
            ]
        else:
            steps = (
                str(data["steps"])
                if data["steps"] is not None
                else "No route"
            )

            lines = [
                f"Path steps: {steps}",
                f"Explored cells: {data['explored']}",
                f"Search time: {data['time']:.3f} ms"
            ]

        for i, line in enumerate(lines):
            rendered = small_font.render(line, True, WHITE)
            screen.blit(rendered, (x, 671 + i * 19))

    # Explain the exploration animation.
    note = small_font.render(
        "Yellow = explored | Blue = BFS route | Purple = A* route",
        True,
        MUTED
    )
    screen.blit(note, (18, 735))


def draw():
    screen.fill(BG)

    visible_explored = set(explored[:animation_index])

    for y in range(ROWS):
        for x in range(COLS):
            cell = (x, y)

            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            color = WHITE

            if cell in visible_explored:
                color = YELLOW

            if cell in walls:
                color = WALL

            if search_finished and cell in path:
                color = path_color

            if cell == START:
                color = GREEN
            elif cell == END:
                color = RED

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID, rect, 1)

    draw_dashboard()
    pygame.display.flip()


running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if my < 600:
                cell = (mx // CELL_SIZE, my // CELL_SIZE)

                if event.button == 1:
                    if cell != START and cell != END:
                        if cell in walls:
                            walls.remove(cell)
                        else:
                            walls.add(cell)

                        explored = []
                        path = []
                        animating = False
                        search_finished = False

                        stats = {
                            "BFS": {
                                "steps": None,
                                "explored": None,
                                "time": None
                            },
                            "A*": {
                                "steps": None,
                                "explored": None,
                                "time": None
                            }
                        }

                        message = "Grid changed. Press 1 or 2 to compare."

                elif event.button == 3:
                    run_search(False)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                run_search(False)

            elif event.key == pygame.K_2:
                run_search(True)

            elif event.key == pygame.K_c:
                clear_all()

    if animating:
        animation_delay += 1

        if animation_delay >= 2:
            animation_delay = 0
            animation_index += 1

            if animation_index >= len(explored):
                animation_index = len(explored)
                animating = False
                search_finished = True

                if path:
                    message = "Route found! Compare the dashboard results."
                else:
                    message = "No route found. Try removing some walls."

    draw()

pygame.quit()
