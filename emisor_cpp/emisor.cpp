// emisor_cpp/main.cpp
#include <iostream>
#include <string>
#include <bitset>
#include <vector>
#include <random>
#include <arpa/inet.h>
#include <unistd.h>
#include "checksum.h"
#include "hamming.h"
#include "viterbi.h"

// Capa 1: Aplicación
std::string solicitar_mensaje() {
    std::string texto, algoritmo;
    std::cout << "Mensaje a enviar: ";
    std::getline(std::cin, texto);
    std::cout << "Algoritmo (hamming/viterbi/checksum): ";
    std::getline(std::cin, algoritmo);
    return algoritmo + "|" + texto;  // Formato: "algoritmo|texto"
}

// Capa 2: Presentación
std::string codificar_mensaje(const std::string& texto) {
    std::string binario;
    for (char c : texto) {
        binario += std::bitset<8>(c).to_string();
    }
    return binario;
}

// Capa 3: Enlace
std::string calcular_integridad(const std::string& binario, const std::string& algoritmo) {
    if (algoritmo == "hamming") return hamming(binario);
    else if (algoritmo == "viterbi") return viterbi(binario);
    else if (algoritmo == "checksum") return checksum(binario);
    return "";
}

// Capa 4: Ruido (Simulación)
std::string aplicar_ruido(const std::string& trama, double probabilidad = 0.01) {
    std::string trama_ruidosa = trama;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);

    for (int i = 0; i < trama.size(); i++) {
        if (dis(gen) < probabilidad) {
            trama_ruidosa[i] = (trama[i] == '0') ? '1' : '0';
        }
    }
    return trama_ruidosa;
}

// Capa 5: Transmisión
void enviar_informacion(const std::string& trama) {
    // Configurar socket (cliente)
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);

    connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
    send(sock, trama.c_str(), trama.size(), 0);
    close(sock);
}

int main() {
    // Flujo del Emisor
    std::string datos = solicitar_mensaje();         // Capa 1
    std::string binario = codificar_mensaje(datos);  // Capa 2
    std::string algoritmo = datos.substr(0, datos.find('|'));
    std::string trama = calcular_integridad(binario, algoritmo); // Capa 3
    // La funcion de ruido recibe como segundo parametro opcional la probabilidad de fallo
    // osea la probabilidad de que cualquiera de los bits se cambie
    // con 0 pues, no cambia nada xd
    std::string trama_ruidosa = aplicar_ruido(trama, 0.0);           // Capa 4
    enviar_informacion(algoritmo + '|' + trama_ruidosa);              // Capa 5
    return 0;
}