import hashlib

RAINBOW_TABLE = {}

# def insert_salt_and_hash(word, salt):
#     """Inserta la sal en medio de la palabra y calcula el hash SHA-256."""
#     salted_word = word + salt  # Insertar la sal en el medio
#     hash_value = hashlib.sha256(salted_word).hexdigest()
#     return hash_value
#
# def process_file(filename):
#     """Lee el archivo línea por línea y prueba todas las sales de 0x00 a 0xFF."""
#     with open(filename, "r", encoding="utf-8") as file:
#         for line in file:
#             word = line.strip().encode()  # Convertir a bytes
#             for salt in range(256):  # 0x00 a 0xFF
#                 salt_byte = bytes([salt])  # Convertir a byte único
#                 hash_value = insert_salt_and_hash(word, salt_byte)
#
#                 print(f"Palabra: {word.decode(errors='ignore')} | Sal: {salt_byte.hex()} | Hash: {hash_value}")

def generate_rainbow_table():

    global RAINBOW_TABLE

    filename = './cheese_list.txt'
    with open(filename,'r') as file:
        for line in file:
            word = line.strip()
            for salt in range(256):
                union = word.lower().encode('utf-8') + bytes([salt])
                hashed = hashlib.sha256(union).hexdigest()
                RAINBOW_TABLE[hashed] = (word,hex(salt))

def main():
    generate_rainbow_table()
    searched_hash = input('Introduce el hash buscado: ')

    print(RAINBOW_TABLE[searched_hash])


if __name__ == '__main__':
    main()
