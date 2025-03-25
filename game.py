import pygame
import random

#pygame basic setup from pygame documentation
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 #delta time

class Ball:
    def __init__(self, x, y, image, speed, direction, angle):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.direction = pygame.Vector2(direction)
        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.rect.y >= screen.get_height():
            self.rect.y = screen.get_height() / 2
            self.rect.x = screen.get_width() / 2
            self.angle = 90
        self.rect.y += self.speed * self.direction.y * dt
        if self.rect.y <= 0:
            self.direction.y *= -1
        if pygame.sprite.collide_mask(self, player):
            self.direction.y *= -1
            self.direction.x = self.angle + 90 + (pygame.math.lerp(-150, 150, (player.speed + player.max_speed)/(player.max_speed + player.max_speed)))
        self.rect.x += self.direction.x * dt
        if self.rect.x <= 0 or self.rect.x >= screen.get_width() - self.rect.width:
            self.direction.x *= -1
        self.angle = pygame.math.Vector2.angle_to(self.direction, pygame.Vector2(0, 0))
        if pygame.Rect.colliderect(self.rect, brick.top):
            self.direction.y *= -1
            brick.rect.x = random.randint(0, screen.get_width() - brick.rect.width)
            brick.rect.y = random.randint(0, screen.get_height() - brick.rect.height)
        if pygame.Rect.colliderect(self.rect, brick.bottom):
            self.direction.y *= -1
            brick.rect.x = random.randint(0, screen.get_width() - brick.rect.width)
            brick.rect.y = random.randint(0, screen.get_height() - brick.rect.height)
        if pygame.Rect.colliderect(self.rect, brick.left):
            self.direction.x *= -1
            brick.rect.x = random.randint(0, screen.get_width() - brick.rect.width)
            brick.rect.y = random.randint(0, screen.get_height() - brick.rect.height)
        if pygame.Rect.colliderect(self.rect, brick.right):
            self.direction.x *= -1
            brick.rect.x = random.randint(0, screen.get_width() - brick.rect.width)
            brick.rect.y = random.randint(0, screen.get_height() - brick.rect.height)


class Player:
    def __init__ (self, x, y, image, speed, max_speed):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.max_speed = max_speed
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.rect.x < 0:
            self.rect.x = 0
            self.speed = 0
        if self.rect.x > screen.get_width() - self.rect.width:
            self.rect.x = screen.get_width() - self.rect.width
            self.speed = 0
        keys = pygame.key.get_pressed()
        self.rect.x += self.speed * dt
        if keys[pygame.K_a]:
            self.speed = pygame.math.clamp(self.speed - 15, -self.max_speed, 0)
        if keys[pygame.K_d]:
            self.speed = pygame.math.clamp(self.speed + 15, 0, self.max_speed)
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.speed = 0

class Brick:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.top = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 1)
        self.bottom = pygame.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.width, 1)
        self.left = pygame.Rect(self.rect.x, self.rect.y, 1, self.rect.height)
        self.right = pygame.Rect(self.rect.x + self.rect.width, self.rect.y, 1, self.rect.height)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.top = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 1)
        self.bottom = pygame.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.width, 1)
        self.left = pygame.Rect(self.rect.x, self.rect.y, 1, self.rect.height)
        self.right = pygame.Rect(self.rect.x + self.rect.width, self.rect.y, 1, self.rect.height)

ball = pygame.image.load("Sprites/ball.png").convert_alpha()
ball = Ball(screen.get_width() / 2, screen.get_height() / 2, ball, 400, (0, 1), 90)

player = pygame.image.load("Sprites/player.png").convert_alpha()
player = pygame.transform.scale(player, (192, 192))
player = Player(screen.get_width() / 2, screen.get_height() - 100, player, 0, 500)

brick = pygame.image.load("Sprites/brick.png").convert_alpha()
brick = pygame.transform.scale(brick, (192, 192))
brick = Brick(screen.get_width() / 4, screen.get_height()/4, brick)


while running:
    #polling for events
    #pygame.QUIT is a constant that represents the user clicking the close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple") #fill the screen with a color

    #render game here

    player.update()
    player.draw()
    ball.update()
    ball.draw()
    brick.update()
    brick.draw()

    #render game here

    pygame.display.flip() #update the screen
    dt = clock.tick(60) /1000 #delta time in seconds (60 frames per second)

pygame.quit() #quit pygame