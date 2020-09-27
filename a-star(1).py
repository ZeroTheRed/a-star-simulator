import pygame
import time
import math
from collections import deque

run = True
draw_mode = False
left_click = False
right_click = False
color = None
X_LENGTH = 300
Y_LENGTH = 350
CELL_SIZE = 10
start = None
goal = None
astar = False

pygame.init()
surface = pygame.display.set_mode((X_LENGTH, Y_LENGTH))
surface.fill((255, 255, 255))
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TEAL = (255, 255, 0)
PINK = (0, 0, 255)

def draw_grid(cells):
    cell_size = CELL_SIZE

    for x in range(X_LENGTH):
        for y in range(5, Y_LENGTH):
            cell = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            cells.append(cell)
            pygame.draw.rect(surface, BLACK, cell, 1)

    return cells

def h(current_x, current_y, goal_x, goal_y):
    return math.sqrt(((current_x - goal_x)**2) + ((current_y - goal_y)**2))

def g(current_x, current_y, start_x, start_y):
    return math.sqrt(((current_x - start_x)**2) + ((current_y - start_y)**2))

def a_star(grid, start, goal):
    goal_found = False
    visual = True

    gScore = [[float('infinity') for row in range(len(grid[0]))] for col in range(len(grid))]
    print(len(gScore[0]), len(gScore))
    gScore[start[0]][start[1]] = 0

    fScore = [[float('infinity') for row in range(len(grid[0]))] for col in range(len(grid))]
    fScore[start[0]][start[1]] = h(start[0], start[1], goal[0], goal[1])

    open_set = [(start[0], start[1], fScore[start[0]][start[1]], gScore[start[0]][start[1]])]
    closed_set = []
    node_tree = {}

    neighbor_check = [[0, -1],
                      [-1, -1],
                      [-1, 0],
                      [-1, 1],
                      [0, 1],
                      [1, 1],
                      [1, 0],
                      [1, -1]]

    while len(open_set) != 0:
        open_set.sort(key = lambda tup: tup[2], reverse = True)
        current_node = open_set.pop()
        closed_set.append(current_node)
        current_x, current_y, current_f, current_g = current_node

        if current_x == goal[0] and current_y == goal[1]:
            goal_found = True
            #print("Goalie!")
            break

        for i in neighbor_check:
            neighbor_x = current_x + i[0]
            neighbor_y = current_y + i[1]
            temp_g = g(neighbor_x, neighbor_y, start[0], start[1])
            temp_f = temp_g + h(neighbor_x, neighbor_y, goal[0], goal[1])
            neighbor_node = (neighbor_x, neighbor_y, temp_f, temp_g)
            if grid[neighbor_y][neighbor_x] != 1:
                if neighbor_node not in closed_set:
                    if temp_g < gScore[neighbor_x][neighbor_y]:
                        gScore[neighbor_x][neighbor_y] = temp_g
                        fScore[neighbor_x][neighbor_y] = temp_f
                        node_tree[neighbor_node] = current_node
                        if visual == True:
                            pygame.draw.rect(surface, TEAL, (neighbor_x * 10, (neighbor_y * 10) + 50, 10, 10))
                            pygame.draw.rect(surface, BLACK, (neighbor_x * 10, (neighbor_y * 10) + 50, 10, 10), 1)
                            time.sleep(0.01)
                            pygame.display.update()
                        if neighbor_node not in open_set:
                            open_set.append(neighbor_node)

    if goal_found == True:
        route = deque()
        route.appendleft(current_node)
        while current_node in node_tree:
            current_node = node_tree[current_node]
            route.appendleft(current_node)
            pygame.draw.rect(surface, PINK, (current_node[0] * 10, (current_node[1] * 10) + 50, 10, 10))
            pygame.draw.rect(surface, BLACK, (current_node[0] * 10, (current_node[1] * 10) + 50, 10, 10), 1)
            time.sleep(0.001)
            pygame.display.update()

        time.sleep(5)

    else:
        print("There is no path from start to goal :(")

