#include <string>
#include "hamming.h"
#include <iostream>
#include <vector>
#include <cmath>

std::string hamming(std::string binary_string) {
    std::cout << "hamming recibio: " << binary_string << std::endl;

    int m = binary_string.length();

    // ahora hay que calcular el valor de r, osea cantidad de bits de pariedad

    int r = 0;

    while ( pow(2, r) < m + r + 1){
        r++;
    }
    
    std::cout << "Son necesarios: " << r << " bits de pariedad"<< std::endl;
    int total_bits = m + r;

    // lista para el codigo de hamming
    std::vector<char> hamming_code(total_bits, '0');

    int data_index = 0;
    for (int i = 0; i < total_bits; i++) {
        // Las posiciones de paridad son 2^k (1,2,4,8...) en base 1
        // pero el vector empieza en 0, entoncse son posiciones 0,1,3,7...
        if ((i & (i + 1)) != 0) {  // Si no es potencia de 2 (base 1)
            if (data_index < m) {
                hamming_code[i] = binary_string[data_index++];
            } else {
                hamming_code[i] = '0'; // Padding si es necesario
            }
        }
    }

    for (int p = 0; p < r; p++) {
        int pos_paridad = pow(2, p) - 1; // Convertir a base 0
        int count = 0;
        
        // Verificar todas las posiciones que cubre este bit de paridad
        for (int i = pos_paridad; i < total_bits; i++) {
            if (((i + 1) & (pos_paridad + 1)) == (pos_paridad + 1)) {
                if (hamming_code[i] == '1') {
                    count++;
                }
            }
        }
        
        // Asignar paridad par
        hamming_code[pos_paridad] = (count % 2 == 0) ? '0' : '1';
    }
    
    // Convertir el vector a string
    std::string resultado;

    for (char bit : hamming_code) {
        resultado += bit;
    }
    
    return resultado;

}