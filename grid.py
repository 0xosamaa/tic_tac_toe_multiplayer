import pygame

X = pygame.image.load('./images/x.png')
O = pygame.image.load('./images/o.png')


class Grid:
    def __init__(self):
        self.grid_lines = [((0, 200), (600, 200)),  # 1h
                           ((0, 400), (600, 400)),  # 2h
                           ((200, 0), (200, 600)),  # 1v
                           ((400, 0), (400, 600))  # 2v
                           ]
        self.grid = [[0 for x in range(3)] for y in range(3)]
        # self.switch_player = True
        self.gameover = False
        self.winner = None


    def draw(self, screen):
        for line in self.grid_lines:
            pygame.draw.line(screen, (0, 0, 0), line[0], line[1], 2)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == 'x':
                    screen.blit(X, (x * 200 + 36, y * 200 + 36))
                elif self.get_cell_value(x, y) == 'o':
                    screen.blit(O, (x * 200 + 36, y * 200 + 36))

    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        if self.get_cell_value(x, y) == 0:
            self.set_cell_value(x, y, player)
            if self.check_win():
                print('{} won!'.format(player.upper()))
                print('Resetting in 2 seconds..')
                self.gameover = True
                self.winner = player
            elif self.has_drawn():
                print('Draw!')
                print('Resetting in 2 seconds..')
                self.gameover = True

        #     self.switch_player = True
        #     self.set_cell_value(x, y, player)
        # else:
        #     self.switch_player = False

    def check_win(self):
        b = self.grid
        return ((b[0][0] != 0 and b[0][0] == b[0][1] and b[0][0] == b[0][2])
                or (b[1][0] != 0 and b[1][0] == b[1][1] and b[1][0] == b[1][2])
                or (b[2][0] != 0 and b[2][0] == b[2][1] and b[2][0] == b[2][2])
                or (b[0][0] != 0 and b[0][0] == b[1][0] and b[0][0] == b[2][0])
                or (b[0][1] != 0 and b[0][1] == b[1][1] and b[0][1] == b[2][1])
                or (b[0][2] != 0 and b[0][2] == b[1][2] and b[0][2] == b[2][2])
                or (b[0][0] != 0 and b[0][0] == b[1][1] and b[0][0] == b[2][2])
                or (b[0][2] != 0 and b[0][2] == b[1][1] and b[0][2] == b[2][0]))

    def has_drawn(self):
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True

    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)

    def print_grid(self):
        print(self.grid)
