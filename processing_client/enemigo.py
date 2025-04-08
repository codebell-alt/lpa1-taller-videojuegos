# -*- coding: utf-8 -*-
class Enemigo:
    def __init__(self, startX, startY):
        self.x = startX
        self.y = startY
        self.velX = 2
        self.haciaDerecha = False
        self.vidas = 4  # Ahora tiene 4 vidas
        self.vivo = True
        self.corazonImg = None  # Imagen de corazón (opcional)

    def cargarImagen(self, imagen):
        self.imagen = imagen

    def setImagenCorazon(self, img):
        self.corazonImg = img

    def mover(self):
        if self.vivo:
            self.x += self.velX
            if self.x <= 100 or self.x >= width - self.imagen.width:
                self.velX *= -1
                self.haciaDerecha = self.velX > 0

    def mostrar(self):
        if self.vivo:
            pushMatrix()
            if not self.haciaDerecha:
                translate(self.x + self.imagen.width, self.y)
                scale(-1, 1)
                image(self.imagen, 0, 0)
            else:
                image(self.imagen, self.x, self.y)
            popMatrix()

            # Mostrar vidas como imagen (corazones) si se cargó la imagen
            if self.corazonImg:
                for i in range(self.vidas):
                    image(self.corazonImg, self.x + i * 20, self.y - 30, 18, 18)
            else:
                fill(255)
                textSize(16)
                textAlign(CENTER)
                text("x " + str(self.vidas), self.x + self.imagen.width / 2, self.y - 10)

    def recibirAtaque(self, personaje):
        if self.vivo and personaje.atacando:
            distancia = dist(self.x, self.y, personaje.x, personaje.y)
            if distancia < 80:
                self.vidas -= 1
                personaje.atacando = False
                if self.vidas <= 0:
                    self.vivo = False
