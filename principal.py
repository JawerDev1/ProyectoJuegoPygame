import random
import pygame

pygame.init()

#TAMAÑOS
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
SCALA_PERSONAJE = 0.50
SCALA_CORAZONES = 0.1
SCALA_PARCIAL_ITEM = 0.2
SCALA_EMPANADA_YELLOW_ITEM = 0.1
SCALA_EMPANADA_GREEN_ITEM = 0.2
#COLORES
RED = (255, 0, 0)
WHITE = (255,255,255,255)
#OTROS
FPS = 60
VELOCIDAD = 3
VELOCIDAD_ITEM_EMPANADA = 2
VELOCIDAD_CRUSH = 2

#CREACION DE LA VENTANA
ventana = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ZERO-ZONE")

#--------------------
#FUNCIONES
#--------------------
def escalar_img(image,scale):
    ancho = image.get_width()
    alto = image.get_height()
    nueva_image = pygame.transform.scale(image, (ancho*scale, alto*scale))
    return nueva_image

#------------------------
# CARGAMOS LAS IMAGENES
#------------------------

#FONDO
background = pygame.image.load("assets//image//background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH,SCREEN_HEIGHT))

#ENERGIA
corazon_vacio = pygame.image.load("assets//image//items//heart_empty.png")
corazon_vacio = escalar_img(corazon_vacio, SCALA_CORAZONES)
corazon_lleno = pygame.image.load("assets//image//items//heart_full.png")
corazon_lleno = escalar_img(corazon_lleno, SCALA_CORAZONES)

#PARCIALES
imagen_parcial = pygame.image.load("assets//image//items//parcial//parcialGreen.png")
imagen_parcial = escalar_img(imagen_parcial, SCALA_PARCIAL_ITEM) # PARCIAL VERDE
imagen_parcial1 = pygame.image.load("assets//image//items//parcial//parcialRed.png")
imagen_parcial1 = escalar_img(imagen_parcial1, SCALA_PARCIAL_ITEM) # PARCIAL ROJO

#EMAPANADA
imagen_empanada = pygame.image.load("assets//image//items//empanada//emapana_salvadora.png")
imagen_empanada = escalar_img(imagen_empanada, SCALA_EMPANADA_YELLOW_ITEM) #EMPANADA SALVADORA
imagen_empanada1 = pygame.image.load("assets//image//items//empanada//empanada_verde.png")
imagen_empanada1 = escalar_img(imagen_empanada1, SCALA_EMPANADA_GREEN_ITEM) #EMPANADA NORMAL

#CRUSH
imgen = pygame.image.load("assets//image//player//crush_1.png")
imgen = escalar_img(imgen,SCALA_PERSONAJE)

#PERSONAJE
animaciones = []
for i in range (7):
    img = pygame.image.load(f"assets//image//player//player_{i}.png")
    img = escalar_img(img, SCALA_PERSONAJE)
    animaciones.append(img)

#--------------------
# CLASES
#--------------------
class Personaje():
    def __init__(self, x, y, animaciones, energia):
        self.energia = energia
        self.flip = False
        self.animaciones = animaciones
        #imagen de la animacion que se esta mostrando actualemente
        self.frame_index = 0
        #Aqui se almacena la hora actual (en milisegundos desde que inicio 'pygame')
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x,y)
    def update(self):
        #cuanto tiempo quiero que se mantenga la animacion
        cooldown_animacion = 210
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0
    def movimiento(self, delta_x, delta_y):
        # Calcula la nueva posición
        nueva_x = self.forma.x + delta_x
        nueva_y = self.forma.y + delta_y
        # Verifica los límites de la ventana
        if nueva_x >= 0 and nueva_x <= SCREEN_WIDTH - self.forma.width:
            self.forma.x = nueva_x
        if nueva_y >= 0 and nueva_y <= SCREEN_HEIGHT - self.forma.height:
            self.forma.y = nueva_y

        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
    def dibujar(self, interfaz):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(image_flip, self.forma)
class Crush():
    def __init__(self, x, y):
        self.image = imgen
        self.forma = self.image.get_rect()
        self.forma.center = (x,y)
        self.admirar = False
        self.velocidad_x = VELOCIDAD_CRUSH
        self.velocidad_y = VELOCIDAD_CRUSH
    def actualizar(self, parciales_ganados):
        if parciales_ganados == 0:
            self.admirar = True
        else:
            self.admirar = False

    def mover_crush(self):
        # Calcula la nueva posición
        nueva_x = self.forma.x + self.velocidad_x
        nueva_y = self.forma.y + self.velocidad_y
        # Verifica los límites de la ventana
        if nueva_x <= 0 or nueva_x >= SCREEN_WIDTH - self.forma.width:
            self.velocidad_x = -self.velocidad_x  # Invierte la dirección en el eje x
        if nueva_y <= 0 or nueva_y >= SCREEN_HEIGHT - self.forma.height:
            self.velocidad_y = -self.velocidad_y  # Invierte la dirección en el eje y

        # Actualiza la posición
        self.forma.x += self.velocidad_x
        self.forma.y += self.velocidad_y

    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.forma.center)
