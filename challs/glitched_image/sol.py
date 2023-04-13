# source for OG image: https://dragonsec.si/assets/images/about-us.jpg
# participants to retreive the image from the dragonsec website
import base64

image = open("about-us.jpeg", "rb")
contents = image.read()
image.close()

copy = open("glitched.jpeg", "rb")
copyCon = copy.read()
copy.close()

msgStr = ""
for og, mask in zip(contents, copyCon):
    if og != mask:
        msgStr += chr(og)

print(base64.b64decode(msgStr).decode())