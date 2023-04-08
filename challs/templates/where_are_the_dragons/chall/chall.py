from PIL import Image
import os

def hide_message(image_path, message):
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = img.load()

    binary_message = ''.join(format(ord(i), '08b') for i in message)
    binary_message += '00000000'

    width, height = img.size
    pixel_index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            if pixel_index < len(binary_message):
                r &= 0b11111110
                r |= int(binary_message[pixel_index])
                pixel_index += 1

            pixels[x, y] = (r, g, b)

        if pixel_index >= len(binary_message):
            break

    filename, extension = os.path.splitext(image_path)
    output_path = f"{filename}_h{extension}"
    img.save(output_path)

    return output_path

def extract_message(image_path):
    img = Image.open(image_path)
    pixels = img.load()

    binary_message = ""
    width, height = img.size
    pixel_index = 0

    while True:
        x = pixel_index % width
        y = pixel_index // width
        r, _, _ = pixels[x, y]

        binary_message += str(r & 1)
        pixel_index += 1

        if pixel_index % 8 == 0 and binary_message[-8:] == "00000000":
            break

    message = ""
    for i in range(0, len(binary_message) - 8, 8):
        byte = binary_message[i:i + 8]
        message += chr(int(byte, 2))

    return message

message = "DCTF{n0t_so_3@sy_aft3r_@ll}"
image_path = "./DragonSec_logo.png"

hidden_image_path = hide_message(image_path, message)

extracted_message = extract_message(hidden_image_path)

print(f"Original message: {message}")
print(f"Extracted message: {extracted_message}")
