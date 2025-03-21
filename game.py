import pygame

#pygame basic setup from pygame documentation
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 #delta time

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 100)
player_model = pygame.Rect(player_pos.x, player_pos.y, 200, 20)
player_model.center = player_pos

while running:
    #polling for events
    #pygame.QUIT is a constant that represents the user clicking the close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple") #fill the screen with a color

    #render game here

    pygame.draw.rect(screen, "black", player_model, ) #draw a circle at player_pos

    keys = pygame.key.get_pressed() #get a list of all keys that are pressed
    if keys[pygame.K_w]:
        player_model.y -= 200* dt
    if keys[pygame.K_s]:
        player_model.y += 200 * dt
    if keys[pygame.K_a]:
        player_model.x -= 200 * dt
    if keys[pygame.K_d]:
        player_model.x += 200 * dt

    #render game here

    pygame.display.flip() #update the screen
    dt = clock.tick(60) /1000 #delta time in seconds (60 frames per second)

pygame.quit() #quit pygame