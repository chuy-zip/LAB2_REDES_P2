# receptor_py/receptor.py
import socket
import threading
from checksum import checksum
from hamming import hamming
from viterbi import viterbi

# Capa 5: Transmisión
def recibir_informacion():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 8080))
    sock.listen()
    conn, addr = sock.accept()
    trama = conn.recv(1024).decode()
    conn.close()
    return trama

# Capa 4: Ruido 
# No se hace nada aquí el receptor no hace ruido

# Capa 3: Enlace
def verificar_integridad(trama):
    # Separar algoritmo y datos (formato: "hamming|010101...")
    print(f"Mensaje recibido: {trama}")
    if '|' not in trama:
        return "error|Formato inválido"
    
    algoritmo, datos = trama.split('|', 1)
    
    if algoritmo == "hamming":
        return hamming(datos)
    elif algoritmo == "viterbi":
        return viterbi(datos)
    elif algoritmo == "checksum":
        return checksum(datos)
    else:
        return f"error|Algoritmo no soportado: {algoritmo}"

# Capa 2: Presentación
def decodificar_mensaje(binario):
    texto = ""
    for i in range(0, len(binario), 8):
        byte = binario[i:i+8]
        texto += chr(int(byte, 2))
    return texto

# Capa 1: Aplicación
def mostrar_mensaje(resultado):
    if resultado.startswith("error|"):
        print(f"\n[!] Error: {resultado.split('|')[1]}")
    else:
        algoritmo = resultado.split('|')[0]
        final = resultado.split('|')[1]
        
        print(f"\nMensaje procesado con {algoritmo}, se ha recibido: {final}")

# Main
if __name__ == "__main__":
    print("Esperando mensajes...")
    while True:
        trama = recibir_informacion()      # Capa 5
        binario = verificar_integridad(trama) # Capa 3
        mensaje = decodificar_mensaje(binario) if not binario.startswith("error") else binario # Capa 2
        mostrar_mensaje(mensaje)            # Capa 1