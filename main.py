#Neil Isaac
#import necessary modules
#core game loop
#input
#update
#draw
#sources:
#https://chatgpt.com/g/g-p-68ffb42bcbc88191b18d019f16717c3d-computer-programming-project-neil/c/68ffb465-8ee4-832d-ba0a-39d2d01acab6: for chasing
# yay I can use github from VS CODE


#Imports all the needed modules to do stuff and imports code from our other files
import math
import random
import sys
import pygame as pg
from settings import *
from sprites import *
from os import path 
from utils import *

#creates class Game and functions
health = 100
class Game:
   def __init__(self):
      pg.init()
      #sets up a clock for fps and time and set
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("Neil Isaac's awesome game!!!!!")
      self.playing = True
   
   #  sets up a game folder directory path that uses the currend foler and contains THIS file
   # gives the Game class a map property which uses the Map class to go through the level1.txt file
   def load_data(self):
      self.game_folder = path.dirname(__file__)
      self.map = Map(path.join(self.game_folder, 'level1.txt'))

   def draw_text(self, surface, text, size, color, x, y):
      font_name = pg.font.match_font('arial')
      font = pg.font.Font(font_name, size)
      text_surface = font.render(text, True, color)
      text_rect = text_surface.get_rect()
      text_rect.midtop = (x,y)
      surface.blit(text_surface, text_rect)

   def new(self):
      # the sprite Group allows us to upate and draw sprite in grouped batches
      self.load_data()
      # create all sprite groups
      self.all_sprites = pg.sprite.Group()
      self.all_mobs = pg.sprite.Group()
      self.all_coins = pg.sprite.Group()
      self.all_walls = pg.sprite.Group()
      #instantiation of a class

      
      for row, tiles, in enumerate(self.map.data):
         print(row)
         for col, tile, in enumerate(tiles):
            print(col)
            if tile == '1':
               Wall(self, col, row, "")

            if tile == 'C':
               Coin(self, col, row)
            elif tile == 'P':
               self.player = Player(self, col, row)
            elif tile == 'M':
               Mob(self, col, row)



      self.all_sprites.add(self.player)
      

   def run(self):
      while self.playing == True:
         self.dt = self.clock.tick(FPS) / 1000
         # input
         self.events()
         # process
         self.update()
         # output
         self.draw()
      pg.quit()

   def events(self):
      for event in pg.event.get():
        if event.type == pg.QUIT:
          print("this is happening")
          self.playing = False
        if event.type == pg.MOUSEBUTTONDOWN:
           #makes sure u can get input from clicking
           print("I can get input from mousey mouse mouse mousekerson")
   def update(self):
      self.all_sprites.update()
      #Time in seconds
      seconds = pg.time.get_ticks()//1000
      #countdown by subtractiing from total seconds
      countdown = 20
      self.time = countdown - seconds
      if self.time <= 0:
         pg.quit


   def draw(self):
      self.screen.fill(WHITE)
      self.all_sprites.draw(self.screen)
      self.draw_text(self.screen, "Health:"+str(self.player.health), 20, BLACK, 30, 20) 
      self.draw_text(self.screen, "Score:"+str(self.player.score), 20, BLACK, 30, 40) 
      self.draw_text(self.screen, "Time:"+ str(self.time), 20, BLACK, 30, 60)
      pg.display.flip()







if __name__ == "__main__":
#    creating an instance or instantiating the Game class
   g = Game()
   g.new()
   g.run()
