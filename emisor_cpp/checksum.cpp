#include <string>
#include <vector>
#include <bitset>
#include "checksum.h"

using namespace std;

string checksum(string binary_string) {
    // Añadir padding con ceros si es necesario para completar bytes
    while (binary_string.length() % 8 != 0) {
        binary_string = "0" + binary_string;
    }

    int sum1 = 0;
    int sum2 = 0;

    // Procesar cada byte el mensaje
    for (size_t i = 0; i < binary_string.length(); i += 8) {
        string byte_str = binary_string.substr(i, 8);
        
        // Convertir el string de 8 bits a un valor numérico
        bitset<8> bits(byte_str);
        unsigned long byte_value = bits.to_ulong();
        
        sum1 = (sum1 + byte_value) % 255;
        sum2 = (sum2 + sum1) % 255;
    }

    // Combinar las dos sumas para formar el checksum de 16 bits
    int checksum_value = (sum2 << 8) | sum1; // << 8 == desplazar 8 bits a la izquierda == multiplicar por 2^8
    
    // Convertir el checksum a string binario de 16 bits y concatenar con la cadena original
    bitset<16> checksum_bits(checksum_value);
    string checksum = checksum_bits.to_string();

    return binary_string + checksum;
}