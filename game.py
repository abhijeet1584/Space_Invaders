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
    COOLDOWN = 30 # half a second as 60 FPS is the range
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
        for laser in self.lasers:
            laser.draw(window)
            
    def move_laser(self, vel, obj):
        self.cooldown() # incrementing the cool_down_counter
        for laser in self.lasers:
            laser.move(vel)
            # vel is the velocity of the laser, eiter positiv or negative
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser) # destroy the laser if laser.x is greater than the height of the window
                
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
        
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
            
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
    def get_height(self):
        return self.ship_img.get_height()
    
    def get_width(self):
        return self.ship_img.get_height()
        
        
class Laser:
    def __init__(self, x, y, img):
        self.x = x - 23;
        self.y = y
        self.img = pygame.transform.scale((img), (80, 40))
        self.mask = pygame.mask.from_surface(self.img)
        
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        
    def move(self, vel): # if vel (velocity) is positive it will move downwards else it will move upwards
        self.y += vel
        
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0) # This will return either true or false, depending on the height argument and the self.y
    
    def collision(self, obj):
        return collide(obj, self) # This will return true if the pixels of the Laser object and the other object are overlaping
        
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = pygame.transform.scale((YELLOW_SPACE_SHIP), (33, 33))
        self.laser_img = YELLO_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        
    def move_laser(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
                
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
                        
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
                        
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 5))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (1 - ((self.max_health - self.health) / self.max_health)), 5))


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
        
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 9, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
        
    def move(self, vel):
        self.y += vel

def collide(object1, object2):
    # using the overlap method (masks)
    offset_x = object2.x - object1.x
    offset_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask, (offset_x, offset_y)) != None
    # Given two masks the overlap function will check if they are overlaping with each other
    # if they are not overlaping then it will return None
    # and that's why when they ARE overlaping it will return true

# Game Loop
def main():
    run = True;
    FPS = 60
    level = 0
    lost_count = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 33)
    
    enemies = []
    wave_length = 3
    enemy_vel = 1
    player_vel = 5
    laser_vel = 10
    ship = Player(200, 433)
    lost = False
    
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
        
        if lost: # if lost == true
            lost_label = main_font.render("THE EARTH HAS BEEN DESTROYED!! :(", 1 , (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 250))
        
        pygame.display.update() # Refreshing the window
        
    while run:
        clock.tick(FPS)
        redraw_window()
        
        if lives <= 0 or ship.health <= 0:
            lost = True
            lost_count += 1
            
        if lost:
            if lost_count > FPS * 3: # a 5 second delay
                run = False
                
            else:
                continue
        
        if len(enemies) == 0:
            level += 1;
            wave_length += 3
            
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
            if ship.x < WIDTH - ship.get_width():
                ship.x += player_vel
                
            else:
                ship.x = WIDTH - ship.get_width()
                
        if keys[pygame.K_w] or keys[pygame.K_UP]: # up
            if ship.y > 0:
                ship.y -= player_vel
                
            else:
                ship.y = 0
                
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: # down
            if ship.y < HEIGHT - ship.get_height() - 20:
                ship.y += player_vel
                
            else:
                ship.y = HEIGHT - ship.get_height() - 20
                
        if keys[pygame.K_SPACE]:
            ship.shoot()
                
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_laser(laser_vel, ship)
            
            if random.randrange(0, 120) == 1: # 50% probablity of the enemy shooting every second
                enemy.shoot()
                
            if collide (enemy, ship):
                ship.health -= 10
                enemies.remove(enemy)
                
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                if enemy in enemies:
                    try:
                        enemies.remove(enemy)
                    except:
                        print("Error")
        
        try:
            ship.move_laser(-laser_vel, enemies)
        except:
            print("Multiple Shots")
        
# Running the program
if __name__ == "__main__":
    main()
