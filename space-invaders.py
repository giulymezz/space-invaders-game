import pygame
import random

# initialize Pygame
pygame.init()

# images
background_img = pygame.image.load("media/spacewallpaper.png")
background_img = pygame.transform.scale(background_img, (1500, 900))

spaceship_img = pygame.image.load("media/spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (60, 60))

alien_img = pygame.image.load("media/alien.png")
alien_img = pygame.transform.scale(alien_img, (40, 40))

master_img = pygame.image.load("media/master.png")
master_img = pygame.transform.scale(master_img, (150, 150))

bullet_img = pygame.image.load("media/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (20, 20))

master_bullet_img = pygame.image.load("media/masterbullet.png")
master_bullet_img = pygame.transform.scale(master_bullet_img, (20, 30))

# set up the window
window_width = 1500
window_height = 900
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Invaders")

# set up the color
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# set up the clock
clock = pygame.time.Clock()

# fonts
font = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 74)

# player setup
player_width = 50
player_height = 40
player_x = window_width // 2
player_y = window_height - 60
player_speed = 7

# spaceship bullets
bullets = []
bullet_speed = -10
can_shoot = True

# master bullets
master_bullets = []
master_bullet_speed = 5

# game states
running = True
game_over = False
victory = False
round_number = 1
max_rounds = 5

# score
score = 0 
font = pygame.font.Font(None, 36)

# master
master = None
master_health = 20
master_speed = 3
master_direction = random.choice([-1, 1])
master_move_interval = 50
master_bullet_interval = 30

# initial aliens for a round
def initialize_aliens(num_aliens, speed):
    return [
        {"x": random.randint(50, window_width - 50),
         "y": random.randint(20, 150),
         "speed_x": speed * random.choice([-1, 1]),
         "speed_y": speed * random.choice([-1, 1])} for _ in range(num_aliens)
    ]

# initial alien setup
alien_speed = 2
num_aliens = 5
aliens = initialize_aliens(num_aliens, alien_speed)

# game loop
while running:

    # draw background
    window.blit(background_img, (0, 0))

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # shooting logic for player
        if event.type == pygame.KEYDOWN and not game_over and not victory:
            if event.key == pygame.K_SPACE and can_shoot:
                bullets.append({"x": player_x + player_width // 2, "y": player_y})
                can_shoot = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                can_shoot = True

    if not game_over and not victory:

        # controls spaceship
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < window_width - player_width:
            player_x += player_speed

        # move bullets
        for bullet in bullets[:]:
            bullet["y"] += bullet_speed
            if bullet["y"] < 0:
                bullets.remove(bullet)

        # move aliens (only horizontally)
        for alien in aliens:
            alien["x"] += alien["speed_x"]

            # bounce off edges horizontally
            if alien["x"] > window_width - 50 or alien["x"] < 0:
                alien["speed_x"] *= -1
                for a in aliens:
                    a["y"] += 20

            # check if an alien reaches the bottom (game over)
            if alien["y"] > window_height - 60:
                game_over = True

        # move master (random direction change)
        if master:
            master["x"] += master_speed * master_direction

            # random direction change after moving
            master_move_interval -= 1
            if master_move_interval <= 0:
                master_direction = random.choice([-1, 1])
                master_move_interval = random.randint(30, 60)

            # shoot master bullets randomly
            if random.random() < 0.02:  
                master_bullets.append({"x": master["x"] + 75, "y": master["y"] + 150})

        # move master bullets
        for bullet in master_bullets[:]:
            bullet["y"] += master_bullet_speed
            if bullet["y"] > window_height:
                master_bullets.remove(bullet)

        # bullet-alien collisions
        for bullet in bullets[:]:
            for alien in aliens[:]:
                if alien["x"] < bullet["x"] < alien["x"] + 40 and alien["y"] < bullet["y"] < alien["y"] + 40:
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 10
                    break

        # bullet-master collisions (player bullets hitting the master)
        for bullet in bullets[:]:
            if master and master["x"] < bullet["x"] < master["x"] + 150 and master["y"] < bullet["y"] < master["y"] + 150:
                bullets.remove(bullet)
                master_health -= 1
                if master_health <= 0:
                    master = None
                    victory = True
                break

        # bullet-master collisions (master bullets hitting the player)
        for bullet in master_bullets[:]:
            if player_x < bullet["x"] < player_x + player_width and player_y < bullet["y"] < player_y + player_height:
                game_over = True  
                break

        # check if all aliens are eliminated
        if not aliens and not master:
            if round_number < max_rounds:
                round_number += 1
                alien_speed += 1
                num_aliens += 3
                aliens = initialize_aliens(num_aliens, alien_speed)
            elif round_number == max_rounds:
                # spawn master in the last round
                master = {"x": window_width // 2 - 75, "y": 50, "speed_x": 3}
                master_health = 20
            else:
                victory = True

        # draw spaceship
        window.blit(spaceship_img, (player_x, player_y))

        #draw bullets
        for bullet in bullets:
            window.blit(bullet_img, (bullet["x"], bullet["y"]))

        # draw aliens
        for alien in aliens:
            window.blit(alien_img, (alien["x"], alien["y"]))

        # draw master
        if master:
            window.blit(master_img, (master["x"], master["y"]))

        # draw master bullets
        for bullet in master_bullets:
            window.blit(master_bullet_img, (bullet["x"], bullet["y"]))

        # draw score and round
        score_text = font.render(f"Score: {score}", True, white)
        round_text = font.render(f"Round: {round_number}", True, white)
        window.blit(score_text, (10, 10))
        window.blit(round_text, (10, 50))

        # draw master health
        if master:
            master_health_text = font.render(f"Master Health: {master_health}", True, red)
            window.blit(master_health_text, (window_width - 250, 10))

        
    elif game_over:
        # draw "GAME OVER" message
        font_large = pygame.font.Font(None, 74)
        game_over_text = font_large.render("GAME OVER", True, red)
        window.blit(game_over_text, (window_width // 2 - 150, window_height // 2 - 50))

    elif victory:
        # draw "YOU WIN" message
        font_large = pygame.font.Font(None, 74)
        victory_text = font_large.render("YOU WIN!", True, green)
        window.blit(victory_text, (window_width // 2 - 150, window_height // 2 - 50))

    # update screen
    pygame.display.flip()
    clock.tick(30)

# quit the game
pygame.quit()