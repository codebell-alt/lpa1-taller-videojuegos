import pygame
import random

class Objetos:
    def __init__(self, img_dinero, img_moneda, img_vida_extra, img_vida):
        self.img_dinero = img_dinero
        self.img_moneda = img_moneda
        self.img_vida_extra = img_vida_extra
        self.img_vida = img_vida

        # Eliminamos "moneda" y "vida_extra" de la lista inicial
        self.lista_objetos = [
            {"tipo": "dinero", "x": 200, "y": 450},  # Solo dejamos "dinero" como ejemplo
        ]

    def actualizar(self, jugador, enemigo):
        for obj in self.lista_objetos[:]:
            if abs(jugador.x - obj["x"]) < 30 and abs(jugador.y - obj["y"]) < 30:
                if obj["tipo"] == "vida_extra":
                    jugador.vidas += 1
                elif obj["tipo"] in ["dinero", "moneda"]:
                    jugador.monedas += 500  # Sumar 500 monedas al jugador
                self.lista_objetos.remove(obj)

    def mostrar(self, pantalla, texto, fuente, color):
        for obj in self.lista_objetos:
            if obj["tipo"] == "dinero" and self.img_dinero:
                pantalla.blit(self.img_dinero, (obj["x"], obj["y"]))
            elif obj["tipo"] == "moneda" and self.img_moneda:
                pantalla.blit(self.img_moneda, (obj["x"], obj["y"]))
            elif obj["tipo"] == "vida_extra" and self.img_vida_extra:
                pantalla.blit(self.img_vida_extra, (obj["x"], obj["y"]))

class Particula:
    def __init__(self, x, y, color, cantidad=15):
        self.particulas = []
        for _ in range(cantidad):
            dx = random.uniform(-3, 3)
            dy = random.uniform(-3, 3)
            radio = random.randint(3, 7)
            self.particulas.append({
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "radio": radio,
                "color": color,
                "vida": random.randint(15, 30)
            })

    def actualizar(self):
        for p in self.particulas:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["radio"] = max(0, p["radio"] - 0.2)
            p["vida"] -= 1
        self.particulas = [p for p in self.particulas if p["vida"] > 0 and p["radio"] > 0]

    def dibujar(self, pantalla):
        for p in self.particulas:
            pygame.draw.circle(pantalla, p["color"], (int(p["x"]), int(p["y"])), int(p["radio"]))