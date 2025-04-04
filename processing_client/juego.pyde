# =================== SOCKET ===================
import socket
import threading

sock = None
out = None

# =================== VARIABLES ===================
fondoImg = None
fondoInicio = None
corazonImg = None
enemigoImg = None
dineroImg = None
monedaImg = None
vidaExtraImg = None

fuenteHelwa = None
fuenteGameOver = None

fondoX = 0
enemigoX = 600
enemigoY = 450
pantallaInicio = True

vidas = 4
invulnerable = False
tiempoInvulnerable = 0
nombreJugador = ""

dineroVisible = True
dineroX = 500
dineroY = 400
dineroFlotanteOffset = 0
subiendo = True

tiempoUltimoCambio = 0
mostrarDinero = True
monedas = 0

mostrarVidaExtra = False
vidaExtraX = 300
vidaExtraY = 400
vidaExtraOffset = 0
subeVida = True
tiempoVidaExtra = 0
intervaloVidaExtra = 60000  # 1 minuto
retardoInicialVida = 9000  # 9 segundos

jugador = None

def setup():
    global fondoImg, fondoInicio, corazonImg, enemigoImg, dineroImg, monedaImg, vidaExtraImg
    global fuenteHelwa, fuenteGameOver, jugador, tiempoUltimoCambio, tiempoVidaExtra

    size(800, 600)

    fondoImg = loadImage("fondo1.jpg")
    fondoInicio = loadImage("fondoinicio.jpg")
    corazonImg = loadImage("vida.png")
    enemigoImg = loadImage("enemigo_caminando.png")
    dineroImg = loadImage("dinero.png")
    monedaImg = loadImage("moneda.png")
    vidaExtraImg = loadImage("vidaextra.png")

    fuenteHelwa = createFont("Helwa.ttf", 20)
    fuenteGameOver = createFont("Super Jungle.ttf", 90)

    jugador = Personaje(100, 450)
    jugador.cargarImagenes()

    tiempoUltimoCambio = millis()
    tiempoVidaExtra = millis()

    conectarConServidor()


def draw():
    if pantallaInicio:
        mostrarPantallaInicio()
    else:
        jugar()


def mostrarPantallaInicio():
    global nombreJugador
    image(fondoInicio, 0, 0, width, height)
    fill(0)
    textFont(fuenteHelwa)
    textSize(30)
    textAlign(CENTER, CENTER)
    text("INGRESA TU NOMBRE:", width / 2, height / 3)

    textSize(32)
    text(nombreJugador + "_", width / 2, height / 2)

    textSize(24)
    text("Presione ENTER para continuar", width / 2, height / 1.5)


