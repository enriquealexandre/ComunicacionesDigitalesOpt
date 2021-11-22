#############################################
# PRÁCTICA 1a
# Codificación fuente con un fichero de texto 
#############################################

######################
# LIBRERÍAS NECESARIAS
######################
import CodFuente
import FuncionesP1

###############
# CONFIGURACIÓN
###############
# Código fuente que vamos a utilizar: "none, "huffman" o "lzw" 
codigo_fuente = "lzw"
# Fichero que de entrada al sistema
fichero_entrada = "entrada.txt"  
# Fichero que de salida al sistema
fichero_salida = "salida.txt"  

###############
# PASOS PREVIOS
###############
# Leemos el mensaje de texto que vamos a transmitir
fichero = open(fichero_entrada, "r")
mensaje = fichero.read()

# Número de bits necesarios para transmitir el mensaje tal cual, sin codificar (asumo 8 bits por carácter)
KB = FuncionesP1.tamanoOriginal(mensaje, 8)
print("Tamaño del archivo: %.2f" % KB, "KBytes")

# Número mínimo de bits teórico que se necesitaría para transmitir el mensaje en condiciones óptimas:
KB = FuncionesP1.tamanoMinimo(mensaje)
print("Tamaño mínimo teórico: %.2f" % KB, "KBytes")

#####################
# CODIFICACIÓN FUENTE
#####################
if codigo_fuente == "huffman":
    diccionario_huffman = FuncionesP1.gen_huffman_dic(mensaje)
    bits = CodFuente.huffman_cod(mensaje, diccionario_huffman)
elif codigo_fuente == "lzw":
    diccionario_lzw = FuncionesP1.gen_lzw_dic(mensaje)
    bits, bitspormuestralzw = CodFuente.lzw_cod(mensaje, diccionario_lzw)
else:   #En cualquier otro caso no utilizo codificación fuente. 
    bits = ''.join(format(ord(i), '08b') for i in mensaje)

KB = FuncionesP1.tamanoCodificado(bits)
print("Tamaño del archivo tras la codificación fuente (", codigo_fuente, "): %.2f" % KB, "KBytes")


#######################
# DECODIFICACIÓN FUENTE
#######################
if codigo_fuente == "huffman":
    salida = CodFuente.huffman_dec(bits, diccionario_huffman)
    salida = "".join(salida)
elif codigo_fuente == "lzw":
    salida = CodFuente.lzw_dec(bits, bitspormuestralzw, diccionario_lzw)
else:   #Si no hay codificación fuente
    salida = ""
    for i in range(0,len(bits),8):
        salida += chr(int(bits[i:i+8],2))


#Grabo la salida en un fichero
f_salida = open(fichero_salida, "w")
f_salida.write(salida)