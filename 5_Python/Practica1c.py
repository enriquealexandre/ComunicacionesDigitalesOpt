######################################
# PRÁCTICA 1c
# Codificación de un fichero de imagen
######################################

######################
# LIBRERÍAS NECESARIAS
######################
import CodFuente
import FuncionesP1
import matplotlib.pyplot as plt     # Para procesar el mapa de colores de la imagen
import matplotlib.image as mpimg    # Para leer y grabar imágenes
import scipy.fftpack                # Transformada del coseno n-dimensional (DCT e IDCT)
import numpy as np                  # Librería matemática

###############
# CONFIGURACIÓN
###############
fichero_entrada = "entrada.bmp"
fichero_salida = "salida.bmp"
#Factor de calidad para la codificación. Cuanto mayor sea, peor será el resultado
factor_calidad = 1          

###############
# PASOS PREVIOS
###############
#Leo la imagen de entrada
img = mpimg.imread(fichero_entrada).astype(int)-128

#Esta es la matriz de cuantificación de JPEG. Se aplica a cada bloque de 8x8 píxeles
Q = np.array([  [16, 11, 10, 16, 24, 40, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99]])
#Reescalo la matriz de cuantificación según el factor de calidad
Q = Q*factor_calidad    
KB = FuncionesP1.tamanoOriginal(img,8)
print("Tamaño de la imagen sin codificar: %.1f" % KB, "KBytes")

#Paso 1: Calculo la transformada DCT de cada bloque de 8x8 píxeles
img_DCT = np.zeros(img.shape, dtype=float)
for x in range(0,img.shape[0],8):
    for y in range(0,img.shape[1],8):
        bloque = img[x:x+8,y:y+8]
        bloqueDCT = scipy.fftpack.dctn(bloque,norm='ortho')
        img_DCT[x:x+8,y:y+8] = bloqueDCT

#Paso 2: Cuantifico cada uno de los bloques utilizando la matriz de cuantificación Q
img_Q = np.zeros(img.shape, dtype=float)
for x in range(0,img.shape[0],8):
    for y in range(0,img.shape[1],8):
        bloque = img_DCT[x:x+8,y:y+8]
        bloque_Q = np.round(bloque/Q)
        img_Q[x:x+8,y:y+8] = bloque_Q
img_Q = img_Q.astype(np.int8)

#Paso 3: Codificación fuente de la imagen
diccionario = FuncionesP1.gen_huffman_dic(img_Q)
codigo = CodFuente.huffman(diccionario)
bits = ""
for x in range(0,img.shape[0]):
    for y in range(0,img.shape[1]):
        pixel = img_Q[x,y]
        bits += codigo[pixel]

KB = FuncionesP1.tamanoCodificado(bits)
print("Tamaño de la imagen JPEG: %.1f" % KB, "KBytes")

#Paso 4: Cuantificación inversa
img_IQ = np.zeros(img.shape, dtype=float)
for x in range(0,img.shape[0],8):
    for y in range(0,img.shape[1],8):
        bloque = img_Q[x:x+8,y:y+8]
        bloque_IQ = bloque*Q
        img_IQ[x:x+8,y:y+8] = bloque_IQ

#Paso 5: Transformada inversa de cada bloque
salida = np.zeros(img.shape, dtype=float)
for x in range(0,img.shape[0],8):
    for y in range(0,img.shape[1],8):
        bloque = img_IQ[x:x+8,y:y+8]
        bloqueIDCT = scipy.fftpack.idctn(bloque, norm='ortho')
        salida[x:x+8,y:y+8] = bloqueIDCT

#Convierto todo a entero sin signo de 8 bits y grabo el archivo
salida = 128+salida.astype(np.uint8)
mpimg.imsave(fichero_salida,salida, cmap=plt.get_cmap('gray'))
