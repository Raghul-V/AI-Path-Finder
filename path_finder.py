import pygame
from pygame.locals import *
import sys
import tkinter_gui
from frontiers import *
import time


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = [[" " for _ in range(size)] for _ in range(size)]
        self.start = (0, 0)
        self.end = (size-1, size-1)
        self.steps = 0
        self.req_steps = 0

    def can_move_to(self, position):
        try:
            i, j = position
            return self.maze[i][j] != "#"
        except:
            return False

    def all_possible_moves(self, state, allow_diagonal):
        i, j = state
        moves = []
        if allow_diagonal:
            change_in_coor = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        else:
            change_in_coor = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for x, y in change_in_coor:
            if i + x < 0 or j + y < 0:
                continue
            if self.can_move_to(position=(i + x, j + y)):
                moves.append((i + x, j + y))
        return moves

    def find_path(self, search_algorithm, allow_diagonal):
        if search_algorithm == "Depth First Search":
            self.frontier = DFS_Frontier()
        elif search_algorithm == "Breadth First Search":
            self.frontier = BFS_Frontier()
        elif search_algorithm == "Greedy Best-First Search":
            self.frontier = GBFS_Frontier(self.end)
        elif search_algorithm == "A* Search":
            self.frontier = A_star_Frontier(self.end)
        else:
            return False

        node = Node(self.start, None, None)
        if search_algorithm == "A* Search":
            self.frontier.add(node, 0)
        else:
            self.frontier.add(node)

        self.explored = set()
        self.path = []


        def backtrack_path(node):
            self.path.append(node)
            
            while node.parent is not None:
                self.path.append(node.parent)
                i, j = node.state
                if (i, j) != self.start and (i, j) != self.end:
                    self.maze[i][j] = "."
                node = node.parent
            
            self.path.reverse()
            return self.path


        while True:
            try:
                node = self.frontier.remove()
            except:
                tkinter_gui.message("showInfo", "No Solution", 
                    "Sorry, your maze has no possible solution!")
                return

            self.explored.add(node.state)
            
            update_screen(bg_color=(0, 0, 0), show_all_path=show_all)
            time.sleep(10/(self.size*self.size))

            i, j = node.state
            if (i, j) != self.start and (i, j) != self.end:
                self.maze[i][j] = "X"

            if node.state == self.end:
                backtrack_path(node)
                break

            self.steps += 1

            for move in self.all_possible_moves(node.state, allow_diagonal):
                if not self.frontier.contains_state(move) and \
                        move not in self.explored:
                    new_node = Node(move, node, None)
                    if new_node.state == self.end:
                        backtrack_path(new_node)
                        break
                    if search_algorithm == "A* Search":
                        if move[0] != node.state[0] and move[1] != node.state[1] \
                                and allow_diagonal:
                            g_cost = node.g_cost + 1.4
                        else:
                            g_cost = node.g_cost + 1
                        self.frontier.add(new_node, g_cost)
                    else:
                        self.frontier.add(new_node)
            if len(self.path) != 0:
                break

        self.req_steps = len(self.path)-1
        update_screen(bg_color=(0, 0, 0), show_all_path=show_all)

    def display_maze(self, show_all=False):
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i][j] == " " or (not show_all and self.maze[i][j] == "X"):
                    color = (255, 255, 255)
                elif self.maze[i][j] == "#":
                    color = (50, 50, 50)
                elif self.maze[i][j] in ("A", "B"):
                    color = (255, 0, 255)
                elif self.maze[i][j] == "X":
                    color = (255, 255, 0)
                elif self.maze[i][j] == ".":
                    color = (0, 255, 0)
                pygame.draw.rect(
                    screen, color, (j * BOX_WIDTH + 0.5, HEADER_HEIGHT + i * BOX_WIDTH + 0.5,
                        BOX_WIDTH - 1, BOX_WIDTH - 1)
                )

        return True



def initialize_game():
    global clock, SCREEN_WIDTH, SCREEN_HEIGHT
    global HEADER_HEIGHT
    global NUM_OF_BOX, algorithm, show_all, allow_diagonal
    global BOX_WIDTH, screen
    global my_maze, state, is_mouseButton_down

    pygame.quit()
    pygame.init()
    
    clock = pygame.time.Clock()

    SCREEN_WIDTH, SCREEN_HEIGHT = (600, 705)
    HEADER_HEIGHT = SCREEN_HEIGHT - SCREEN_WIDTH
    
    try:
        NUM_OF_BOX, algorithm, show_all, allow_diagonal = tkinter_gui.get_inputs()
    except ValueError:
        pygame.quit()
        sys.exit()

    BOX_WIDTH = SCREEN_WIDTH / NUM_OF_BOX
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Path-Finding Search Algorithms")
    
    my_maze = Maze(NUM_OF_BOX)
    state = "A"
    is_mouseButton_down = False


def display_header():
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))

    font = pygame.font.Font("freesansbold.ttf", 18)

    text = font.render(f"Total no.of steps taken :     {my_maze.steps}", True, (10, 10, 10))
    screen.blit(text, (30, 15))
    text = font.render(f"Required no.of steps     :     {my_maze.req_steps}", True, (10, 10, 10))
    screen.blit(text, (30, 45))
    text = font.render(f"Searching Algorithm     :     {algorithm}", True, (10, 10, 10))
    screen.blit(text, (30, 75))


def update_screen(bg_color, show_all_path=False):
    screen.fill(bg_color)
    display_header()
    my_maze.display_maze(show_all_path)
    pygame.display.update()


def cursor_in_maze_pos():
    cursorX, cursorY = pygame.mouse.get_pos()
    i = int((cursorY - HEADER_HEIGHT) // BOX_WIDTH)
    j = int(cursorX // BOX_WIDTH)
    return i, j


initialize_game()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if tkinter_gui.message("askokcancel", "Quit", "Do you want do quit?"):
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if tkinter_gui.message("askokcancel", "Quit", "Do you want do quit?"):
                    pygame.quit()
                    sys.exit()
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if state == "#":
                    state = "search"
        elif event.type == pygame.MOUSEBUTTONUP:
            is_mouseButton_down = False
            if state in ("A", "B"):
                i, j = cursor_in_maze_pos()
                if my_maze.maze[i][j] == " " and i >= 0 and j >= 0:
                    my_maze.maze[i][j] = state
                    if state == "A":
                        state, my_maze.start = "B", (i, j)
                    else:
                        state, my_maze.end = "#", (i, j)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_mouseButton_down = True

    if state == "#" and is_mouseButton_down:
        i, j = cursor_in_maze_pos()
        if my_maze.maze[i][j] == " " and i >= 0 and j >= 0:
            my_maze.maze[i][j] = "#"

    if state == "search":
        my_maze.find_path(algorithm, allow_diagonal)
        if tkinter_gui.message("askokcancel", "Program Ended!", "This program has ended. Do you want to try again?"):
            initialize_game()
        else:
            pygame.quit()
            sys.exit()

    update_screen(bg_color=(0, 0, 0), show_all_path=show_all)


pygame.quit()


