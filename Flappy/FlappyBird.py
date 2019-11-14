import pygame
import sys
import random
import time

ANCHO = 420 # Ancho de la pantalla.
ALTO = 420  # Alto de la pantalla.
default_gravity = 2 #gravedad por defecto
color_azul = (0, 0, 64)  # Color azul para el fondo.
color_blanco = (255, 255, 255) # Color blanco, para textos.


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('imagenes/1.png')
        # Obtener rectángulo de la imagen
        #self.rect = pygame.Rect(65, 50, 50, 50)
        self.rect = self.image.get_rect()

        #posicion del pajaro al inicio
        self.rect.centerx = 75
        self.posy = 20
        self.puntuacion = 0
        #variable de muerte a false
        self.dead = False

        #variable que nos servirá para contar cuantos frames salta
        self.jump = 0
        #velocidad de salto
        self.jumpSpeed = 10
        #inicializamos la gravedad del pajaro a la default
        self.gravity = default_gravity

    def update(self):
        #si esta saltando
        if self.jump != 0:
            #restamos 1 a la velocidad de salto de forma que cada vez tenga menos velocidad
            self.jumpSpeed -= 1
            self.posy -= self.jumpSpeed
            #restamos 1 a la cantidad de frames que dura el salto
            self.jump -= 1
        else:
            #hacemos que le "afecte" la gravedad al pajaro
            self.posy += self.gravity
            #que aumenta poco a poco
            self.gravity += 1

        #desplazamos al pajaro
        self.rect[1] = self.posy

        #para que el pajaro no se salga por debajo de la pantalla
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
            self.jump = 0
            #self.posy = ALTO
            self.gravity = 0
        #para que el pajaro no se salga por encima de la pantalla
        elif self.rect.top < 0:
            self.rect.top = 0
            self.jump = 0

        #si el pajaro colisiona con un obstaculo
        lista = pygame.sprite.spritecollide(self, listadoObstaculos, False)
        if lista:
            self.dead = True


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('imagenes/ladrillo.png')
        #tomar el rect de la imagen
        self.rect = self.image.get_rect()
        self.generate()

        #le damos una velocidad aleatoria dentro de un rango
        #self.speed = random.randint(1, 7)

    def update(self):

        if self.rect.centerx != 0:
            self.rect.centerx -= self.speed
        else:
            self.generate()

    def generate(self):
        # cuando se crear el objeto lo hace en una posicion aleatoria entre 0 y el ALTO de la pantalla
        self.rect.centery = random.randint(0, ALTO)
        # aparece en la derecha
        self.rect.centerx = ANCHO
        # le damos una velocidad aleatoria dentro de un rango
        self.speed = random.randint(1, 7)

class Moneda(Obstacle):
    def __init__(self):
        Obstacle.__init__(self)
        self.image = pygame.image.load('imagenes/bolita.png')
        # tomar el rect de la imagen
        self.rect = self.image.get_rect()
        self.generate()

    def update(self):
        Obstacle.update(self)
        #cuando la moneda colisiona con el pajaro
        if self.rect.colliderect(pajaro.rect):
            pajaro.puntuacion += 1
            #se regenera
            self.generate()

def mostrar_puntuacion():
    fuente = pygame.font.SysFont('Consolas', 35)
    texto = fuente.render(str(pajaro.puntuacion).zfill(5), True, color_blanco)
    texto_rect = texto.get_rect()
    texto_rect.topleft = [0, 0]
    pantalla.blit(texto, texto_rect)

def colisionEntreObstaculos(obs):
    lista = pygame.sprite.spritecollide(obs, listadoObstaculos, False)
    if lista:
        return True
    return False


pygame.init()
# Inicializando pantalla.
res = (ANCHO, ALTO)
pantalla = pygame.display.set_mode(res)
titulo = "Flappy bird"
# Configurar título de pantalla.
pygame.display.set_caption(titulo)
# Crear el reloj.
reloj = pygame.time.Clock()

background = pygame.image.load('imagenes/back1.png')

jugando = True

#creamos el pajaro
pajaro = Bird()

#lista de los obstaculos
listadoObstaculos = []

#genero un numero aleatorio de obstaculos
numeroObstaculos = random.randint(3, 5 )

#creo obstaculos y los añado a la lista
i = 0
while i < numeroObstaculos:

    obs = Obstacle()
    listadoObstaculos.append(obs)
    i += 1

listaMonedas = []

i = 0
#creo monedas y los añado a la lista
while i < 3:
    mon = Moneda()
    listaMonedas.append(mon)
    i += 1

while jugando:
    reloj.tick(60)
    eventos = pygame.event.get()
    pantalla.fill(color_blanco)
    # colocamos la imagen de fondo
    pantalla.blit(background, (0, 0))
    # Revisar todos los eventos.
    for evento in eventos:
        # Si se presiona la cruz de la barra de título,
        if evento.type == pygame.QUIT:
            # cerrar el videojuego.
            jugando = False

        #si presionan un boton y el pajaro sigue vivo
        elif (evento.type == pygame.KEYDOWN) and not pajaro.dead:
            #salta durante 17 frames
            pajaro.jump = 17
            #a una velocidad de 10
            pajaro.jumpSpeed = 10
            #reseteamos la gravedad
            pajaro.gravity = default_gravity


    if pajaro.dead:
        #reloj.tick(0)
        #jugando = False
        fuente = pygame.font.SysFont('Arial', 30)
        texto = fuente.render('Juego terminado', True, color_blanco)
        texto_rect = texto.get_rect()
        texto_rect.center = [ANCHO / 2, ALTO / 2]
        pantalla.blit(texto, texto_rect)

        #texto de puntuacion
        texto2 = fuente.render('Puntos: ' + str(pajaro.puntuacion), True, color_blanco)
        texto2_rect = texto.get_rect()
        texto2_rect.center = [ANCHO / 2 + 30, ALTO / 2 + 30]
        pantalla.blit(texto2, texto2_rect)

        for evento in eventos:

            if (evento.type == pygame.KEYDOWN):
                jugando = False
    else:

        #ejecutamos el update del pajaro
        pajaro.update()

        #por cada obstaculo, lo pintamos en pantalla y ejecutamos update
        for elemento in listadoObstaculos:
            pantalla.blit(elemento.image, elemento.rect)
            elemento.update()

        #por cada moneda, la pintamos en la pantalla y hacemos update
        for elemento in listaMonedas:
            pantalla.blit(elemento.image, elemento.rect)
            elemento.update()
    mostrar_puntuacion()
    # pintamos al pajaro en la pantalla
    pantalla.blit(pajaro.image, pajaro.rect)

    pygame.display.update()