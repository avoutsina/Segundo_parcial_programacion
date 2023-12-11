import pygame
import random
from soporte_file import *
from bloques import *
from clase_proyectil import *


class Jugador(pygame.sprite.Sprite):
    def __init__(self,x, y,pantalla,actualizar_vida,actualizar_power_up,check_estado_power_up):
        super().__init__()
        self.display_surface = pantalla
        self.check_estado_power_up = check_estado_power_up
        self.power_up = self.check_estado_power_up()
        self.importar_assets_jugador()
        self.indice_frames = 0
        self.velocidad_animacion = 0.15
        self.image = self.animaciones["quieto"][self.indice_frames]
        self.rect = self.image.get_rect(topleft=(x,y))
       
        

        #movimientos del jugador
        self.direccion = pygame.math.Vector2(0,0) 
        self.velocidad = 3
        self.gravity = 0.8
        self.velocidad_salto = -18
        self.rectangulo_colision = pygame.Rect(self.rect.topleft,(45,self.rect.height))


        #jugador status
        self.que_hace = 'quieto'
        self.mirando_derecha = True
        self.piso = False
        self.actualizar_power_up = actualizar_power_up

        #sonidos y efectos
        self.sonido_salto = pygame.mixer.Sound(r"tiles\sonidos\Finn\Voice\salto.wav")
        self.efecto_salto = pygame.mixer.Sound(r"tiles\sonidos\Finn\SFX\salto\salto.wav")
        self.sonido_herido = pygame.mixer.Sound(r"tiles\sonidos\Finn\Voice\herido.wav")
        self.sonido_estocada = pygame.mixer.Sound(r"tiles\sonidos\Finn\Voice\estocada.wav")
        self.sonidos_ataque = import_sonidos(r"tiles\sonidos\Finn\SFX\ataque")
        self.sonidos_disparo = import_sonidos(r"tiles\sonidos\Finn\SFX\disparos")

        #manejo vida
        self.invencible = False
        self.duracion_invencible = 300
        self.tiempo_herido = 0
        self.actualizar_vida = actualizar_vida

        #manejo ataques
        self.esta_atacando = False
        self.esta_disparando = False
        self.duracion_atacando = 500
        self.reiniciar_ataque = True
        self.lista_proyectiles = []


  
    def importar_assets_jugador(self):
        if not self.power_up:
            character_path = r'tiles\personaje'
            self.animaciones = {'quieto':[],'correr':[],'salto':[],'caer':[],'ataque':[],'herido':[]}
        else:
            character_path = r'tiles\power'
            self.animaciones ={'quieto':[],'correr':[],'salto':[],'caer':[],'ataque':[],'disparo':[]}

        for animacion in self.animaciones.keys():
            path_completo = character_path +"\\"+ animacion
            self.animaciones[animacion] = import_carpeta(path_completo)

    def animate(self):
        animacion = self.animaciones[self.que_hace]
        if self.que_hace == "ataque" and self.reiniciar_ataque:
            self.indice_frames = 0
            self.reiniciar_ataque = False
		 
        self.indice_frames += self.velocidad_animacion
        if self.indice_frames >= len(animacion):
            self.indice_frames = 0
            
        image = animacion[int(self.indice_frames)]
        if self.mirando_derecha:
            self.image = image
            self.rect.bottomleft = self.rectangulo_colision.bottomleft
        else:
            imagen_volteada = pygame.transform.flip(image,True,False)
            self.image =  imagen_volteada
            self.rect.bottomright = self.rectangulo_colision.bottomright

		

    def invertir_imagen(self):
        if self.velocidad > 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if not self.invencible:
            if keys[pygame.K_RIGHT]:
                self.direccion.x = 1
                self.mirando_derecha = True
            elif keys[pygame.K_LEFT]:
                self.direccion.x = -1
                self.mirando_derecha = False
            else:
                self.direccion.x = 0
            if not self.esta_atacando and keys[pygame.K_z]:
                self.atacar()
                self.sonido_estocada.set_volume(.3)
                self.sonido_estocada.play()
                numero_random=random.randint(0,10)
                self.sonidos_ataque[numero_random].set_volume(.3)
                self.sonidos_ataque[numero_random].play()
            if self.power_up and not self.esta_disparando:
                if keys[pygame.K_x]:
                    self.disparo()
                    self.lanzar_proyectil()
                    numero_random=random.randint(0,3)
                    self.sonidos_disparo[numero_random].set_volume(.3)
                    self.sonidos_disparo[numero_random].play()
            if keys[pygame.K_SPACE] and self.piso:
                self.saltar()
                self.sonido_salto.set_volume(.3)
                self.sonido_salto.play()
                self.efecto_salto.set_volume(.3)
                self.efecto_salto.play()
        

    def obtener_estado(self):
        if not self.invencible and not self.esta_atacando and not self.esta_disparando:
            if self.direccion.y < 0:
                self.que_hace = 'salto'
            elif self.direccion.y > 1:
                self.que_hace = 'caer'
            else:
                if self.direccion.x != 0:
                    self.que_hace = 'correr'
                else:
                    self.que_hace = 'quieto'
        
    
    def aplicar_gravedad(self):
        self.direccion.y += self.gravity
        self.rectangulo_colision.y += self.direccion.y

    def saltar(self):
        self.direccion.y = self.velocidad_salto

    def get_damage(self,danio,velocidad_enemigo):
        self.sonido_herido.set_volume(.3)
        self.sonido_herido.play()
        if not self.power_up:
            if not self.invencible:
                self.actualizar_vida(danio)
                self.direccion.y = -5
                if velocidad_enemigo > 2:
                    self.direccion.x = 2
                elif velocidad_enemigo < -2:
                    self.direccion.x = -2
                else:
                    self.direccion.x = velocidad_enemigo
            self.que_hace = 'herido'
        else:
            self.actualizar_power_up(False)
            self.direccion.x = velocidad_enemigo
            self.direccion.y = -5
            if velocidad_enemigo > 2:
                self.direccion.x = 2
            elif velocidad_enemigo < -2:
                self.direccion.x = -2
        self.invencible = True
        self.tiempo_herido = pygame.time.get_ticks()
        
            
    def timer_invencible(self):
        if self.invencible:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_herido >= self.duracion_invencible:
                self.invencible = False
    def atacar(self):
        if not self.esta_atacando:
            self.que_hace = 'ataque'
            self.esta_atacando = True
            self.tiempo_atancando = pygame.time.get_ticks()
    def disparo(self):
        if not self.esta_disparando:
            self.que_hace = 'disparo'
            self.esta_disparando = True
            self.tiempo_atancando = pygame.time.get_ticks()
    def lanzar_proyectil(self):
        x = None
        margen = 47
        y = self.rectangulo_colision.centery - 20
        if self.mirando_derecha:
            x = self.rectangulo_colision.right - margen
        elif not  self.mirando_derecha:
            x = self.rectangulo_colision.left -100 + margen
        if x is not None:
            self.lista_proyectiles.append(Proyectil(x,y,20,self.mirando_derecha,(r"tiles\power\proyectil"),12))
    
    def timer_atacando(self):
        if self.esta_atacando:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_atancando >= self.duracion_atacando:
                self.esta_atacando = False
                self.reiniciar_ataque = True
    def timer_disparo(self):
        if self.esta_disparando:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_atancando >= self.duracion_atacando:
                self.esta_disparando = False
                self.reiniciar_ataque = True
    def update(self):
        if not self.invencible:
            self.power_up = self.check_estado_power_up()
        self.importar_assets_jugador()
        self.get_input()
        self.obtener_estado()
        self.animate()
        self.timer_invencible()
        self.timer_atacando()
        self.timer_disparo()

        
        