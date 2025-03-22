import pygame
import random

#pygame basic setup from pygame documentation
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 #delta time

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update(self):
        if self.y >= screen.get_height():
            self.y = screen.get_height() / 2
            self.x = screen.get_width() / 2

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


circle_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
circle = pygame.Rect(circle_pos.x, circle_pos.y, 20, 20)
circle_direction_y = 1
initial_circle_direction_x = random.randint(-100, 100)
circle_direction_x = 0
circle_speed = 400
circle_angle = 90

player = Player(screen.get_width() / 2, screen.get_height() - 100, 400, 10, "black", 0 , 500)


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

    pygame.draw.circle(screen, "red", circle.center, circle.width/2) #draw a circle at circle_pos
    
    def circle_collision():
        if pygame.Rect.colliderect(player.rect, circle):
            return True
        else:
            return False  

    circle_angle = pygame.math.Vector2.angle_to(pygame.Vector2(circle_direction_x, circle_direction_y), pygame.Vector2(0, 0))
    circle.center += pygame.Vector2(circle_direction_x, circle_direction_y * 400) * dt

    if circle.x <= 0 or circle.x >= screen.get_width() - circle.width:
        circle_direction_x *= -1
    if circle.y <= 0:
        circle_direction_y *= -1
    if circle.y >= screen.get_height():
        circle_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        circle = pygame.Rect(circle_pos.x, circle_pos.y, 20, 20)
        circle_direction_y = 1
        circle_direction_x = 0

    if circle_collision():
        circle_direction_y *= -1
        circle_direction_x = circle_angle + 90 + (pygame.math.lerp(-150, 150, (player.speed + player.max_speed)/(player.max_speed + player.max_speed)))

    #render game here

    pygame.display.flip() #update the screen
    dt = clock.tick(60) /1000 #delta time in seconds (60 frames per second)

pygame.quit() #quit pygame