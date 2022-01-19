#######################
# CODIFICACIÓN DE CANAL
#######################
import numpy as np  #Librería matemática

##########################################################################
# FUNCIÓN:
#   numErrores(entrada, salida)
# DESCRIPCIÓN:
#   Dados los datos de entrada y salida del codificador devuelve el número 
#       de errores encontrados.
# ENTRADAS:
#   entrada: datos de entrada
#   salida: datos de salida
# SALIDA:
#   errores: Número de errores encontrados
##########################################################################
def numErrores(entrada, salida):
    print("¡OJO!  HAY QUE IMPLEMENTAR LA FUNCION numErrores")
    errores = 0
    return errores


#########################
#########################
# CÓDIGOS DE REPETICIÓN #
#########################
#########################

##########################################################################
# FUNCIÓN:
#   repeticion_cod(bits_in,k)
# DESCRIPCIÓN:
#   Dado un vector de bits en formato de String, y el valor del parámetro 
#   k (número de repeticiones), devuelve el mismo vector aplicando un 
#   código de repetición de parámetro k
# ENTRADAS:
#   bits_in: Cadena de bits a codificar
#   k: Número de repeticiones de cada bit
# SALIDA:
#   bits_out: Cadena de bits codificada
##########################################################################    
def repeticion_cod(bits_in,k):
    print("¡OJO!  HAY QUE IMPLEMENTAR LA FUNCION repeticion_cod")
    bits_out = bits_in
    return bits_out

##########################################################################
# FUNCIÓN:
#   repeticion_dec(bits_in,k)
# DESCRIPCIÓN:
#   Realiza la decodificación, incluyendo la corrección de errores, de 
#   una cadena de bits codificada mediante un código de repetición con 
#   parámetro k. 
# ENTRADAS:
#   bits_in: Cadena de bits a decodificar
#   k: Número de repeticiones de cada bit
# SALIDA:
#   bits_out: Cadena de bits decodificada
##########################################################################
def repeticion_dec(bits_in,k):
    print("¡OJO!  HAY QUE IMPLEMENTAR LA FUNCION repeticion_dec")
    bits_out = bits_in
    return bits_out


######################
######################
# CÓDIGOS DE PARIDAD #
######################
######################

##########################################################################
# FUNCIÓN:
#   paridad_cod(bits_in,n)
# DESCRIPCIÓN:
#   Realiza la codifcación por paridad de una cadena de bits
# ENTRADAS:
#   bits_in: Cadena de bits a codificar
#   n: Número de bits por palabra (n-1 bits de información + 1 de paridad)
# SALIDA:
#   bits_out: Cadena de bits codificada
##########################################################################
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

##########################################################################
# FUNCIÓN:
#   paridad_dec(bits_in,n)
# DESCRIPCIÓN:
#   Realiza la decodifcación por paridad de una cadena de bits. 
# ENTRADAS:
#   bits_in: Cadena de bits a decodificar
#   n: Número de bits por palabra (n-1 bits de información + 1 de paridad)
# SALIDAS:
#   erroresDetectados: Número de palabras código en las que se ha 
#       detectado algún error
#   bits_out: Cadena de bits codificada (es la de entrada a la que 
#       únicamente se le quitan los bits de paridad)
##########################################################################
def paridad_dec(bits_in,n):
    x = [int(k) for k in bits_in]
    y = []
    erroresDetectados = 0
    for i in range(0,len(x),n):
        if sum(x[i:i+n])%2 != 0:
            erroresDetectados += 1
        y += x[i:i+n-1]
    bits_out = "".join([str(k) for k in y])    
    return erroresDetectados, bits_out

##########################################################################
# FUNCIÓN:
#   erroresParidad(bits_in, bits_out,n)
# DESCRIPCIÓN:
#   Calcula el número de palabras código con errores para un código de 
#   paridad
# ENTRADAS:
#   bits_in: Cadena de bits original, codificada con un código de paridad
#   bits_out: Cadena de bits recibida
#   n: Número de bits por palabra (n-1 bits de información + 1 de paridad)
# SALIDA:
#   erroresReales: Número de palabras código en las que existe algún error
##########################################################################
def erroresParidad(bits_in, bits_out,n):
    erroresReales = 0
    for i in range(0, len(bits_in), n):
        errores = sum(1 for a, b in zip(bits_in[i:i+n], bits_out[i:i+n]) if a != b)
        if errores > 0:
            erroresReales += 1
    return erroresReales


###################
###################
# CÓDIGOS HAMMING #
###################
###################

##########################################################################
# FUNCIÓN:
#   matrices_hamming(q)
# DESCRIPCIÓN:
#   Genera las matrices Hamming (G y H) para un código con q bits de 
#   control
# ENTRADA:
#   q: Número de bits de control del código Hamming.
# SALIDAS:
#   G: Matriz generadora del código
#   H: Matriz de comprobación de paridad
##########################################################################
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

##########################################################################
# FUNCIÓN:
#   hamming_cod(bits_in,q)
# DESCRIPCIÓN:
#   Realiza la codificación Hamming de una cadena de bits
# ENTRADAS:
#   bits_in: Cadena de bits a codificar
#   q: Número de bits de control del código Hamming.
# SALIDA:
#   bits_out: Cadena de bits codificada
##########################################################################
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

##########################################################################
# FUNCIÓN:
#   hamming_dec(bits_in,q)
# DESCRIPCIÓN:
#   Realiza la decodificación Hamming de una cadena de bits
# ENTRADAS:
#   bits_in: Cadena de bits a decodificar
#   q: Número de bits de control del código Hamming.
# SALIDA:
#   bits_out: Cadena de bits decodificada
##########################################################################
def hamming_dec(bits_in,q):
    x = np.array(list(bits_in),dtype=int)
    G,H = matrices_hamming(q)
    q ,n = H.shape
    bits_relleno = np.mod(-x.size,n)
    x = np.append(x, np.zeros(bits_relleno, dtype=int))
    k=n-q
    entrada = np.reshape(x, (-1,n))
    sindromes = np.mod(np.matmul(entrada,np.transpose(H)),2)
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






