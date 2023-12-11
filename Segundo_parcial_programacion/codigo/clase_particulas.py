import pygame
from soporte_file import *

class EfectosParticulas(pygame.sprite.Sprite):
    def __init__(self,pos,type):
        super().__init__()
        self.indice_frame = 0
        self.velocidad_animacion = 0.2
        if type == "explocion":
            self.frames = import_carpeta(r"tiles\efectos\explocion")
        if type == "proyectil":
            self.frames = import_carpeta(r"tiles\efectos\proyectil")
        self.image = self.frames[self.indice_frame]
        self.rect = self.image.get_rect(center = pos)

    def animar(self):
        self.indice_frame += self.velocidad_animacion
        if self.indice_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.indice_frame)]
    def update (self):
        self.animar()