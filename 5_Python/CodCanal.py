#######################
# CODIFICACIÓN DE CANAL
#######################
import numpy as np  #Librería matemática


#Codificador de paridad
# Entradas:
#   bits_in: Mensaje binario a codificar (string)
#   n: Número de bits por palabra (n-1 bits de información + 1 de paridad) (Int)
# Salida:
#   bits_out: Mensaje binario con el bit de paridad (string)
def paridad_cod(bits_in,n):
    x = [int(k) for k in bits_in]
    bits_relleno = -len(x)%(n-1)
    x = x + [0]*bits_relleno
    for i in range(0,int(len(x)+len(x)/(n-1)),n):
        aux = x[i:i+n-1]
        if sum(aux)%2 == 0:
            x.insert(i+n-1,0)
        else:
            x.insert(i+n-1,1)
    bits_out = "".join([str(k) for k in x])
    return bits_out

#Decodificador de paridad
# Entradas:
#   bits_in: Mensaje binario de entrada para decodificar (string)
#   n: Número de bits por palabra (n-1 bits de información + 1 de paridad) (Int)
#   detectar: Si es True, marca las palabras con errores con una '2'. En caso contrario lo deja tal cual
# Salida:
#   bits_out: Mensaje binario decodificado. Aquellas palabras en las que hay un error se marcan con '2' si detectar es True.
def paridad_dec(bits_in,n,detectar):
    x = [int(k) for k in bits_in]
    y = []
    for i in range(0,len(x),n):
        if sum(x[i:i+n])%2 != 0:
            if detectar:
                y += [2]*(n-1)
            else:
                y += x[i:i+n-1]
        else:
            y += x[i:i+n-1]
    bits_out = "".join([str(k) for k in y])
    return bits_out

def matrices_hamming(q):
    H = np.empty((q,pow(2,q)),dtype=int)
    for i in range(0,pow(2,q)):
        aux = np.binary_repr(i,q)
        H[:,i] = [int(j) for j in aux]   
    P = np.delete(H, np.argwhere(np.sum(H,0)<=1), axis=1)
    Iq = np.identity(q,dtype=int)
    H = np.concatenate((P,Iq),axis=1)

    Ik = np.identity(P.shape[1],dtype=int)
    PT = np.transpose(P)
    G = np.concatenate((Ik, PT),axis=1)

    return G, H

def hamming_cod(bits_in,q):
    x = np.array(list(bits_in),dtype=int)
    G, H = matrices_hamming(q)
    k,n = G.shape
    bits_relleno = np.mod(-x.size, k)
    bits = np.reshape(np.append(x,np.zeros(bits_relleno, dtype=int)),(-1,k))
    xham = np.mod(np.matmul(bits,G),2)
    xham = np.reshape(xham, (1,-1))
    bits_out = xham.astype('|S1').tostring().decode('utf-8')
    return bits_out

def hamming_dec(bits_in,q):
    x = np.array(list(bits_in),dtype=int)
    G,H = matrices_hamming(q)
    q ,n = H.shape
    bits_relleno = np.mod(-x.size,n)
    x = np.append(x, np.zeros(bits_relleno, dtype=int))
    k=n-q
    entrada = np.reshape(x, (-1,n))
    sindromes = np.mod(np.matmul(entrada,np.transpose(H)),2)
    errores = np.sum(sindromes, axis=1)
    num_errores = np.sum(errores)

    E = np.identity(n,dtype=int)
    E = np.append(E,np.zeros((1,n),dtype=int),axis=0)
    tablasindromes = np.mod(np.matmul(E,np.transpose(H)),2)

    for i in range(0,sindromes.shape[0]):
        posicion = (tablasindromes == sindromes[i,:]).all(axis=1).nonzero()
        entrada[i,:] = np.bitwise_xor(entrada[i,:],E[posicion[0],:])

    mensaje = entrada[:,0:k]
    mensaje = np.reshape(mensaje, (1,-1))
    bits_out = mensaje.astype('|S1').tostring().decode('utf-8')
    return bits_out






