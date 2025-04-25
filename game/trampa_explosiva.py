import pygame

class TrampaExplosiva:
    def __init__(self, x, y, alcance, daño):
        self.x = x
        self.y = y
        self.alcance = alcance
        self.daño = daño
        self.activa = True  # La trampa está activa inicialmente
        self.img_trampa = None

    def cargar_imagen(self, imagen):
        self.img_trampa = imagen

    def obtener_rect(self):
        """Devuelve el rectángulo de la trampa para detección de colisiones."""
        return pygame.Rect(self.x, self.y, self.img_trampa.get_width(), self.img_trampa.get_height())

    def detonar(self, objetivo):
        if not self.activa:
            return False  # No detonar si ya fue usada

        if self.obtener_rect().colliderect(objetivo.obtener_rect()):  # Verificar colisión con el jugador
            if hasattr(objetivo, "recibir_daño"):
                objetivo.recibir_daño(self.daño)
            self.activa = False  # Desactivar la trampa después de detonar
            return True
        return False

    def mostrar(self, pantalla):
        if self.activa and self.img_trampa:
            pantalla.blit(self.img_trampa, (self.x, self.y))
