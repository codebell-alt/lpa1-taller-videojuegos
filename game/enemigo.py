import pygame
import os

class Enemigo:
    def __init__(self, x, y, rango_movimiento, puntos_vida=50, ataque=50, defensa=3, tipo="terrestre"):
        self.x = x
        self.y = y
        self.vidas = 4  # Vidas iniciales del enemigo
        self.velocidad = 2
        self.direccion = "derecha"
        self.rango_movimiento = rango_movimiento  # Rango de movimiento (x_min, x_max)
        self.atacando = False  # Añadido para controlar la animación de ataque
        self.ultimo_ataque = 0
        self.cooldown_ataque = 1000  # Tiempo entre ataques (en milisegundos)
        self.vivo = True  # El enemigo está vivo inicialmente

        # Nuevos atributos
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.defensa = defensa
        self.tipo = tipo
        self.distancia_vision = 200  # Distancia para "ver" al jugador

        # Animaciones
        self.animaciones = {}
        self.frame_actual = 0
        self.estado_actual = "idle"
        self.tiempo_ultimo_frame = 0
        self.velocidad_animacion = 100  # Velocidad de animación en milisegundos

    def cargar_imagenes(self, quieto, caminando, atacando):
        self.img_quieto = quieto
        self.img_caminando = caminando
        self.img_atacando = atacando

    def cargar_animaciones(self, carpeta):
        acciones = ["idle", "walk", "attack"]
        for accion in acciones:
            ruta = os.path.join(carpeta, accion)
            if os.path.exists(ruta):  # Verificamos que la carpeta exista
                self.animaciones[accion] = [
                    pygame.image.load(os.path.join(ruta, img)).convert_alpha()
                    for img in sorted(os.listdir(ruta))
                ]
            else:
                print(f"Advertencia: No se encontró la carpeta de animaciones para '{accion}' en {ruta}")

        # Aseguramos que haya al menos una animación para 'idle'
        if "idle" not in self.animaciones:
            print("Advertencia: No se encontró la animación para 'idle'. Usando un marcador de posición.")
            self.animaciones["idle"] = [pygame.Surface((50, 50))]  # Placeholder vacío

    def detectar_jugador(self, jugador):
        """Devuelve True si el jugador está dentro del rango de visión horizontal del enemigo."""
        distancia = abs((self.x + 25) - (jugador.x + jugador.ancho // 2))
        return distancia <= self.distancia_vision and abs(self.y - jugador.y) < 50

    def mover(self, jugador=None):
        if not self.vivo:
            return  # No mover si el enemigo está muerto

        ahora = pygame.time.get_ticks()
        # Si está atacando, no se mueve
        if self.atacando:
            return

        # Si está en cooldown pero no atacando, se queda quieto (idle)
        if ahora - self.ultimo_ataque < self.cooldown_ataque:
            self.estado_actual = "idle"
            return

        # Si el jugador está cerca, seguirlo pero mantener distancia mínima
        if jugador and self.detectar_jugador(jugador):
            distancia_x = jugador.x - self.x
            distancia_minima = 30  # píxeles de separación mínima
            if abs(distancia_x) > distancia_minima:
                if distancia_x < 0:
                    self.x -= self.velocidad
                    self.direccion = "izquierda"
                elif distancia_x > 0:
                    self.x += self.velocidad
                    self.direccion = "derecha"
                self.estado_actual = "walk"
            else:
                self.estado_actual = "idle"
        else:
            # Movimiento automático dentro del rango
            if self.direccion == "derecha":
                self.x += self.velocidad
                if self.x >= self.rango_movimiento[1]:  # Límite derecho
                    self.direccion = "izquierda"
            elif self.direccion == "izquierda":
                self.x -= self.velocidad
                if self.x <= self.rango_movimiento[0]:  # Límite izquierdo
                    self.direccion = "derecha"
            self.estado_actual = "walk"

    def obtener_rect(self):
        """Devuelve el rectángulo del enemigo para detección de colisiones."""
        return pygame.Rect(self.x, self.y, 50, 80)  # Ajustar tamaño según el sprite del enemigo

    def atacar(self, jugador):
        ahora = pygame.time.get_ticks()
        if self.vivo and self.obtener_rect().colliderect(jugador.obtener_rect()):
            # Solo atacar si el enemigo está de frente al jugador
            if (self.direccion == "derecha" and self.x < jugador.x) or (self.direccion == "izquierda" and self.x > jugador.x):
                if not self.atacando and ahora - self.ultimo_ataque > self.cooldown_ataque:
                    self.ultimo_ataque = ahora
                    jugador.recibir_daño(self.ataque)
                    self.estado_actual = "attack"
                    self.frame_actual = 0
                    self.atacando = True

    def reducir_vidas(self, cantidad):
        if not self.vivo:
            return False  # No hacer nada si el enemigo ya está muerto

        self.vidas -= cantidad
        if self.vidas <= 0:
            self.vivo = False  # Marcar al enemigo como muerto
            return True  # El enemigo ha sido derrotado
        return False

    def recibir_daño(self, daño):
        daño_reducido = max(daño - self.defensa, 0)
        self.puntos_vida -= daño_reducido
        if self.puntos_vida <= 0:
            self.puntos_vida = 0
            self.vivo = False  # Marcar al enemigo como muerto
            self.estado_actual = "idle"  # Cambiar a estado "idle" al morir
        return daño_reducido

    def actualizar_animacion(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_frame > self.velocidad_animacion:  # Control de velocidad de animación
            self.tiempo_ultimo_frame = ahora
            self.frame_actual += 1
            if self.estado_actual in self.animaciones:
                if self.frame_actual >= len(self.animaciones[self.estado_actual]):
                    self.frame_actual = 0
                    # Solo salir de ataque si estaba atacando
                    if self.estado_actual == "attack":
                        self.estado_actual = "idle"
                        self.atacando = False  # Termina la animación de ataque
            else:
                print(f"Advertencia: Estado '{self.estado_actual}' no tiene animaciones cargadas.")
                self.frame_actual = 0

    def mostrar(self, pantalla):
        if self.vivo and self.estado_actual in self.animaciones and self.animaciones[self.estado_actual]:
            if self.frame_actual >= len(self.animaciones[self.estado_actual]):
                self.frame_actual = 0  # Reiniciar el índice si está fuera de rango
            imagen = self.animaciones[self.estado_actual][self.frame_actual]
            # Corregido: flip solo si va a la izquierda
            if self.direccion == "izquierda":
                imagen = pygame.transform.flip(imagen, True, False)
            pantalla.blit(imagen, (self.x, self.y))
        elif not self.vivo:
            fuente = pygame.font.Font("assets/fonts/helwa.ttf", 24)
            texto_muerto = fuente.render("Muerto", True, (255, 0, 0))
            pantalla.blit(texto_muerto, (self.x, self.y - 20))
        else:
            print(f"Advertencia: No se puede mostrar el estado '{self.estado_actual}' porque no tiene animaciones.")

        # Ya no mostrar el contador de vidas sobre el enemigo
        # if self.vivo:
        #     fuente = pygame.font.Font("assets/fonts/helwa.ttf", 24)
        #     texto_vidas = fuente.render(f"x{self.puntos_vida}", True, (255, 255, 255))
        #     pantalla.blit(texto_vidas, (self.x + 20, self.y - 25))