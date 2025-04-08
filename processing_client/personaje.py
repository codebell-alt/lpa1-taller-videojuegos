# -*- coding: utf-8 -*-
class Personaje:
    def __init__(self, startX, startY):
        self.x = startX
        self.y = startY
        self.velX = 0
        self.enElAire = False
        self.atacando = False
        self.velocidad = 3
        self.ALTURA_SUELO = 450
        self.haciaDerecha = True
        self.tiempoAtaque = 0
        self.duracionAtaque = 500
        self.vidas = 4  # 🔸 También tiene 4 vidas como el enemigo

    def cargarImagenes(self):
        self.imgQuieto = loadImage("muneco_quieto.png")
        self.imgCaminando = loadImage("muneco_caminando.png")
        self.imgSaltando = loadImage("muneco_saltando.png")
        self.imgAtacando = loadImage("muneco_atacando.png")
        self.imagenActual = self.imgQuieto

    def mover(self):
        self.x += self.velX
        if self.enElAire:
            self.y += 5
            if self.y >= self.ALTURA_SUELO:
                self.y = self.ALTURA_SUELO
                self.enElAire = False
                if not self.atacando:
                    self.imagenActual = self.imgQuieto
        if self.velX != 0 and not self.enElAire and not self.atacando:
            self.imagenActual = self.imgCaminando
        self.x = constrain(self.x, 100, width - self.imagenActual.width)

        # Terminar animación de ataque
        if self.atacando and millis() - self.tiempoAtaque > self.duracionAtaque:
            self.atacando = False
            if not self.enElAire:
                self.imagenActual = self.imgCaminando if self.velX != 0 else self.imgQuieto

    def mostrar(self):
        pushMatrix()
        if not self.haciaDerecha:
            translate(self.x + self.imagenActual.width, self.y)
            scale(-1, 1)
            image(self.imagenActual, 0, 0)
        else:
            image(self.imagenActual, self.x, self.y)
        popMatrix()

    def actualizarMovimiento(self, dirX):
        self.velX = dirX * self.velocidad
        if dirX != 0:
            self.haciaDerecha = dirX > 0
        if not self.enElAire and not self.atacando:
            self.imagenActual = self.imgCaminando

    def saltar(self):
        if not self.enElAire:
            self.enElAire = True
            self.imagenActual = self.imgSaltando
            self.y -= 50

    def atacar(self):
        if not self.atacando:
            self.atacando = True
            self.tiempoAtaque = millis()
            self.imagenActual = self.imgAtacando

    def detenerMovimiento(self):
        self.velX = 0
        if not self.enElAire and not self.atacando:
            self.imagenActual = self.imgQuieto
