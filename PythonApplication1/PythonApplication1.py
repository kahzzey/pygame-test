# Import the pygame module

from typing import Self
import pygame
import pygame.freetype
import random
black = ((0,0,0))
white = (255,255,255)
red = (255,0,0)
sky = (228, 246, 248)
# Import pygame.locals for easier access to key coordinates
pygame.font.init()
pygame.mixer.init()

from pygame.locals import (
    RLEACCEL,
    
    K_UP,

    K_DOWN,

    K_LEFT,

    K_RIGHT,

    K_ESCAPE,

    KEYDOWN,

    QUIT,

)
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf = pygame.image.load("nightraiderfixed.png").convert()
        self.surf = pygame.transform.scale( self.surf, (75,30))

        self.surf.set_colorkey(black, RLEACCEL)
        self.rect = self.surf.get_rect()
    # Move the sprite based on user keypresses

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
         self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
          self.rect.move_ip(5, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH  
        if self.rect.top <=  0 :
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enenmy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enenmy,self).__init__()
        self.surf = pygame.Surface((20,10))
        self.surf.fill(red)
        self.rect = self.surf.get_rect(
            center =(
                random.randint(SCREEN_WIDTH + 20 , SCREEN_WIDTH + 100),
                random.randint(0,SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5,20)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


#class Cloud(pygame.sprite.Sprite)
 #   def __init__(self):
  #      super(Cloud,self).__init()
   #     self.surf = pygame.surface(SCREEN_WIDTH,SCREEN_HEIGHT)
    #    self.surf = pygame.image.load("")
        


# Initialize pygame
pygame.init()
pygame.font.init()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
text_surface = my_font.render('GAME OVER!',False, black)

#create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,250)

# Instantiate player. Right now, this is just a rectangle.

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
pygame.mixer.music.load("Tobu - Candyland.mp3")
pygame.mixer.music.play(loops=-1)

running = True

pygame.display.update()
# Main loop

while running:
    clock.tick(75) #165 fps
    # for loop through the event queue

    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
        #add an enemy?
        elif event.type == ADDENEMY:
            new_enemy = Enenmy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    


    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()                 
    screen.fill(sky) 
#draw all sprites

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    #now we check for collisions
    if pygame.sprite.spritecollideany(player,enemies):
        player.kill() 
        screen.blit(text_surface, (0,0))
        running = False
        

    screen.blit(player.surf,player.rect )     # Draw the player on the screen
    pygame.display.flip()  # Update the display
