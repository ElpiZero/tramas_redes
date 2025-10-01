import socket
import threading

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.connect(("localhost", 60000))

def enviar_mensaje(socket_cliente):
    mensaje = ""
    try:
        
        while mensaje != "exit":

            mensaje = input("Mensaje cliente:")
            socket_cliente.send(mensaje.encode())
            mensaje = mensaje.lower()
    except Exception as error:
        print(f"Error al enviar:{error}")
        
    
    socket_cliente.close()
    return


def recibir_mensaje(socket_cliente):
    respuesta = ""
    while respuesta != "exit":
        
        try:
            respuesta = socket_cliente.recv(100).decode("utf-8")
        except Exception as error:
            print(f"Error al recibir:{error}")
            break
        print(f"Respuesta del servidor: {respuesta}")
        respuesta = respuesta.lower()
    
    
hilo_envio = threading.Thread(target=enviar_mensaje, args= (socket_cliente,))
hilo_recepcion = threading.Thread(target=recibir_mensaje, args = (socket_cliente,))

hilo_envio.start()
hilo_recepcion.start()

hilo_envio.join()
hilo_recepcion.join()
