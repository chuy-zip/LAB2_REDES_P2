# Laboratorio 2 - Esquemas de detección y corrección - Parte 1

[DESCRIPCIÓN]

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