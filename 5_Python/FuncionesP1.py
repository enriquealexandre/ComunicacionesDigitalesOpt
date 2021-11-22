#Librerías que son necesarias a priori
import numpy as np                  #Esta permite trabajar fácilmente con arrays y tiene funciones matemáticas 
from collections import Counter     #Esta función viene bien para generar los diccionarios (ver guión de la práctica)

################################################################################
# Dados los datos de entrada al codificador, esta función debe devolver una 
#  variable diccionario (Dict) con pares datos/número.
# El número es simplemente un contador que identifica a cada dato. 
# Ejemplo: 
#   Entrada: 'ababacad' -> Salida: {'a': 0, 'b': 1, 'c': 2, 'd': 3}
# Debe funcionar también si la entrada es una Lista o un array de datos:
#   Entrada: [1,2,1,2,1,3,1,4] -> Salida: {1: 0, 2: 1, 3: 2, 4: 3}
################################################################################
def gen_lzw_dic(datos):
    print("Falta por implementar la función gen_lzw_dict")
    diccionario = 0
    return diccionario

################################################################################
# Función muy parecida a la anterior. 
# Dados los datos de entrada al codificador, esta función debe devolver una 
#  variable diccionario (Dict) con pares datos/probabilidad.
# Ejemplo: 
#   Entrada: 'ababacad' -> Salida: {'a': 0.5, 'b': 0.25, 'c': 0.125, 'd': 0.125}
# Igual que antes, tiene que funcionar también si la entrada es una Lista
#   Entrada: [1,2,1,2,1,3,1,4] -> {1: 0.5, 2: 0.25, 3: 0.125, 4: 0.125}
################################################################################
def gen_huffman_dic(datos) -> dict:
    print("Falta por implementar la función gen_huffman_dic")
    diccionario = 0
    return diccionario

################################################################################
# Función que debe calcular el valor de la entropía dados unos datos de entrada.
# Se puede ayudar de la salida de la función gen_huffman_dic para facilitar los
# cálculos
# Ejemplo: 
#   Entrada: 'ababacad' -> Salida: 1.75
################################################################################
def entropia(datos):
    print("Falta por implementar la función entropia")
    H = 0

################################################################################
# Función que debe calcular el tamaño del mensaje en KB tal cual, sin aplicar 
# ninguna codificación. 
# El número de bits por palabra será 8 para el caso de imágenes y textos y 16
# para archivos de audio.
# Ejemplo: 
#   Entrada: 'Esto es una prueba' -> Salida: 0.017578125
################################################################################
def tamanoOriginal(mensaje, bitsporpalabra):
    print("Falta por implementar la función tamanoOriginal")
    KB = 0
    return KB

################################################################################
# Función que debe calcular el tamaño mínimo que se podría conseguir para un 
# mensaje dado en KB si alcanzásemos una eficiencia máxima.
# Ejemplo: 
#   Entrada: 'Esto es una prueba' -> Salida: 0.00760
################################################################################
def tamanoMinimo(mensaje):
    print("Falta por implementar la función tamanoMinimo")
    KB = 0
    return KB

################################################################################
# Función que debe calcular el tamañoen KB de una secuencia de bits dada, que se 
# pasa como un String.
# Ejemplo: 
#   Entrada: 1024 bits. Generados como x = "".join('0' for i in range(1024))
#   Salida: 0.125
################################################################################
def tamanoCodificado(bits):
    print("Falta por implementar la función tamanoCodificado")
    KB = 0
    return KB