cells = []
draw_grid(cells)
grid = [[0 for x in range(X_LENGTH // CELL_SIZE)] for y in range((Y_LENGTH // CELL_SIZE)-5)]
print(len(grid[0]), len(grid))

obstacle_rect = pygame.Rect(4, 4, 30, 10)
start_rect = pygame.Rect(4, 16, 30, 10)
goal_rect = pygame.Rect(4, 28, 30, 10)

pygame.draw.rect(surface, GREY, obstacle_rect)
pygame.draw.rect(surface, GREEN, start_rect)
pygame.draw.rect(surface, RED, goal_rect)

pygame.display.update()

while run == True:
    if obstacle_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        color = GREY

    elif start_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        color = GREEN

    elif goal_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        color = RED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            draw_mode = True
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] > 50:
                if event.button == 1:
                    left_click = True
                    pygame.draw.rect(surface, color, (mouse_pos[0] - (mouse_pos[0]%10), mouse_pos[1] - (mouse_pos[1]%10), 10, 10))
                    pygame.draw.rect(surface, BLACK, (mouse_pos[0] - (mouse_pos[0] % 10), mouse_pos[1] - (mouse_pos[1] % 10), 10, 10), 1)
                    if color == GREY:
                        grid[((mouse_pos[1] - (mouse_pos[1] % 10)) - 50) // 10][(mouse_pos[0] - (mouse_pos[0]%10)) // 10] = 1
                    elif color == GREEN:
                        grid[((mouse_pos[1] - (mouse_pos[1] % 10)) - 50) // 10][(mouse_pos[0] - (mouse_pos[0]%10)) // 10]= 5
                        start = ((mouse_pos[0] - (mouse_pos[0] % 10)) // 10, ((mouse_pos[1] - (mouse_pos[1] % 10)) - 50) // 10)
                    elif color == RED:
                        grid[((mouse_pos[1] - (mouse_pos[1] % 10)) - 50) // 10][(mouse_pos[0] - (mouse_pos[0]%10)) // 10]= 6
                        goal = ((mouse_pos[0] - (mouse_pos[0] % 10)) // 10, ((mouse_pos[1] - (mouse_pos[1] % 10)) - 50) // 10)
                    pygame.display.update()
                else:
                    right_click = True
                    pygame.draw.rect(surface, WHITE, (mouse_pos[0] - (mouse_pos[0] % 10), mouse_pos[1] - (mouse_pos[1] % 10), 10, 10))
                    pygame.draw.rect(surface, BLACK, (mouse_pos[0] - (mouse_pos[0] % 10), mouse_pos[1] - (mouse_pos[1] % 10), 10, 10), 1)
                    grid[((mouse_pos[1] - (mouse_pos[1] % 10)) - 50) // 10][(mouse_pos[0] - (mouse_pos[0] % 10)) // 10] = 0
                    pygame.display.update()


        elif event.type == pygame.MOUSEBUTTONUP:
            draw_mode = False
            left_click = False
            right_click = False

        elif event.type == pygame.MOUSEMOTION:
            if draw_mode == True:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[1] > 50:
                    if left_click:
                        pygame.draw.rect(surface, color, (mouse_pos[0] - (mouse_pos[0] % 10), mouse_pos[1] - (mouse_pos[1] % 10), 10, 10))
                        pygame.draw.rect(surface, BLACK, (mouse_pos[0] - (mouse_pos[0] % 10), mouse_pos[1] - (mouse_pos[1] % 10), 10, 10), 1)
                        if color == GREY:
                            grid[((mouse_pos[1] - (mouse_pos[1] % 10)) - 50) // 10][(mouse_pos[0] - (mouse_pos[0] % 10)) // 10] = 1
                        elif color == GREEN:
                            grid[((mouse_pos[1] - (mouse_pos[1] % 10)) - 50) // 10][(mouse_pos[0] - (mouse_pos[0] % 10)) // 10] = 5
                        elif color == RED:
                            grid[((mouse_pos[1] - (mouse_pos[1] % 10)) - 50) // 10][(mouse_pos[0] - (mouse_pos[0] % 10)) // 10] = 6
                        pygame.display.update()
                    elif right_click:
                        pygame.draw.rect(surface, WHITE, (mouse_pos[0] - (mouse_pos[0] % 10), mouse_pos[1] - (mouse_pos[1] % 10), 10, 10))
                        pygame.draw.rect(surface, BLACK, (mouse_pos[0] - (mouse_pos[0] % 10), mouse_pos[1] - (mouse_pos[1] % 10), 10, 10), 1)
                        grid[((mouse_pos[1] - (mouse_pos[1] % 10)) - 50) // 10][(mouse_pos[0] - (mouse_pos[0] % 10)) // 10] = 0
                        pygame.display.update()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                for row in grid:
                    line = " ".join(str(row))
                    print(line)
                print(start, goal)
                astar = True

        if astar == True:
            a_star(grid, start, goal)
            run = False





