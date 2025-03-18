from PIL import Image

def extract_lsb(image_path):
    # Abrir imagen
    img = Image.open(image_path)
    pixels = list(img.getdata())  # Extraer los datos de los píxeles
    
    lsb_bits = []  # Lista para almacenar los bits menos significativos
    
    for pixel in pixels:
        # Si la imagen es en escala de grises, pixel será un solo valor (int)
        # Si es RGB, pixel será una tupla (R, G, B)
        # Si es RGBA, será (R, G, B, A)
        if isinstance(pixel, int):
            pixel = (pixel,)  # Convertir a tupla de un solo elemento
        
        for channel in pixel:
            lsb_bits.append(channel & 1)  # Extraer el LSB (bit menos significativo)
    
    return lsb_bits

# Uso de la función
image_path = "./red.png"  # Cambia esto con la ruta de tu imagen
lsb_result = extract_lsb(image_path)

binary_string = ''.join([str(num) for num in lsb_result])

result = ''

for i in range(0,len(binary_string),8):
    result += chr(int(binary_string[i:i+8],2))

print(result)
