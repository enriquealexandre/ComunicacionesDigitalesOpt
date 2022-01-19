#############
# MODULADORES
#############
import numpy as np

####################
####################
# MODULACIÓN 2-ASK #
####################
####################

##########################################################################
# FUNCIÓN:
#   mod_2ASK(bits, h)
# DESCRIPCIÓN:
#   Modulador 2-ASK. Asumimos codificación polar 
# ENTRADA:
#   bits: Trama de bits a modular
#   h: Filtro transmisor
# SALIDA:
#   y: Señal modulada 
##########################################################################
def mod_2ASK(bits, h):
    aux = [int(k) for k in bits]
    aux = [(k*2)-1 for k in aux] #Codificación polar +-1
    y = []
    for i in aux:
        for k in h:
            y.append(i*k)
    return y
    
##########################################################################
# FUNCIÓN:
#   dem_2ASK(senal, h, Ts)
# DESCRIPCIÓN:
#   Demodulador 2-ASK. Asumimos codificación polar 
# ENTRADA:
#   senal: Señal modulada que se desea demodular
#   h: Filtro receptor
#   Ts: Periodo de símbolo (en muestras)
# SALIDA:
#   bits: Trama binaria de salida
##########################################################################
def dem_2ASK(senal, h, Ts):
    y = np.convolve(senal,h)
    y = y[Ts-1::Ts]
    y[y<0] = int(0)
    y[y>0] = int(1)
    y = y.astype(int)
    bits = "".join([str(k) for k in y])
    return bits


####################
####################
# MODULACIÓN 4-ASK #
####################
####################

##########################################################################
# FUNCIÓN:
#   mod_4ASK(bits,h)
# DESCRIPCIÓN:
#   Modulador 4-ASK.  
# ENTRADA:
#   bits: Trama de bits a modular
#   h: Filtro transmisor
# SALIDA:
#   y: Señal modulada 
##########################################################################
def mod_4ASK(bits,h):
    y = []
    A = 1/np.sqrt(5)
    diccionario = { '0':  [-3*A*k for k in h], 
                    '00': [-3*A*k for k in h], 
                    '01': [-A*k for k in h], 
                    '11': [A*k for k in h], 
                    '10': [3*A*k for k in h], 
                    '1':  [3*A*k for k in h]}
    for i in range(0,len(bits),2):
        y.extend(diccionario[bits[i:i+2]])
    return y

##########################################################################
# FUNCIÓN:
#   dem_4ASK(senal, h, Ts)
# DESCRIPCIÓN:
#   Demodulador 4-ASK.  
# ENTRADA:
#   senal: Señal modulada que se desea demodular
#   h: Filtro receptor
#   Ts: Periodo de símbolo (en muestras)
# SALIDA:
#   bits: Trama binaria de salida
##########################################################################
def dem_4ASK(senal, h, Ts):
    umbral = 2/np.sqrt(5)
    y = np.convolve(senal,h)
    y = y[Ts-1::Ts]
    s0 = y <-umbral
    s1 = (y>=-umbral) & (y < 0)
    s2 = (y>=0) & (y<umbral)
    s3 = y>=umbral
    y = y.astype(object)
    y[s0] = "00"
    y[s1] = "01"
    y[s2] = "11"
    y[s3] = "10"
    bits = "".join(y)
    return bits


####################
####################
# MODULACIÓN Q-PSK #
####################
####################

##########################################################################
# FUNCIÓN:
#   mod_QPSK(bits, h, g)
# DESCRIPCIÓN:
#   Modulador Q-PSK.  
# ENTRADA:
#   bits: Trama de bits a modular
#   h: Filtro transmisor 1 
#   g: Filtro transmisor 2
# SALIDA:
#   y: Señal modulada 
##########################################################################
def mod_QPSK(bits, h, g):
    y = []
    A = 1/np.sqrt(2)
    simbolo_x = [A*i for i in h]
    simbolo_y = [A*i for i in g]
    diccionario = { '11': [simbolo_x[i]+simbolo_y[i] for i in range(0,len(simbolo_x))],
                    '01': [-simbolo_x[i]+simbolo_y[i] for i in range(0,len(simbolo_x))],
                    '10': [simbolo_x[i]-simbolo_y[i] for i in range(0,len(simbolo_x))],
                    '1': [simbolo_x[i]-simbolo_y[i] for i in range(0,len(simbolo_x))],
                    '00': [-simbolo_x[i]-simbolo_y[i] for i in range(0,len(simbolo_x))],
                    '0':  [-simbolo_x[i]-simbolo_y[i] for i in range(0,len(simbolo_x))],}
    for i in range(0,len(bits),2):
        y.extend(diccionario[bits[i:i+2]])
    return y

##########################################################################
# FUNCIÓN:
#   dem_QPSK(senal,h,g,Ts)
# DESCRIPCIÓN:
#   Demodulador Q-PSK.  
# ENTRADA:
#   senal: Señal modulada que se desea demodular
#   h: Filtro receptor 1
#   g: Filtro receptor 2
#   Ts: Periodo de símbolo (en muestras)
# SALIDA:
#   bits: Trama binaria de salida
##########################################################################
def dem_QPSK(senal,h,g,Ts):
    y1 = np.convolve(senal,h)
    y2 = np.convolve(senal,g)
    y1 = y1[Ts-1::Ts]
    y1 = ["1" if i>=0 else "0" for i in y1]
    y2 = y2[Ts-1::Ts]
    y2 = ["1" if i>=0 else "0" for i in y2]
    bits = "".join(i + j for i, j in zip(y1, y2))
    return bits

