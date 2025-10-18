import socket
import threading
import os

socket_server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind(("0.0.0.0", 60000))

socket_archivos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_archivos.bind(("0.0.0.0", 60001))
socket_archivos.listen(1)

socket_server.listen(2)

socket_cliente = None

lock= threading.Lock()

start_input_event = threading.Event()

def aceptar_peticion():
    global socket_cliente
    while True:
        try:
            (cliente, direcciones) = socket_server.accept()
        except OSError:
            print("Socket del servidor cerrado.")
            break  # termina el loop si el socket ya no existe
        
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

            mensaje = input("Mensaje servidor:\n")
            with lock:
                if socket_cliente is None:
                    print("No hay clientes conectados. Solo se puede usar \"exit\" para cerrar el servidor.")
                    if mensaje.lower() == "exit":
                        socket_server.close()
                        break
                    else:
                        continue
            if mensaje.lower().startswith("send_file"): # detectamos que queremos enviar un archivo.
                nombre_archivo = mensaje[len("send_file "):]
                if os.path.exists(nombre_archivo):  # verificamos la existencia del archivo antes de mandarlo.
                    print("El archivo se encontró correctamente. Preparando para ser enviado.")
                    socket_enviar_archivo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # creamos una conexión nueva
                    socket_enviar_archivo.connect(("localhost", 60002))
                    nombre_sin_ruta = os.path.basename(nombre_archivo)
                    socket_enviar_archivo.send(nombre_sin_ruta.encode()) # enviamos el nombre del archivo para que el serv. sepa con qué nombre guardarlo.
                    with open(nombre_archivo, "rb") as archivo: # abrimos el archivo como un binario
                        bloque = archivo.read(1024)
                        while bloque:   # le mandamos la información en bloques de 1024B cada uno.
                            socket_enviar_archivo.send(bloque)
                            bloque = archivo.read(1024)
                    socket_enviar_archivo.close()
                else:
                    print("No se encontró el archivo.")
            else:
                socket_cliente.send(mensaje.encode())
                mensaje = mensaje.lower()
            if mensaje.lower() =="exit":
                if socket_cliente:
                    print("No es posible cerrar el proceso servidor si hay un cliente conectado")
                else:
                    socket_server.close()
                    break
            # Verificamos si el cliente está conectado, si no lo está avisamos y seguimos.
            if socket_cliente is None:
                print("No hay clientes conectados.")
                continue

            # Intentamos enviar el mensaje, si no se puede el cliente se desconectó y solo podemos cerrar el servidor mediante "exit"
            try:
                socket_cliente.send(mensaje.encode())
            except OSError as e:
                print(f"Error al enviar: {e}. El cliente se desconectó.")
                socket_cliente = None
                continue

    except Exception as error:
        print(f"Error al enviar: {error}")


def recibir_mensaje(cliente):
    global socket_cliente
    respuesta = ""
    while respuesta != "exit":
        
        try:
            respuesta = socket_cliente.recv(100).decode("utf-8")
            
            if not respuesta:
                print("Cliente desconectado.")
                break
            if respuesta.lower().startswith("send_file"):   # detectamos que el cliente quiere enviar un archivo
                nombre_archivo = respuesta[len("send_file "):]
                print(f"El cliente envía un archivo: {nombre_archivo}.")
        except (OSError, ConnectionResetError): # excepción para cuando se haga shutdown_client
            print("El cliente se desconectó mediante una fuerza mayor.")
            break
        except Exception as error:
            print(f"Error al recibir:{error}")
            break
        
        print(f"Respuesta del cliente: {respuesta}")
        start_input_event.set()
        respuesta = respuesta.lower()
    with lock:
        socket_cliente.close()
        socket_cliente = None

def recibir_archivos(): # funcion para recibir los archivos
    while True:
        (cliente_archivo, direccion) = socket_archivos.accept()
        
        nombre_archivo = cliente_archivo.recv(1024).decode()
        with open(nombre_archivo, "wb") as archivo:
            print(f"Guardando archivo en: {os.path.abspath(nombre_archivo)}")
            while True:
                bloque = cliente_archivo.recv(1024)
                if not bloque:
                    break
                archivo.write(bloque)
        cliente_archivo.close()
        print(f"Archivo {nombre_archivo} recibido correctamente.")

hilo_archivos = threading.Thread(target=recibir_archivos, daemon=True)
hilo_archivos.start()

hilo_aceptar = threading.Thread(target=aceptar_peticion)
hilo_aceptar.start()
hilo_aceptar.join()
