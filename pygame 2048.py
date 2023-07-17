import pygame
import sys
import random
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30) #font and size

#initialize game
def start_game():
    mat = [[0] * 4 for _ in range(4)]
    
    #controls for user
    print("Welcome to 2048! The commands are as follows : ")
    print(" ^ arrow : Move Up")
    print(" v arrow : Move Down")
    print(" < arrow : Move Left")
    print(" > arrow : Move Right")
    print()
    
    # add random empty cell at start
    add_new(mat)
    return mat

#  add a new 2 or 4 in grid at any random empty cell
def add_new(mat):
    r, c = random.randint(0, 3), random.randint(0, 3)
    
    # while loop will break at empty cell
    while mat[r][c] != 0:
        r, c = random.randint(0, 3), random.randint(0, 3)
    
    # place a 2 or 4 at that empty random cell
    mat[r][c] = random.randint(1, 2) * 2
    return mat

def compress(mat):
    # Empty grid
    new_mat = [[0] * 4 for _ in range(4)]
    
    for i in range(4):
        pos = 0
        
        for j in range(4):
            if mat[i][j] != 0:
                
                new_mat[i][pos] = mat[i][j]
                pos += 1
    return new_mat

def merge(mat):
    for i in range(4):
        for j in range(3):
            
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                double = mat[i][j] * 2
                mat[i][j] = double
                
                mat[i][j + 1] = 0
    return mat

def reverse(mat):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[i][3 - j])
    return new_mat

def transpose(mat):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[j][i])
    return new_mat

#WON or LOST
def get_current_state(mat):
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 2048:
                return 'WON'
    # If we can not move this grid to any direction and any cell does not contains zero= LOST
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 0:
                return 'GAME NOT OVER'
    for i in range(3):
        for j in range(3):
            if mat[i][j] == mat[i + 1][j] or mat[i][j] == mat[i][j + 1]:
                return 'GAME NOT OVER'
    for j in range(3):
        if mat[3][j] == mat[3][j + 1]:
            return 'GAME NOT OVER'
    for i in range(3):
        if mat[i][3] == mat[i + 1][3]:
            return 'GAME NOT OVER'
    return 'LOST'

def print_board(mat, screen):
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, get_color(mat[i][j]), pygame.Rect(j*80, i*80, 75, 75))
            label = myfont.render(str(mat[i][j]), 1, (0,0,0))
            screen.blit(label, (j*80+30, i*80+30))

# color
def get_color(n):
    if n > 2048: n = 2048
    colors = [(0, 0, 0), (236, 244, 95), (236, 179, 95), (236, 138, 95), (236, 95, 103),
              (236, 95, 179), (181, 95, 236), (95, 107, 236), (95, 204, 236), (95, 236, 202),
              (95, 236, 138), (149, 236, 95)]
    return colors[int(n.bit_length())]

def exit_game():
    pygame.quit()
    sys.exit()

# Game Loop
def game_loop(mat):
    
    pygame.init()
    clock = pygame.time.Clock()
    #myfont = pygame.font.SysFont("Arial", 30)
    screen = pygame.display.set_mode((320, 320))
    pygame.display.set_caption("2048")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                initial_mat = [x[:] for x in mat]  # to check if initial = current

                if event.key == pygame.K_UP:
                    mat = transpose(mat)
                    mat = compress(mat)
                    mat = merge(mat)
                    mat = compress(mat)
                    mat = transpose(mat)
                elif event.key == pygame.K_DOWN:
                    mat = transpose(mat)
                    mat = reverse(mat)
                    mat = compress(mat)
                    mat = merge(mat)
                    mat = compress(mat)
                    mat = reverse(mat)
                    mat = transpose(mat)
                elif event.key == pygame.K_LEFT:
                    mat = compress(mat)
                    mat = merge(mat)
                    mat = compress(mat)
                elif event.key == pygame.K_RIGHT:
                    mat = reverse(mat)
                    mat = compress(mat)
                    mat = merge(mat)
                    mat = compress(mat)
                    mat = reverse(mat)

                #test case 
                if mat != initial_mat:
                    mat = add_new(mat)

                current_state = get_current_state(mat)
                if current_state == 'WON':
                    print("You Won!")
                    exit_game()
                    break
                if current_state == 'LOST':
                    print("You Lost!")
                    exit_game()
                    break

        screen.fill((255, 255, 255))
        print_board(mat, screen)
        pygame.display.flip()
        clock.tick(60)
                
if __name__ == '__main__':
    mat = start_game()
    game_loop(mat)
