from PIL import Image

import sys
sys.path.append("..")
from Lekhaka import Scribe
import telugu as language
from utils import slab_print_255

scriber = Scribe(language, 32, 5, 5, 7)
print(scriber)

try:
    while True:
        image, text, indices = scriber()
        slab_print_255(image)
        print("Text: ", text)
        print("Indices", indices)
        print(f"Shape:{image.shape}\tMax:{image.max():.0f} Mean:{image.mean():.0f}({image.mean() / image.max():.0%}) Min:{image.min():.0f}")

        print("Press Enter to continue and Ctrl-D to quit.")
        input()
except (KeyboardInterrupt, EOFError):
    im = Image.fromarray(255 - image)
    im.show()
