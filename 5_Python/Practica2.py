#######################
# PRÁCTICA 2
# Codificación de canal
#######################

######################
# LIBRERÍAS NECESARIAS
######################
import CodCanal
import FuncionesP1
import FuncionesP2
from Canal import canalAWGN

###############
# CONFIGURACIÓN
###############
fichero_entrada = "entrada.txt"
fichero_salida = "salida.txt"
codigo_canal = "repeticion"    # "none", "repeticion", "paridad" o "hamming"
n = 4       # Número de bits por palabra
k = 3       # Número de bits de información
q = 3       # Número de bits de control para Hamming
N0 = 0.05  # Densidad espectral de potencia de ruido

###############
# PASOS PREVIOS
###############
#Leo el mensaje a transmitir
fichero = open(fichero_entrada, "r")
mensaje = fichero.read()

# Número de bits necesarios para transmitir el mensaje tal cual, sin codificar (asumo 8 bits por carácter)
KB = FuncionesP1.tamanoOriginal(mensaje,8)
print("Tamaño del archivo: %.1f" % KB, "KBytes")

#Convierto el mensaje de texto a formato binario
bits_fuente = ''.join(format(ord(i), '08b') for i in mensaje)

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

KB = FuncionesP1.tamanoCodificado(bits_canal)
print("Tamaño del archivo tras la codificación de canal (", codigo_canal, "): %.1f" % KB, "KBytes")

############
# MODULACIÓN
############
#Hago una modulación sencilla: '0' -> 0 y '1' -> +1
senal_tx = [int(i) for i in bits_canal]

############
# CANAL AWGN
############
sigma = pow(N0/2, 0.5)
senal_rx = canalAWGN(senal_tx, sigma)

##############
# DEMODULACIÓN
##############
#Decisor: <0.5->'0', >=0.5->'1'
bits_rx = "".join(["0" if i<0.5 else "1" for i in senal_rx])

#Cuento el número de bits erróneos recibidos
errores = FuncionesP2.numErrores(bits_canal, bits_rx)
print("Número de bits erroneos recibidos: ", errores)

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

#Ahora cuento los bits erróneos tras la corrección de errores
errores = FuncionesP2.numErrores(bits_fuente, bits_rx_canal)
print("Número de bits erróneos tras la corrección de errores:", errores)

#Convierto los bits recibidos a texto
salida = ""
#Voy cogiendo los bits de 8 en 8 y los paso a carácter
for i in range(0,len(bits_rx_canal),8):
    salida += chr(int(bits_rx_canal[i:i+8],2))

#Grabo la salida en un fichero
f_salida = open(fichero_salida, "w")
f_salida.write(salida)
