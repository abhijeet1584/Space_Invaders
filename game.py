import pygame
import os
import time
import random
pygame.font.init()

WIDTH = 500
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load Images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player Ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
YELLO_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
#BG = pygame.image.load(os.path.join("assets", "background-black.png"))
BG = pygame.transform.scale((pygame.image.load("assets/background-black.png")), (WIDTH, HEIGHT))

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        
        
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = pygame.transform.scale((YELLOW_SPACE_SHIP), (33, 33))
        self.laser_img = YELLO_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class EnemyShip(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }
    
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img = self.COLOR_MAP[color][0]
        self.laser_img = self.COLOR_MAP[color][1]
        self.mask = pygame.mask.from_surface(self.ship_img)
        
    def move(self, vel):
        self.y += vel

# Game Loop
def main():
    run = True;
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 33)
    
    enemies = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 5
    ship = Player(200, 433)
    
    clock = pygame.time.Clock()
    
    def redraw_window():
        WIN.blit(BG,(0,0))
        # draw text
        lives_lable = main_font.render(f"Lives : {lives}", 1, (255, 255, 255))
        level_lable = main_font.render(f"Level : {level}", 1, (255, 255, 255))
        WIN.blit(lives_lable, (10, 10))
        WIN.blit(level_lable, (WIDTH - level_lable.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(WIN)
            
        ship.draw(WIN)
        
        pygame.display.update() # Refreshing the window
        
    while run:
        clock.tick(FPS)
        
        if len(enemies) == 0:
            level += 1;
            wave_length += 5
            
            for i in range(wave_length):
                enemy = EnemyShip(random.randrange(50, WIDTH-100), random.randrange(-1500 * level / 5, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: # left
            if ship.x > 0:
                ship.x -= player_vel
                
            else:
                ship.x = 0
            
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: # right
            if ship.x < WIDTH - 33:
                ship.x += player_vel
                
            else:
                ship.x = WIDTH - 33
                
        if keys[pygame.K_w] or keys[pygame.K_UP]: # up
            if ship.y > 0:
                ship.y -= player_vel
                
            else:
                ship.y = 0
                
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: # down
            if ship.y < HEIGHT - 33:
                ship.y += player_vel
                
            else:
                ship.y = HEIGHT - 33
                
                
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + 50 > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
                
        redraw_window()
        
# Running the program
if __name__ == "__main__":
    main()
