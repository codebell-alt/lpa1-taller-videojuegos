import pygame

class Tienda:
    def __init__(self):
        # Cambia los nombres y precios según lo solicitado
        self.objetos = [
            {"nombre": "Vida Extra", "precio": 100, "tipo": "vida", "valor": 1},
            {"nombre": "Defensa (Aura)", "precio": 200, "tipo": "defensa", "valor": 1},
            {"nombre": "PowerUp Disparo", "precio": 300, "tipo": "disparo", "valor": 1},
        ]
        fondo_original = pygame.image.load("assets/imagenes/fondotienda.jpg").convert()
        self.fondo_tienda = pygame.transform.scale(fondo_original, (800, 600))  # Escalar al tamaño de la ventana

    def mostrar_tienda(self, pantalla, fuente):
        # Dibujar el fondo de la tienda
        pantalla.blit(self.fondo_tienda, (0, 0))  # Fondo ocupa toda la pantalla

        # Coordenadas base para centrar el texto en la parte blanca
        base_x = 150  # Más hacia el lado izquierdo
        base_y = 300  # Más abajo en la parte blanca

        # Título de la tienda (más grande, centrado, con fondo blanco y borde rojo)
        fuente_titulo = pygame.font.Font("assets/fonts/Super Jungle.ttf", 50)  # Fuente jungle más grande
        texto_titulo = fuente_titulo.render("Tienda", True, (255, 0, 0))  # Texto en rojo
        borde_titulo = fuente_titulo.render("Tienda", True, (255, 255, 255))  # Borde blanco
        titulo_rect = texto_titulo.get_rect(center=(400, base_y - 200))  # Centrado horizontalmente

        # Dibujar el borde blanco y el texto rojo
        pantalla.blit(borde_titulo, (titulo_rect.x - 2, titulo_rect.y - 2))
        pantalla.blit(borde_titulo, (titulo_rect.x + 2, titulo_rect.y - 2))
        pantalla.blit(borde_titulo, (titulo_rect.x - 2, titulo_rect.y + 2))
        pantalla.blit(borde_titulo, (titulo_rect.x + 2, titulo_rect.y + 2))
        pantalla.blit(texto_titulo, titulo_rect.topleft)

        # Mostrar los objetos disponibles
        for i, objeto in enumerate(self.objetos):
            texto_objeto = fuente.render(
                f"{i + 1}. {objeto['nombre']} - {objeto['precio']} monedas", True, (0, 0, 0)
            )
            pantalla.blit(texto_objeto, (base_x, base_y + i * 40))

        # Mostrar instrucciones con fuente más pequeña
        fuente_instrucciones = pygame.font.Font("assets/fonts/helwa.ttf", 20)
        texto_instrucciones = fuente_instrucciones.render(
            "Presiona el número para comprar o ESC para salir", True, (0, 0, 0)
        )
        pantalla.blit(texto_instrucciones, (base_x, base_y + 150))

    def comprar_objeto(self, pantalla, fuente, jugador, indice):
        # Verificar si el índice es válido
        if 0 <= indice < len(self.objetos):
            objeto = self.objetos[indice]
            # Verificar si el jugador tiene suficientes monedas
            if jugador.monedas >= objeto["precio"]:
                jugador.monedas -= objeto["precio"]
                if objeto["tipo"] == "vida":
                    jugador.vidas += objeto["valor"]  # Agregar vidas
                elif objeto["tipo"] == "defensa":
                    # Activa el aura de defensa al comprar
                    if hasattr(jugador, "activar_aura"):
                        jugador.activar_aura()
                    else:
                        # Si no existe el método, puedes usar una variable global o similar
                        global activar_aura_flag
                        activar_aura_flag = True
                elif objeto["tipo"] == "disparo":
                    # Activa el powerup de disparo al comprar
                    if hasattr(jugador, "activar_disparo"):
                        jugador.activar_disparo()
                    else:
                        global activar_disparo_flag
                        activar_disparo_flag = True
                mensaje = f"Compraste {objeto['nombre']}!"
            else:
                mensaje = "No tienes suficientes monedas."
        else:
            mensaje = "Opción inválida."

        # Mostrar el mensaje en pantalla
        texto_mensaje = fuente.render(mensaje, True, (255, 0, 0))  # Mensaje en rojo
        pantalla.blit(texto_mensaje, (200, 500))  # Mostrar el mensaje en la parte inferior
        pygame.display.flip()  # Actualizar la pantalla
        pygame.time.delay(2000)  # Pausar por 2 segundos para que el usuario vea el mensaje
