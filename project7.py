
from collections import deque

maze = [
    ["S", " ", "#", " ", " ", " "],
    ["#", " ", "#", " ", "#", " "],
    [" ", " ", " ", " ", "#", " "],
    [" ", "#", "#", " ", " ", " "],
    [" ", " ", " ", "#", "#", " "],
    ["#", "#", " ", " ", " ", "E"]
]

def find_position(symbol):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == symbol:
                return (row, col)
    return None


def solve_maze():
    start = find_position("S")
    end = find_position("E")

    if start is None or end is None:
        print("Start or exit not found!")
        return

    queue = deque([[start]])
    visited = {start}

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == end:
            for row, col in path[1:-1]:
                maze[row][col] = "*"

            print("\nShortest path found!\n")
            display_maze()
            print("Path length:", len(path) - 1)
            return

        row, col = current

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            new_position = (new_row, new_col)

            if (
                0 <= new_row < len(maze)
                and 0 <= new_col < len(maze[0])
                and maze[new_row][new_col] != "#"
                and new_position not in visited
            ):
                visited.add(new_position)
                queue.append(path + [new_position])

    print("No path found!")


def display_maze():
    for row in maze:
        print(" ".join(row))


print("===== MAZE SOLVER =====")
print("S = Start | E = Exit")
print("# = Wall | * = Path\n")

display_maze()
solve_maze()
