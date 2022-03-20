import pygame
import sys
import copy

n = int(input('Размер поля: '))
m = int(input('Длина линии: '))


def sign_in_row_and_col(c_mas, sign):
    new_mas = copy.deepcopy(c_mas)
    new_mas.sort()
    for i in range(len(new_mas)):
        new_mas[i][1] += 1 + len(new_mas) - i
    for j in range(len(new_mas)):
        if new_mas.count(new_mas[j]) >= m:
            return sign
    return False


def sign_in_diagonal(c_mas, sign):
    diagonal1 = copy.deepcopy(c_mas)
    diagonal1.sort()
    diagonal2 = copy.deepcopy(diagonal1)
    for i in range(len(diagonal1)):
        diagonal1[i][0] += 1 + len(diagonal1) - i
        diagonal1[i][1] += 1 + len(diagonal1) - i
    for i in range(len(diagonal2)):
        diagonal2[i][0] += 1 + len(diagonal2) - i
        diagonal2[i][1] += 1 - len(diagonal2) + i
    for i in range(len(diagonal1)):
        if diagonal1.count(diagonal1[i]) >= m:
            return sign
    for i in range(len(diagonal2)):
        if diagonal2.count(diagonal2[i]) >= m:
            return sign
    return False



def check_win(mas, sign):
    r_mas = []
    c_mas = []
    for row in range(n):
        for col in range(n):
            if mas[row][col] == sign:
                r_mas += [[row, col]]
                c_mas += [[col, row]]
    if sign_in_row_and_col(r_mas, sign):
        return sign
    elif sign_in_row_and_col(c_mas, sign):
        return sign
    elif sign_in_diagonal(r_mas, sign):
        return sign
    return False



pygame.init()
size_block = 100
margin = 15
width = height = size_block * n + margin * (n+1)
size_window = (width, height)
screen = pygame.display.set_mode(size_window)
pygame.display.set_caption('TicTacToe')

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
mas = [[0]*n for i in range(n)]
query = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            col = x_mouse // (size_block + margin)
            row = y_mouse // (size_block + margin)
            if mas[row][col] == 0:
                if query % 2 == 0:
                    mas[row][col] = 'x'
                else:
                    mas[row][col] = 'o'
                query += 1

    for row in range(n):
        for col in range(n):
            if mas[row][col] == 'x':
                color = blue
            elif mas[row][col] == 'o':
                color = green
            else:
                color = white
            x = col * size_block + (col + 1) * margin
            y = row * size_block + (row + 1) * margin
            pygame.draw.rect(screen, color, (x,y, size_block, size_block))
            if color == blue:
                pygame.draw.line(screen, white, (x, y), (x + size_block, y + size_block), 5)
                pygame.draw.line(screen, white, (x + size_block, y), (x, y + size_block), 5)
            elif color == green:
                pygame.draw.circle(screen, white, (x + size_block//2, y + size_block//2), size_block//2, 3)
    if (query -1)%2 == 0:
       game_over = check_win(mas,'x')
    else:
        game_over = check_win(mas, 'o')

    if game_over:
        screen.fill(black)
        font = pygame.font.SysFont('stxingkai', 80)
        text1 = font.render(game_over, True, white)
        text_rect = text1.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text1, [text_x, text_y])

    pygame.display.update()
