import pygame
import os
import time
from board import Board


board = pygame.transform.scale( pygame.image.load(os.path.join("img", "board_alt.png") ), (750, 750) )
rect = (118,118,515,515)

def redraw_gameWindow(win, bo, timer=0):

    win.blit(board, (0,0))
    pygame.draw.rect(win, (0, 0, 0), rect, 1)

    bo.draw(win)

    pygame.display.update()

def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text,1, (255,0,0))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False


def click(pos):
    x = pos[0]
    y = pos[1]

    if (rect[0] < x < rect[0] + rect[2]) and (rect[1] < y < rect[1] + rect[3]):
        divX = x - rect[0]
        divY = y - rect[1]
        i = int( divX / (rect[2]/8) )
        j = int( divY / (rect[3]/8) )

        return i, j

    return -1, -1

def main():
    p1Time = 60*15
    p2Time = 60*15

    turn = "w"
    bo = Board(8, 8)
    clock = pygame.time.Clock()
    run = True
    startTimer = time.time()

    while run:
        timer = time.time() - startTimer
        clock.tick(10)
        redraw_gameWindow(win, bo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()

            if event.type == pygame.MOUSEMOTION:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                i, j = click(pos)
                change = bo.select(i, j, turn)
                bo.update_moves()

                if change:
                    timeGone = int(time.time() - startTimer)
                    startTimer = time.time()
                    if turn == "w":
                        p1Time -= timeGone
                        turn = 'b'
                    elif bo.turn == "b":
                        p2Time -= timeGone
                        turn = 'w'



        if bo.is_checked("w"):
            end_screen(win, "Black wins")
            run = False
        elif bo.is_checked("b"):
            end_screen(win, "White wins")
            run = False


#name = input("Please type your name: ")
width = 750
height = 750

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
main()
