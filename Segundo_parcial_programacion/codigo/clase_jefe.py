import pygame
from soporte_file import *
from config import * 
from clase_proyectil import *

class Jefe(pygame.sprite.Sprite):
    def __init__(self,x, y,pantalla,check_vida,check_en_rango,check_transformate):
        super().__init__()
        #transformacion
        self.check_transformate = check_transformate
        self.transformacion = self.check_transformate()
        self.se_esta_trasformando = False
        self.se_transformo = False
        self.reiniciar_animacion = True
        self.duracion_transformacion = 1000
        self.tiempo_transformandose = 0

        #manejo vida
        self.check_vida = check_vida
        self.vida = self.check_vida()
        self.vida_anterior = self.vida
        self.display_surface = pantalla

        #assets
        self.importar_assets_jefe()
        self.indice_frames = 0
        self.velocidad_animacion = 0.15
        self.image = self.animaciones["quieto"][self.indice_frames]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.rectangulo_colision = pygame.Rect(((self.rect.topleft[0]+41),self.rect.topleft[1]),(45,self.rect.height))
       
        #movimientos del jugador
        self.direccion = pygame.math.Vector2(0,0) 
        self.velocidad = -5
        #sonido
        self.sonido_en_rango = pygame.mixer.Sound(r"tiles\sonidos\efectos\se_theme_act.wav")
        #herido
        self.invencible = False
        self.duracion_invencible = 600
        self.tiempo_herido = 0

        #enemigo status
        self.que_hace = 'quieto'
        self.mirando_derecha = False
        self.piso = False
        self.techo = False
        self.herido = False

        #manejo ataques
        self.check_en_rango = check_en_rango
        self.en_rango = self.check_en_rango()
        self.bandera_sonido = self.check_en_rango()
        self.esta_atacando = False
        self.esta_disparando = False
        self.duracion_atacando = 750
        self.tiempo_atancando = 0
        self.lista_proyectiles = []

    def importar_assets_jefe(self):
        if not self.se_transformo:
            character_path = r'tiles/jefe/marceline'
            self.animaciones = {'quieto':[],'herido':[],"transformacion":[],'disparo':[]}
        elif self.se_transformo and not self.se_esta_trasformando:
            character_path = r'tiles\jefe\murcielago'
            self.animaciones ={'quieto':[],'disparo':[],'herido':[]}

        for animacion in self.animaciones.keys():
            path_completo = character_path +"\\"+ animacion
            self.animaciones[animacion] = import_carpeta(path_completo,True)
    
    def animate(self):
        animacion = self.animaciones[self.que_hace]
        if self.que_hace == "transformacion" and self.reiniciar_animacion:
            self.indice_frames = 0
            self.reiniciar_animacion = False

        self.indice_frames += self.velocidad_animacion
            
        if self.indice_frames >= len(animacion):
            self.indice_frames = 0
            
        image = animacion[int(self.indice_frames)]
        if not self.mirando_derecha:
            self.image = image
            

        else:
            imagen_volteada = pygame.transform.flip(image,True,False)
            self.image =  imagen_volteada
            

    def mover(self):
        self.rect.x += self.velocidad 
        if self.rect.x < 0 or self.rect.right > WIDTH:
            self.reversa()
            self.cambiar_sentido()
    def reversa(self):
        self.velocidad *= -1
    def get_input(self):
        if self.vida != self.vida_anterior:
                self.recivio_danio()
        elif self.vida == self.vida_anterior and not self.invencible and not self.esta_disparando and not self.esta_atacando and not self.se_esta_trasformando and not self.en_rango:
            self.que_hace = "quieto"
        if self.en_rango and not self.invencible and not self.esta_disparando and not self.se_esta_trasformando:
                self.disparo()
                
        if self.transformacion and not self.se_transformo and not self.se_esta_trasformando:
            self.activar_transformacion()
        elif self.se_transformo and not self.se_esta_trasformando and not self.invencible and not self.esta_disparando and not self.esta_atacando and not self.en_rango:
            self.mover()
        if self.en_rango != self.bandera_sonido :
            self.sonido_en_rango.set_volume(0.2)
            self.sonido_en_rango.play()
            self.bandera_sonido = self.en_rango
            

            
        
    def cambiar_sentido(self):
        self.mirando_derecha = not self.mirando_derecha
    def recivio_danio(self):
        self.que_hace = 'herido'
        self.vida_anterior = self.vida
        self.invencible = True
        self.tiempo_herido = pygame.time.get_ticks()
    def timer_invencible(self):
        if self.invencible:
            tiempo_actual_invencible = pygame.time.get_ticks()
            if tiempo_actual_invencible - self.tiempo_herido >= self.duracion_invencible:
                self.invencible = False
    def timer_disparo(self):
        if self.esta_disparando:
            tiempo_actual_disparo = pygame.time.get_ticks()
            if tiempo_actual_disparo - self.tiempo_atancando >= self.duracion_atacando:
                self.lanzar_proyectil()
                self.esta_disparando = False
                self.salio_el_proyectil = True
                self.reiniciar_animacion = True

    
    def timer_transformacion(self):
        if self.transformacion and self.se_esta_trasformando:
            tiempo_actual_transformacion = pygame.time.get_ticks()
            if tiempo_actual_transformacion - self.tiempo_transformandose >= self.duracion_transformacion:
                self.se_transformo = True
                self.se_esta_trasformando = False
    
    def activar_transformacion(self):
        self.que_hace = 'transformacion'
        self.tiempo_transformandose = pygame.time.get_ticks()
        self.se_esta_trasformando = True
    def disparo(self):
        if not self.esta_disparando and not self.invencible:
            self.que_hace = 'disparo'
            self.esta_disparando = True
            self.tiempo_atancando = pygame.time.get_ticks()
    def lanzar_proyectil(self):
        if not self.invencible:
            x = None
            margen = 47
            y = self.rectangulo_colision.centery
            if  self.mirando_derecha:
                x = self.rectangulo_colision.right - margen
            elif not  self.mirando_derecha:
                x = self.rectangulo_colision.left -100 + margen
            if x is not None:
                if not self.se_transformo:
                    path = r"tiles\jefe\marceline\proyectiles"
                    self.lista_proyectiles.append(Proyectil(x,y,20,self.mirando_derecha,(path),False))
                else:
                    path = r"tiles\jefe\murcielago\proyectil"
                    self.lista_proyectiles.append(Proyectil(x,y,20,self.mirando_derecha,(path),False,15))
    def update(self):
        self.get_input()
        self.animate()
        self.vida = self.check_vida()
        self.en_rango = self.check_en_rango()
        self.transformacion = self.check_transformate ()
        self.timer_transformacion()
        self.importar_assets_jefe()
        self.timer_invencible()
        self.timer_disparo()
        self.rectangulo_colision = pygame.Rect(((self.rect.topleft[0]+41),self.rect.topleft[1]),(45,self.rect.height))
        if self.se_transformo and not self.se_esta_trasformando:
            self.velocidad_animacion = 0.30
            self.duracion_atacando = 300