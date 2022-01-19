########################
# CANALES DE TRANSMISIÓN
########################
import numpy as np

##########################################################################
# FUNCIÓN:
#   canalAWGN(senal_tx,sigma)
# DESCRIPCIÓN:
#   Canal AWGN (Additive White Gaussian Noise)
# ENTRADAS:
#   senal_tx: Lista de floats con la señal de entrada al canal
#   sigma: Desviación típica del ruido (sigma^2 = N0/2)
# SALIDA:
#   senal_rx: Lista de floats con la señal de salida del canal 
##########################################################################
def canalAWGN(senal_tx,sigma):
    senal_tx = np.array(senal_tx)
    rng = np.random.default_rng(12345)  #Fijo la semilla para asegurar la repetibilidad de los resultados
    senal_rx = senal_tx + rng.normal(0,sigma,senal_tx.size)
    return senal_rx
