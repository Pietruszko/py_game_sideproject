import pygame
import random

#pygame basic setup from pygame documentation
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 #delta time

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 100)
player_model = pygame.Rect(player_pos.x, player_pos.y, 200, 20)
player_model.center = player_pos
speed_y = 0
speed_x = 0
circle_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
circle = pygame.Rect(circle_pos.x, circle_pos.y, 20, 20)
circle_direction_y = 1
initial_circle_direction_x = random.randint(-100, 100)
circle_direction_x = 0

while running:
    #polling for events
    #pygame.QUIT is a constant that represents the user clicking the close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple") #fill the screen with a color

    #render game here

    pygame.draw.rect(screen, "black", player_model) #draw a rect at player_pos
    pygame.draw.circle(screen, "red", circle.center, circle.width/2) #draw a circle at circle_pos

    keys = pygame.key.get_pressed() #get a list of all keys that are pressed
    player_model.y += speed_y * dt
    player_model.x += speed_x * dt
    if player_model.x < 0:
        player_model.x = 0
    if player_model.x > screen.get_width() - player_model.width:
        player_model.x = screen.get_width() - player_model.width
    if keys[pygame.K_w]:
        speed_y = -200
    if keys[pygame.K_s]:
        speed_y = 200
    if keys[pygame.K_a]:
        if speed_x > 0:
            speed_x = 0
        if speed_x == -400:
            speed_x == -400
        else:
            speed_x -= 15
    if keys[pygame.K_d]:
        if speed_x < 0:
            speed_x = 0
        if speed_x == 400:
            speed_x == 400
        else:
            speed_x += 15
    if not keys[pygame.K_w] and not keys[pygame.K_s]:
        speed_y = 0
    if not keys[pygame.K_a] and not keys[pygame.K_d]:
        speed_x = 0
    
    def circle_collision():
        if circle.colliderect(player_model):
            return True
        else:
            return False  

    circle.y += 300 * circle_direction_y * dt 
    circle.x += circle_direction_x * dt
    if circle.x <= 0 or circle.x >= screen.get_width() - circle.width:
        circle_direction_x *= -1
    if circle.y <= 0:
        circle_direction_y *= -1
    if circle.y >= screen.get_height():
        circle_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        circle = pygame.Rect(circle_pos.x, circle_pos.y, 20, 20)
        circle_direction_y = 1
        circle_direction_x = initial_circle_direction_x

    if circle_collision():
        circle_direction_y *= -1
        circle_direction_x += speed_x
        circle_direction_x = min(400, circle_direction_x)
        circle_direction_x = max(-400, circle_direction_x)

    #render game here

    pygame.display.flip() #update the screen
    dt = clock.tick(60) /1000 #delta time in seconds (60 frames per second)

pygame.quit() #quit pygame