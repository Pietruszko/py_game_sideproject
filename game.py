import pygame
import random

#pygame basic setup from pygame documentation
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 #delta time

class Ball:
    def __init__(self, x, y, image, speed, direction, angle, bricks):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.direction = pygame.Vector2(direction)
        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.bricks = bricks

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
        collision = pygame.sprite.spritecollide(self, self.bricks, dokill = True)
        for brick in collision:
            if pygame.Rect.colliderect(self.rect, brick.top) or pygame.Rect.colliderect(self.rect, brick.bottom):
                self.direction.y *= -1
                break
            if pygame.Rect.colliderect(self.rect, brick.left) or pygame.Rect.colliderect(self.rect, brick.right):
                self.direction.x *= -1
                break


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

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load("Sprites/brick.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (w, h))
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


bricks = pygame.sprite.Group()
screen_w = screen.get_width()
screen_h = screen.get_height()
width = screen_w/15
height = width/2
start_x = width/2 + width/2
start_y = height/2 + height/2

for i in range(int(screen_h/(height*3))):
    for j in range(int(screen_w/width-1)):
        bricks.add(Brick(start_x, start_y, width, height))
        start_x += width       
    start_x = width/2 + width/2
    start_y += height


ball = pygame.image.load("Sprites/ball.png").convert_alpha()
ball = Ball(screen.get_width() / 2, screen.get_height() / 2, ball, 400, (0, 1), 90, bricks)

player = pygame.image.load("Sprites/player.png").convert_alpha()
player = pygame.transform.scale(player, (192, 192))
player = Player(screen.get_width() / 2, screen.get_height() - 100, player, 0, 500)


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
    bricks.update()
    bricks.draw(screen)

    #render game here

    pygame.display.flip() #update the screen
    dt = clock.tick(60) /1000 #delta time in seconds (60 frames per second)

pygame.quit() #quit pygame