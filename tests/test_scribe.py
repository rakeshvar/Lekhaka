from PIL import Image

import sys
sys.path.append("..")
from Lekhaka import Scribe
import telugu as language
from utils import slab_print_255

scriber = Scribe(language, 32, 5, 5, 10)
print(scriber)

try:
    while True:
        image, text, indices = scriber()
        slab_print_255(image)
        print("Text: ", text)
        print("Indices", indices)
        print(f"Images \tshape:{image.shape}\tmax:{image.max():.2f} min:{image.min():.2f}")
        print("Press Enter to continue and Ctrl-D to quit.")
        input()
except (KeyboardInterrupt, EOFError):
    im = Image.fromarray(255 - image)
    im.show()
