import pygame
from soporte_file import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,tamanio, x, y):
        super().__init__()
        self.image = pygame.Surface((tamanio,tamanio))
        self.rect = self.image.get_rect(topleft = (x,y))
    

class TileEstatica(Tile):
    def __init__(self,tamanio, x, y, surface):
        super().__init__(tamanio, x, y)
        self.image = surface


class TileAnimado(Tile):
    def __init__(self,tamanio,x,y,path):
        super().__init__(tamanio, x, y)
        self.frames = import_carpeta(path)
        self.indice_frames = 0
        self.image = self.frames[self.indice_frames]

    def update(self):
        self.animar()

class Platita(TileAnimado):
    def __init__(self,tamanio,x, y, path):
        super().__init__(tamanio, x, y ,path)
        centro_x = x + int(tamanio / 2)
        centro_y = y + int(tamanio / 2)
        self.rect = self.image.get_rect(center = (centro_x, centro_y))
        
    
    def animar(self):
        self.indice_frames += 0.1
        if self.indice_frames >= 3:
            self.indice_frames = 0
        self.image = self.frames[int(self.indice_frames)]

class Vida(TileAnimado):
    def __init__(self,tamanio,x, y, path):
        super().__init__(tamanio, x, y ,path)
        centro_x = x + int(tamanio / 2)
        centro_y = y + int(tamanio / 2)
        self.rect = self.image.get_rect(center = (centro_x, centro_y))
        
    
    def animar(self):
        self.indice_frames += 0.2
        if self.indice_frames >= 3:
            self.indice_frames = 0
        self.image = self.frames[int(self.indice_frames)]

class Power_up(TileAnimado):
    def __init__(self,tamanio,x, y, path):
        super().__init__(tamanio, x, y ,path)
        centro_x = x + int(tamanio / 2)
        centro_y = y + int(tamanio / 2)
        self.rect = self.image.get_rect(center = (centro_x, centro_y))
      
    
    def animar(self):
        self.indice_frames += 0.2
        if self.indice_frames >= 7:
            self.indice_frames = 0
        self.image = self.frames[int(self.indice_frames)]

class Trampa(TileAnimado):
    def __init__(self,tamanio,x, y, path):
        super().__init__(tamanio, x, y ,path)
        centro_x = x + int(tamanio / 2)
        centro_y = y + int(tamanio / 2)
        self.rect = self.image.get_rect(center = (centro_x, centro_y))
      
    
    def animar(self):
        self.indice_frames += 0.1
        if self.indice_frames >= 3:
            self.indice_frames = 0
        self.image = self.frames[int(self.indice_frames)]

