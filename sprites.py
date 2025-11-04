import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
from utils import Cooldown
from random import choice
vec = pg.math.Vector2

# The sprites module contains all the sprites
# Sprites incldue: player, mob - moving object


#creates new class bullet which shoots and breaks walls
class Bullet(Sprite):
    def __init__(self, game, x, y, direction):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)  
        self.image = pg.Surface((TILESIZE[0]/2, TILESIZE[1]/2))
        self.image.fill((255, 192, 203))
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.dir = direction
        self.pos = vec(x+(TILESIZE[0]/4), y+(TILESIZE[0]/4))
        self.speed = 500
    def collide(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, True)
        if hits:
            self.kill()

    def update(self):
        if self.dir == "up":
            self.vel.y = -self.speed*self.game.dt
        elif self.dir == "down":
            self.vel.y = self.speed*self.game.dt
        elif self.dir == "right":
            self.vel.x = self.speed*self.game.dt
        elif self.dir == "left":
            self.vel.x = -self.speed*self.game.dt
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


#Creates player by creating a class
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill((GREEN))
        self.rect = self.image.get_rect()
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.speed = 300
        self.health = 100
        self.score = 0
        self.cd = Cooldown(1000)
        self.bcd = Cooldown(250)
        self.lastdir = "up"
        
    def update(self):
        pass
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            if self.bcd.ready():
                self.bcd.start()
                Bullet(self.game, self.rect.x, self.rect.y, self.lastdir)
        if keys[pg.K_w]:
            self.vel.y = -self.speed*self.game.dt
            self.lastdir = "up"
            # self.rect.y -= self.speed
        if keys[pg.K_a]:
            self.vel.x = -self.speed*self.game.dt
            self.lastdir = "left"
            # self.rect.x -= self.speed
        if keys[pg.K_s]:
            self.vel.y = self.speed*self.game.dt
            self.lastdir = "down"
            # self.rect.y += self.speed
        if keys[pg.K_d]:
            self.vel.x = self.speed*self.game.dt
            self.lastdir = "right"
            # self.rect.x += self.speed
        # accounting for diagonal movement
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
            # uses collide with walls to check if wall is moveable and then changing its velocity based on that
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                        
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                    
                self.rect.x = self.pos.x
            
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                


    def collide_with_stuff(self, group, kill):
        #constantly checking whether a spirte has collided with a certain group
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: 
            if str(hits[0].__class__.__name__) == "Mob":
                print("i collided with a mob")
                if self.cd.ready():
                    self.health -= 10
                    self.cd.start()

                if self.health == 0:
                    pg.quit()
            if str(hits[0].__class__.__name__) == "Coin":
                self.score += 1    
    def update(self):
        self.get_keys()
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_coins, True)
        if not self.cd.ready():
            self.image.fill(BLUE)
            print("not ready")
        else:
            self.image.fill(GREEN)
            print("ready")

#Creates Mob using same code as player but not controllable with keys
class Mob(Sprite):
    def __init__(self, game, x, y):
        Sprite.__init__(self)
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)  
        self.vel = vec(choice([-10, 10]),choice([-10, 10]))
        self.pos = vec(x*TILESIZE[0], y*TILESIZE[1])
        self.image = pg.Surface((32, 32))
        self.image.fill((RED))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
        self.speed = 5
    def collide_with_walls(self, dir):
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
                if hits:
                    if self.vel.x > 0:
                        self.pos.x = hits[0].rect.left - self.rect.width
                    if self.vel.x < 0:
                        self.pos.x = hits[0].rect.right
                    self.rect.x = self.pos.x
                    self.vel.x = 0
                    # makes the mobs bounce randomly off wall using vectors
                    # self.rect.x = self.pos.x
                    # self.vel.x *= choice([-1, 1])
                    
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
                if hits:
                    if self.vel.y > 0:
                        self.pos.y = hits[0].rect.top - self.rect.height
                    if self.vel.y < 0:
                        self.pos.y = hits[0].rect.bottom
                    self.rect.y = self.pos.y
                    self.vel.y = 0
                    # makes the mobs bounce randomly off wall using vectors
                    # self.rect.y = self.pos.y
                    # self.vel.y *= choice([-1, 1])
    def chase_player(self, dir):
        #used chat gpt for help because my mobs were only moving when I moved
            # Get player reference from game
        player = self.game.player

        # Vector pointing from mob to player
        dir = player.pos - self.pos

        # Normalize to length 1 so movement is consistent
        if dir.length() > 0:
            dir = dir.normalize()

        # Move in that direction
        self.vel = dir * self.speed

        # Move on each axis separately so it collides with walls
        self.pos.x += self.vel.x * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')

        self.pos.y += self.vel.y * self.game.dt
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        # if dir == 'x':
        #     if self.game.player.pos.x > self.pos.x:
        #         self.vel.x = abs(0.7 * self.game.player.vel.x)
        #     elif self.game.player.pos.x < self.pos.x:
        #         self.vel.x = -abs(0.7 * self.game.player.vel.x)
        # if dir == 'y':
        #     if self.game.player.pos.y > self.pos.y:
        #         self.vel.y = abs(0.7 * self.game.player.vel.y)
        #     elif self.game.player.pos.y < self.pos.y:
        #         self.vel.y = -abs(0.7 * self.game.player.vel.y)


        

    def update(self):
        #mob behavior
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.chase_player('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.chase_player('y')
        # if self.game.player.vel.x > self.vel.x:
        #     self.vel.x = self.game.player.vel.x
#Creates coin using same code as mob but it doesnt move
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)  
        self.image = pg.Surface(TILESIZE)
        self.image.fill((YELLOW))
        self.rect = self.image.get_rect()
        self.rect.x = x* TILESIZE[0]
        self.rect.y = y* TILESIZE[1]
        
class Wall(Sprite):
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pg.Surface(TILESIZE)
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.state = state
    def update(self):
        # wall
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
       






