#include <stdio.h>
#include <string.h>

// Función que verifica si la entrada coincide con una cadena esperada
int check(char *input) {
    size_t input_length;
    int result;
    size_t current_index;
    
    // Cadena esperada (almacenada en variables locales)
    unsigned long long expected_part1 = 0x617b2375f81ea7e1;
    unsigned long long expected_part2 = 0x69df5b5afc9db9;
    unsigned char expected_part3 = 0xd2;
    unsigned long long expected_part4 = 0xf467edf4ed1bfe;
    
    // Variables de control
    int bit_index = 0;
    int char_index = 0;
    unsigned int bit_mask_input;
    unsigned int bit_mask_expected;
    
    // Obtener la longitud de la entrada
    input_length = strlen(input);
    
    // Verificar si la longitud de la entrada es exactamente 27 caracteres
    if (input_length == 27) {
        for (size_t expected_index = 0; expected_index < 23; expected_index++) {
            for (int bit_pos = 0; bit_pos < 8; bit_pos++) {
                if (bit_index == 0) {
                    bit_index = 1;
                }
                
                // Crear máscaras de bits para comparar cada bit de la entrada con la cadena esperada
                bit_mask_input = 1 << (7 - bit_pos);
                bit_mask_expected = 1 << (7 - bit_index);
                
                // Comparar bits de la entrada con la cadena esperada
                if (((input[char_index] & bit_mask_expected) > 0) != 
                    (((char *)(&expected_part1))[expected_index] & bit_mask_input) > 0) {
                    return 1; // La entrada no coincide con la cadena esperada
                }
                
                bit_index++;
                if (bit_index == 8) {
                    bit_index = 0;
                    char_index++;
                }
                
                // Si se ha recorrido toda la entrada, devolver éxito (0)
                if (char_index == input_length) {
                    return 0;
                }
            }
        }
        result = 0;
    } else {
        result = 1; // La longitud no es correcta, por lo que la entrada es inválida
    }
    return result;
}

