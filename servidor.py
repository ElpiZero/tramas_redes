import socket
import threading

socket_server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind(("0.0.0.0", 60000))

socket_server.listen(2)

socket_cliente = None

lock= threading.Lock()

start_input_event = threading.Event()

def aceptar_peticion():
    global socket_cliente
    while True:
        (cliente, direcciones) = socket_server.accept()
        with lock:
            if not socket_cliente:
                socket_cliente = cliente
                print(f"Cliente conectado: {direcciones}")
                threading.Thread(target=recibir_mensaje, args=(cliente,)).start()
                threading.Thread(target=enviar_mensaje, args=(cliente,)).start()
            else:
                print("Ya hay un cliente conectado. Rechazando conexión...")
                cliente.send("Servidor ocupado, intente más tarde.".encode())
                cliente.close()


def enviar_mensaje(cliente):
    global socket_cliente
    start_input_event.wait()
    try:
        while True:

            mensaje = input("Mensaje servidor:")
    
            if mensaje.lower() =="exit":
                if socket_cliente:
                    print("No es posible cerrar el proceso servidor si hay un cliente conectado")
                else:
                    socket_server.close()
                    break

            socket_cliente.send(mensaje.encode())
            
    except Exception as error:
        print(f"Error al enviar:{error}")



def recibir_mensaje(cliente):
    global socket_cliente
    respuesta = ""
    while respuesta != "exit":
        
        try:
            respuesta = socket_cliente.recv(100).decode("utf-8")
        except Exception as error:
            print(f"Error al recibir:{error}")
            break
        
        print(f"Respuesta del cliente: {respuesta}")
        start_input_event.set()
        respuesta = respuesta.lower()
    with lock:
        socket_cliente.close()
        socket_cliente = None

    
hilo_aceptar = threading.Thread(target=aceptar_peticion)

hilo_aceptar.start()
hilo_aceptar.join()
