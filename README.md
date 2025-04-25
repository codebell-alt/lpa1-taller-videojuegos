# Taller Videojuegos

![commits](https://badgen.net/github/commits/UR-CC/lpa1-taller-videojuegos?icon=github) 
![last_commit](https://img.shields.io/github/last-commit/UR-CC/lpa1-taller-videojuegos)

> Consulta [badgen](https://badgen.net/) o [shields](https://shields.io/) para otros tipos de _badges_.

---

## Autores

**Juan Alejandro Ramírez**  
- GitHub: [@juanrs69](https://github.com/juanrs69)

**Isabella Ramírez**  
- GitHub: [@codebell-alt](https://github.com/codebell-alt)

---

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un videojuego básico utilizando los principios de la **Programación Orientada a Objetos** (POO).  
Los estudiantes crean un mundo de juego interactivo donde los jugadores pueden:

- Controlar un personaje
- Explorar escenarios
- Interactuar con objetos y enemigos
- Progresar a través de una historia

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/UR-CC/lpa1-taller-videojuegos.git
cd lpa1-taller-videojuegos
```

### 2. Crear y activar un entorno virtual

Crea un entorno virtual para instalar las dependencias del proyecto:

```bash
python -m venv venv
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

Instala las librerías necesarias, como `pygame`:

```bash
pip install -r requirements.txt
```

---

## Ejecución del Juego

### 1. Navegar al directorio del juego

Ve al directorio donde se encuentra el archivo `main.py`:

```bash
cd game
```

### 2. Ejecutar el juego

Ejecuta el siguiente comando para iniciar el juego:

```bash
python main.py
```

### 3. Disfruta el juego

Sigue las instrucciones en pantalla para jugar.

---

## Solución de Problemas

- **Error: "No module named 'pygame'"**  
  Asegúrate de haber instalado Pygame correctamente ejecutando:
  ```bash
  pip install pygame
  ```

- **Error: "No file 'assets/imagenes/vida.png' found"**  
  Verifica que los archivos necesarios estén en la carpeta `assets/imagenes`. Si faltan, asegúrate de copiarlos o descargarlos.

- **Error: "python no se reconoce como un comando interno o externo"**  
  Asegúrate de que Python esté correctamente instalado y agregado a la variable de entorno `PATH`.

---

¡Diviértete jugando!