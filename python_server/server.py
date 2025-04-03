import socket

# Configurar el servidor
HOST = "127.0.0.1"  # IP local
PORT = 12345        # Puerto de conexión

# Crear socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Permite 1 conexión a la vez

print("Servidor esperando conexión...")

# Aceptar conexión de Processing
conn, addr = server_socket.accept()
print(f"Conectado con {addr}")

while True:
    data = conn.recv(1024).decode()  # Recibir datos
    if not data:
        break  # Terminar si no hay datos

    print(f"Processing envió: {data}")  
    respuesta = f"Recibido: {data}"  # Respuesta del servidor

    conn.send(respuesta.encode())  # Enviar respuesta a Processing

conn.close()
