# === IMPORTACIONES ===
import pygame
import sys
import random
from personaje import *
from enemigo import *
from objetos import *
from trampa_explosiva import *
from tesoro import Tesoro
from tienda import Tienda

# === CONFIGURACIÓN INICIAL ===
pygame.init()

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego en Pygame Isa y Juan")
reloj = pygame.time.Clock()
FPS = 60

# Tamaños de sprites e íconos
ANCHO_MUÑECO = 70
ALTO_MUÑECO = 90
ANCHO_ENEMIGO = 80
ALTO_ENEMIGO = 80
ANCHO_ICONO = 30
ALTO_ICONO = 30

# === FUNCIONES AUXILIARES ===
def cargar_imagen(path, ancho, alto):
    """
    Carga una imagen desde el path y la escala al tamaño especificado.
    """
    imagen = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(imagen, (ancho, alto))

def mostrar_texto(texto, fuente, color, x, y, centrar=False):
    """
    Muestra un texto en pantalla en la posición y formato indicados.
    """
    render = fuente.render(texto, True, color)
    rect = render.get_rect()
    if centrar:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    pantalla.blit(render, rect)

# === CARGA DE IMÁGENES ===
img_vida = cargar_imagen("assets/imagenes/vida.png", ANCHO_ICONO, ALTO_ICONO)
img_moneda = cargar_imagen("assets/imagenes/moneda.png", ANCHO_ICONO, ALTO_ICONO)
img_fondo_inicio = cargar_imagen("assets/imagenes/fondoinicio.jpg", ANCHO, ALTO)
img_fondo_juego = cargar_imagen("assets/imagenes/fondo1.jpg", ANCHO, ALTO)
img_powerup_disparo = cargar_imagen("assets/imagenes/powerup_disparo.png", 40, 40)
img_powerup_defensa = cargar_imagen("assets/imagenes/powerup_defensa.png", 40, 40)
img_aura = cargar_imagen("assets/imagenes/aura_azul.png", 90, 100)

# === SONIDOS ===
pygame.mixer.quit()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
def cargar_sonido(path):
    """
    Carga un sonido desde el path especificado.
    """
    try:
        sonido = pygame.mixer.Sound(path)
        sonido.set_volume(1.0)
        return sonido
    except Exception as e:
        print(f"Advertencia: No se pudo cargar el sonido '{path}': {e}")
        return None

# Carga de sonidos
sonido_disparo = cargar_sonido("assets/sonidos/disparo.wav")
sonido_trampa = cargar_sonido("assets/sonidos/trampa.wav")
sonido_moneda = cargar_sonido("assets/sonidos/moneda.wav")
sonido_daño_personaje = cargar_sonido("assets/sonidos/daño_personaje.wav")
sonido_daño_enemigo = cargar_sonido("assets/sonidos/daño_enemigo.wav")
sonido_vida_extra = cargar_sonido("assets/sonidos/vida_extra.wav")
musica_fondo = "assets/sonidos/musica_fondo.mp3"

# Música de fondo
try:
    pygame.mixer.music.load(musica_fondo)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"Advertencia: No se pudo cargar la música de fondo: {e}")

# === FUENTES ===
fuente = pygame.font.Font("assets/fonts/helwa.ttf", 32)
fuente_gameover = pygame.font.Font("assets/fonts/helwa.ttf", 48)

