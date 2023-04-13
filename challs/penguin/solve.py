from PIL import Image
import numpy as np

ct = open("penguin.png.enc", "rb").read()
arr = np.array(list(ct), dtype=np.uint8)
arr = arr.reshape((4 * 7 * 13, 2459, 4))
img = Image.fromarray(arr)
img.save("flag.png")
