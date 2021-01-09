import socket
import threading
import pygame
import os
from grid import Grid
from time import sleep

os.environ['SDL_VIDEO_WINDOW_POS'] = '900,100'

HEIGHT = 600
WIDTH = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe - Player 2')


# !!!


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


HOST = '127.0.0.1'
PORT = 65432

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))  # Connecting to the server


def receive_data():
    global turn
    while True:
        # Receiving the byte string and decoding it
        data = sock.recv(1024).decode()
        # This is also a blocking code so threading is needed
        # Spliting data at the dashes which creates a list
        data = data.split('-')
        x = int(data[0])
        y = int(data[1])
        if data[2] == 'your turn':
            turn = True
        if data[3] == 'False':
            grid.gameover = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'x')


create_thread(receive_data)
# !!!


grid = Grid()
running = True
player = 'o'
turn = False
playing = 'True'

def draw_screen(color):
    screen.fill(color)
    grid.draw(screen)
    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not grid.gameover:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.gameover:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player)
                    if grid.gameover:
                        playing = 'False'
                    send_data = '{}-{}-{}-{}'.format(cellX,
                                                     cellY, 'your turn', playing).encode()
                    sock.send(send_data)
                    turn = False
                # if grid.check_win() or grid.has_drawn():
                #     grid.switch_player = False
                # if grid.switch_player:
                #     if player == 'x':
                #         player = 'o'
                #     else:
                #         player = 'x'


    draw_screen((0,128,128))

    if grid.gameover:
        if grid.winner == player:
            draw_screen((0,128,0))
        else:
            draw_screen((128,0,0))
        sleep(2)
        grid.winner = None
        grid.clear_grid()
        grid.gameover = False
        playing = 'True'

    # if grid.check_win():
    #     print(f'{player.upper()} wins!')
    #     if player == 'x':
    #         player = 'o'
    #     else:
    #         player = 'x'
    #     sleep(2)
    #     grid.grid = [[0 for x in range(3)] for y in range(3)]

    # if grid.has_drawn():
    #     print("It's a draw!")
    #     if player == 'x':
    #         player = 'o'
    #     else:
    #         player = 'x'
    #     sleep(2)
    #     grid.grid = [[0 for x in range(3)] for y in range(3)]
