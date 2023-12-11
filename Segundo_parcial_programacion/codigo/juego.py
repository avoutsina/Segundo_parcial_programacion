import pygame, sys, re, sqlite3
from config import *
from clase_nivel import *
from data import *
from modo import *
from puntajes import Interfas
from clase_menu import *


class Juego:
    def __init__(self):
        #SQLite 
        
        self.conn = sqlite3.connect(r'data_base\sql_db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS "Jugadores" (
        "nombre"    TEXT UNIQUE,
        "puntaje"   INTEGER
    )
''')
        self.ranking = self.obtener_ranking()
        #usuario
        self.nombre = ""
        #atrivutos del juego
        self.nivel_maximo = 0
        self.nivel_actual = 0
        self.vida_maxima = 10
        self.vida_actual = 10
        self.gemas = 0
        self.puntaje = 0
        self.power_up = False
        #interfas
        self.inter = Interfas(PANTALLA)
        #sonidos
        self.sonido_muerte = pygame.mixer.Sound(r"tiles\sonidos\Finn\Voice\muerte.wav")
        self.music_track = pygame.mixer.music.load(r"tiles\menu\menusong.mp3")
        pygame.mixer.music.set_volume(1)
        #setup menu
        self.menu = Menu(self.nivel_actual,self.nivel_maximo,PANTALLA,self.crear_nivel)
        self.estado = "menu"


    def crear_nivel(self,nivel):
        self.nivel = Nivel(nivel,PANTALLA,self.actualizar_menu,self.actualizar_gemas,self.actualizar_vidas,self.actualizar_power_up,self.check_estado_power_up,self.check_cantidad_gemas,self.actualizar_puntaje,self.check_vida,self.actualizar_estado )
        self.estado = "lvl"
        
    def actualizar_menu(self,nivel,nivel_desbloqueado):
        if nivel_desbloqueado > self.nivel_maximo:
            self.nivel_maximo = nivel_desbloqueado
        self.menu = Menu(nivel,self.nivel_maximo,PANTALLA,self.crear_nivel)
        self.estado = "menu"  
    def actualizar_gemas (self,monto,bool):
        if bool == True:
            self.gemas += monto
        else:
            self.gemas = monto
    def actualizar_vidas (self,monto):
        if monto > 0:
            if self.vida_actual == self.vida_maxima:
                self.vida_maxima+=monto
            self.vida_actual+=monto
        else:
            if self.power_up:
                self.power_up = False
            else:
                self.vida_actual += monto
    def check_vida(self):
        return self.vida_actual
    def check_cantidad_gemas (self):
        return self.gemas
    def actualizar_power_up(self,valor):
        self.power_up = valor
    def check_estado_power_up(self):
        return self.power_up
    def actualizar_puntaje(self,valor):
        self.puntaje = valor
    def actualizar_estado(self,valor):
        self.estado = valor
    def guardar_partida(self):
        player_name = self.nombre
        puntaje_int = self.puntaje

        # Utiliza la cláusula ON CONFLICT REPLACE para sobrescribir el nombre si ya existe
        self.cursor.execute('''
                INSERT INTO Jugadores (nombre, puntaje)
                VALUES (?, ?)
            ''', (player_name, puntaje_int))
        self.conn.commit()
    def obtener_ranking(self):
        try:
            self.cursor.execute('''
                SELECT nombre, puntaje FROM Jugadores
                ORDER BY puntaje DESC 
                LIMIT 3
            ''')
            ranking = self.cursor.fetchall()
            return ranking
        except Exception as e:
            print("Error al obtener ranking:", e)
            return []

    def run(self):
        if self.vida_actual <= 0:
            self.sonido_muerte.set_volume(.3)
            self.sonido_muerte.play()
            self.vida_actual = 10
            self.vida_maxima = 10
            self.gemas = 0
            self.nivel_maximo = 0
            self.nivel_actual = 0
            self.menu = Menu(self.nivel_actual,self.nivel_maximo,PANTALLA,self.crear_nivel)
            self.estado = "menu"
        if self.estado == "menu":
            cur = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if cur[0] >= 108 and cur[0] <= 208 and cur[1] >= 595 and cur[1] <= 700:
                if click[0] == 1:
                    juego.estado = "ranking"
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            self.menu.run()
        elif self.estado == "lvl":
            self.nivel.run()
            self.inter.mostrar_vida(self.vida_actual,self.vida_maxima) 
            self.inter.mostrar_gemas(self.gemas)
        elif self.estado == "nombre":
            self.estado,self.nombre = ingresar_nombre(PANTALLA, WIDTH, HEIGHT, self.estado, self.nombre)
        elif juego.estado == "ranking":
            juego.estado = mostrar_pantalla_ranking(PANTALLA, WIDTH, self.estado,self.ranking)

def validar_nombre(name):
    return re.match("^[a-zA-Z0-9]+$", name) is not None
def ingresar_nombre(PANTALLA, width, height, estado, nombre):
    fondo_nombre = pygame.image.load(r"tiles\menu\fondo nombre.jpg")
    PANTALLA.blit(fondo_nombre, (0, 0))
    fuente_mediana = pygame.font.Font(r"tiles\puntaje\fuente\DePixelHalbfett.ttf",30)
    fuente_chica = pygame.font.Font(r"tiles\puntaje\fuente\DePixelHalbfett.ttf",20)
    titulo = fuente_mediana.render("Ingrese su nombre:", False, "White")
    usuario_input = fuente_chica.render(nombre, False, "white")
    mensaje_error = fuente_mediana.render("",False, "white")

    PANTALLA.blit(titulo, (width // 4+80, height // 2 - 150))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        if validar_nombre(nombre):
            juego.guardar_partida()
            pygame.time.wait(500)
            estado = "menu"
        else:
            mensaje_error = fuente_chica.render("Nombre no válido. Solo letras y números.", True, (255, 0, 0))


    usuario_input = fuente_chica.render(nombre, True, "white")
    PANTALLA.blit(usuario_input, (width // 2.75+70, height // 2 + 50))
    PANTALLA.blit(mensaje_error, (width // 4.3, height // 2 + 250))
    return estado, nombre

def mostrar_pantalla_ranking(pantalla, pantalla_width, status, ranking):
    fondo_pausa = pygame.image.load(r"tiles\menu\fondo nombre.jpg")
    pantalla.blit(fondo_pausa, (0, 0))
    fuente_mediana = pygame.font.Font(r"tiles\puntaje\fuente\DePixelHalbfett.ttf",30)
    fuente_chica = pygame.font.Font(r"tiles\puntaje\fuente\DePixelHalbfett.ttf",20)



    header_text = fuente_mediana.render("Ranking global", False, "#910101")
    pantalla.blit(header_text, (pantalla_width // 3.3 + 100, pantalla.get_height() // 3.2))
    keys = pygame.key.get_pressed()

    y = 350
    for i, jugador in enumerate(ranking, 1):
        nombre, puntaje = jugador
        jugador_text = fuente_chica.render(f"{i}. {nombre}: {puntaje}", True, "white")
        pantalla.blit(jugador_text, (pantalla_width // 3+100, y))
        y += 100
    if keys[pygame.K_ESCAPE]:
        status = "menu"

    pygame.display.flip()
    return status


pygame.init()
FPS = 60
PANTALLA = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
juego = Juego()
maximo_caractreres = 10
corriendo = True

while corriendo:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()
        if juego.estado == "nombre":
            if keys[pygame.K_BACKSPACE]:
                juego.nombre = juego.nombre[:-1]
            else:
                if len(juego.nombre) < maximo_caractreres:
                        if event.type == pygame.KEYDOWN:
                            if event.key != pygame.K_RETURN:
                                key_name = pygame.key.name(event.key)
                                if len(key_name) == 1 and key_name.isprintable():
                                    juego.nombre += key_name
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    cambiar_modo()
    juego.run()
    
    pygame.display.update()
    clock.tick(FPS)