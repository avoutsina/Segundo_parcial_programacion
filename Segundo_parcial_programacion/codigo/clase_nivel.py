import pygame
from data import *
from soporte_file import *
from config import *
from bloques import *
from enemigos import *
from jugador import *
from clase_jefe import *
from puntajes import *
from modo import *
from clase_particulas import EfectosParticulas



class Nivel:
    def __init__(self,nivel_actual,surface,actualizar_menu,actualizar_gemas,actualizar_vidas,actualizar_power_up,check_valor_power_up,check_cantidad_gemas,actualizar_puntaje,check_vida,actualizar_estado):
        #General
        self.display_surface = surface
        self.actualizar_estado = actualizar_estado
        #Menu
        self.actualizar_menu = actualizar_menu
        self.nivel_actual = nivel_actual
        nivel_data = niveles[self.nivel_actual]
        self.nivel_maximo = nivel_data["desbloquea"]
        #Ui
        self.inter = Interfas(self.display_surface,False)
        #Interfas
        self.actualizar_gemas = actualizar_gemas
        self.actualizar_vidas = actualizar_vidas
        self.actualizar_power_up = actualizar_power_up
        self.check_valor_power_up = check_valor_power_up
        self.power_up = self.check_valor_power_up()
        self.check_cantidad_gemas = check_cantidad_gemas
        self.cantidad_gemas = self.check_cantidad_gemas()
        self.actualizar_puntaje = actualizar_puntaje
        self.check_vida = check_vida
        self.vida = self.check_vida()
        self.puntaje = 0
        #musica y efectos
        self.music_track = pygame.mixer.music.load(nivel_data["musica"])
        pygame.mixer.music.set_volume(.3)
        self.sonido_victoria = pygame.mixer.Sound(r"tiles\sonidos\Finn\Voice\victoria.wav")
        self.sonido_muerte = pygame.mixer.Sound(r"tiles\sonidos\Finn\Voice\muerte.wav")
        self.sonido_explocion = pygame.mixer.Sound(r"tiles\sonidos\Finn\SFX\explocion\se_theme_bom.wav")
        self.sonido_gema = pygame.mixer.Sound(r"tiles\sonidos\Finn\SFX\items\gema.wav")
        self.sonido_vida = pygame.mixer.Sound(r"tiles\sonidos\Finn\SFX\items\vida.wav")
        self.sonido_power_up = pygame.mixer.Sound(r"tiles\sonidos\Finn\SFX\items\power_up.wav")


        #Fondo
        if self.nivel_actual == 0:
            path = r"tiles\fondo\fondo_lvl_1.png"
        elif self.nivel_actual == 1:
            path = r"tiles\fondo\fondo lvl2.jpg"
        else:
            path = r"tiles\fondo\fondo lvl3.jpg"
        self.fondo = pygame.transform.scale(pygame.image.load(path),(WIDTH, HEIGHT))

        #Jugador
        jugador_layout = import_csv_layout(nivel_data['jugador'])
        self.jugador = pygame.sprite.GroupSingle()
        self.jugador_setups(jugador_layout,actualizar_vidas)
        self.jugador_en_el_piso = False

        #Terreno
        terreno_layout= import_csv_layout(nivel_data["terreno"])
        self.terreno_sprites = self.crear_grupo_tiles(terreno_layout,"terreno")

        #Items
        vidas_layout= import_csv_layout(nivel_data["vida"])
        self.vidas_sprites = self.crear_grupo_tiles(vidas_layout,"vida")
        gemas_layout= import_csv_layout(nivel_data["gemas"])
        self.gemas_sprites = self.crear_grupo_tiles(gemas_layout,"gemas")
        power_up_layout= import_csv_layout(nivel_data["power_up"])
        self.power_up_sprites = self.crear_grupo_tiles(power_up_layout,"power_up")

        #Trampas
        trampas_layout= import_csv_layout(nivel_data["trampas"])
        self.trampas_sprites = self.crear_grupo_tiles(trampas_layout,"trampas")

        #explocion
        self.explocion_sprites = pygame.sprite.Group()
        #Enemigos
        enemigos_layout= import_csv_layout(nivel_data["enemigos"])
        self.enemigos_sprites = self.crear_grupo_tiles(enemigos_layout,"enemigos")
        #jefe
        self.en_rango = False
        self.transformate = False
        self.choco_proyectil = False
        if self.nivel_actual == 2:
            self.vida_maxima_jefe = 40
            self.vida_jefe = 40
            jefe_layout = import_csv_layout(nivel_data['jefe'])
            self.jefe = pygame.sprite.GroupSingle()
            self.jefe_setups(jefe_layout)

            
        #Limites enemigos
        limites_layout= import_csv_layout(nivel_data["limites"])
        self.limites_sprites = self.crear_grupo_tiles(limites_layout,"limites")

    def blitear_bordes(self):
        for bordes in self.bordes:
            self.display_surface.blit(bordes,(0,0))

    def crear_grupo_tiles(self,layout,type):
        grupo_sprites = pygame.sprite.Group()

        for indice_fila, fila in enumerate(layout):
            for indice_columna, bloque in enumerate(fila):
                if bloque != "-1":
                    x = indice_columna * tamanio_tiles
                    y = indice_fila * tamanio_tiles

                    if type == "terreno":
                        if self.nivel_actual == 0:
                            lista_terrenos_tiles = import_imagen_fraccionada(r"tiles\terreno\pasto - Copy.png")
                        elif self.nivel_actual == 1:
                            lista_terrenos_tiles = import_imagen_fraccionada(r"tiles\terreno\lianas.png")
                        else:
                            lista_terrenos_tiles = import_imagen_fraccionada(r"tiles\terreno\ladrillo.png")
                        tile_surface = lista_terrenos_tiles[int(bloque)]
                        sprite = TileEstatica(tamanio_tiles, x, y, tile_surface)
                    
                    if type == "vida":
                        if bloque == "0":
                            sprite = Vida(tamanio_tiles, x, y, r"tiles\items\vida")

                    if type == "gemas":
                        if bloque == "0":
                            sprite = Platita(tamanio_tiles, x, y, r"tiles\items\platita")

                    if type == "power_up":
                        if bloque == "0":
                            sprite = Power_up(tamanio_tiles, x, y, r"tiles\items\power_up")
                    
                    if type == "trampas":
                        sprite = Trampa(tamanio_tiles, x, y, r"tiles\trampas\trampa_fuego")
                    
                    if type == "enemigos":
                        if bloque == "0":
                            if self.nivel_actual == 0:
                                sprite = Gusano(tamanio_tiles, x, y)
                            elif self.nivel_actual == 1:
                                sprite = Estrella(tamanio_tiles, x, y)
                            else:
                                sprite = Zombie(tamanio_tiles, x, y)
                        
                    if type == "limites":
                        sprite = Tile(tamanio_tiles,x ,y)
                        
                    grupo_sprites.add(sprite)
           
        return grupo_sprites

    def jugador_setups(self,layout,actualizar_vida):
        for indice_fila, fila in enumerate(layout):
            for indice_columna, valor in enumerate(fila):
                x = indice_columna *tamanio_tiles
                y = indice_fila *tamanio_tiles
                if valor == "0":
                    sprite = Jugador(x,y,self.display_surface,actualizar_vida,self.actualizar_power_up,self.check_valor_power_up)
                    self.jugador.add(sprite)
    def jefe_setups(self,layout):
        for indice_fila, fila in enumerate(layout):
            for indice_columna, valor in enumerate(fila):
                x = indice_columna * tamanio_tiles
                y = indice_fila * tamanio_tiles
                if valor == "0":
                    sprite = Jefe(x,y,self.display_surface,self.check_vida_jefe,self.check_en_rango,self.check_transformate)
                    self.jefe.add(sprite)
    def colision_enemigo_limites(self):
        for enemigo in self.enemigos_sprites.sprites():
            if pygame.sprite.spritecollide(enemigo,self.limites_sprites,False):
                enemigo.reversa()
    def colision_movimentos_horizontal(self):
        jugador = self.jugador.sprite
        jugador.rectangulo_colision.x += jugador.direccion.x * jugador.velocidad
        sprites_colicionables = self.terreno_sprites.sprites()
        for sprite in sprites_colicionables:
            if sprite.rect.colliderect(jugador.rectangulo_colision):
                if jugador.direccion.x < 0: 
                    jugador.rectangulo_colision.left = sprite.rect.right
                    jugador.izquierda = True
                    self.x_actual = jugador.rectangulo_colision.left
                elif jugador.direccion.x > 0:
                    jugador.rectangulo_colision.right = sprite.rect.left
                    jugador.derecha = True
                    self.x_actual = jugador.rectangulo_colision.right
        if jugador.rectangulo_colision.x <= 0:
            jugador.rectangulo_colision.x = 0
        elif jugador.rectangulo_colision.x >= 1235:
            jugador.rectangulo_colision.x = 1235
    def colision_movimentos_vertical(self):
        jugador = self.jugador.sprite
        jugador.aplicar_gravedad()
        sprites_colicionables = self.terreno_sprites.sprites()
        
        for sprite in sprites_colicionables:
            if sprite.rect.colliderect(jugador.rectangulo_colision):
                if jugador.direccion.y > 0: 
                    jugador.rectangulo_colision.bottom = sprite.rect.top
                    jugador.direccion.y = 0
                    jugador.piso = True
                elif jugador.direccion.y < 0:
                    jugador.rectangulo_colision.top = sprite.rect.bottom
                    jugador.direccion.y = 0
                    jugador.techo = True

        if jugador.piso and jugador.direccion.y < 0 or jugador.direccion.y > 1:
            jugador.piso = False
    def poner_jugador_en_el_piso(self):
        if self.jugador.sprite.piso:
            self.jugador_en_el_piso = True
        else:
            self.jugador_en_el_piso = False
    def chequear_caida(self):
        if self.jugador.sprite.rect.top > HEIGHT:
            self.actualizar_vidas(-1)
            self.actualizar_menu(self.nivel_actual,0)
            self.actualizar_gemas(self.cantidad_gemas,False)
            self.sonido_muerte.set_volume(0.3)
            self.sonido_muerte.play()
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.actualizar_gemas(self.cantidad_gemas,False)
            self.actualizar_menu(self.nivel_actual,self.nivel_actual)
    def chequear_colision_power_up(self):
        power_up_colicionadas = pygame.sprite.spritecollide(self.jugador.sprite,self.power_up_sprites,True)
        if power_up_colicionadas:
            for power_up in power_up_colicionadas:
                self.actualizar_power_up(True)
                self.sonido_power_up.set_volume(0.3)
                self.sonido_power_up.play()
    def chequear_colision_gemas(self):
        gemas_colicionadas = pygame.sprite.spritecollide(self.jugador.sprite,self.gemas_sprites,True)
        if gemas_colicionadas:
            for gemas in gemas_colicionadas:
                self.actualizar_gemas(1,True)
                self.sonido_gema.set_volume(0.2)
                self.sonido_gema.play()
        if len(self.gemas_sprites) == 0 and self.nivel_actual !=2:
            nuevo_valor = lambda g,v:g*v
            puntaje = nuevo_valor(self.cantidad_gemas,self.vida)
            self.actualizar_puntaje(puntaje)
            self.sonido_victoria.play()
            self.actualizar_menu(self.nivel_actual,self.nivel_maximo)
    def chequear_colision_vidas(self):
        vidas_colicionadas = pygame.sprite.spritecollide(self.jugador.sprite,self.vidas_sprites,True)
        if vidas_colicionadas:
            for vidas in vidas_colicionadas:
                self.actualizar_vidas(1)
                self.sonido_vida.set_volume(0.3)
                self.sonido_vida.play()
    def chequear_colision_enemigos(self):
        match self.nivel_actual:
            case 0:
                danio = -1
            case 1:
                danio = -2
            case 2:
                danio = -2
        enemigos_colisionados = pygame.sprite.spritecollide(self.jugador.sprite,self.enemigos_sprites,False)
        if enemigos_colisionados:
            for enemigo in enemigos_colisionados:
                centro_enemigo = enemigo.rect.centery
                top_enemigo = enemigo.rect.top
                left_enemigo = enemigo.rect.left
                right_enemigo = enemigo.rect.right
                bottom_jugador = self.jugador.sprite.rectangulo_colision.bottom
                right_jugador = self.jugador.sprite.rectangulo_colision.right
                left_jugador = self.jugador.sprite.rectangulo_colision.left
                if top_enemigo < bottom_jugador < centro_enemigo and self.jugador.sprite.direccion.y >= 0:
                    self.jugador.sprite.direccion.y = -15
                    explocion_sprite = EfectosParticulas(enemigo.rect.center,"explocion")
                    self.explocion_sprites.add(explocion_sprite)
                    enemigo.kill()
                    self.sonido_explocion.set_volume(0.2)
                    self.sonido_explocion.play()
                elif not self.jugador.sprite.esta_atacando and (right_jugador > left_enemigo and right_enemigo > right_jugador) or (right_enemigo > left_jugador and right_jugador > right_enemigo):
                    if not self.power_up:
                        self.jugador.sprite.get_damage(danio,enemigo.velocidad)
                    else:
                        self.jugador.sprite.get_damage(0,enemigo.velocidad)
                        self.power_up = False
                else:
                    if not self.jugador.sprite.mirando_derecha and (right_jugador > left_enemigo and right_jugador< right_enemigo):
                        if not self.power_up:
                            self.jugador.sprite.get_damage(danio,enemigo.velocidad)
                        else:
                            self.jugador.sprite.get_damage(0,enemigo.velocidad)
                            self.power_up = False
                    elif self.jugador.sprite.mirando_derecha and (left_jugador < right_enemigo and left_jugador > left_enemigo):
                        if not self.power_up:
                            self.jugador.sprite.get_damage(danio,enemigo.velocidad)
                        else:
                            self.jugador.sprite.get_damage(0,enemigo.velocidad)
                            self.power_up = False
    def chequear_colision_jefe(self):
        jugador = self.jugador.sprite
        if self.jefe.sprite.rect.colliderect(jugador.rectangulo_colision) and not self.jefe.sprite.invencible:
            self.jugador.sprite.get_damage(2,self.jefe.sprite.velocidad)
    def chequear_colision_ataques(self):
        enemigos_colisionados = pygame.sprite.spritecollide(self.jugador.sprite,self.enemigos_sprites,False)
        if enemigos_colisionados:
            for enemigo in enemigos_colisionados:
                left_enemigo = enemigo.rect.left
                right_enemigo = enemigo.rect.right
                right_jugador = self.jugador.sprite.rect.right
                left_jugador = self.jugador.sprite.rect.left
                if self.jugador.sprite.esta_atacando:
                    if self.jugador.sprite.mirando_derecha:
                        if (right_jugador > left_enemigo and right_jugador < right_enemigo ):
                            explocion_sprite = EfectosParticulas(enemigo.rect.center,"explocion")
                            self.explocion_sprites.add(explocion_sprite)
                            enemigo.kill()
                            self.sonido_explocion.set_volume(0.2)
                            self.sonido_explocion.play()
                    elif not self.jugador.sprite.mirando_derecha:
                        if (left_jugador < right_enemigo and right_jugador > right_enemigo):
                            explocion_sprite = EfectosParticulas(enemigo.rect.center,"explocion")
                            self.explocion_sprites.add(explocion_sprite)
                            enemigo.kill()
                            self.sonido_explocion.set_volume(0.2)
                            self.sonido_explocion.play()
        if self.nivel_actual == 2:
            jefe = self.jefe.sprite
            left_jefe = jefe.rect.left
            right_jefe = jefe.rect.right
            right_jugador = self.jugador.sprite.rect.right
            left_jugador = self.jugador.sprite.rect.left
            if self.jugador.sprite.esta_atacando:
                if self.jugador.sprite.mirando_derecha:
                    if (right_jugador > left_jefe and right_jugador < right_jefe ) and not jefe.invencible:
                        self.vida_jefe -=1
                elif not self.jugador.sprite.mirando_derecha:
                    if (left_jugador < right_jefe and right_jugador > right_jefe)and not jefe.invencible:
                        self.vida_jefe -=1
    def chequear_colision_disparo(self):
        i = 0 
        
        while i < len(self.jugador.sprite.lista_proyectiles):
            p = self.jugador.sprite.lista_proyectiles[i]
            self.display_surface.blit(p.image,p.rect)
            p.update()
            enemigos_colisionados = pygame.sprite.spritecollide(p,self.enemigos_sprites,True)
            terreno_colisionado = pygame.sprite.spritecollide(p,self.terreno_sprites,False)
            trampas_colisionadas = pygame.sprite.spritecollide(p,self.trampas_sprites,False)
            if self.nivel_actual ==2:
                jefe = self.jefe.sprite
            if p.rect.centerx < 0 or p.rect.centerx > WIDTH:
                self.jugador.sprite.lista_proyectiles.pop(i)
                i -=1
            elif enemigos_colisionados:
                    for enemigo in enemigos_colisionados:
                        explocion_sprite = EfectosParticulas(enemigo.rect.center,"explocion")
                        self.explocion_sprites.add(explocion_sprite)
                        self.jugador.sprite.lista_proyectiles.pop(i)
                        i-=1
                        self.sonido_explocion.set_volume(0.2)
                        self.sonido_explocion.play()
            elif terreno_colisionado:
                for terreno in terreno_colisionado:
                    self.jugador.sprite.lista_proyectiles.pop(i)
                    i-=1
            elif trampas_colisionadas:
                for trampas in trampas_colisionadas:
                    self.jugador.sprite.lista_proyectiles.pop(i)
                    i-=1
            if self.nivel_actual == 2:
                if p.rect.colliderect(jefe.rect) and not jefe.invencible and not jefe.se_esta_trasformando:
                    self.vida_jefe -=4
                    self.jugador.sprite.lista_proyectiles.pop(i)
                    i-=1
            i +=1
    def chequear_colision_disparo_jefe(self):
        i = 0 
        
        while i < len(self.jefe.sprite.lista_proyectiles):
            p = self.jefe.sprite.lista_proyectiles[i]
            self.display_surface.blit(p.image,p.rect)
            p.update()
            jugador = self.jugador.sprite
            jefe = self.jefe.sprite
            if p.rect.centerx < 0 or p.rect.centerx > WIDTH:
                self.jefe.sprite.lista_proyectiles.pop(i)
                i -=1
                self.choco_proyectil = True
        
            if p.rect.colliderect(jugador.rect):
                explocion_sprite = EfectosParticulas(jugador.rect.center,"proyectil")
                self.explocion_sprites.add(explocion_sprite)
                self.sonido_explocion.set_volume(0.2)
                self.sonido_explocion.play()
                if self.vida_jefe >25:
                    danio = -2
                else:
                    danio = -3
                self.jugador.sprite.get_damage(danio,jefe.velocidad)
                self.jefe.sprite.lista_proyectiles.pop(i)
                i-=1
            i +=1
    def chequear_colision_trampas(self):
        jugador = self.jugador.sprite
        jugador.rectangulo_colision.x += jugador.direccion.x * jugador.velocidad
        sprites_colicionables = self.trampas_sprites.sprites()
        for sprite in sprites_colicionables:
            if sprite.rect.colliderect(jugador.rectangulo_colision):
                left_trampa = sprite.rect.left
                right_jugador = self.jugador.sprite.rectangulo_colision.right
                if left_trampa < right_jugador and jugador.direccion.x < 0:  
                    if not self.power_up:
                        self.jugador.sprite.get_damage(-1,3)
                    else:
                        self.jugador.sprite.get_damage(0,3)
                        self.power_up = False
                else:
                    if not self.power_up:
                        self.jugador.sprite.get_damage(-1,-3)
                    else:
                        self.jugador.sprite.get_damage(0,-3)
                        self.power_up = False
    def activar_transformacion(self):
        if self.vida_jefe <=20:
            self.transformate = True
    def check_vida_jefe (self):
        return self.vida_jefe
    def check_en_rango (self):
        return self.en_rango
    def check_transformate (self):
        return self.transformate
    def jugador_en_rango(self):
        top_jefe = self.jefe.sprite.rect.top
        left_jefe = self.jefe.sprite.rectangulo_colision.left
        right_jefe = self.jefe.sprite.rectangulo_colision.right
        bottom_jugador = self.jugador.sprite.rectangulo_colision.bottom
        right_jugador = self.jugador.sprite.rectangulo_colision.right
        left_jugador = self.jugador.sprite.rectangulo_colision.left
        if top_jefe <= bottom_jugador:
            if left_jugador > left_jefe and left_jugador > right_jefe and right_jugador > left_jefe and right_jugador > right_jefe and self.jefe.sprite.mirando_derecha:
                self.en_rango = True
            elif left_jugador < left_jefe and left_jugador < right_jefe and right_jugador < left_jefe and right_jugador < right_jefe and not self.jefe.sprite.mirando_derecha:
                self.en_rango = True
        else:
            self.en_rango = False

    def run(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        self.display_surface.blit(self.fondo,(0,0))
        self.terreno_sprites.draw(self.display_surface)
        self.vida = self.check_vida()
        self.cantidad_gemas = self.check_cantidad_gemas()
        self.jugador.update()
        self.colision_movimentos_horizontal()
        self.poner_jugador_en_el_piso()
        self.colision_movimentos_vertical()
        self.jugador.draw(self.display_surface)
        if self.nivel_actual == 2:
            self.inter.mostrar_vida(self.vida_jefe,self.vida_maxima_jefe)
            self.chequear_colision_jefe()
            self.jugador_en_rango()
            self.activar_transformacion()
            self.jefe.update()
            self.jefe.draw(self.display_surface)
            self.chequear_colision_disparo_jefe()
            if self.vida_jefe <=0:
                self.actualizar_estado("nombre")
                


        self.vidas_sprites.update()
        self.vidas_sprites.draw(self.display_surface)
        self.gemas_sprites.update()
        self.gemas_sprites.draw(self.display_surface)
        self.power_up_sprites.update()
        self.power_up_sprites.draw(self.display_surface)

        self.trampas_sprites.update()
        self.trampas_sprites.draw(self.display_surface)
        
        #enemigos
        self.enemigos_sprites.update()   
        self.limites_sprites.update()
        self.colision_enemigo_limites()
        self.enemigos_sprites.draw(self.display_surface)
        self.explocion_sprites.update()
        self.explocion_sprites.draw(self.display_surface)

        #cheks
        self.input()
        self.chequear_caida()
        self.chequear_colision_power_up()
        self.chequear_colision_gemas()
        self.chequear_colision_vidas()
        self.power_up = self.check_valor_power_up()
        self.chequear_colision_enemigos()
        self.chequear_colision_trampas()
        self.chequear_colision_ataques()
        self.chequear_colision_disparo()
        if obtener_modo():
            for sprite in self.terreno_sprites:
                pygame.draw.rect(self.display_surface,"purple",sprite.rect,1)
            for sprite in self.vidas_sprites:
                pygame.draw.rect(self.display_surface,"green",sprite.rect,1)
            for sprite in self.gemas_sprites:
                pygame.draw.rect(self.display_surface,"blue",sprite.rect,1)
            for sprite in self.power_up_sprites:
                pygame.draw.rect(self.display_surface,"grey",sprite.rect,1)
            for sprite in self.enemigos_sprites:
                pygame.draw.rect(self.display_surface,"red",sprite.rect,1)
            for sprite in self.trampas_sprites:
                pygame.draw.rect(self.display_surface,"red",sprite.rect,1)
            for sprite in self.jugador:
                pygame.draw.rect(self.display_surface,"yellow",sprite.rect,1)
                pygame.draw.rect(self.display_surface,"yellow",sprite.rectangulo_colision,1)
            for proyectil in self.jugador.sprite.lista_proyectiles:
                pygame.draw.rect(self.display_surface,"yellow",proyectil.rectangulo_colision)
            if self.nivel_actual == 2:
                for sprite in self.jefe:
                    pygame.draw.rect(self.display_surface,"red",sprite.rect,1)
                    pygame.draw.rect(self.display_surface,"red",sprite.rectangulo_colision,1)
                for proyectil in self.jefe.sprite.lista_proyectiles:
                    pygame.draw.rect(self.display_surface,"red",proyectil.rectangulo_colision)
