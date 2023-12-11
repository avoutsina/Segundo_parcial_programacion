import pygame

class Interfas:
    def __init__(self,surface,valor=True):
        #setup
        self.display_surface = surface
        self.valor = valor

        #vida
        self.barra_vida = pygame.image.load(r"tiles\puntaje\barra_vida.png").convert_alpha()
        if self.valor:
            self.barra_vida_topleft = (52,19)
            self.ancho_maximo_barra = 163
        else:
            self.barra_vida_topleft = (1100,19)
            self.ancho_maximo_barra = 163
        self.alto_barra = 24

        #fuente
        self.font = pygame.font.Font(r"tiles\puntaje\fuente\DePixelHalbfett.ttf",30)

        #gemas
        self.barra_gemas = pygame.image.load(r"tiles\puntaje\puntaje.png").convert_alpha()
        self.barra_gemas_rect = self.barra_gemas.get_rect(topleft = (10,50))
    
    def mostrar_vida(self,vida_actual,vida_maxima):
        vida_actual_ratio = vida_actual / vida_maxima
        ancho_actual_barra = self.ancho_maximo_barra * vida_actual_ratio
        barra_vida_rect = pygame.Rect((self.barra_vida_topleft),(ancho_actual_barra,self.alto_barra))
        cantidad_vida_surf = self.font.render(str(vida_actual),False,"White")
        if self.valor:
            cantidad_vida_rect = cantidad_vida_surf.get_rect(midleft = (225,33))
            pygame.draw.rect(self.display_surface,"red",barra_vida_rect)
            self.display_surface.blit(self.barra_vida,(20,10))
        else:
            cantidad_vida_rect = cantidad_vida_surf.get_rect(midleft = (1010,33))
            pygame.draw.rect(self.display_surface,"Purple",barra_vida_rect)
            self.display_surface.blit(self.barra_vida,(1068,10))
        self.display_surface.blit(cantidad_vida_surf,cantidad_vida_rect)

    def mostrar_gemas(self,gemas_actual):
        self.display_surface.blit(self.barra_gemas,self.barra_gemas_rect)
        cantidad_gemas_surf = self.font.render(str(gemas_actual),False,"White")
        cantidad_gemas_rect = cantidad_gemas_surf.get_rect(midleft = (self.barra_gemas_rect.right +4 ,self.barra_gemas_rect.centery))
        self.display_surface.blit(cantidad_gemas_surf,cantidad_gemas_rect)

