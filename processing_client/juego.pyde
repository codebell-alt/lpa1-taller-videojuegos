from personaje import Personaje
from enemigo import Enemigo
from objetos import Objetos
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
pantallaInicio = True
nombreJugador = ""

enemigo = None
jugador = None
objetos = None

def setup():
    global fondoImg, fondoInicio, corazonImg, enemigoImg, dineroImg, monedaImg, vidaExtraImg
    global fuenteHelwa, fuenteGameOver, jugador, enemigo, objetos

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

    enemigo = Enemigo(600, 450)
    enemigo.cargarImagen(enemigoImg)

    objetos = Objetos(dineroImg, monedaImg, vidaExtraImg, corazonImg)

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
    global fondoX

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

    enemigo.mover()
    enemigo.mostrar()

    # Aquí está el ataque
    enemigo.recibirAtaque(jugador)

    objetos.actualizar(jugador, enemigo)
    objetos.mostrar(nombreJugador, fuenteHelwa, fuenteGameOver)


def keyPressed():
    global pantallaInicio
    if pantallaInicio:
        if key == ENTER and len(nombreJugador) > 0:
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

def mousePressed():
    objetos.revisarClickReinicio(jugador)
