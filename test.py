import pygame

class JumpingCircle:
    def __init__(self, x, y, radius, color, jump_height):
        self.x_velocity = 0
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.y_velocity = 0
        self.is_jumping = False
        self.jump_height = jump_height
        self.c2_pos = [x-720, y-400]

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = 5
            self.x_velocity = 10

    def update(self):
        if self.is_jumping:
            self.y += self.y_velocity
            self.x += self.x_velocity
            self.c2_pos[0] += self.x_velocity
            self.c2_pos[1] += self.y_velocity
            # if self.y >= 400 - self.radius:
            #     self.y = 400 - self.radius
            #     self.y_velocity = 0
            #     self.is_jumping = False
            # elif self.y <= self.jump_height:
            #     self.y_velocity = 1
        if self.x > 720:
            self.c2_pos[0] -= 720
        if self.y > 400:
            self.c2_pos[1] -= 400
        if self.c2_pos[0] > 720:
            self.x -= 720
        if self.c2_pos[1] > 400:
            self.y -= 400

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, int(self.y)), self.radius)
        pygame.draw.circle(screen, self.color, self.c2_pos, self.radius)


pygame.init()

screen_size = (640, 400)
screen = pygame.display.set_mode(screen_size)

circle = JumpingCircle(50, 350, 50, [180, 50, 0], 120)
clock = pygame.time.Clock()
FPS = 30
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                circle.jump()

    screen.fill((0, 0, 0))
    circle.update()
    circle.draw(screen)

    pygame.display.update()
