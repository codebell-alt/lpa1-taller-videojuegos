import pygame

class Tesoro:
    def __init__(self, x, y, valor):
        self.x = x
        self.y = y
        self.valor = valor
        self.recogido = False
        self.img_tesoro = None

    def cargar_imagen(self, imagen):
        self.img_tesoro = imagen

    def recoger(self, jugador):
        if not self.recogido:
            # Aseguramos que el tesoro solo se recoja una vez
            jugador.agregar_al_inventario({"tipo": "tesoro", "valor": self.valor})
            self.recogido = True
            return self.valor
        return 0

    def mostrar(self, pantalla):
        # Solo mostramos el tesoro si no ha sido recogido
        if not self.recogido and self.img_tesoro:
            pantalla.blit(self.img_tesoro, (self.x, self.y))
