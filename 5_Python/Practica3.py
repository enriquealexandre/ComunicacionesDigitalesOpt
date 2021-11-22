##################
# PRÁCTICA 3
# Sistema completo 
##################

######################
# LIBRERÍAS NECESARIAS
######################
import CodFuente
import CodCanal
import Moduladores
from Canal import canalAWGN
import FuncionesP1
import FuncionesP2
import os                           # Para manejar nombres de archivos
import numpy as np                  # Librería matemática
import matplotlib.pyplot as plt     # Para procesar el mapa de colores de la imagen
import matplotlib.image as mpimg    # Para leer y grabar imágenes
import scipy.io.wavfile as wav      # Para leer y escribir archivos .wav

###############
# CONFIGURACIÓN
###############
fichero_entrada = "entrada.bmp"
fichero_salida = "salida"
codigo_fuente = "huffman"      # "none, "huffman" o "lzw" (lzw sólo si es texto)
codigo_canal = "repeticion"    # "none", "repeticion", "paridad" o "hamming"
modulacion = "QPSK"        #"2-ASK", "4-ASK", "QPSK"
n = 4       # Número de bits por palabra
k = 3       # Número de bits de información
q = 3       # Número de bits de control para Hamming
N0 = 0.1  # Densidad espectral de potencia de ruido

ht = [0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0]   #Filtro transmisor 
gt = [0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5]   #Filtro transmisor
hr = [0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5]   #Filtro receptor 1
gr = [0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0]   #Filtro receptor 2

###############
# PASOS PREVIOS
###############
#Leo el mensaje a transmitir
nombre, extension = os.path.splitext(fichero_entrada)
if extension == ".txt":
    fichero = open(fichero_entrada, "r")
    mensaje = fichero.read()
    bitsporpalabra = 8
elif extension == ".wav":
    fs, mensaje = wav.read(fichero_entrada)
    bitsporpalabra = 16
elif extension == ".bmp":
    mensaje = mpimg.imread(fichero_entrada).astype(int)-128
    tamanoX, tamanoY = mensaje.shape
    mensaje = np.reshape(mensaje,-1)
    bitsporpalabra = 8
else:
    print("No conozco este tipo de archivo")
    quit()

# # Número de bits necesarios para transmitir el mensaje tal cual, sin codificar (asumo 8 bits por carácter)
# KB = FuncionesP1.tamanoOriginal(mensaje, bitsporpalabra)
# print("Tamaño del archivo: %.1f" % KB, "Kbytes")

#####################
# CODIFICACIÓN FUENTE
#####################
if codigo_fuente == "huffman":
    diccionario_huffman = FuncionesP1.gen_huffman_dic(mensaje)
    bits_fuente = CodFuente.huffman_cod(mensaje, diccionario_huffman)
elif codigo_fuente == "lzw":
    diccionario_lzw = FuncionesP1.gen_lzw_dic(mensaje)
    codigo_lzw = CodFuente.lzw_cod(mensaje, diccionario_lzw)
    bits_fuente, bitspormuestralzw = CodFuente.lzw2bits(codigo_lzw)
else:   #En cualquier otro caso no utilizo codificación fuente. 
    if extension == ".txt":
        bits_fuente = ''.join(format(ord(i), '08b') for i in mensaje)
    elif extension == ".wav":
        bits_fuente = ''.join([bin(i)[2:].zfill(bitsporpalabra) if i >=0 else bin(pow(2,bitsporpalabra)+i)[2:].zfill(bitsporpalabra) for i in mensaje])    

# KB = FuncionesP1.tamanoCodificado(bits_fuente)
# print("Tamaño del archivo tras la codificación fuente (", codigo_fuente, "): %.1f" % KB, "Kbytes")

#######################
# CODIFICACIÓN DE CANAL
#######################
if codigo_canal == "repeticion":
    bits_canal = FuncionesP2.repeticion_cod(bits_fuente,k)
elif codigo_canal == "paridad":
    bits_canal = CodCanal.paridad_cod(bits_fuente,n)
elif codigo_canal == "hamming":
    bits_canal = CodCanal.hamming_cod(bits_fuente, q)
else:   #En cualquier otro caso no utilizo codificación de canal
    bits_canal = bits_fuente

# KB = FuncionesP1.tamanoCodificado(bits_canal)
# print("Tamaño del archivo tras la codificación de canal (", codigo_canal, "): %.1f" % KB, "Kbytes")

############
# MODULACIÓN
############
if modulacion == "4-ASK":
    senal_tx = Moduladores.mod_4ASK(bits_canal,ht)
elif modulacion == "QPSK":
    senal_tx = Moduladores.mod_QPSK(bits_canal, ht, gt)
else:   #Por defecto utilizo 2-ASK
    senal_tx = Moduladores.mod_2ASK(bits_canal, ht)

######################
# CANAL DE TRANSMISIÓN
######################
sigma = pow(N0/2, 0.5)
senal_rx = canalAWGN(senal_tx, sigma)


##############
# DEMODULACIÓN
##############
if modulacion == "4-ASK":
    bits_rx = Moduladores.dem_4ASK(senal_rx,hr,len(ht))
elif modulacion == "QPSK":
    bits_rx = Moduladores.dem_QPSK(senal_rx, hr, gr, len(ht))
else:   #Por defecto considero una 2-ASK
    bits_rx = Moduladores.dem_2ASK(senal_rx, hr, len(ht))


#########################
# DECODIFICACIÓN DE CANAL
#########################
if codigo_canal == "repeticion":
    bits_rx_canal = FuncionesP2.repeticion_dec(bits_rx,k)
elif codigo_canal == "paridad":
    bits_rx_canal = CodCanal.paridad_dec(bits_rx,n,False)
elif codigo_canal == "hamming":
    bits_rx_canal = CodCanal.hamming_dec(bits_rx, q)
else:
    bits_rx_canal = bits_rx


#######################
# DECODIFICACIÓN FUENTE
#######################
if codigo_fuente == "huffman":
    salida = CodFuente.huffman_dec(bits_rx_canal, diccionario_huffman)
    if fichero_entrada.endswith(".txt"):
        salida = "".join(salida)
elif codigo_fuente == "lzw":
    codigoLZW = CodFuente.bits2lzw(bits_rx_canal, bitspormuestralzw)
    salida = CodFuente.lzw_dec(codigoLZW, diccionario_lzw)
else:
    if extension == ".txt":
        salida = ""
        for i in range(0,len(bits_rx_canal),8):
            salida += chr(int(bits_rx_canal[i:i+8],2))
    elif extension == ".wav":
        salida = []
        for i in range(0,len(bits_rx_canal),16):
            palabra = bits_rx_canal[i:i+16]
            if palabra[0] == '0':
                salida.append(int(palabra,2))
            else:
                aux = ''.join('0' if i=='1' else '1' for i in palabra)
                salida.append(-(int(aux,2)+1))


#Grabo la salida en un fichero
if extension == ".txt":
    f_salida = open(fichero_salida+extension, "w")
    f_salida.write(salida)
elif extension == ".wav":
    salida = np.array(salida, dtype=np.int16)
    wav.write(fichero_salida+extension, fs, salida)
elif extension == ".bmp":
    salida = np.reshape(salida[0:tamanoX*tamanoY],(tamanoX,tamanoY))
    salida += 128
    mpimg.imsave(fichero_salida+extension,salida, cmap=plt.get_cmap('gray'))






