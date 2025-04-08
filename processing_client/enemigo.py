# -*- coding: utf-8 -*-
class Enemigo:
    def __init__(self, startX, startY):
        self.x = startX
        self.y = startY
        self.velX = 2
        self.haciaDerecha = False
        self.vidas = 3
        self.vivo = True  # 👈 NUEVO: indica si el enemigo sigue activo

    def cargarImagen(self, imagen):
        self.imagen = imagen

    def mover(self):
        if self.vivo:  # 👈 Solo se mueve si está vivo
            self.x += self.velX
            if self.x <= 100 or self.x >= width - self.imagen.width:
                self.velX *= -1
                self.haciaDerecha = self.velX > 0

    def mostrar(self):
        if self.vivo:  # 👈 Solo se muestra si está vivo
            pushMatrix()
            if not self.haciaDerecha:
                translate(self.x + self.imagen.width, self.y)
                scale(-1, 1)
                image(self.imagen, 0, 0)
            else:
                image(self.imagen, self.x, self.y)
            popMatrix()

    def recibirAtaque(self, personaje):
        if self.vivo and personaje.atacando:
            distancia = dist(self.x, self.y, personaje.x, personaje.y)
            if distancia < 80:
                self.vidas -= 1
                personaje.atacando = False  # para evitar ataques múltiples seguidos
                if self.vidas <= 0:
                    self.vivo = False  # 👈 Enemigo "muere"
