import pygame
import random
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 102, 255),
    (255, 255, 0),
    (153, 0, 255)
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5], [4, 5], [9, 5], [6, 5]],
        [[1, 5], [4, 5], [9, 5], [6, 5]],
        [[1, 5], [4, 5], [9, 5], [6, 5]],
        [[1, 5, 2], [10, 5, 6], [8, 5, 9], [0, 4, 5]],
        [[1, 5, 2], [10, 5, 6], [8, 5, 9], [0, 4, 5]],
        [[9, 10, 5, 6], [9, 10, 5, 6], [9, 10, 5, 6], [9, 10, 5, 6]]
    ]
    colorings = [
        [[0, 1], [0, 1], [1, 0], [1, 0]],
        [[0, 1], [0, 1], [1, 0], [1, 0]],
        [[0, 1], [0, 1], [1, 0], [1, 0]],
        [[1, 1, 0], [0, 1, 1], [0, 1, 1], [1, 1, 0]],
        [[1, 1, 0], [0, 1, 1], [0, 1, 1], [1, 1, 0]],
        [[1, 1, 0, 0], [0, 1, 0, 1], [0, 0, 1, 1], [1, 0, 1, 0]]]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        if bool(random.getrandbits(1)) == True:
            self.colors = [random.randint(1, len(colors) - 1), random.randint(1, len(colors) - 1)]
        else:
            self.colors = [random.randint(1, len(colors) - 1)]
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    level = 1
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 30
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(width):
            new_line = []
            for j in range(height):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[j + self.figure.x][i + self.figure.y] > 0:
                        intersection = True
        return intersection

    def break_color(self, x, y, col):
        queue = [[x, y]]
        q2 = [[x, y]]
        while len(queue) > 0:
            x, y = queue.pop(0)
            if self.field[x][y] == col:
                if x > 0:
                    if [x - 1, y] not in q2:
                        queue.append([x - 1, y])
                        q2.append([x - 1, y])
                if x < 5:
                    if [x + 1, y] not in q2:
                        queue.append([x + 1, y])
                        q2.append([x + 1, y])
                if y > 0:
                    if [x, y - 1] not in q2:
                        queue.append([x, y - 1])
                        q2.append([x, y - 1])
                if y < 11:
                    if [x, y + 1] not in q2:
                        queue.append([x, y + 1])
                        q2.append([x, y + 1])
            else:
                q2.remove([x, y])
        if len(q2) >= 4:
            self.score += len(q2) - 3
            while len(q2) > 0:
                x, y = q2.pop(0)
                self.field[x][y] = 0
        self.descent()


    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def descent(self):
        for i in range(len(self.field)):
            counter = 0
            for j in range(len(self.field[i])):
                if self.field[i][j] == 0:
                    counter += 1
            for _ in range(counter):
                self.field[i].remove(0)
            self.field[i] = [0] * counter + self.field[i]

    def freeze(self):
        tile_num = 0
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if  len(self.figure.colors) == 1:
                        self.field[j + self.figure.x][i + self.figure.y] = self.figure.colors[0]
                    else:
                        color = game.figure.colorings[game.figure.type][game.figure.rotation][tile_num]
                        self.field[j + self.figure.x][i + self.figure.y] = self.figure.colors[color]
                        tile_num += 1
        self.descent()
        #for i in self.field:
        #    print(i)
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if self.field[i][j] != 0:
                    self.break_color(i, j, self.field[i][j])
        print("")
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Puyo Puyo PY")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(12, 6)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_ESCAPE:
                game.__init__(12, 6)
    #for i in game.field:
    #    print(*i)
    #print("")
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[j][i] > 0:
                pygame.draw.rect(screen, colors[game.field[j][i]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        tile_num = 0
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    if  len(game.figure.colors) == 1:
                        pygame.draw.rect(screen, colors[game.figure.colors[0]],
                                         [game.x + game.zoom * (j + game.figure.x) + 1,
                                          game.y + game.zoom * (i + game.figure.y) + 1,
                                          game.zoom - 2, game.zoom - 2])
                    else:
                        color = game.figure.colorings[game.figure.type][game.figure.rotation][tile_num]
                        pygame.draw.rect(screen, colors[game.figure.colors[color]],
                                         [game.x + game.zoom * (j + game.figure.x) + 1,
                                          game.y + game.zoom * (i + game.figure.y) + 1,
                                          game.zoom - 2, game.zoom - 2])
                        tile_num += 1

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()