file = open("output.txt", "r")
string = file.read()
text = ""
for i in range(0, len(string), 2):
    num = string[i]
    ch = string[i+1]
    text += ch * int(num)

for i in range(0, len(text), 8):
    byte = text[i:i+8]
    byte = byte[::-1]
    #print(byte)
    cc = int(byte, 2)
    print(chr(cc), end="")