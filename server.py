import socket
import threading
import pygame
import os
from grid import Grid
from time import sleep

os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'

HEIGHT = 600
WIDTH = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe - Player 1')


# !!!


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    # Daemons are only useful when the main program is running,
    # and it's okay to kill them off once the other non-daemon threads have exited.
    #  Without daemon threads, we have to keep track of them, and tell them to exit, before our program can completely quit.
    #  By setting them as daemon threads,
    #  we can let them run and forget about them, and when our program quits, any daemon threads are killed automatically.
    thread.start()


HOST = '127.0.0.1'
PORT = 65432
connection_established = False
conn, addr = None, None
# These are the default arguements already
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# so we can just pass in nothing and this will work the same: 'sock = socket.socket()'
# The first arg means that we use ipv4 and the second means that we are using a TCP connection

sock.bind((HOST, PORT))  # Binding the port to the host
sock.listen(1)  # Allowing for a connection with 1 client only at a time


def receive_data():
    global turn
    while True:
        data = conn.recv(1024).decode()
        data = data.split('-')
        x = int(data[0])
        y = int(data[1])
        if data[2] == 'your turn':
            turn = True
        if data[3] == 'False':
            grid.gameover = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'o')


def waiting_for_connection():
    global connection_established, conn, addr
    conn, addr = sock.accept() # Hangs the code until a connection is established so threading is needed
    print('Client connected')
    connection_established = True
    receive_data()


# Allowing waiting_for_connection() function to run simultaneously to the rest of the code
create_thread(waiting_for_connection)

grid = Grid()
running = True
player = 'x'
turn = True
playing = 'True'

def draw_screen(color):
    screen.fill(color)
    grid.draw(screen)
    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Only play if a connection is established
        if event.type == pygame.MOUSEBUTTONDOWN and connection_established:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.gameover:
                    pos = pygame.mouse.get_pos()
                    # Saving clicked cells
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player)
                    if grid.gameover:
                        playing = 'False'
                    # Encoding the string to abyte string so that can be able to send data accross TCP ports

                    send_data = '{}-{}-{}-{}'.format(cellX,
                                                     cellY, 'your turn', playing).encode()
                    conn.send(send_data)  # Sending data to client
                    turn = False  # Ending turn

                # if grid.check_win() or grid.has_drawn():
                    # grid.switch_player = False
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
