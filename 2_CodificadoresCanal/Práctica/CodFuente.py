########################
# CODIFICACIÓN DE FUENTE
########################
import numpy as np  #Librería matemática
import heapq        #Librería para crear pilas (la utilizamos para generar el árbol de Huffman)
from collections import Counter

##########################################################################
# FUNCIÓN:
#   entropia(datos)
# DESCRIPCIÓN:
#   Cálculo de la entropía de una fuente
# ENTRADA:
#   datos: datos de entrada
# SALIDA:
#   H: Valor de la entropía (Float) 
##########################################################################
def entropia(datos):
    probabilidades,codigos = gen_huffman_dic(datos)
    p = list(probabilidades.values())
    H = sum([-k*np.log2(k) for k in p])
    return H


########################
########################
# CODIFICACIÓN HUFFMAN #
########################
########################

##########################################################################
# FUNCIÓN:
#   gen_huffman_dic(datos)
# DESCRIPCIÓN:
#   Genera un diccionario de probabilidades para la codificación Huffmann. 
#   El diccionario de salida incluye pares símbolo/probabilidad
# ENTRADA:
#   datos: Los datos de entrada que se quieren codificar
# SALIDA:
#   diccionario: Diccionario para la codificación, con pares 
#       símbolos/probabilidades 
#   codigo: Diccionario para la codificación, con pares símbolos/código 
#       binario {Dict, String:String}
##########################################################################
def gen_huffman_dic(datos):
    if type(datos) == np.ndarray:
        datos = np.ravel(datos)
    diccionario = dict(Counter(list(datos)))
    N = len(datos)
    for k in diccionario.keys():
        diccionario[k] /= N
    heap = [[p, [caracter, '']] for caracter, p in diccionario.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    codigos = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    codigos = dict(codigos)
    return diccionario, codigos

##########################################################################
# FUNCIÓN:
#   huffman_cod(mensaje,diccionario)
# DESCRIPCIÓN:
#   Realiza la codificación Huffman de un mensaje dado un diccionario. 
# ENTRADAS:
#   mensaje: Mensaje a codificar (string)
#   codigos: Diccionario de pares símbolos/código {Dict string:float}
# SALIDA:
#   bits: Mensaje codificado en binario (string)
##########################################################################
def huffman_cod(mensaje,codigos):
    bits = ""
    for letra in mensaje:
        bits += codigos[letra]
    return bits

##########################################################################
# # FUNCIÓN:
#   huffman_dec(bits, diccionario)
# DESCRIPCIÓN:
#   Realiza la decodificación Huffman dado un mensaje binario y el 
#       diccionario.
# ENTRADAS:
#   bits: Mensaje binario a decodificar 
#   diccionario: Diccionario de pares símbolos/probabilidades 
# SALIDA:
#   salida: Mensaje decodificado 
##########################################################################
def huffman_dec(bits, codigos):
    busca = ""
    salida = []
    codigo_dec = {v: k for k, v in codigos.items()}
    for k in bits:
        busca += k
        if busca in codigo_dec:
            salida.append(codigo_dec[busca])
            busca = ""
    return salida


####################
####################
# CODIFICACIÓN LZW #
####################
####################

##########################################################################
# FUNCIÓN:
#   gen_lzw_dic(datos)
# DESCRIPCIÓN:
#   Genera el diccionario inicial para una codificación LZW
# ENTRADA:
#   datos: Datos a procesar
# SALIDAS:
#   diccionario: Diccionario para la codificación LZW
##########################################################################
def gen_lzw_dic(datos):
    if type(datos) == np.ndarray:
        datos = np.ravel(datos)
    diccionario = dict(Counter(list(datos)))
    n=0
    for k in diccionario.keys():
        diccionario[k] = n
        n+=1
    return diccionario

##########################################################################
# FUNCIÓN:
#   lzw_cod(cadena, diccionario)
# DESCRIPCIÓN:
#   Realiza la codificación LZW (Lempel–Ziv–Welch) de una cadena de texto 
#       dado el diccionario
# ENTRADAS:
#   cadena: Mensaje a codificar (string)
#   diccionario: Diccionario inicial con símbolos/códigos {Dict string:Int}
# SALIDAS:
#   codigobinario: Mensaje codificado [string]
#   bitspormuestra: Número de bits que ocupa cada muestra del código [Int]
#   codigo: Códigos del diccionario correspondientes al mensaje
##########################################################################
def lzw_cod(cadena, diccionario):
    C = cadena[0]
    i=1
    codigo = []
    for k in cadena[1:]:
        busca = C+k
        if busca in diccionario:
            C = busca
        else:
            codigo.append(diccionario[C])
            diccionario[busca] = len(diccionario)
            C = k
        i += 1
    codigo.append(diccionario[C])
    bitspormuestra = int(np.ceil(np.log2(1+max(codigo))))
    codigobinario = ""
    for k in codigo:
        codigobinario += bin(k)[2:].zfill(bitspormuestra)
    return codigobinario, bitspormuestra, codigo

##########################################################################
# FUNCIÓN:
#   lzw_dec(codigo, diccionario)
# DESCRIPCIÓN:
#   Realiza la decodificación LZW (Lempel–Ziv–Welch) dado un código de 
#       entrada y el diccionario.
# ENTRADAS:
#   codigobinario: Código a decodificar [List Int]
#   bitspormuestra: Número de bits que ocupa cada muestra [Int]
#   diccionario: Diccionario de pares símbolos/códigos {Dict char:Int}
# SALIDA:
#   mensaje: Mensaje decodificado (String)
##########################################################################
def lzw_dec(codigobinario, bitspormuestra, diccionario):
    codigo = []
    for i in range(0,len(codigobinario),bitspormuestra):
        palabra = codigobinario[i:i+bitspormuestra]
        codigo.append(int(palabra,2))
    diccionario_dec = {v: k for k, v in diccionario.items()}
    old_code = codigo[0]
    mensaje = diccionario_dec[old_code]
    caracter = old_code    
    for new_code in codigo[1:]:
        if new_code >= len(diccionario_dec):
            cadena = diccionario_dec[old_code]
            cadena += cadena
        else:
            cadena = diccionario_dec[new_code]
        outputString = cadena
        mensaje += outputString
        caracter = outputString[0]
        nueva_entrada = diccionario_dec[old_code] + caracter
        diccionario_dec[len(diccionario_dec)] = nueva_entrada
        old_code = new_code
    return mensaje

