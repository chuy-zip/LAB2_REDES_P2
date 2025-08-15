# Laboratorio 2 - Esquemas de detección y corrección - Parte 2

LAB2 poarte 2

## Lenguajes de programación

- Receptor: Python
- Emisor: C++

## Algoritmos

- Códigos de Hamming - Chuy
- Códigos convolucionales - Eunice
- Fletcher Checksum - Dan

#### Comando para compilar todos los cpp's y los .h

Dentro de la carpeta emisor_cpp:

```
g++ emisor.cpp hamming.cpp viterbi.cpp checksum.cpp -o emisor
```

#### Como correr el emisor
```
Usage: ./emisor
```

#### Como correr el receptor

```
Usage: python receptor.py
```

Correr primero el receptor y luego el emisor. El receptor lo que hace es escuchar mensajes constantemente, los cuales debe enviar el emisor. El receptor espera un formato: algoritmo|cadena. Si no se cumple el formato se marca un error. 

El receptor pide un mennsaje (Aplicacion), que en este caso ya no es en binario sino directamente palabras. Y luego del mensaje pide el algoritmo de codificación. Se procesa la cadena y se convierte a binario (Presentacion) para codificarla con el algoritmo seleccionado (Enlace) y luego de codificarla pasa a la siguiente capa (Ruido), para que algunos bits se cambien aleatoriamente. Finalmente el mensaje se envía el mensaje (Transmisión).