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
            i += 2
        else:
            i += 2
            
    if inicio_trama is not None:
        tramas_totales.append(tramas[0][inicio_trama:-1])
    return tramas_totales

def print_listas(arr):
    for i in range(0,len(arr)):
        print(i, arr[i])
    return

def longitud(arr):
    longitud_correcta = 0
    longitud_incorrecta = 0

    for i in range (0, len(arr)):
        current= arr[i]
        hex= current[2:6]
        decimal= int(hex, 16)
        long= (len(arr[i])-8) // 2
        
        if current.find("7D7E") != -1:
            long -= 1
            
        if decimal == long:
            longitud_correcta += 1
            if "7D7E" in current:
                current = sacar7D(current)
        else:
            longitud_incorrecta += 1
            print("Trama incorrecta. Número: ", i, " | ", arr[i])
    return "Tramas correctas: ", longitud_correcta, "Tramas incorrectas: ", longitud_incorrecta

def verificar_secuencia_escape(tramas):
    trama_sin_secuencia_escape = ""
    contador_secuencia_escape = 0
    for i in range(len(tramas)):
        trama = tramas[i]
        if "7D7E" in trama:
            contador_secuencia_escape += 1
            trama_sin_secuencia_escape = sacar7D(trama)
            print("Trama con secuencia de escape. Número: ", i, " | ", trama_sin_secuencia_escape)
    return contador_secuencia_escape

def sacar7D(trama):
    trama_sin_secuencia_escape = ""
    if "7D7E" in trama:
        posicion_7D = trama.find("7D")
        trama_sin_secuencia_escape = trama[0:posicion_7D]
        trama_sin_secuencia_escape = trama_sin_secuencia_escape + trama[posicion_7D + 2 : ]
    return trama_sin_secuencia_escape

def checkSum(arr):
    checkSum_correcto = 0
    checkSum_incorrecto = 0
    for i in range (0, len(arr)):
        current= arr[i]
        hex= current[2:6]
        decimal= int(hex, 16)
        long= (len(arr[i])-8) // 2
        
        if current.find("7D7E") != -1:
            long -= 1
            
        if decimal == long:
            if "7D7E" in current:
                current = sacar7D(current)
            if checkSumR(current):
                checkSum_correcto += 1
            else:
                checkSum_incorrecto += 1
                print("Trama con checkSum incorrecta. Número: ", i+1, " | ", current)
        
    return "Tramas con checkSum correcto: ", checkSum_correcto, "Tramas con checkSum incorrecto: ", checkSum_incorrecto

def checkSumR(trama):
    total = 0
    for i in range(6, len(trama)-2, 2):
        byte = int(trama[i:i+2], 16)
        total += byte
    byte = int(trama[-2:], 16)
    return ((total + byte) & 0xFF) == 0xFF


tramas= dividir_tramas("Tramas_802-15-4.log")
print("La cantidad total de tramas son: ", len(tramas))
print(longitud(tramas))
print(checkSum(tramas))
print("La cantidad total de tramas con secuencia de escape son: ", verificar_secuencia_escape(tramas))
