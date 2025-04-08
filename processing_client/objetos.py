# -*- coding: utf-8 -*-
class Objetos:
    def __init__(self, dineroImg, monedaImg, vidaExtraImg, corazonImg):
        self.dineroImg = dineroImg
        self.monedaImg = monedaImg
        self.vidaExtraImg = vidaExtraImg
        self.corazonImg = corazonImg
        self.vidas = 4
        self.monedas = 0
        self.dineroX = 400
        self.dineroY = 500  # POSICIÓN MÁS BAJA
        self.vidaExtraX = 200
        self.vidaExtraY = 510  # POSICIÓN MÁS BAJA
        self.mostrarDinero = True
        self.mostrarVidaExtra = False
        self.tiempoDinero = millis()
        self.tiempoVidaExtra = millis()
        self.intervaloDinero = 10000
        self.intervaloVidaExtra = 9000
        self.reaparicionVidaExtra = 60000
        self.perdioVida = False
        self.estadoGameOver = False
        self.tiempoUltimaColision = 0
        self.cooldownColision = 1000

    def actualizar(self, jugador, enemigo):
        t = millis()

        # Centro del personaje
        centroJugadorX = jugador.x + jugador.imagenActual.width / 2
        centroJugadorY = jugador.y + jugador.imagenActual.height / 2

        # Colisión con dinero
        if self.mostrarDinero and self.colision(centroJugadorX, centroJugadorY, self.dineroX + 20, self.dineroY + 20, 40):
            self.monedas += 500
            self.mostrarDinero = False
            self.tiempoDinero = t

        # Reaparición dinero en zona más baja
        if not self.mostrarDinero and t - self.tiempoDinero >= 5000:
            self.dineroX = random(100, width - 100)
            self.dineroY = random(500, height - 80)  # POSICIÓN MÁS BAJA
            self.mostrarDinero = True

                # Colisión con enemigo (solo si está vivo)
        if enemigo.vivo and not self.estadoGameOver and self.colision(centroJugadorX, centroJugadorY, enemigo.x + enemigo.imagen.width / 2, enemigo.y + enemigo.imagen.height / 2, 70):
            if t - self.tiempoUltimaColision >= self.cooldownColision:
                self.vidas -= 1
                self.perdioVida = True
                self.tiempoUltimaColision = t
                if self.vidas <= 0:
                    self.estadoGameOver = True

        # Vida extra aparece si pierde una
        if self.perdioVida:
            if self.vidas < 4 and not self.mostrarVidaExtra and t - self.tiempoVidaExtra >= self.intervaloVidaExtra:
                self.mostrarVidaExtra = True
                self.vidaExtraX = random(100, width - 100)
                self.vidaExtraY = random(510, height - 70)  # POSICIÓN MÁS BAJA
                self.tiempoVidaExtra = t

        # Colisión con vida extra
        if self.mostrarVidaExtra and self.colision(centroJugadorX, centroJugadorY, self.vidaExtraX + 20, self.vidaExtraY + 20, 40):
            self.vidas += 1
            if self.vidas > 4:
                self.vidas = 4
            self.mostrarVidaExtra = False
            self.tiempoVidaExtra = t

    def mostrar(self, nombre, fuenteTexto, fuenteGO):
        for i in range(self.vidas):
            image(self.corazonImg, 10 + i * 35, 10, 30, 30)

        fill(255)
        textFont(fuenteTexto)
        textSize(20)
        image(self.monedaImg, width - 60, 10, 30, 30)
        text(str(self.monedas), width - 95, 30)

        if self.mostrarDinero:
            image(self.dineroImg, self.dineroX, self.dineroY, 40, 40)
        if self.mostrarVidaExtra:
            image(self.vidaExtraImg, self.vidaExtraX, self.vidaExtraY + 10, 40, 40)

        if self.estadoGameOver:
            textFont(fuenteGO)
            textAlign(CENTER, CENTER)
            fill(255)
            for dx in [-3, 3]:
                for dy in [-3, 3]:
                    text("GAME OVER", width / 2 + dx, height / 2 - 100 + dy)

            fill(128, 0, 255)
            text("GAME OVER", width / 2, height / 2 - 100)

            textFont(fuenteTexto)
            fill(255)
            textSize(30)

            rectMode(CENTER)
            fill(100)
            rect(width / 2, height / 2 + 60, textWidth(nombre + ", haz perdido") + 20, 40, 10)
            fill(255)
            text(nombre + ", haz perdido", width / 2, height / 2 + 60)

            fill(90, 50, 150, 200)
            rect(width / 2, height / 2 + 110, textWidth("Haz clic para jugar de nuevo") + 40, 40, 10)
            fill(255)
            textSize(20)
            text("Haz clic para jugar de nuevo", width / 2, height / 2 + 115)

    def colision(self, x1, y1, x2, y2, distancia):
        return dist(x1, y1, x2, y2) < distancia

    def revisarClickReinicio(self, jugador):
        if self.estadoGameOver:
            self.vidas = 4
            self.monedas = 0
            self.estadoGameOver = False
            self.tiempoUltimaColision = 0
            jugador.x = 100
            jugador.y = 450
