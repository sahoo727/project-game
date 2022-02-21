import pygame
import requests

width = 600
background_color = (251, 247, 245)
button_color = (255, 255, 0)

original_grid_element_color = (52, 31, 151)
buffer = 5

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']
grid_original = [[grid[x][y]
                  for y in range(len(grid[0]))] for x in range(len(grid))]


def solve():
    # N is the size of the 2D matrix   N*N
    N = 9
    # A utility function to print solve_grid

    def printing(arr):
        for i in range(N):
            for j in range(N):
                print(arr[i][j], end=" ")
            print()
    # Checks whether it will be
    # legal to assign num to the
    # given row, col

    def isSafe(solve_grid, row, col, num):
        # Check if we find the same num
        # in the similar row , we
        # return false
        for x in range(9):
            if solve_grid[row][x] == num:
                return False
        # Check if we find the same num in
        # the similar column , we
        # return false
        for x in range(9):
            if solve_grid[x][col] == num:
                return False
        # Check if we find the same num in
        # the particular 3*3 matrix,
        # we return false
        startRow = row - row % 3
        startCol = col - col % 3
        for i in range(3):
            for j in range(3):
                if solve_grid[i + startRow][j + startCol] == num:
                    return False
        return True
    # Takes a partially filled-in solve_grid and attempts
    # to assign values to all unassigned locations in
    # such a way to meet the requirements for
    # Sudoku solution (non-duplication across rows,
    # columns, and boxes) */

    def solveSuduko(solve_grid, row, col):
        # Check if we have reached the 8th
        # row and 9th column (0
        # indexed matrix) , we are
        # returning true to avoid
        # further backtracking
        if (row == N - 1 and col == N):
            return True
        # Check if column value  becomes 9 ,
        # we move to next row and
        # column start from 0
        if col == N:
            row += 1
            col = 0
        # Check if the current position of
        # the solve_grid already contains
        # value >0, we iterate for next column
        if solve_grid[row][col] > 0:
            return solveSuduko(solve_grid, row, col + 1)
        for num in range(1, N + 1, 1):
            # Check if it is safe to place
            # the num (1-9)  in the
            # given row ,col  ->we
            # move to next column
            if isSafe(solve_grid, row, col, num):
                # Assigning the num in
                # the current (row,col)
                # position of the solve_grid
                # and assuming our assigned
                # num in the position
                # is correct
                solve_grid[row][col] = num
                # Checking for next possibility with next
                # column
                if solveSuduko(solve_grid, row, col + 1):
                    return True
            # Removing the assigned num ,
            # since our assumption
            # was wrong , and we go for
            # next assumption with
            # diff num value
            solve_grid[row][col] = 0
        return False

    # Driver Code
    # 0 means unassigned cells
    solve_grid = [[grid[x][y]
                   for y in range(len(grid[0]))] for x in range(len(grid))]
    if (solveSuduko(solve_grid, 0, 0)):
        printing(solve_grid)
    else:
        print("no solution  exists ")


solve()


def insert(win, position):
    i, j = position[1], position[0]
    print(i, j)
    myfont = pygame.font.SysFont('Comic Sans Ms', 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if(grid_original[i-1][j-1] != 0):
                    return
                if(event.key == 48):
                    grid[i-1][j-1] == event.key - 48
                    pygame.draw.rect(win, background_color, (
                        position[0]*50 + buffer, position[1]*50+buffer, 50-2*buffer, 50-2*buffer))
                    pygame.display.update()
                    return
                if(0 < event.key-48 < 10):
                    pygame.draw.rect(win, background_color, (
                        position[0]*50 + buffer, position[1]*50+buffer, 50-2*buffer, 50-2*buffer))
                    value = myfont.render(str(event.key - 48), True, (0, 0, 0))
                    win.blit(value, (position[0]*50+15, position[1]*50))
                    grid[i-1][j-1] = event.key-48
                    pygame.display.update()
                    return
                return


def main():
    pygame.init()
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("suduko")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans Ms', 35)

    for i in range(0, 10):
        if(i % 3 == 0):
            pygame.draw.line(win, (0, 0, 0), (50+50*i, 50), (50+50*i, 500), 4)
            pygame.draw.line(win, (0, 0, 0), (50, 50+50*i), (500, 50+50*i), 4)
        pygame.draw.line(win, (0, 0, 0), (50+50*i, 50), (50+50*i, 500), 2)
        pygame.draw.line(win, (0, 0, 0), (50, 50+50*i), (500, 50+50*i), 2)

    pygame.display.update()

    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if(0 < grid[i][j] < 10):
                value = myfont.render(
                    str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j+1)*50 + 15, (i+1)*50))

    pygame.display.update()
    pygame.draw.rect(win, button_color, (
        525, 525, 50-2*buffer, 50-2*buffer))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(win, (pos[0]//50, pos[1]//50))
            if event.type == pygame.QUIT:
                print("\n", grid)
                print("\n", grid_original)
                pygame.quit()
                return


main()
