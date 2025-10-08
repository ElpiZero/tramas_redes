import socket
import threading

# Crear un socket global
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind(("", 60000))
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
corriendo = True
# Función para unirse
def unirse():
    while True:
        user_name = input("Ingrese nombre de usuario: ")
        if len(user_name) > 0:
            # Al unirse, se envía un mensaje de "nuevo"
            enviar(" nuevo", user_name)
            return user_name
        else:
            print("El nombre de usuario no puede estar vacío. Intente nuevamente.")

# Función para enviar mensajes
def enviar(mensaje, user_name):
    # Enviar el mensaje general
    socket_server.sendto(f"{user_name}:{mensaje}".encode(), ("<broadcast>", 60000))

# Función para recibir mensajes
def recibir():
    while corriendo:
        try:
            
            datos_recibidos, address = socket_server.recvfrom(3000)
            mensaje = datos_recibidos.decode()
            #parseo
            if(":") in mensaje:
                u,contenido = mensaje.split(":",1)
                
                
                if contenido.lower() == "nuevo":
                    print(f"{u} ({address[0]}): se ha unido la conversacion")
                elif contenido.lower() == "exit":
                    print(f"{u} ({address[0]}): ha abandonado la conversacion")
                else:
                    print(f"{u} ({address[0]}):{contenido}")
        except Exception as e:
            if corriendo:
                print(f"error recibiendo mensaje : {e}")    

# Hilo para recibir mensajes
def hilo_recibir():
    thread_reception = threading.Thread(target=recibir)
    thread_reception.daemon = True
    thread_reception.start()

# Hilo para enviar mensajes
def hilo_enviar(user_name):
    global corriendo
    while True:
        msg = input("")
        if msg.lower() == "exit":
            enviar("exit", user_name)
            corriendo = False
            socket_server.close()
            break
        enviar(msg, user_name)

# Función principal
def main():
    nombre = unirse()

    # Crear y lanzar los hilos
    hilo_recibir()
    hilo_enviar(nombre)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
