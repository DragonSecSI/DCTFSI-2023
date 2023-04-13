import random
import io

new = io.BytesIO()

strin = "RENURntmMW5EXzdoM19kMUZmM3IzTkNlNX0K"
strIndex = 0

with open("about-us.jpeg", "rb") as f:
    old = f.read()

for i in range(len(old)):
    if i < 200 or strIndex >= len(strin): 
        #skip header/beginning and if entire string already masked
        new.write(old[i:i+1])
        continue
    r = random.random()
    if chr(old[i]) == strin[strIndex] and r < 0.05:
        #random to spread out the mask through the file
        new.write(b'!') #could use any garbage here
        strIndex += 1
    else:
        new.write(old[i:i+1])

with open("./glitched.jpeg", "wb") as f2:
    f2.write(new.getvalue())

