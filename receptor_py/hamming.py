def hamming(binary_string):
    print(f"hamming con: {binary_string}")
    
    # string a lista de bits 
    bits = list(binary_string)
    n = len(bits)
    
    # clculo de cantidad de bits de pariedad
    r = 0
    while 2**r < n + 1:
        r += 1
    
    # nota importante, este algoritmo detecta errores y funciona mu b ien para 1 error, pero en 2 errores en adelante puede haber comportamiento inesperado
    # calcular el síndrome aka las posiciones erroneas
    syndrome = 0
    for p in range(r):
        pos_paridad = 2**p - 1  # Índice base 0
        
        # Calcular XOR solo de los bits de DATOS en el grupo
        data_xor = 0
        for i in range(n):
            # Saltar el bit de paridad actual
            if i == pos_paridad:
                continue
                
            # Incluir solo si pertenece al grup que ve el bit
            if (i + 1) & (1 << p):
                data_xor ^= int(bits[i])
        
        # Comparar con el bit de paridad recibido
        if data_xor != int(bits[pos_paridad]):
            #print("Error encontrado")
            syndrome += (1 << p)  # Sumar 2^p al síndrome
    
    if syndrome != 0:
        if syndrome - 1 < n:
            #print(f"Error detectado en posición {syndrome}")
            bits[syndrome - 1] = '1' if bits[syndrome - 1] == '0' else '0'
        else:
            #print("Error no corregible ")
            return "error|hamming: multiples errores detectados (no corregibles)" 
    
    # Extraer bits de datos
    data_bits = []
    for i in range(n):
        if (i + 1) & (i) != 0:
            data_bits.append(bits[i])
    
    result = ''.join(data_bits)
    #print(f"Cadena original: {result}")
    return result