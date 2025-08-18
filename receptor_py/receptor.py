# receptor_py/receptor.py
import socket
import threading
from checksum import checksum
from hamming import hamming
from viterbi import viterbi
from time import time
import matplotlib.pyplot

STATS = {
    "hamming": {
        "tiempo": 0,
        "exitos": 0,
        "fallos": 0
    },
    "viterbi": {
        "tiempo": 0,
        "exitos": 0,
        "fallos": 0
    },
    "checksum": {
        "tiempo": 0,
        "exitos": 0,
        "fallos": 0
    }
}

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

    algoritmo, datos, probabilidad = trama.split('|', 2)

    if algoritmo == "hamming":
        start_time = time()
        resultado = hamming(datos)
        STATS["hamming"]["tiempo"] += time() - start_time
        return resultado, algoritmo, probabilidad

    elif algoritmo == "viterbi":
        start_time = time()
        resultado = viterbi(datos)
        STATS["viterbi"]["tiempo"] += time() - start_time
        return resultado, algoritmo, probabilidad
    
    elif algoritmo == "checksum":
        start_time = time()
        resultado = checksum(datos)
        STATS["checksum"]["tiempo"] += (time() - start_time)
        return resultado, algoritmo, probabilidad

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
def mostrar_mensaje(resultado, algoritmo):
    try:
        if resultado.startswith("error|"):
            print(f"\n[!] Error: {resultado.split('|')[1]} {algoritmo}")
            STATS[algoritmo]["fallos"] += 1

        else:
            algoritmo = resultado.split('|')[0]
            final = resultado.split('|')[1]
            STATS[algoritmo]["exitos"] += 1

            print(f"\nMensaje procesado con {algoritmo}, se ha recibido: {final}")
            
    except Exception as e:
        print(f"\n[!] Error al mostrar el mensaje: {e}")
        STATS["hamming"]["fallos"] += 1 # Debido al ruido, el nombre del algoritmo se corrompe, pero solo sucede con este

# Pruebas y gráficas
def recopilar_stats(probabilidad):
    # Gráfica 1: Tiempo promedio por algoritmo
    fig2, ax2 = matplotlib.pyplot.subplots(figsize=(8, 6))
    algoritmos = []
    tiempos_promedio = []
    for algoritmo, datos in STATS.items():
        total = datos["exitos"] + datos["fallos"]
        if total > 0:
            promedio = datos["tiempo"] / total
            algoritmos.append(algoritmo)
            tiempos_promedio.append(promedio)
    ax2.bar(algoritmos, tiempos_promedio, color="blue")
    ax2.set_title("Tiempo promedio de procesamiento por algoritmo")
    ax2.set_ylabel("Tiempo (s)")
    fig2.savefig(f"graficas/tiempos_{probabilidad}.png")
    print(f"Gráfico de tiempos guardado en graficas/tiempos_{probabilidad}.png")

    # Gráfica 2: Tasa de error
    fig3, ax3 = matplotlib.pyplot.subplots(figsize=(8, 6))
    algoritmos = []
    tasas_error = []
    for algoritmo, datos in STATS.items():
        total = datos["exitos"] + datos["fallos"]
        if total > 0:
            tasa = (datos["fallos"] / total) * 100
            algoritmos.append(algoritmo)
            tasas_error.append(tasa)
    ax3.bar(algoritmos, tasas_error, color="orange")
    ax3.set_title("Tasa de error por algoritmo")
    ax3.set_ylabel("Error (%)")
    fig3.savefig(f"graficas/error_{probabilidad}.png")
    print(f"Gráfico de error guardado en graficas/error_{probabilidad}.png")

    STATS.clear()  # Limpiar estadísticas para la próxima prueba


# Main
if __name__ == "__main__":
    print("Esperando mensajes...")
    while True:
        trama = recibir_informacion()      # Capa 5

        if trama != "EOT":
            binario, algoritmo, probabilidad = verificar_integridad(trama) # Capa 3
            mensaje = decodificar_mensaje(binario) if not binario.startswith("error") else binario # Capa 2
            mostrar_mensaje(mensaje, algoritmo)            # Capa 1

        elif trama == "EOT":
            recopilar_stats(probabilidad)

        else:
            print("Trama inválida recibida.")