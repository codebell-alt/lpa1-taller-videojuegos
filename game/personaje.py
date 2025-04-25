import pygame
import os

class Personaje:
    def __init__(self, x, y, nombre, puntos_vida, ataque, defensa, nivel, inventario):
        """
        Inicializa un personaje con sus atributos principales.
        """
        if puntos_vida <= 0 or ataque <= 0 or defensa < 0 or nivel <= 0:
            raise ValueError("Los atributos iniciales deben ser valores positivos.")
        self.x = x
        self.y = y
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.defensa = defensa
        self.nivel = nivel
        self.inventario = inventario if isinstance(inventario, list) else []
        self.animaciones = {}
        self.frame_actual = 0
        self.estado_actual = "idle"
        self.direccion = "derecha"
        self.ancho = 60
        self.alto = 80
        self.velocidad = 5
        self.saltando = False
        self.contador_salto = 10
        self.atacando = False
        self.puede_atacar = True
        self.cooldown_ataque = 500  # milisegundos
        self.ultimo_ataque = 0
        self.vidas = 4
        self.monedas = 0
        self.tiempo_ultimo_frame = 0
        self.velocidad_animacion = 100  # ms entre cuadros
        self.icono_vida = None
        self.icono_moneda = None

    def cargar_animaciones(self, carpeta):
        """
        Carga las animaciones del personaje desde la carpeta especificada.
        """
        acciones = ["idle", "walk", "attack", "jump"]
        for accion in acciones:
            ruta = os.path.join(carpeta, accion)
            if os.path.exists(ruta):
                self.animaciones[accion] = [
                    pygame.image.load(os.path.join(ruta, img)).convert_alpha()
                    for img in sorted(os.listdir(ruta))
                ]
            else:
                print(f"Advertencia: No se encontró la carpeta de animaciones para '{accion}' en {ruta}")

    def mover(self):
        """
        Gestiona el salto del personaje.
        """
        if self.saltando:
            if self.contador_salto >= -10:
                neg = 1 if self.contador_salto > 0 else -1
                self.y -= (self.contador_salto ** 2) * 0.5 * neg
                self.contador_salto -= 1
            else:
                self.saltando = False
                self.contador_salto = 10

    def actualizar_movimiento(self, direccion):
        """
        Actualiza la posición y el estado del personaje según la dirección.
        Limita el movimiento para que no salga de la pantalla.
        """
        if self.atacando:
            return
        if direccion < 0:
            self.x -= self.velocidad
            self.direccion = "izquierda"
            self.estado_actual = "walk"
        elif direccion > 0:
            self.x += self.velocidad
            self.direccion = "derecha"
            self.estado_actual = "walk"
        else:
            self.estado_actual = "idle"
        # Delimitación de pantalla
        if self.x < 0:
            self.x = 0
        if self.x > 800 - self.ancho:
            self.x = 800 - self.ancho
        if self.y < 0:
            self.y = 0
        if self.y > 600 - self.alto:
            self.y = 600 - self.alto

    def saltar(self):
        """
        Inicia el salto del personaje si no está saltando.
        """
        if not self.saltando:
            self.saltando = True
            self.estado_actual = "jump"

    def obtener_rect(self):
        """
        Devuelve el rectángulo del personaje para detección de colisiones.
        """
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def atacar(self, objetivo):
        """
        Inicia el ataque y verifica colisión con el objetivo.
        """
        ahora = pygame.time.get_ticks()
        if self.puede_atacar:
            self.atacando = True
            self.puede_atacar = False
            self.ultimo_ataque = ahora
            self.estado_actual = "attack"
            self.frame_actual = 0
            if self.obtener_rect().colliderect(objetivo.obtener_rect()):
                if hasattr(objetivo, "recibir_daño"):
                    return objetivo.recibir_daño(self.ataque)

    def recibir_daño(self, daño):
        """
        Reduce los puntos de vida del personaje en función del daño recibido.
        """
        daño_reducido = max(daño - self.defensa, 0)
        self.puntos_vida -= daño_reducido
        if self.puntos_vida <= 0:
            self.vidas -= 1
            if self.vidas > 0:
                self.puntos_vida = 0
                print(f"{self.nombre} perdió una vida. Vidas restantes: {self.vidas}")
                self.puntos_vida = 20
            else:
                self.puntos_vida = 0
                print(f"{self.nombre} ha muerto.")
        return daño_reducido

    def subir_nivel(self):
        """
        Incrementa el nivel y mejora los atributos del personaje.
        """
        self.nivel += 1
        self.puntos_vida += 10
        self.ataque += 2
        self.defensa += 1
        print(f"{self.nombre} ha subido al nivel {self.nivel}.")

    def actualizar_ataque(self):
        """
        Actualiza el estado del ataque y permite atacar nuevamente después del cooldown.
        """
        ahora = pygame.time.get_ticks()
        if self.atacando and ahora - self.ultimo_ataque > 200:
            self.atacando = False
            self.estado_actual = "idle"
        if ahora - self.ultimo_ataque > self.cooldown_ataque:
            self.puede_atacar = True

    def actualizar_animacion(self):
        """
        Actualiza el frame de animación del personaje según el estado.
        """
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_frame > self.velocidad_animacion:
            self.tiempo_ultimo_frame = ahora
            self.frame_actual += 1
            if self.estado_actual in self.animaciones:
                if self.frame_actual >= len(self.animaciones[self.estado_actual]):
                    self.frame_actual = 0
                    if self.estado_actual == "attack":
                        self.estado_actual = "idle"
            else:
                print(f"Advertencia: Estado '{self.estado_actual}' no tiene animaciones cargadas.")
                self.frame_actual = 0

    def mostrar(self, pantalla):
        """
        Dibuja el personaje y sus iconos de vida y monedas en pantalla.
        """
        if self.estado_actual in self.animaciones and self.animaciones[self.estado_actual]:
            if self.frame_actual >= len(self.animaciones[self.estado_actual]):
                self.frame_actual = 0
            imagen = self.animaciones[self.estado_actual][self.frame_actual]
            if self.direccion == "izquierda":
                imagen = pygame.transform.flip(imagen, True, False)
            pantalla.blit(imagen, (self.x, self.y))
        else:
            print(f"Advertencia: No se puede mostrar el estado '{self.estado_actual}' porque no tiene animaciones.")

        # Dibujar vidas (corazones)
        for i in range(self.vidas):
            if self.icono_vida:
                pantalla.blit(self.icono_vida, (10 + i * 30, 10))

        # Dibujar monedas
        if self.icono_moneda:
            pantalla.blit(self.icono_moneda, (10, 50))
            font = pygame.font.Font("assets/fonts/helwa.ttf", 24)
            texto_monedas = font.render(f"{self.monedas}", True, (255, 255, 255))
            pantalla.blit(texto_monedas, (50, 50))

    def agregar_al_inventario(self, objeto):
        """
        Agrega un objeto al inventario del personaje.
        """
        self.inventario.append(objeto)

    def esta_vivo(self):
        """
        Verifica si el personaje está vivo.
        """
        return self.puntos_vida > 0

    def eliminar_del_inventario(self, objetos):
        """
        Elimina uno o varios objetos del inventario del personaje.
        """
        if not isinstance(objetos, list):
            objetos = [objetos]
        eliminados = []
        no_encontrados = []
        for objeto in objetos:
            if objeto in self.inventario:
                self.inventario.remove(objeto)
                eliminados.append(objeto)
            else:
                no_encontrados.append(objeto)
        if eliminados:
            print(f"Se eliminaron del inventario: {eliminados}")
        if no_encontrados:
            print(f"No se encontraron en el inventario: {no_encontrados}")
