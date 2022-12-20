function y = jpegDec(imagenJPEG)
%function y = jpegDec(imagenJPEG)
%
% Función de ejemplo para estudiar la aplicación de la codificación Huffman
%a la codificación JPEG de imágenes. 
%
% Entrada:
%  - imagenJPG: imagen codificada en JPEG, tal cual sale de la función jpegCod 
%
% Salida:
%  - y: La imagen reconstruida.
%
% Requiere tener instalada la Toolbox de Image Processing


%Matriz de cuantificación (es la misma que en el codificador
Q = [ 16 11 10 16 24 40 51 61;
     12 12 14 19 26 58 60 55;
     14 13 16 24 40 57 69 56;
     14 17 22 29 51 87 80 62; 
     18 22 37 56 68 109 103 77;
     24 35 55 64 81 104 113 92;
     49 64 78 87 103 121 120 101;
     72 92 95 98 112 100 103 99];

%Decuantifico cada bloque utilizando la matriz de cuantificación
imagenIQ = blockproc(imagenJPEG, [8 8], @(block_struct) (block_struct.data.*Q));

%Hago la IDCT de la imagen en bloques de 8x8
y = blockproc(imagenIQ, [8 8], @(block_struct) idct2(block_struct.data));
%Por compatibilidad, vuelvo al formato uint8. 
y = uint8(y+128);   

%Para ver la imagen, imshow
