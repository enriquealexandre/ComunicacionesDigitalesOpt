#####################################
# PRÁCTICA 1b
# Codificación de un fichero de audio
#####################################

######################
# LIBRERÍAS NECESARIAS
######################
import CodFuente
import FuncionesP1
import scipy.io.wavfile as wav  # Para leer y escribir archivos .wav
import numpy as np              # Librería matemática
import scipy.fftpack            # Para las transformadas del coseno (DCT e IDCT)

###############
# CONFIGURACIÓN
###############
fichero_entrada = "entrada.wav"
fichero_salida_1 = "salida1.wav"
fichero_salida_2 = "salida2.wav"
# Escalón de cuantificación para el dominio temporal
Q_t = 512
# Escalón de cuantificación para el dominio de la frecuencia
Q_f = 64
# Tamaño de cada trama para la transformada DCT
N = 2048

###############
# PASOS PREVIOS
###############
fs, mensaje = wav.read(fichero_entrada)
KB = FuncionesP1.tamanoOriginal(mensaje, 16)
print("Tamaño del archivo sin codificar: %.1f" % KB, "KBytes")

KB = FuncionesP1.tamanoMinimo(mensaje)
print("Tamaño mínimo que podríamos conseguir en teoría: %.1f" % KB, "Kbytes")

##################################################
# PROCEDIMIENTO 1
# Trabajamos directamente en el dominio del tiempo
##################################################
# Cuantificación del mensaje
x_t = np.round(mensaje/Q_t)
# Codificación fuente (Huffman)
diccionario_huffman = FuncionesP1.gen_huffman_dic(x_t)
bits = CodFuente.huffman_cod(x_t, diccionario_huffman)

KB = FuncionesP1.tamanoCodificado(bits)
print("Tamaño del archivo codificado en el tiempo: %.1f" % KB, "Kbytes")

# Decodificación fuente
bits_r = np.array(CodFuente.huffman_dec(bits, diccionario_huffman))
# Cuantificación inversa
x_r = bits_r*Q_t
# Lo convertimos a formato entero 16bits y grabamos el archivo 
y = x_r.astype(np.int16)
wav.write(fichero_salida_1, fs, y)


#######################################
# PROCEDIMIENTO 2
# Trabajamos en el dominio transformado
#######################################
# Antes de nada relleno con ceros para que el tamaño sea múltiplo de N
mensaje = np.append(mensaje, np.zeros(len(mensaje)%N))

# Voy cogiendo tramas de N muestras y calculo la DCT de cada una de ellas
x_t = np.array([])
for i in range(0,len(mensaje),N):
    trama = mensaje[i:i+N]
    trama_dct = scipy.fftpack.dct(trama, norm='ortho')    #Transformada DCT
    trama_dct = np.round(trama_dct/Q_f)       #Cuantificación
    x_t = np.append(x_t, trama_dct)

# Codificación fuente (Huffman)
diccionario_huffman = FuncionesP1.gen_huffman_dic(x_t)
bits = CodFuente.huffman_cod(x_t, diccionario_huffman)

KB = FuncionesP1.tamanoCodificado(bits)
print("Tamaño del archivo codificado en frecuencia: %.1f" % KB, "KBytes")

#Decodificación fuente
bits_r = np.array(CodFuente.huffman_dec(bits, diccionario_huffman))

#Ahora hacemos la transformada inversa. Voy cogiendo cada trama de N muestras y calculo la IDCT
y = np.array([])
for i in range(0, len(bits_r), N):
    trama = bits_r[i:i+N]
    trama = trama*Q_f                       #Cuantificación inversa
    trama_idct = scipy.fftpack.idct(trama, norm='ortho')  #Transformada IDCT
    y = np.append(y, trama_idct)

#Convierto todo a formato entero de 16 bits y grabo el archivo
y = y.astype(np.int16)
wav.write(fichero_salida_2, fs, y)




