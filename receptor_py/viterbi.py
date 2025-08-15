# buenas, hay que hacerle unos pocos ajustes, los states creo que tienen que ser dinamicos, porque supongo dependen del largo
# de la cadena de entrada y además el algoritmo creo que debería mostrar el output cuando corrige el error
# a y creo que este si es capaz de corregir mas de 2

# Para que sea compatible con el sistema, se debe de regresar la cadena binaria decodificada
# también si hay un error se regresa una cadena con el formato error|<descripcion de error>
# en checksum y hamming ya esta por si te sirve de referencia

def viterbi(received: str):
    states = ['00', '01', '10', '11']

    def encode_bit(input_bit, state):
        bit0 = int(input_bit)
        bit1 = int(state[0])
        bit2 = int(state[1])
        out1 = bit0 ^ bit1 ^ bit2
        out2 = bit0 ^ bit2
        return f"{out1}{out2}"

    paths = {'00': ("", 0)}

    for i in range(0, len(received), 2):
        r = received[i:i+2]
        new_paths = {}

        for state in states:
            for input_bit in ['0', '1']:
                prev_state = state
                next_state = input_bit + state[0]
                next_state = next_state[:2]
                expected = encode_bit(input_bit, prev_state)
                metric = sum(a != b for a, b in zip(r, expected))

                if prev_state in paths:
                    prev_path, prev_metric = paths[prev_state]
                    total_metric = prev_metric + metric

                    if next_state not in new_paths or new_paths[next_state][1] > total_metric:
                        new_paths[next_state] = (prev_path + input_bit, total_metric)

        paths = new_paths

    best_state = min(paths, key=lambda s: paths[s][1])
    decoded, errors = paths[best_state]

    print("\n--- Resultado Viterbi ---")
    #print("Mensaje decodificado:", decoded)
    if errors == 0:
        print("No se detectaron errores.")
    elif errors == 1:
        print("Se detectó y corrigió 1 error.")
    else:
        print(f"Se detectaron múltiples errores: {errors}. El mensaje puede no ser confiable.")