class Parcial:
    def __init__(self, x, y):
        self.image_ganado = imagen_parcial #Verde
        self.image_perdido = imagen_parcial1 #Rojo
        self.forma = self.image_ganado.get_rect()
        self.forma = self.image_perdido.get_rect()
        self.forma.center = (x,y)
        self.visible = True
        self.tiempo_cambio = pygame.time.get_ticks()
    def actualizar(self):
        #Cambia la imagen cada 5 segundos
        if pygame.time.get_ticks() - self.tiempo_cambio > 5000:
            self.tiempo_cambio = pygame.time.get_ticks()
            if self.image_ganado == imagen_parcial:
                self.image_ganado = imagen_parcial1 # rojo
            else:
                self.image_ganado = imagen_parcial # verde
    def dibujar(self, interfaz):
        if self.visible:
            interfaz.blit(self.image_ganado, self.forma.center)
class Empanada:
    def __init__(self, x, y):
        self.image_salvadora = imagen_empanada
        self.forma = self.image_salvadora.get_rect()
        self.forma.center = (x,y)
        self.visible = True
        self.tiempo_cambio = pygame.time.get_ticks()
        self.velocidad_x = VELOCIDAD_ITEM_EMPANADA
        self.velocidad_y = VELOCIDAD_ITEM_EMPANADA
    def actualizar(self):
        #Cambia la imagen cada 10 segundos
        if pygame.time.get_ticks() - self.tiempo_cambio > 10000:
            self.tiempo_cambio = pygame.time.get_ticks()
            if self.image_salvadora == imagen_empanada:
                self.image_salvadora = imagen_empanada1
            else:
                self.image_salvadora = imagen_empanada

    def mover_empanada(self):
        self.forma.x += self.velocidad_x
        self.forma.y += self.velocidad_y

        # Mantener la empanada dentro de la ventana
        if self.forma.left <= 0 or self.forma.right >= SCREEN_WIDTH:
            self.velocidad_x = -self.velocidad_x
        if self.forma.top <= 0 or self.forma.bottom >= SCREEN_HEIGHT:
            self.velocidad_y = -self.velocidad_y

    def dibujar(self, interfaz):
        if self.visible:
            interfaz.blit(self.image_salvadora, self.forma.center)

def generar_parciales(parciales):
    x = (random.randint(40, 400))
    y = (random.randint(40, 400))
    parciales.append(Parcial(x,y))
def detectar_colision(objet1, objet2):
    return objet1.colliderect(objet2)

#DEFINIR OBJETOS PARA PODER LLAMAR LAS CLASES
#Creamos a los personajes principales de las clases Personajes y Crush
jugador = Personaje(30, 550, animaciones, 75)
crush = Crush(500, 500)
def vida_jugador():
    for i in range(3):
        if jugador.energia >= ((i)*30):
            ventana.blit(corazon_lleno, (5+i*30, 10))
        else:
            ventana.blit(corazon_vacio, (5+i*30, 10))
def mostrar_texto(ventana, text, x, y):
    FONT = pygame.font.SysFont(None, 20)
    texto = FONT.render(text, True, (WHITE))
    ventana.blit(texto, (x, y))

parciales = []
for _ in range(3):
    x = (random.randint(40, 500))
    y = (random.randint(30, 400))
    parciales.append(Parcial(x,y))

empanadas = []
for _ in range(3):
    x = (random.randint(40, 500))
    y = (random.randint(30, 400))
    empanadas.append(Empanada(x,y))

tiempo_ultimo_parcial = pygame.time.get_ticks() #TOMA EL TIEMPO EN MILISEGUNDOS DESDE QUE INICIO PYGAME
parcial_inactivo = 5000
parcial_colision_time = 0

empana_inactiva = 10000
empanada_colision_time = 0

#definir variables de moviminetos del juego
mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

sound_game_over = pygame.mixer.Sound("assets//sonidos//game-over.mp3")
sound_win = pygame.mixer.Sound("assets//sonidos//win.mp3")
sound_malo = pygame.mixer.Sound("assets//sonidos//malo.wav")
sound_bueno = pygame.mixer.Sound("assets//sonidos//bueno.mp3")

#Controlar el frame rate
reloj = pygame.time.Clock()

