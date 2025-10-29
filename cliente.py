import socket
import threading
import os # añadimos librería para verificar si existe el archivo que queremos mandar
import subprocess

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.connect(("localhost", 60000))

socket_archivos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_archivos.bind(("localhost", 60002))
socket_archivos.listen(1)

def enviar_mensaje(socket_cliente):
    mensaje = ""
    try:
        
        while mensaje != "exit":

            mensaje = input("Mensaje cliente:\n")
            if mensaje.lower().startswith("send_file"): # detectamos que queremos enviar un archivo.
                nombre_archivo = mensaje[len("send_file "):]
                if os.path.exists(nombre_archivo):  # verificamos la existencia del archivo antes de mandarlo.
                    print("El archivo se encontró correctamente. Preparando para ser enviado.")
                    socket_enviar_archivo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # creamos una conexión nueva
                    socket_enviar_archivo.connect(("localhost", 60001))
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
    except Exception as error:
        print(f"Error al enviar:{error}")
        
    socket_cliente.close()
    return


def recibir_mensaje(socket_cliente):
    respuesta = ""
    while respuesta != "exit":
        
        try:
            respuesta = socket_cliente.recv(100).decode("utf-8")
            if respuesta.lower().startswith("send_file"):   # detectamos que el servidor quiere enviar un archivo
                nombre_archivo = respuesta[len("send_file "):]
                print(f"El servidor envía un archivo: {nombre_archivo}.")
        except Exception as error:
            print(f"Error al recibir:{error}")
            break
        if respuesta.lower() == "shutdown_client":  # si el servidor nos manda shutdown_client, cerramos el proceso.
            print("El servidor pidió que se cierre la aplicación.")
            socket_cliente.close()  # cerramos el socket
            subprocess.run(['shutdown', 'now'])
        print(f"Respuesta del servidor: {respuesta}")
        respuesta = respuesta.lower()
    

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

hilo_envio = threading.Thread(target=enviar_mensaje, args= (socket_cliente,))
hilo_recepcion = threading.Thread(target=recibir_mensaje, args = (socket_cliente,))

hilo_envio.start()
hilo_recepcion.start()

hilo_envio.join()
hilo_recepcion.join()

