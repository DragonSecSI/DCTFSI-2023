# Glitched image

You are provided a viisbly corrupted image. As per the description, the idea is to think a bit outside of the box and search for the original image outside of the provided files.

The solution (example provided in `sol.py`) is to:
1. Locate and retreive the original image, found directly on the landing page of dragonsec.si
2. Simply byte diff the two files, taking the characters from the original where the two differ
3. The resulting string is the base64 encoded flag