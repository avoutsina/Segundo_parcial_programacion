import pygame 
from soporte_file import *
from data import *

class Nodo(pygame.sprite.Sprite):
	def __init__(self,posicion,estado,velocidad_icono,path):
		super().__init__()
		self.image = pygame.image.load(path)
		if estado == 'desbloqueado':
			self.estado = 'desbloqueado'
		else:
			self.estado = 'bloqueado'
		self.rect = self.image.get_rect(center = posicion)

		self.zona_deteccion = pygame.Rect(self.rect.centerx-(velocidad_icono/2),self.rect.centery-(velocidad_icono/2),velocidad_icono,velocidad_icono)
	def update(self):
		if self.estado == 'bloqueado':
			lvl_bloqueado = self.image.copy()
			lvl_bloqueado.fill("black",None,pygame.BLEND_RGBA_MULT)
			self.image.blit(lvl_bloqueado,(0,0))

class Icono(pygame.sprite.Sprite):
	def __init__(self,posicion,path):
		super().__init__()
		self.frames = import_carpeta(path)
		self.frame_indice = 0
		self.image = self.frames[self.frame_indice]
		self.posicion = posicion
		self.rect = self.image.get_rect(center = posicion)

	def animar(self):
		self.frame_indice += 0.1
		if self.frame_indice >= 6:
			self.frame_indice = 0
		self.image = self.frames[int(self.frame_indice)]

	def update(self):
		self.animar()
		self.rect.center = self.posicion

class Menu:
	def __init__(self,nivel_inicio,nivel_maximo,pantalla,crear_nivel):

		# setup 
		self.display_surface = pantalla 
		self.nivel_maximo = nivel_maximo
		self.nivel_actual = nivel_inicio
		self.crear_nivel = crear_nivel
		self.frames = importar_fondo(r"tiles\menu\fondo.png")
		self.frame_indice = 0
		self.image = self.frames[self.frame_indice]
		self.rect = self.image.get_rect(center = (0,0))
		# movement logic
		self.moviendose = False
		self.direccion_movimiento = pygame.math.Vector2(0,0)
		self.velocidad = 8
		
		self.ranking = pygame.image.load(r"tiles\menu\puntaje.png")
		self.rect_ranking = self.ranking.get_rect(center = (150,640))
		#musica
		self.music_track = pygame.mixer.music.load(r"tiles\menu\menusong.mp3")
		pygame.mixer.music.set_volume(1)
		# sprites 
		self.setup_nodos()
		self.setup_icono()

	def setup_nodos(self):
		self.nodos = pygame.sprite.Group()

		for indice, data_nodo in enumerate(niveles.values()):
			if indice <= self.nivel_maximo:
				nodo_sprite = Nodo((data_nodo["posicion"][0],data_nodo["posicion"][1]),'desbloqueado',self.velocidad,data_nodo["icono_nivel"])
			else:
				nodo_sprite = Nodo((data_nodo["posicion"][0],data_nodo["posicion"][1]),'blockeado',self.velocidad,data_nodo["icono_nivel"])
			self.nodos.add(nodo_sprite)

	def dibujar_camino(self):
		puntos = []
		for indice,nodo in enumerate(niveles.values()) :
			if indice <= self.nivel_maximo:
				puntos.append(nodo["posicion"]) 
		if len(puntos) >1:
			pygame.draw.lines(self.display_surface,"green",False,puntos,6)     

	def setup_icono(self):
		self.icono = pygame.sprite.GroupSingle()
		icono_sprite = Icono(self.nodos.sprites()[self.nivel_actual].rect.center,r"tiles\personaje\correr")
		self.icono.add(icono_sprite)

	def input(self):
		keys = pygame.key.get_pressed()

		if not self.moviendose:
			if (keys[pygame.K_DOWN] or keys[pygame.K_RIGHT]) and self.nivel_actual < self.nivel_maximo:
				self.direccion_movimiento = self.get_movement_data('siguiente')
				self.nivel_actual += 1
				self.moviendose = True
			elif (keys[pygame.K_UP] or keys[pygame.K_LEFT]) and self.nivel_actual > 0:
				self.direccion_movimiento = self.get_movement_data('previo')
				self.nivel_actual -= 1
				self.moviendose = True
			elif keys[pygame.K_RETURN]:
				if self.nivel_actual == self.nivel_maximo:
					self.crear_nivel(self.nivel_actual)

	def get_movement_data(self,target):
		start = pygame.math.Vector2(self.nodos.sprites()[self.nivel_actual].rect.center)
		
		if target == 'siguiente': 
			end = pygame.math.Vector2(self.nodos.sprites()[self.nivel_actual + 1].rect.center)
		else:
			end = pygame.math.Vector2(self.nodos.sprites()[self.nivel_actual - 1].rect.center)

		return (end - start).normalize()

	def actualizar_icono_posiciono(self):
		if self.moviendose and self.direccion_movimiento:
			self.icono.sprite.posicion += self.direccion_movimiento * self.velocidad
			target_nodo = self.nodos.sprites()[self.nivel_actual]
			if target_nodo.zona_deteccion.collidepoint(self.icono.sprite.posicion):
				self.moviendose = False
				self.direccion_movimiento = pygame.math.Vector2(0,0)

	def animar(self):
		self.frame_indice += 0.25
		if self.frame_indice >= 10:
			self.frame_indice = 0
		self.image = self.frames[int(self.frame_indice)]
		self.display_surface.blit(self.image, (0,0))

	def run(self):
		if not pygame.mixer.music.get_busy():
			pygame.mixer.music.play()
		self.input()
		self.animar()
		self.actualizar_icono_posiciono()
		self.icono.update()
		self.nodos.update()
		self.dibujar_camino()
		self.nodos.draw(self.display_surface)
		self.icono.draw(self.display_surface)
		self.display_surface.blit(self.ranking,self.rect_ranking)
        
        
        
