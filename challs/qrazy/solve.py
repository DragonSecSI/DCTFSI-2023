import base64
import cv2
import numpy as np

scale = 300
scanner = cv2.QRCodeDetector()

def scan(img):
    img = np.bitwise_xor(img, ~img[0,0])
    img = cv2.resize(img, (scale * 5, scale * 5), interpolation = cv2.INTER_AREA)
    ret, _, _ = scanner.detectAndDecode(img)
    return ret if ret else ""

img = cv2.imread('qr.png', cv2.IMREAD_GRAYSCALE)
w,h = img.shape
msg = "".join([scan(img[y:y+scale, x:x+scale]) for y in range(0, h, scale) for x in range(0,w,scale)])
print("Decoded message: " + msg)

im_str = msg.split("...")[1].strip()
im_str = bytes(im_str,"UTF-8")

with open("flag_test_out.png", "wb") as fh:
    fh.write(base64.decodebytes(im_str))

img = cv2.imread("flag_test_out.png")
img = cv2.resize(img, (300, 300), interpolation = cv2.INTER_AREA)
ret, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
print(ret)