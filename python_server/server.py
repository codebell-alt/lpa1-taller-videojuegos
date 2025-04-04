import socket

# Configuración del servidor
HOST = '127.0.0.1'  # Dirección local
PORT = 12345        # Puerto a usar (el mismo que en Processing)

# Crear socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"[Servidor iniciado en {HOST}:{PORT}] Esperando conexiones...")

# Aceptar conexión del cliente (Processing)
while True:
    client_socket, client_address = server_socket.accept()
    print(f"[Conexión aceptada desde {client_address}]")

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"[Mensaje recibido] {data}")
        except ConnectionResetError:
            print("[Cliente desconectado]")
            break

    client_socket.close()
    print("[Conexión cerrada]")