run = True
while run:
    #que vaya a 60 FPS
    reloj.tick(FPS)
    ventana.blit(background, [0,0])

    #Calcular el movimiento del jugardor
    delta_x = 0
    delta_y = 0

    if mover_derecha == True:
        delta_x = VELOCIDAD  # se mueve la cantidad de pixeles que tenga la variable velocidad hacia la derecha
    if mover_izquierda == True:
        delta_x = -VELOCIDAD  # se mueve la cantidad de pixeles que tenga la variable velocidad hacia la izquierda y deben ser negativo
    if mover_arriba == True:
        delta_y = -VELOCIDAD  # se mueve la cantidad de pixeles que tenga la variable velocidad hacia arriba y debe ser negativo
    if mover_abajo == True:
        delta_y = VELOCIDAD  # se mueve la cantidad de pixeles que tenga la variable velocidad hacia abajo

    tiempo_concurrido = pygame.time.get_ticks()

    #GENERAMOS UN PARCIAL CADA 5 SEGUNDOS
    if (tiempo_concurrido - tiempo_ultimo_parcial) > 5000:
        generar_parciales(parciales)
        tiempo_ultimo_parcial = tiempo_concurrido

    #ACTUALIZAR PARCIALES
    parciales_ganados = 0
    for exam in parciales:
        exam.actualizar()
        if exam.visible and detectar_colision(jugador.forma, exam.forma):
            exam.visible = False
            parcial_colision_time = tiempo_concurrido
            if exam.image_ganado == imagen_parcial:
                sound_bueno.play()
                print("Parcial Ganado")
            else:
                sound_malo.play()
                print("Parcial Perdido")
                jugador.energia -= 25
        if tiempo_concurrido - parcial_colision_time > parcial_inactivo:
            exam.visible = True
        if exam.visible:
            parciales_ganados += 1

    #ACTUALIZAR EMPANADAS
    for salvadora in empanadas:
        salvadora.actualizar()
        salvadora.mover_empanada()
        # DETECTAMOS SI HAY COLISION ENTRE DOS OBJETOS
        if salvadora.visible and detectar_colision(jugador.forma, salvadora.forma):
            salvadora.visible = False
            empanada_colision_time = tiempo_concurrido
            if salvadora.image_salvadora ==  imagen_empanada and jugador.energia < 75:
                jugador.energia += 25
                sound_bueno.play()
                print("Vida recuperada")
            elif salvadora.image_salvadora == imagen_empanada1:
                sound_malo.play()
                print("Empanada en mal estado")
            empanadas.remove(salvadora)

    #DETECTAMOS SI EL JUGADOR A PERDIDO
    if jugador.energia <= 0:
        sound_game_over.play()
        font = pygame.font.SysFont(None, 55)
        text = font.render("GAME-OVER!", True, (RED))
        ventana.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        run = False

    #DETECTAMOS SI HAY COLISION CON LA CRUSH Y GANAR EL JUEGO
    if crush.admirar and detectar_colision(jugador.forma, crush.forma):
        sound_win.play()
        font = pygame.font.SysFont(None, 55)
        text = font.render("YOU WIN!", True, (RED))
        ventana.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        run = False

    # Mover al jugardor
    jugador.movimiento(delta_x, delta_y)

    # Actualiza el estado del jugador
    jugador.update()
    #Actualizamos al crush para saber si el jugador NO TIENE PARCIALES DISPONIBLES
    crush.actualizar(parciales_ganados)
    #mover a la crush dentro del mapa
    crush.mover_crush()

    # Dibujar a los personajes
    jugador.dibujar(ventana)
    crush.dibujar(ventana)

    # Dibujar los corazones
    vida_jugador()

    #DIBUJAR PARCIALES EN LA VENTANA
    for exms in parciales:
        exms.dibujar(ventana)
    #DIBUJAR EMPANADAS EN LA VENTANA
    for empanada in empanadas:
        empanada.dibujar(ventana)

    #REGISTRAR TODOS LOS EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #RECONOCIMIENTOS DE TECLAS
        if event.type == pygame.KEYDOWN: #TECLA PRESIONADA
            if event.key == pygame.K_LEFT:
                mover_izquierda = True
            if event.key == pygame.K_RIGHT:
                mover_derecha = True
            if event.key == pygame.K_UP:
                mover_arriba = True
            if event.key == pygame.K_DOWN:
                mover_abajo = True

        #PARA CUANDO SOLTEMOS LA TECLA
        if event.type == pygame.KEYUP: # TECLA SUELTA
            if event.key == pygame.K_LEFT:
                mover_izquierda = False
            if event.key == pygame.K_RIGHT:
                mover_derecha = False
            if event.key == pygame.K_UP:
                mover_arriba = False
            if event.key == pygame.K_DOWN:
                mover_abajo = False

    mostrar_texto(ventana, f"Parciales restantes: {parciales_ganados}", 10, 40)

    #Actualizar cambios que se realicen
    pygame.display.update()
pygame.quit()