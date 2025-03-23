import pygame
import random

#pygame basic setup from pygame documentation
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 #delta time

class Ball:
    def __init__(self, x, y, radius, color, speed, direction, angle):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.direction = pygame.Vector2(direction)
        self.angle = angle
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.rect.center = (x, y)

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def update(self):
        if self.rect.y >= screen.get_height():
            self.rect.y = screen.get_height() / 2
            self.rect.x = screen.get_width() / 2
        self.rect.y += self.speed * self.direction.y * dt
        if self.rect.y <= 0:
            self.direction.y *= -1
        if pygame.Rect.colliderect(self.rect, player.rect):
            self.direction.y *= -1
            self.direction.x = self.angle + 90 + (pygame.math.lerp(-150, 150, (player.speed + player.max_speed)/(player.max_speed + player.max_speed)))
        self.rect.x += self.direction.x * dt
        if self.rect.x <= 0 or self.rect.x >= screen.get_width() - self.radius:
            self.direction.x *= -1
        self.angle = pygame.math.Vector2.angle_to(self.direction, pygame.Vector2(0, 0))

class Player:
    def __init__(self, x, y, width, height, color, speed, max_speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.max_speed = max_speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (x, y)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)       

    def update(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screen.get_width() - self.width:
            self.rect.x = screen.get_width() - self.width
        keys = pygame.key.get_pressed()
        self.rect.x += self.speed * dt
        if keys[pygame.K_a]:
            self.speed = pygame.math.clamp(self.speed - 15, -self.max_speed, 0)
        if keys[pygame.K_d]:
            self.speed = pygame.math.clamp(self.speed + 15, 0, self.max_speed)
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.speed = 0

player = Player(screen.get_width() / 2, screen.get_height() - 100, 400, 10, "black", 0 , 500)
ball = Ball(screen.get_width() / 2, screen.get_height() / 2, 20, "blue", 400, (0, 1), 90)


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

    #render game here

    pygame.display.flip() #update the screen
    dt = clock.tick(60) /1000 #delta time in seconds (60 frames per second)

pygame.quit() #quit pygame