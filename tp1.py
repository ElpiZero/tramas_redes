def dividir_tramas(nombre_archivo):
    tramas_totales = []
    archivo = open(nombre_archivo)
    tramas = archivo.readlines()
    i = 0
    inicio_trama = None
    
    while i < len(tramas[0]):
        if tramas[0][i:i+2] == "7E":
            if i == 0 or tramas[0][i-2:i] != "7D":
                if inicio_trama is not None:
                    trama = tramas[0][inicio_trama:i]
                    tramas_totales.append(trama)
                inicio_trama = i
            elif tramas[0][i-2:i] == "7D":
                tramas[0]
            i += 2
        else:
            i += 2
            
    if inicio_trama is not None:
        tramas_totales.append(tramas[0][inicio_trama:])
    return tramas_totales

def print_listas(arr):
    for i in range(0,len(arr)):
        print(i, arr[i])
    return

def longitud(arr):
    correcto=0
    incorrecto=0

    for i in range (0, len(arr)):
        current= arr[i]
        hex= current[2:6]
        decimal= int(hex, 16)
        long= (len(arr[i])-8)//2
        
        if current.find("7D7E")!=-1:
            long -=1
            
        if decimal==long:
            correcto+=1
        else:
            incorrecto+=1
            print("Trama incorrecta. Número: ", i, " | ", arr[i])
    return "Tramas correctas: ", correcto, "Tramas incorrectas: ", incorrecto

def verificar_secuencia_escape(tramas):
    posicion_7D = 0
    trama_sin_secuencia_escape = ""
    contador_secuencia_escape = 0
    for i in range(len(tramas)):
        trama = tramas[i]
        if "7D7E" in trama:
            contador_secuencia_escape += 1
            posicion_7D = tramas[i].find("7D")
            trama_sin_secuencia_escape = tramas[i][0:posicion_7D]
            trama_sin_secuencia_escape = trama_sin_secuencia_escape + tramas[i][posicion_7D + 2 : ]
            print("Trama con secuencia de escape. Número: ", i, " | ", trama_sin_secuencia_escape)
    return contador_secuencia_escape

#def checkSum(arr):
    
    

#print_listas(dividir_tramas("Tramas_802-15-4.log"))
#print(longitud(dividir_tramas("Tramas_802-15-4.log")))
print(verificar_secuencia_escape(dividir_tramas("Tramas_802-15-4.log")))
