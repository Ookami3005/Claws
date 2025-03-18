#!/usr/bin/env python3

# ------------------
# Chatgpt ft. Ookami
# Hackers Fight Club
# ------------------

import stepic # Virtal env required for installation
from PIL import Image

# Deactivates size warning
Image.MAX_IMAGE_PIXELS = None

img = Image.open("./upz.png")
flag = stepic.decode(img)
print(flag)
