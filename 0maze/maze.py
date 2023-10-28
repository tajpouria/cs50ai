import sys
from copy import deepcopy
import matplotlib.pyplot as plt

# Read the sample number from the command line argument
sample_no = sys.argv[1]


# Function to convert a maze from a text file to a 2D list
def convert_maze(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    maze = []
    for line in lines:
        row = []
        for char in line.strip():
            if char == "#":
                row.append(0)  # Wall
            elif char == ".":
                row.append(1)  # Open path
            elif char == "a":
                row.append(2)  # Start point
            elif char == "b":
                row.append(3)  # End point
        maze.append(row)

    return maze


# Function to convert a maze to an image and save it
def maze_to_image(maze, output_path):
    # Define the color map for different elements in the maze
    cmap = plt.cm.colors.ListedColormap(["brown", "black", "yellow", "green", "orange"])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    # Plot the maze
    plt.imshow(maze, cmap=cmap, norm=norm)
    plt.grid(True, which="both", color="white")
    plt.axis("off")  # Hide the axis
    plt.tight_layout()  # Remove white space around the edges
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)


# Function to print the maze
def print_maze(maze):
    for row in maze:
        print(row)


# Function to find a path through the maze using Depth-First Search (DFS)
def find_path_dfs(maze):
    _maze = deepcopy(maze)

    # Find the start and end points in the maze
    start, end = (0, 0), (len(_maze[0]) - 1, len(_maze) - 1)
    for i, row in enumerate(_maze):
        for j, cell in enumerate(row):
            if cell == 2:
                start = (i, j)
            elif cell == 3:
                end = (i, j)

    print(f"Start {start}")
    print(f"End {end}")

    # Depth-First Search (DFS) algorithm
    def dfs():
        stack = [
            (start, [start])
        ]  # Initialize the stack with the start point and its path
        visited = set()  # Keep track of visited cells

        while stack:
            (x, y), path = stack.pop()  # Get the current cell and its path
            if (x, y) == end:
                return path  # Path found
            if (x, y) in visited:
                continue
            visited.add((x, y))

            # Check adjacent cells (up, down, left, right)
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for nx, ny in neighbors:
                if (
                    0 <= nx < len(_maze)
                    and 0 <= ny < len(_maze[0])
                    and _maze[nx][ny] != 0
                ):
                    stack.append(((nx, ny), path + [(nx, ny)]))

        return None  # No path found

    # Call the DFS function to find a path
    path = dfs()

    if path:
        print("Path found:")
        print(path)
    else:
        print("No path found.")

    if path:
        for x, y in path:
            # Do not overwrite start and end points
            if _maze[x][y] not in [2, 3]:
                _maze[x][y] = 4  # Mark the path in the maze

    return _maze


# Function to find a path through the maze using Breadth-First Search (BFS)
def find_path_bfs(maze):
    _maze = deepcopy(maze)

    # Find the start and end points in the maze
    start, end = (0, 0), (len(_maze[0]) - 1, len(_maze) - 1)
    for i, row in enumerate(_maze):
        for j, cell in enumerate(row):
            if cell == 2:
                start = (i, j)
            elif cell == 3:
                end = (i, j)

    print(f"Start {start}")
    print(f"End {end}")

    # Breadth-First Search (BFS) algorithm
    def bfs():
        queue = [
            (start, [start])
        ]  # Initialize the queue with the start point and its path
        visited = set()  # Keep track of visited cells

        while queue:
            (x, y), path = queue.pop(0)  # Get the current cell and its path
            if (x, y) == end:
                return path  # Path found
            if (x, y) in visited:
                continue
            visited.add((x, y))

            # Check adjacent cells (up, down, left, right)
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for nx, ny in neighbors:
                if (
                    0 <= nx < len(_maze)
                    and 0 <= ny < len(_maze[0])
                    and _maze[nx][ny] != 0
                ):
                    queue.append(((nx, ny), path + [(nx, ny)]))

        return None  # No path found

    # Call the BFS function to find a path
    path = bfs()

    if path:
        print("Path found:")
        print(path)
    else:
        print("No path found.")

    if path:
        for x, y in path:
            # Do not overwrite start and end points
            if _maze[x][y] not in [2, 3]:
                _maze[x][y] = 4  # Mark the path in the maze

    return _maze


# Convert the maze from a text file
maze = convert_maze(f"samples/maze{sample_no}.txt")

# Find a path using DFS and BFS
dfs_maze = find_path_dfs(maze)
bfs_maze = find_path_bfs(maze)

# Convert the maze with the found path to images
maze_to_image(dfs_maze, f"samples/maze{sample_no}_dfs.png")
maze_to_image(bfs_maze, f"samples/maze{sample_no}_bfs.png")
