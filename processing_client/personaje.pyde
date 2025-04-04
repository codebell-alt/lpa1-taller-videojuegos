# personaje
class Personaje:
    def __init__(self, startX, startY):
        self.x = startX
        self.y = startY
        self.velX = 0
        self.enElAire = False
        self.atacando = False
        self.velocidad = 3
        self.ALTURA_SUELO = 450

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

    def mostrar(self):
        image(self.imagenActual, self.x, self.y)

    def actualizarMovimiento(self, dirX):
        self.velX = dirX * self.velocidad
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
            self.imagenActual = self.imgAtacando
            threading.Thread(target=self.resetAtaque).start()

    def resetAtaque(self):
        delay(500)
        self.atacando = False
        self.imagenActual = self.imgQuieto

    def detenerMovimiento(self):
        self.velX = 0
        if not self.enElAire and not self.atacando:
            self.imagenActual = self.imgQuieto
