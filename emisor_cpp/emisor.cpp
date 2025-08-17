// emisor_cpp/main.cpp
#include <iostream>
#include <string>
#include <bitset>
#include <vector>
#include <random>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstdlib>
#include <ctime>
#include "checksum.h"
#include "hamming.h"
#include "viterbi.h"

using namespace std; // Más bonito solo poniendo este xdd

// Capa 1: Aplicación
string solicitar_mensaje() {
    string texto, algoritmo;
    cout << "Mensaje a enviar: ";
    getline(cin, texto);
    cout << "Algoritmo (hamming/viterbi/checksum): ";
    getline(cin, algoritmo);
    return algoritmo + "|" + texto;  // Formato: "algoritmo|texto"
}

// Capa 2: Presentación
string codificar_mensaje(const string& texto) {
    string binario;
    for (char c : texto) {
        binario += bitset<8>(c).to_string();
    }
    return binario;
}

// Capa 3: Enlace
string calcular_integridad(const string& binario, const string& algoritmo) {
    if (algoritmo == "hamming") return hamming(binario);
    else if (algoritmo == "viterbi") return viterbi(binario);
    else if (algoritmo == "checksum") return checksum(binario);
    return "";
}

// Capa 4: Ruido (Simulación)
string aplicar_ruido(const string& trama, double probabilidad = 0.01) {
    string trama_ruidosa = trama;
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0.0, 1.0);

    for (int i = 0; i < trama.size(); i++) {
        if (dis(gen) < probabilidad) {
            trama_ruidosa[i] = (trama[i] == '0') ? '1' : '0';
        }
    }
    return trama_ruidosa;
}

// Capa 5: Transmisión
void enviar_informacion(const string& trama) {
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

void hacer_pruebas(int num_pruebas, double error_prob, string algoritmo) {
    srand(time(0));
    
    int longitud[3] = {8, 16, 32};
    
    for (int i = 0; i < num_pruebas; i++) {
        string binario_random = "";

        for (int i = longitud[rand() % 3]; i > 0; i--) {
            binario_random += to_string(rand() % 2);
        }

        string binario = codificar_mensaje(algoritmo + "|" + binario_random);
        string trama = calcular_integridad(binario, algoritmo);
        string trama_ruidosa = aplicar_ruido(trama, 0.0);
        enviar_informacion(algoritmo + '|' + trama_ruidosa);
        cout << "Prueba " << i + 1 << ": Enviando binario: '" << binario_random
             << "' con algoritmo '" << algoritmo << "' y probabilidad de error "
             << error_prob << endl;
        sleep(1);
    }
}


int main() {
        // Flujo del Emisor
    // string datos = solicitar_mensaje();         // Capa 1
    // string binario = codificar_mensaje(datos);  // Capa 2
    // string algoritmo = datos.substr(0, datos.find('|'));
    // string trama = calcular_integridad(binario, algoritmo); // Capa 3
    // // La funcion de ruido recibe como segundo parametro opcional la probabilidad de fallo
    // // osea la probabilidad de que cualquiera de los bits se cambie
    // // con 0 pues, no cambia nada xd
    // string trama_ruidosa = aplicar_ruido(trama, 0.0);           // Capa 4
    // enviar_informacion(algoritmo + '|' + trama_ruidosa);              // Capa 5

    string algoritmos[3] = {"hamming", "viterbi", "checksum"};
    for (const string& alg : algoritmos) {
        hacer_pruebas(10, 0.0, alg);
    }

    return 0;
    
}