def jugar():
    global fondoX, invulnerable, tiempoInvulnerable, mostrarDinero, tiempoUltimoCambio
    global dineroFlotanteOffset, subiendo, monedas, mostrarVidaExtra, vidaExtraOffset
    global subeVida, tiempoVidaExtra, vidas

    background(0)

    image(fondoImg, fondoX, 0, width, height)
    image(fondoImg, fondoX + width, 0, width, height)
    image(fondoImg, fondoX - width, 0, width, height)

    if jugador.velX != 0:
        fondoX -= jugador.velX

    if fondoX <= -width:
        fondoX += width
    elif fondoX >= width:
        fondoX -= width

    jugador.mover()
    jugador.mostrar()

    image(enemigoImg, enemigoX, enemigoY)

    fill(255)
    textSize(20)
    textFont(fuenteHelwa)
    textAlign(LEFT, CENTER)

    stroke(0)
    strokeWeight(3)
    text("Jugador: " + nombreJugador, 20, 30)
    text("Vida:", 220, 30)
    noStroke()

    for i in range(vidas):
        image(corazonImg, 280 + i * 30, 15, 25, 25)

    image(monedaImg, width - 130, 20, 30, 30)
    text(str(monedas), width - 90, 35)

    if not invulnerable and dist(jugador.x, jugador.y, enemigoX, enemigoY) < 50:
        vidas = max(vidas - 1, 0)
        invulnerable = True
        tiempoInvulnerable = millis()
    if invulnerable and millis() - tiempoInvulnerable > 2000:
        invulnerable = False

    tiempoActual = millis()
    if mostrarDinero and tiempoActual - tiempoUltimoCambio >= 10000:
        mostrarDinero = False
        tiempoUltimoCambio = tiempoActual
    elif not mostrarDinero and tiempoActual - tiempoUltimoCambio >= 30000:
        mostrarDinero = True
        tiempoUltimoCambio = tiempoActual

    if mostrarDinero:
        if subiendo:
            dineroFlotanteOffset -= 0.5
            if dineroFlotanteOffset <= -10:
                subiendo = False
        else:
            dineroFlotanteOffset += 0.5
            if dineroFlotanteOffset >= 10:
                subiendo = True

        image(dineroImg, dineroX, dineroY + dineroFlotanteOffset, 40, 40)

        if dist(jugador.x, jugador.y, dineroX, dineroY) < 50:
            monedas += 500
            mostrarDinero = False
            tiempoUltimoCambio = millis()
            enviarDatos()

    if not mostrarVidaExtra and tiempoActual - tiempoVidaExtra > retardoInicialVida and vidas < 4:
        mostrarVidaExtra = True

    if mostrarVidaExtra:
        if subeVida:
            vidaExtraOffset -= 0.4
            if vidaExtraOffset <= -10:
                subeVida = False
        else:
            vidaExtraOffset += 0.4
            if vidaExtraOffset >= 10:
                subeVida = True

        image(vidaExtraImg, vidaExtraX, vidaExtraY + vidaExtraOffset, 40, 40)

        if dist(jugador.x, jugador.y, vidaExtraX, vidaExtraY) < 50:
            if vidas < 4:
                vidas += 1
            mostrarVidaExtra = False
            tiempoVidaExtra = millis() + intervaloVidaExtra

    if vidas == 0:
        textFont(fuenteGameOver)
        textAlign(CENTER, CENTER)
        fill(0)
        text("GAME OVER", width / 2 + 4, height / 2 + 4)
        fill(170, 0, 255)
        text("GAME OVER", width / 2, height / 2)

        botonX = width / 2 - 100
        botonY = height / 2 + 80
        botonAncho = 200
        botonAlto = 50

        fill(255, 100)
        stroke(255)
        strokeWeight(2)
        rect(botonX, botonY, botonAncho, botonAlto, 10)

        fill(255)
        textFont(fuenteHelwa)
        textSize(24)
        noStroke()
        text("JUGAR DE NUEVO", width / 2, botonY + botonAlto / 2)

        noLoop()


def mousePressed():
    if vidas == 0:
        botonX = width / 2 - 100
        botonY = height / 2 + 80
        botonAncho = 200
        botonAlto = 50

        if botonX < mouseX < botonX + botonAncho and botonY < mouseY < botonY + botonAlto:
            reiniciarJuego()


def reiniciarJuego():
    global vidas, monedas, mostrarDinero, mostrarVidaExtra, tiempoUltimoCambio, tiempoVidaExtra, jugador
    vidas = 4
    monedas = 0
    mostrarDinero = True
    mostrarVidaExtra = False
    tiempoUltimoCambio = millis()
    tiempoVidaExtra = millis()
    jugador = Personaje(100, 450)
    jugador.cargarImagenes()
    loop()


def keyPressed():
    global pantallaInicio
    if pantallaInicio:
        if key == ENTER:
            if len(nombreJugador) > 0:
                pantallaInicio = False
    else:
        if key == 'w' or keyCode == UP:
            jugador.saltar()
        elif key == 'a' or keyCode == LEFT:
            jugador.actualizarMovimiento(-1)
        elif key == 'd' or keyCode == RIGHT:
            jugador.actualizarMovimiento(1)
        elif key == ' ':
            jugador.atacar()


def keyReleased():
    if not pantallaInicio:
        jugador.detenerMovimiento()


def keyTyped():
    global nombreJugador
    if pantallaInicio:
        if key == BACKSPACE and len(nombreJugador) > 0:
            nombreJugador = nombreJugador[:-1]
        elif key != ENTER and key != RETURN and key != BACKSPACE:
            nombreJugador += key


# =================== CLASE PERSONAJE ===================

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

# =================== SOCKET CLIENTE ===================

def conectarConServidor():
    global sock, out
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 12345))
        out = sock.makefile('w')
        print("Conectado al servidor Python")
    except Exception as e:
        print("Error al conectar con el servidor:", e)

def enviarDatos():
    global out
    if out:
        try:
            out.write(nombreJugador + " tiene " + str(monedas) + " monedas.\n")
            out.flush()
        except:
            print("Error al enviar datos al servidor")