def pantalla_control_sonido():
    """
    Pantalla para controlar el volumen de la música y los efectos.
    """
    volumen = pygame.mixer.music.get_volume()
    fuente = pygame.font.Font("assets/fonts/helwa.ttf", 36)
    ejecutando = True
    while ejecutando:
        pantalla.fill((30, 30, 30))
        texto = fuente.render("Control de Volumen", True, (255, 255, 255))
        texto2 = fuente.render("Usa ← y → para bajar/subir. ENTER para continuar.", True, (200, 200, 200))
        texto_vol = fuente.render(f"Volumen: {int(volumen*100)}%", True, (255, 255, 0))
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 150))
        pantalla.blit(texto2, (ANCHO//2 - texto2.get_width()//2, 220))
        pantalla.blit(texto_vol, (ANCHO//2 - texto_vol.get_width()//2, 300))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    volumen = max(0, volumen - 0.05)
                    pygame.mixer.music.set_volume(volumen)
                elif evento.key == pygame.K_RIGHT:
                    volumen = min(1, volumen + 0.05)
                    pygame.mixer.music.set_volume(volumen)
                elif evento.key == pygame.K_RETURN:
                    ejecutando = False
        # Ajusta el volumen de los sonidos
        if sonido_disparo: sonido_disparo.set_volume(volumen)
        if sonido_trampa: sonido_trampa.set_volume(volumen)
        if sonido_moneda: sonido_moneda.set_volume(volumen)

def pantalla_inicio():
    """
    Pantalla de inicio donde el jugador ingresa su nombre y ajusta el volumen.
    """
    nombre_jugador = ""
    ejecutando = True
    barra_x = ANCHO - 220
    barra_y = ALTO - 60
    barra_ancho = 200
    barra_alto = 20
    volumen = pygame.mixer.music.get_volume()
    arrastrando = False

    while ejecutando:
        pantalla.blit(img_fondo_inicio, (0, 0))
        mostrar_texto("Ingrese su nombre", fuente, (0, 0, 0), ANCHO // 2, 150, centrar=True)
        mostrar_texto(nombre_jugador, fuente, (0, 0, 0), ANCHO // 2, 250, centrar=True)
        mostrar_texto("Presione ENTER para continuar", fuente, (0, 0, 0), ANCHO // 2, ALTO - 80, centrar=True)

        # Barra de volumen
        pygame.draw.rect(pantalla, (60, 60, 60), (barra_x, barra_y, barra_ancho, barra_alto), border_radius=10)
        barra_progreso = int(barra_ancho * volumen)
        pygame.draw.rect(pantalla, (255, 215, 0), (barra_x, barra_y, barra_progreso, barra_alto), border_radius=10)
        pygame.draw.rect(pantalla, (255, 255, 255), (barra_x, barra_y, barra_ancho, barra_alto), 2, border_radius=10)
        texto_vol = fuente.render(f"Volumen: {int(volumen*100)}%", True, (0, 0, 0))
        pantalla.blit(texto_vol, (barra_x + barra_ancho//2 - texto_vol.get_width()//2, barra_y - 32))
        pygame.draw.circle(pantalla, (255, 215, 0), (barra_x - 25, barra_y + barra_alto//2), 12)
        pygame.draw.polygon(pantalla, (0,0,0), [
            (barra_x - 32, barra_y + barra_alto//2 - 7),
            (barra_x - 18, barra_y + barra_alto//2 - 7),
            (barra_x - 12, barra_y + barra_alto//2),
            (barra_x - 18, barra_y + barra_alto//2 + 7),
            (barra_x - 32, barra_y + barra_alto//2 + 7)
        ])

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre_jugador != "":
                    return nombre_jugador
                elif evento.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                else:
                    nombre_jugador += evento.unicode
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if barra_x <= mx <= barra_x + barra_ancho and barra_y <= my <= barra_y + barra_alto:
                    arrastrando = True
            elif evento.type == pygame.MOUSEBUTTONUP:
                arrastrando = False
            elif evento.type == pygame.MOUSEMOTION and arrastrando:
                mx, my = pygame.mouse.get_pos()
                nuevo_vol = (mx - barra_x) / barra_ancho
                nuevo_vol = max(0, min(1, nuevo_vol))
                volumen = nuevo_vol
                pygame.mixer.music.set_volume(volumen)
                if sonido_disparo: sonido_disparo.set_volume(volumen)
                if sonido_trampa: sonido_trampa.set_volume(volumen)
                if sonido_moneda: sonido_moneda.set_volume(volumen)

def pantalla_gameover(nombre_jugador):
    """
    Pantalla de Game Over con opción para reiniciar el juego.
    """
    fuente_gameover_personalizada = pygame.font.Font("assets/fonts/super jungle.ttf", 100)
    fuente_boton = pygame.font.Font("assets/fonts/helwa.ttf", 28)
    ejecutando = True

    while ejecutando:
        pantalla.blit(img_fondo_juego, (0, 0))
        texto_gameover = fuente_gameover_personalizada.render("Game Over", True, (128, 0, 255))
        sombra_gameover = fuente_gameover_personalizada.render("Game Over", True, (255, 255, 255))
        rect_gameover = texto_gameover.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        pantalla.blit(sombra_gameover, (rect_gameover.x + 4, rect_gameover.y + 4))
        pantalla.blit(texto_gameover, rect_gameover.topleft)

        # Botón de reinicio
        boton_x = ANCHO // 2 - 150
        boton_y = ALTO // 2 + 50
        boton_ancho = 300
        boton_alto = 100
        pygame.draw.rect(pantalla, (0, 0, 0), (boton_x + 5, boton_y + 5, boton_ancho, boton_alto), border_radius=10)
        pygame.draw.rect(pantalla, (0, 128, 0), (boton_x, boton_y, boton_ancho, boton_alto), border_radius=10)
        pygame.draw.rect(pantalla, (255, 255, 255), (boton_x, boton_y, boton_ancho, boton_alto), 3, border_radius=10)

        texto_boton1 = fuente_boton.render("Presione ENTER", True, (255, 255, 255))
        texto_boton2 = fuente_boton.render("para Jugar de Nuevo", True, (255, 255, 255))
        rect_boton1 = texto_boton1.get_rect(center=(boton_x + boton_ancho // 2, boton_y + boton_alto // 2 - 15))
        rect_boton2 = texto_boton2.get_rect(center=(boton_x + boton_ancho // 2, boton_y + boton_alto // 2 + 15))
        pantalla.blit(texto_boton1, rect_boton1.topleft)
        pantalla.blit(texto_boton2, rect_boton2.topleft)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True

def mostrar_victoria(puntuacion=0, tiempo_transcurrido=0):
    """
    Pantalla de victoria al completar el juego.
    """
    ejecutando = True
    while ejecutando:
        pantalla.fill((0, 0, 0))
        fuente_victoria = pygame.font.Font("assets/fonts/super jungle.ttf", 80)
        fuente_info = pygame.font.Font("assets/fonts/helwa.ttf", 36)
        fuente_opciones = pygame.font.Font("assets/fonts/helwa.ttf", 28)
        texto = fuente_victoria.render("¡Victoria!", True, (0, 255, 0))
        rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 100))
        pantalla.blit(texto, rect)
        texto_punt = fuente_info.render(f"Puntos: {puntuacion}", True, (255, 255, 0))
        texto_time = fuente_info.render(f"Tiempo: {tiempo_transcurrido}s", True, (255, 255, 255))
        rect_punt = texto_punt.get_rect(center=(ANCHO // 2, ALTO // 2))
        rect_time = texto_time.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
        pantalla.blit(texto_punt, rect_punt)
        pantalla.blit(texto_time, rect_time)
        texto_opciones = fuente_opciones.render("Presiona ESC para salir o ENTER para reiniciar", True, (255, 255, 255))
        rect_opciones = texto_opciones.get_rect(center=(ANCHO // 2, ALTO // 2 + 120))
        pantalla.blit(texto_opciones, rect_opciones)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_ESCAPE:
                    ejecutando = False

def mostrar_tienda(jugador, tienda, pantalla, fuente):
    """
    Muestra la tienda y permite comprar objetos.
    """
    ejecutando = True
    while ejecutando:
        tienda.mostrar_tienda(pantalla, fuente)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    indice = int(evento.key - pygame.K_1)
                    tienda.comprar_objeto(pantalla, fuente, jugador, indice)

class Particula:
    """
    Sistema de partículas para efectos visuales.
    """
    def __init__(self, x, y, color, cantidad=15):
        self.particulas = []
        for _ in range(cantidad):
            dx = random.uniform(-3, 3)
            dy = random.uniform(-3, 3)
            radio = random.randint(3, 7)
            self.particulas.append({
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "radio": radio,
                "color": color,
                "vida": random.randint(15, 30)
            })

    def actualizar(self):
        """
        Actualiza la posición y vida de las partículas.
        """
        for p in self.particulas:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["radio"] = max(0, p["radio"] - 0.2)
            p["vida"] -= 1
        self.particulas = [p for p in self.particulas if p["vida"] > 0 and p["radio"] > 0]

    def dibujar(self, pantalla):
        """
        Dibuja las partículas en pantalla.
        """
        for p in self.particulas:
            pygame.draw.circle(pantalla, p["color"], (int(p["x"]), int(p["y"])), int(p["radio"]))

def mostrar_transicion_nivel2():
    """
    Pantalla de transición entre el nivel 1 y el nivel 2.
    """
    fuente_grande = pygame.font.Font("assets/fonts/super jungle.ttf", 36)
    ejecutando = True
    while ejecutando:
        pantalla.fill((0, 0, 0))
        texto = fuente_grande.render("¡Nivel 2!", True, (255, 255, 0))
        texto2 = fuente_grande.render("Presiona ENTER para ir al nivel 2", True, (255, 255, 255))
        rect1 = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 60))
        rect2 = texto2.get_rect(center=(ANCHO // 2, ALTO // 2 + 40))
        pantalla.blit(texto, rect1)
        pantalla.blit(texto2, rect2)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    ejecutando = False

# === FUNCIÓN PRINCIPAL DEL JUEGO ===
def iniciar_juego(nombre_jugador):
    jugador = Personaje(
        x=100, 
        y=450, 
        nombre=nombre_jugador, 
        puntos_vida=50,  # Solo 20 puntos de vida
        ataque=10,       
        defensa=0, 
        nivel=1, 
        inventario=[]
    )
    jugador.cargar_animaciones("assets/imagenes/Knight")  # Cargamos las animaciones del jugador

    # Asignamos los íconos de vida y monedas
    jugador.icono_vida = img_vida
    jugador.icono_moneda = img_moneda

    fondo_actual = img_fondo_juego
    nivel = 1
    enemigos_derrotados = 0
    enemigos_derrotados_nivel2 = 0

    # --- AJUSTE: El enemigo debe morir de 6 golpes de 10 de daño ---
    # 6 golpes x 10 daño = 60, así que puntos_vida=60, defensa=0
    enemigo = Enemigo(
        x=300, 
        y=450, 
        rango_movimiento=(200, 600), 
        puntos_vida=60,   # 6 golpes de 10
        ataque=10,
        defensa=0,        # Sin defensa para que cada golpe reste 10
        tipo="terrestre"
    )
    enemigo.cargar_animaciones("assets/imagenes/Mage")  # Primer enemigo: Mage

    objetos = Objetos(
        img_dinero=None,  # Eliminamos referencias a imágenes no utilizadas
        img_moneda=img_moneda,
        img_vida_extra=None,
        img_vida=img_vida
    )

    trampa = TrampaExplosiva(x=400, y=450, alcance=50, daño=20)
    trampa.cargar_imagen(cargar_imagen("assets/imagenes/trampa.png", 40, 40))

    trampas = []  # Lista para las trampas que caen del cielo
    tiempo_ultima_trampa = pygame.time.get_ticks()
    intervalo_trampas = 5000  # Cada 5 segundos

    # Configuración de tiempos de respawn
    tiempo_respawn_enemigos = 7000  # 7 segundos
    tiempo_respawn_objetos = 15000  # 15 segundos para monedas y vidas
    ultimo_respawn_enemigos = pygame.time.get_ticks()
    ultimo_respawn_objetos = pygame.time.get_ticks()

    moneda = None
    vida_extra = None

    tienda = Tienda()
    # --- NUEVO: Añadir atributos para power-ups y proyectiles ---
    powerup_disparo = None
    powerup_defensa = None
    proyectiles = []
    aura_activa = False
    aura_duracion = 0
    aura_tiempo_inicio = 0
    puede_disparar = False
    disparo_cooldown = 200  # Más rápido para disparos automáticos
    ultimo_disparo = 0
    powerup_disparo_duracion = 2000  # 2 segundos en milisegundos
    powerup_disparo_tiempo = 0

    # NUEVO: Tiempos de aparición para objetos que caen
    tiempo_powerup_disparo = 0
    tiempo_powerup_defensa = 0
    tiempo_moneda = 0
    tiempo_vida_extra = 0

    puntuacion = 0
    tiempo_inicio = pygame.time.get_ticks()
    particulas = []

    # Elimina la creación inicial de moneda y vida_extra
    # if moneda is None:
    #     moneda = Tesoro(x=random.randint(100, 700), y=450, valor=100)
    #     moneda.cargar_imagen(cargar_imagen("assets/imagenes/moneda.png", 40, 40))
    # if vida_extra is None:
    #     vida_extra = Tesoro(x=random.randint(100, 700), y=450, valor=0)
    #     vida_extra.cargar_imagen(cargar_imagen("assets/imagenes/vida.png", 40, 40))

    ejecutando = True
    while ejecutando:  # Corregido "mientras" por "while"
        reloj.tick(FPS)
        ahora = pygame.time.get_ticks()
        tiempo_transcurrido = (ahora - tiempo_inicio) // 1000  # en segundos

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_w, pygame.K_UP):
                    jugador.saltar()
                elif evento.key == pygame.K_SPACE:
                    jugador.atacar(enemigo)  # Solo llamar atacar, no cambiar estado manualmente
                elif evento.key == pygame.K_t:
                    mostrar_tienda(jugador, tienda, pantalla, fuente)

        teclas = pygame.key.get_pressed()
        dir_x = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dir_x = -1
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dir_x = 1

        # Solo actualizar movimiento si NO está atacando
        if not jugador.atacando:
            jugador.actualizar_movimiento(dir_x)
        jugador.mover()
        jugador.actualizar_ataque()
        jugador.actualizar_animacion()  # Actualizamos la animación del jugador

        if enemigo.vivo:
            enemigo.mover(jugador)  # Ahora el enemigo te "ve" y te sigue si estás cerca
            enemigo.actualizar_animacion()

        # Actualizar rectángulos antes de detectar colisiones
        rect_jugador = jugador.obtener_rect()
        rect_enemigo = enemigo.obtener_rect()

        # Detectar al jugador y atacar si está cerca
        if enemigo.vivo and rect_enemigo.colliderect(rect_jugador):
            enemigo.atacar(jugador)

        # Colisión entre jugador y enemigo
        if enemigo.vivo and jugador.obtener_rect().colliderect(enemigo.obtener_rect()):
            enemigo.atacar(jugador)  # El enemigo ataca al jugador si hay colisión

        # Verificar si el enemigo ha muerto
        if not enemigo.vivo:
            if nivel == 1:
                enemigos_derrotados += 1
                puntuacion += 100
                particulas.append(Particula(enemigo.x + 25, enemigo.y + 40, (200, 0, 0)))  # Partículas rojas
                print(f"Enemigos derrotados en nivel 1: {enemigos_derrotados}/5")
                if enemigos_derrotados >= 5:
                    mostrar_transicion_nivel2()
                    nivel = 2
                    fondo_actual = cargar_imagen("assets/imagenes/fondo2.jpg", ANCHO, ALTO)
                    enemigo = Enemigo(
                        x=300,
                        y=450,
                        rango_movimiento=(200, 600),
                        puntos_vida=60,   # También 6 golpes en nivel 2
                        ataque=12,
                        defensa=0,
                        tipo="terrestre"
                    )
                    enemigo.cargar_animaciones("assets/imagenes/Rogue")
                    print("¡Nivel 2! Aparece el Rogue.")
                    continue
                else:
                    enemigo = Enemigo(
                        x=random.randint(200, 600), 
                        y=450, 
                        rango_movimiento=(200, 600), 
                        puntos_vida=60,   # 6 golpes
                        ataque=10, 
                        defensa=0, 
                        tipo="terrestre"
                    )
                    enemigo.cargar_animaciones("assets/imagenes/Mage")
                    ultimo_respawn_enemigos = pygame.time.get_ticks()
            elif nivel == 2:
                enemigos_derrotados_nivel2 += 1
                puntuacion += 200
                particulas.append(Particula(enemigo.x + 25, enemigo.y + 40, (200, 0, 0)))  # Partículas rojas
                print(f"Enemigos derrotados en nivel 2: {enemigos_derrotados_nivel2}/5")
                if enemigos_derrotados_nivel2 >= 5:
                    mostrar_victoria(puntuacion, tiempo_transcurrido)
                    return
                else:
                    enemigo = Enemigo(
                        x=random.randint(200, 600), 
                        y=450, 
                        rango_movimiento=(200, 600), 
                        puntos_vida=60,   # 6 golpes
                        ataque=12, 
                        defensa=0, 
                        tipo="terrestre"
                    )
                    enemigo.cargar_animaciones("assets/imagenes/Rogue")
                    ultimo_respawn_enemigos = pygame.time.get_ticks()

        # Verificar si el enemigo activa la trampa (no interactúa)
        if trampa.activa and trampa.detonar(jugador):
            print("¡Trampa activada! El jugador pierde una vida.")
            jugador.vidas -= 1
            jugador.puntos_vida = 20  # Reinicia la vida a 20, no a 100
            if sonido_daño_personaje:
                try:
                    sonido_daño_personaje.stop()
                    sonido_daño_personaje.play()
                except Exception as e:
                    print(f"Error al reproducir sonido_daño_personaje: {e}")

        # Respawn de objetos (moneda y vida extra)
        if ahora - ultimo_respawn_objetos > tiempo_respawn_objetos:
            if moneda is None or (moneda and moneda.recogido):
                moneda = Tesoro(x=random.randint(100, 700), y=0, valor=100)  # Moneda cae desde arriba
                moneda.cargar_imagen(cargar_imagen("assets/imagenes/moneda.png", 40, 40))
                tiempo_moneda = ahora  # Guardar tiempo de aparición
            if vida_extra is None or (vida_extra and vida_extra.recogido):
                vida_extra = Tesoro(x=random.randint(100, 700), y=0, valor=0)  # Vida extra cae desde arriba
                vida_extra.cargar_imagen(cargar_imagen("assets/imagenes/vida.png", 40, 40))
                tiempo_vida_extra = ahora
            ultimo_respawn_objetos = ahora

        # Actualizar posición de moneda si está cayendo
        if moneda and not moneda.recogido:
            moneda.y += 3  # Velocidad de caída
            if moneda.y > 450:
                moneda.y = 450
            if ahora - tiempo_moneda > 4000:
                moneda.recogido = True

        # Actualizar posición de vida extra si está cayendo
        if vida_extra and not vida_extra.recogido:
            vida_extra.y += 3  # Velocidad de caída
            if vida_extra.y > 450:
                vida_extra.y = 450
            if ahora - tiempo_vida_extra > 4000:
                vida_extra.recogido = True

        # Verificar si el jugador recoge la moneda
        if moneda and not moneda.recogido and abs(jugador.x - moneda.x) < 30 and abs(jugador.y - moneda.y) < 30:
            valor_recogido = moneda.recoger(jugador)
            jugador.monedas += valor_recogido  # Actualizamos el marcador de monedas
            print(f"¡Moneda recogida! Valor: {valor_recogido}")
            if sonido_moneda:
                try:
                    sonido_moneda.stop()
                    sonido_moneda.play()
                except Exception as e:
                    print(f"Error al reproducir sonido_moneda: {e}")

        # Verificar si el jugador recoge la vida extra
        if vida_extra and not vida_extra.recogido and abs(jugador.x - vida_extra.x) < 30 and abs(jugador.y - vida_extra.y) < 30:
            vida_extra.recoger(jugador)
            jugador.vidas += 1
            jugador.puntos_vida = 20  # Al ganar una vida extra, también reinicia la vida a 20
            print("¡Vida extra recogida!")
            particulas.append(Particula(jugador.x + jugador.ancho // 2, jugador.y + jugador.alto // 2, (255, 0, 0)))  # Partículas rojas
            if sonido_vida_extra:
                try:
                    sonido_vida_extra.stop()
                    sonido_vida_extra.play()
                except Exception as e:
                    print(f"Error al reproducir sonido_vida_extra: {e}")

        # Generar trampas que caen del cielo
        if ahora - tiempo_ultima_trampa > intervalo_trampas:
            nueva_trampa = TrampaExplosiva(
                x=random.randint(50, ANCHO - 50), 
                y=0, 
                alcance=50, 
                daño=20
            )
            nueva_trampa.cargar_imagen(cargar_imagen("assets/imagenes/trampa.png", 40, 40))
            trampas.append(nueva_trampa)
            tiempo_ultima_trampa = ahora

        # Actualizar trampas
        for trampa in trampas[:]:
            trampa.y += 5  # Velocidad de caída
            if trampa.y > ALTO:  # Eliminar trampas que salen de la pantalla
                trampas.remove(trampa)
            elif trampa.detonar(jugador):  # Verificar colisión con el jugador
                print("¡Trampa activada! El jugador pierde vida.")
                trampas.remove(trampa)
                if sonido_trampa:
                    try:
                        sonido_trampa.stop()
                        sonido_trampa.play()
                    except Exception as e:
                        print(f"Error al reproducir sonido_trampa: {e}")
                if sonido_daño_personaje:
                    try:
                        sonido_daño_personaje.stop()
                        sonido_daño_personaje.play()
                    except Exception as e:
                        print(f"Error al reproducir sonido_daño_personaje: {e}")
                # Partículas negras y amarillas
                particulas.append(Particula(jugador.x + jugador.ancho // 2, jugador.y + jugador.alto // 2, (0, 0, 0), 10))
                particulas.append(Particula(jugador.x + jugador.ancho // 2, jugador.y + jugador.alto // 2, (255, 255, 0), 10))

        # --- NUEVO: Generar power-ups que caen del cielo ---
        if random.randint(0, 1000) < 2 and powerup_disparo is None:
            powerup_disparo = {
                "x": random.randint(50, ANCHO-50),
                "y": 0,
                "img": img_powerup_disparo,
                "tipo": "disparo"
            }
            tiempo_powerup_disparo = ahora
        if random.randint(0, 1000) < 2 and powerup_defensa is None:
            powerup_defensa = {
                "x": random.randint(50, ANCHO-50),
                "y": 0,
                "img": img_powerup_defensa,
                "tipo": "defensa"
            }
            tiempo_powerup_defensa = ahora

        # --- NUEVO: Caída de power-ups ---
        if powerup_disparo:
            powerup_disparo["y"] += 3
            if powerup_disparo["y"] > 450:
                powerup_disparo["y"] = 450
            # Desaparecer si no se recoge en 4 segundos
            if ahora - tiempo_powerup_disparo > 4000:
                powerup_disparo = None
            # Recoger power-up disparo
            elif abs(jugador.x + jugador.ancho // 2 - (powerup_disparo["x"] + 20)) < 30 and abs(jugador.y + jugador.alto // 2 - (powerup_disparo["y"] + 20)) < 30:
                puede_disparar = True
                powerup_disparo_tiempo = ahora
                powerup_disparo = None
                particulas.append(Particula(jugador.x + jugador.ancho // 2, jugador.y + jugador.alto // 2, (255, 255, 0)))  # Amarillas

        if powerup_defensa:
            powerup_defensa["y"] += 3
            if powerup_defensa["y"] > 450:
                powerup_defensa["y"] = 450
            if ahora - tiempo_powerup_defensa > 4000:
                powerup_defensa = None
            elif abs(jugador.x + jugador.ancho // 2 - (powerup_defensa["x"] + 20)) < 30 and abs(jugador.y + jugador.alto // 2 - (powerup_defensa["y"] + 20)) < 30:
                aura_activa = True
                aura_duracion = 2000  # 2 segundos
                aura_tiempo_inicio = ahora
                powerup_defensa = None
                particulas.append(Particula(jugador.x + jugador.ancho // 2, jugador.y + jugador.alto // 2, (255, 255, 0)))  # Amarillas

        # --- NUEVO: Aura de defensa (protección) ---
        if aura_activa and ahora - aura_tiempo_inicio > aura_duracion:
            aura_activa = False

        # --- NUEVO: PowerUp disparo solo dura 2 segundos ---
        if puede_disparar and ahora - powerup_disparo_tiempo > powerup_disparo_duracion:
            puede_disparar = False

        # --- Disparo automático si tiene power-up ---
        if puede_disparar and ahora - ultimo_disparo > disparo_cooldown:
            proyectiles.append({
                "x": jugador.x + jugador.ancho // 2,
                "y": jugador.y + jugador.alto // 2 - 5,
                "dir": 1 if jugador.direccion == "derecha" else -1
            })
            ultimo_disparo = ahora
            if sonido_disparo:
                try:
                    sonido_disparo.stop()
                    sonido_disparo.play()
                except Exception as e:
                    print(f"Error al reproducir sonido_disparo: {e}")

        # --- NUEVO: Proyectiles (disparo) ---
        for proyectil in proyectiles[:]:
            proyectil["x"] += 10 * proyectil["dir"]
            # Colisión con enemigo
            if enemigo.vivo and abs(proyectil["x"] - enemigo.x) < 40 and abs(proyectil["y"] - enemigo.y) < 40:
                # Solo inflige daño si el enemigo sigue vivo y no hay aura especial
                daño_real = 10
                if hasattr(enemigo, "recibir_daño"):
                    daño_real = enemigo.recibir_daño(10)
                proyectiles.remove(proyectil)
                if sonido_daño_enemigo and daño_real > 0:
                    try:
                        sonido_daño_enemigo.stop()
                        sonido_daño_enemigo.play()
                    except Exception as e:
                        print(f"Error al reproducir sonido_daño_enemigo: {e}")
                # Partículas rojas al matar enemigo con proyectil
                if not enemigo.vivo:
                    particulas.append(Particula(enemigo.x + 25, enemigo.y + 40, (200, 0, 0)))
                    puntuacion += 100
            elif proyectil["x"] < 0 or proyectil["x"] > ANCHO:
                proyectiles.remove(proyectil)

        # --- NUEVO: Aura protege al jugador (reduce daño a la mitad) ---
        def recibir_daño_con_aura(self, daño):
            # El aura sigue funcionando: reduce el daño a la mitad si está activa
            if aura_activa:
                daño = daño // 2
            resultado = self.recibir_daño_original(daño)
            if sonido_daño_personaje and daño > 0:
                try:
                    sonido_daño_personaje.stop()
                    sonido_daño_personaje.play()
                except Exception as e:
                    print(f"Error al reproducir sonido_daño_personaje: {e}")
            return resultado
        if not hasattr(jugador, "recibir_daño_original"):
            jugador.recibir_daño_original = jugador.recibir_daño
            jugador.recibir_daño = recibir_daño_con_aura.__get__(jugador)

        # Colisión entre jugador y enemigo
        if enemigo.vivo and jugador.obtener_rect().colliderect(enemigo.obtener_rect()):
            # Solo inflige daño si el jugador está atacando y el enemigo sigue vivo
            if jugador.atacando and sonido_daño_enemigo:
                daño_real = enemigo.recibir_daño(jugador.ataque)
                if daño_real > 0:
                    try:
                        sonido_daño_enemigo.stop()
                        sonido_daño_enemigo.play()
                    except Exception as e:
                        print(f"Error al reproducir sonido_daño_enemigo: {e}")
            enemigo.atacar(jugador)
            if sonido_daño_personaje:
                try:
                    sonido_daño_personaje.stop()
                    sonido_daño_personaje.play()
                except Exception as e:
                    print(f"Error al reproducir sonido_daño_personaje: {e}")

        if jugador.vidas <= 0:
            if pantalla_gameover(nombre_jugador):
                return
            else:
                pygame.quit()
                sys.exit()

        # --- Actualizar partículas ---
        for p in particulas[:]:
            p.actualizar()
            if not p.particulas:
                particulas.remove(p)

        pantalla.blit(fondo_actual, (0, 0))
        # --- Dibuja el aura centrada en el personaje (ajuste más abajo y a la derecha) ---
        if aura_activa:
            # Ajusta estos valores para que el aura quede más abajo y a la derecha
            aura_x = jugador.x + jugador.ancho // 2 - img_aura.get_width() // 2 + 10
            aura_y = jugador.y + jugador.alto - img_aura.get_height() // 2 + 10
            pantalla.blit(img_aura, (aura_x, aura_y))
        jugador.mostrar(pantalla)
        if enemigo.vivo:
            enemigo.mostrar(pantalla)
        trampa.mostrar(pantalla)
        if moneda and not moneda.recogido:
            moneda.mostrar(pantalla)
        if vida_extra and not vida_extra.recogido:
            vida_extra.mostrar(pantalla)
        if powerup_disparo:
            # Centrar el powerup respecto al personaje
            powerup_x = powerup_disparo["x"]
            powerup_y = powerup_disparo["y"]
            pantalla.blit(powerup_disparo["img"], (powerup_x, powerup_y))
        if powerup_defensa:
            powerup_x = powerup_defensa["x"]
            powerup_y = powerup_defensa["y"]
            pantalla.blit(powerup_defensa["img"], (powerup_x, powerup_y))
        # Dibuja los proyectiles como rectángulos amarillos
        for proyectil in proyectiles:
            pygame.draw.rect(pantalla, (255, 255, 0), (proyectil["x"], proyectil["y"], 30, 10))

        # --- Dibuja partículas ---
        for p in particulas:
            p.dibujar(pantalla)

        # Dibujar trampas
        for trampa in trampas:
            trampa.mostrar(pantalla)

        # Barras de vida pequeñas sobre la cabeza de los personajes
        # Barra de vida del jugador
        barra_ancho = 40
        barra_alto = 6
        vida_jugador = max(jugador.puntos_vida, 0)
        pygame.draw.rect(
            pantalla, (60, 60, 60), 
            (jugador.x + 15, jugador.y - 15, barra_ancho, barra_alto)
        )
        pygame.draw.rect(
            pantalla, (0, 255, 0),  # Verde
            (jugador.x + 15, jugador.y - 15, barra_ancho * vida_jugador / 20, barra_alto)
        )
        # Barra de vida del enemigo
        if enemigo.vivo:
            vida_enemigo = max(enemigo.puntos_vida, 0)
            pygame.draw.rect(
                pantalla, (60, 60, 60), 
                (enemigo.x + 20, enemigo.y - 15, barra_ancho, barra_alto)
            )
            pygame.draw.rect(
                pantalla, (0, 255, 0),  # Verde
                (enemigo.x + 20, enemigo.y - 15, barra_ancho * vida_enemigo / 20, barra_alto)
            )

        # Mostrar marcador original (ya funcional)
        objetos.mostrar(pantalla, nombre_jugador, fuente, (255, 255, 255))

        # === NUEVO: Mostrar puntuación y tiempo en la esquina superior derecha ===
        texto_punt = fuente.render(f"Puntos: {puntuacion}", True, (255, 255, 0))
        texto_time = fuente.render(f"Tiempo: {tiempo_transcurrido}s", True, (255, 255, 255))
        pantalla.blit(texto_punt, (ANCHO - texto_punt.get_width() - 20, 10))
        pantalla.blit(texto_time, (ANCHO - texto_time.get_width() - 20, 50))

        pygame.display.flip()

# === EJECUCIÓN PRINCIPAL ===
nombre = pantalla_inicio()
while True:
    iniciar_juego(nombre)
