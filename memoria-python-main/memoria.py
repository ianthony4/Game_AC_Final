import pygame
import sys
import math
import time
import random
from settings import *

class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierto = False
        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)

class Memorama:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        
        self.cuadros = [
            [Cuadro("assets/chip.png"), Cuadro("assets/chip.png"),
             Cuadro("assets/tarjeta de audio.png"), Cuadro("assets/tarjeta de audio.png")],
            [Cuadro("assets/hdd.png"), Cuadro("assets/hdd.png"),
             Cuadro("assets/memoria ram.png"), Cuadro("assets/memoria ram.png")],
            [Cuadro("assets/placa.png"), Cuadro("assets/placa.png"),
             Cuadro("assets/procesador.png"), Cuadro("assets/procesador.png")],
            [Cuadro("assets/ssd.png"), Cuadro("assets/ssd.png"),
             Cuadro("assets/tarjeta grafica.png"), Cuadro("assets/tarjeta grafica.png")],
        ]

        self.sonido_fondo = pygame.mixer.Sound(SOUND_BACKGROUND)
        self.sonido_clic = pygame.mixer.Sound(SOUND_CLICK)
        self.sonido_exito = pygame.mixer.Sound(SOUND_SUCCESS)
        self.sonido_fracaso = pygame.mixer.Sound(SOUND_FAILURE)
        self.sonido_voltear = pygame.mixer.Sound(SOUND_FLIP)

        self.anchura_pantalla = len(self.cuadros[0]) * CARD_WIDTH
        self.altura_pantalla = (len(self.cuadros) * CARD_HEIGHT) + BUTTON_HEIGHT
        self.anchura_boton = self.anchura_pantalla

        self.tamanio_fuente = 20
        self.fuente = pygame.font.SysFont("Arial", self.tamanio_fuente)
        self.xFuente = int((self.anchura_boton / 2) - (self.tamanio_fuente / 2))
        self.yFuente = int(self.altura_pantalla - BUTTON_HEIGHT)

        self.boton = pygame.Rect(0, self.altura_pantalla - BUTTON_HEIGHT,
                                 self.anchura_boton, self.altura_pantalla)

        self.ultimos_segundos = None
        self.puede_jugar = True
        self.juego_iniciado = False
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        self.pantalla_juego = pygame.display.set_mode((self.anchura_pantalla, self.altura_pantalla))
        pygame.display.set_caption('Memorama en Python')
        pygame.mixer.Sound.play(self.sonido_fondo, -1)

    def ocultar_todos_los_cuadros(self):
        for fila in self.cuadros:
            for cuadro in fila:
                cuadro.mostrar = False
                cuadro.descubierto = False

    def aleatorizar_cuadros(self):
        cantidad_filas = len(self.cuadros)
        cantidad_columnas = len(self.cuadros[0])
        for y in range(cantidad_filas):
            for x in range(cantidad_columnas):
                x_aleatorio = random.randint(0, cantidad_columnas - 1)
                y_aleatorio = random.randint(0, cantidad_filas - 1)
                cuadro_temporal = self.cuadros[y][x]
                self.cuadros[y][x] = self.cuadros[y_aleatorio][x_aleatorio]
                self.cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal

    def comprobar_si_gana(self):
        if self.gana():
            pygame.mixer.Sound.play(self.sonido_exito)
            self.reiniciar_juego()

    def gana(self):
        for fila in self.cuadros:
            for cuadro in fila:
                if not cuadro.descubierto:
                    return False
        return True

    def reiniciar_juego(self):
        self.juego_iniciado = False

    def iniciar_juego(self):
        pygame.mixer.Sound.play(self.sonido_clic)
        for i in range(3):
            self.aleatorizar_cuadros()
        self.ocultar_todos_los_cuadros()
        self.juego_iniciado = True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.puede_jugar:
                    xAbsoluto, yAbsoluto = event.pos
                    if self.boton.collidepoint(event.pos):
                        if not self.juego_iniciado:
                            self.iniciar_juego()
                    else:
                        if not self.juego_iniciado:
                            continue
                        x = math.floor(xAbsoluto / CARD_WIDTH)
                        y = math.floor(yAbsoluto / CARD_HEIGHT)
                        cuadro = self.cuadros[y][x]
                        if cuadro.mostrar or cuadro.descubierto:
                            continue
                        if self.x1 is None and self.y1 is None:
                            self.x1 = x
                            self.y1 = y
                            self.cuadros[self.y1][self.x1].mostrar = True
                            pygame.mixer.Sound.play(self.sonido_voltear)
                        else:
                            self.x2 = x
                            self.y2 = y
                            self.cuadros[self.y2][self.x2].mostrar = True
                            cuadro1 = self.cuadros[self.y1][self.x1]
                            cuadro2 = self.cuadros[self.y2][self.x2]
                            if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                                self.cuadros[self.y1][self.x1].descubierto = True
                                self.cuadros[self.y2][self.x2].descubierto = True
                                self.x1 = None
                                self.x2 = None
                                self.y1 = None
                                self.y2 = None
                                pygame.mixer.Sound.play(self.sonido_clic)
                            else:
                                pygame.mixer.Sound.play(self.sonido_fracaso)
                                self.ultimos_segundos = int(time.time())
                                self.puede_jugar = False
                    self.comprobar_si_gana()

            ahora = int(time.time())
            if self.ultimos_segundos is not None and ahora - self.ultimos_segundos >= SHOW_PAIR_DELAY:
                self.cuadros[self.y1][self.x1].mostrar = False
                self.cuadros[self.y2][self.x2].mostrar = False
                self.x1 = None
                self.y1 = None
                self.x2 = None
                self.y2 = None
                self.ultimos_segundos = None
                self.puede_jugar = True

            self.pantalla_juego.fill(WHITE)
            x = 0
            y = 0
            for fila in self.cuadros:
                x = 0
                for cuadro in fila:
                    if cuadro.descubierto or cuadro.mostrar:
                        self.pantalla_juego.blit(cuadro.imagen_real, (x, y))
                    else:
                        self.pantalla_juego.blit(pygame.image.load(HIDDEN_IMAGE_FILE), (x, y))
                    x += CARD_WIDTH
                y += CARD_HEIGHT

            if self.juego_iniciado:
                pygame.draw.rect(self.pantalla_juego, WHITE, self.boton)
                self.pantalla_juego.blit(self.fuente.render(
                    "Iniciar juego", True, GRAY), (self.xFuente, self.yFuente))
            else:
                pygame.draw.rect(self.pantalla_juego, BLUE, self.boton)
                self.pantalla_juego.blit(self.fuente.render(
                    "Iniciar juego", True, WHITE), (self.xFuente, self.yFuente))

            pygame.display.update()

if __name__ == "__main__":
    juego = Memorama()
    juego.run()
