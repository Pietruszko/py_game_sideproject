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
max_speed = 400
circle_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
circle = pygame.Rect(circle_pos.x, circle_pos.y, 20, 20)
circle_direction_y = 1
initial_circle_direction_x = random.randint(-100, 100)
circle_direction_x = 0
circle_speed = 400
circle_angle = 90

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
        speed_x = 0
    if player_model.x > screen.get_width() - player_model.width:
        player_model.x = screen.get_width() - player_model.width
        speed_x = 0
    if keys[pygame.K_w]:
        speed_y = -200
    if keys[pygame.K_s]:
        speed_y = 200
    if keys[pygame.K_a]:
        speed_x = pygame.math.clamp(speed_x - 15, -max_speed, 0)
    if keys[pygame.K_d]:
        speed_x = pygame.math.clamp(speed_x + 15, 0, max_speed)
    if not keys[pygame.K_w] and not keys[pygame.K_s]:
        speed_y = 0
    if not keys[pygame.K_a] and not keys[pygame.K_d]:
        speed_x = 0
    
    def circle_collision():
        if pygame.Rect.colliderect(player_model, circle):
            return True
        else:
            return False  

    circle_angle = pygame.math.Vector2.angle_to(pygame.Vector2(circle_direction_x, circle_direction_y), pygame.Vector2(0, 0))
    circle.center += pygame.Vector2(circle_direction_x, circle_direction_y * 400) * dt

    if circle.x <= 0 or circle.x >= screen.get_width() - circle.width:
        circle_direction_x *= -1
        #print(f"Hit wall, angle: {pygame.math.Vector2.angle_to(pygame.Vector2(circle_direction_x, circle_direction_y), pygame.Vector2(0, 0))}")
    if circle.y <= 0:
        circle_direction_y *= -1
        #print(f"Hit ceiling, angle: {pygame.math.Vector2.angle_to(pygame.Vector2(circle_direction_x, circle_direction_y), pygame.Vector2(0, 0))}")
    if circle.y >= screen.get_height():
        circle_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        circle = pygame.Rect(circle_pos.x, circle_pos.y, 20, 20)
        circle_direction_y = 1
        circle_direction_x = 0

    if circle_collision():
        circle_direction_y *= -1
        print ((speed_x + max_speed)/(max_speed + max_speed))
        print (pygame.math.lerp(-150, 150, (speed_x + max_speed)/(max_speed + max_speed)))
        print (circle_angle)
        circle_direction_x = circle_angle + 90 + (pygame.math.lerp(-150, 150, (speed_x + max_speed)/(max_speed + max_speed)))
        print (circle_direction_x)
        
        #print(f"Hit player, angle: {pygame.math.Vector2.angle_to(pygame.Vector2(circle_direction_x, circle_direction_y), pygame.Vector2(0, 0))}")

    #render game here

    pygame.display.flip() #update the screen
    dt = clock.tick(60) /1000 #delta time in seconds (60 frames per second)

pygame.quit() #quit pygame