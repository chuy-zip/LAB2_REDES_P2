def checksum(received_message):
    # Separar el mensaje original y el checksum
    original_message = received_message[:-16]
    received_checksum = received_message[-16:]
    
    # Añadir padding con ceros si es necesario para completar bytes
    padded_message = original_message
    while len(padded_message) % 8 != 0:
        padded_message = '0' + padded_message
    
    sum1 = 0
    sum2 = 0
    
    # Procesar cada byte del mensaje
    for i in range(0, len(padded_message), 8):
        byte_str = padded_message[i:i+8]
        byte_value = int(byte_str, 2)
        
        sum1 = (sum1 + byte_value) % 255
        sum2 = (sum2 + sum1) % 255
    
    # Calcular el checksum esperado
    calculated_checksum = (sum2 << 8) | sum1 # << 8 == desplazar 8 bits a la izquierda == multiplicar por 2^8
    calculated_checksum_bits = f"{calculated_checksum:016b}"
    
    # Comparar con el checksum recibido
    if calculated_checksum_bits == received_checksum:
        #print(f"Mensaje original: {original_message}\nNo se detectaron errores.")
        return original_message
    else:
        #print(f"Error en el mensaje.")
        return "error|Checksum inválido, la cadena contiene errores" 