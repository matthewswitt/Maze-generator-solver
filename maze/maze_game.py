import pygame
import random

# Define colours in RBG
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# initialise pygame
pygame.init()
window = pygame.display.set_mode((650, 650))
pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()

# setup maze variables
x = 0
y = 0
w = 20
grid = []
visited = []
stack = []
solution = {}


# builds the 30 by 30 grid
def build_grid(x, y, w):
    for i in range(1, 31):
        x = 20
        y = y + 20
        for j in range(1, 31):
            pygame.draw.line(window, WHITE, [x, y], [x + w, y])
            pygame.draw.line(window, WHITE, [x + w, y], [x + w, y + w])
            pygame.draw.line(window, WHITE, [x + w, y + w], [x, y + w])
            pygame.draw.line(window, WHITE, [x, y + w], [x, y])

            grid.append((x, y))
            x = x + 20
    # blacks out two parts of the grid to indicate start and end
    pygame.draw.line(window, BLACK, [20, 20], [20, 39])
    pygame.draw.line(window, BLACK, [620, 600], [620, 619])


# creates a cell in the up direction
def up(x, y):
    pygame.draw.rect(window, BLUE, (x + 1, y - w + 1, 19, 39), 0)
    pygame.display.update()


# creates a cell in the down direction
def down(x, y):
    pygame.draw.rect(window, BLUE, (x + 1, y + 1, 19, 39), 0)
    pygame.display.update()


# creates a cell in the left direction
def left(x, y):
    pygame.draw.rect(window, BLUE, (x - w + 1, y + 1, 39, 19), 0)
    pygame.display.update()


# creates a cell in the right direction
def right(x, y):
    pygame.draw.rect(window, BLUE, (x + 1, y + 1, 39, 19), 0)
    pygame.display.update()


# creates a single width cell
def single_cell(x, y):
    pygame.draw.rect(window, GREEN, (x + 1, y + 1, 18, 18), 0)
    pygame.display.update()


# re-colours the path after single_cell has visited it
def backtracking_cell(x, y):
    pygame.draw.rect(window, BLUE, (x + 1, y + 1, 18, 18), 0)
    pygame.display.update()


# creates a small rectangle within each cell showing the solution
def solution_cell(x, y):
    pygame.draw.rect(window, WHITE, (x + 8, y + 8, 5, 5), 0)
    pygame.display.update()


# creates the maze
def create_maze(x, y):
    # the cell the maze is currently on
    single_cell(x, y)

    # appends the coordinates to stack and visited to know where to
    # backtrack and where it has visited
    stack.append((x, y))
    visited.append((x, y))

    # loop continues until stack is empty
    while len(stack) > 0:
        cell = []

        # next if statements determine whether or not a cell
        # can be created in a certain direction from current location
        if (x + w, y) not in visited and (x + w, y) in grid:
            cell.append("R")

        if (x - w, y) not in visited and (x - w, y) in grid:
            cell.append("L")

        if (x, y + w) not in visited and (x, y + w) in grid:
            cell.append("D")

        if (x, y - w) not in visited and (x, y - w) in grid:
            cell.append("U")

        # chooses a random way for a new cell to be created and
        # creates a blue square there and adds it to the lists stack
        # and visited
        if len(cell) > 0:
            cell_chosen = (random.choice(cell))

            if cell_chosen == "R":
                right(x, y)
                solution[(x + w, y)] = x, y
                x += w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "L":
                left(x, y)
                solution[(x - w, y)] = x, y
                x -= w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "D":
                down(x, y)
                solution[(x, y + w)] = x, y
                y += w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "U":
                up(x, y)
                solution[(x, y - w)] = x, y
                y -= w
                visited.append((x, y))
                stack.append((x, y))
        # if there is nowhere for the cell to go, it removes itself
        # from stack and begins to backtrack
        else:
            x, y = stack.pop()
            single_cell(x, y)
            backtracking_cell(x, y)


# solves the maze and illustrates the shortest path back to the start
def solve_maze(x, y):
    solution_cell(x, y)
    pygame.draw.rect(window, WHITE, (10, 28, 5, 5), 0)
    pygame.draw.rect(window, WHITE, (630, 608, 5, 5), 0)
    while (x, y) != (20, 20):
        x, y = solution[x, y]
        solution_cell(x, y)


# starting position and calling functions
x, y = 20, 20
build_grid(0, 0, 20)
create_maze(x, y)
solve_maze(600, 600)

# pygame loop
running = True
while running:
    # keep running at 30 FPS
    clock.tick(30)
    # process input
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False

