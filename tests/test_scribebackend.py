import sys
sys.path.append("..")

from Lekhaka.scribe_pango_backend import scribe_text
from utils.trimmers import trim
from utils import slab_print_255
import telugu as language

if len(sys.argv) < 2:
    print("Usage:\n"
          "{0} text_file"
          "\n or \n"
          "{0} <(echo 'text')".format(sys.argv[0]))
    sys.exit()

corpus_file = sys.argv[1]
with open(corpus_file) as fin:
    print("Opening ", corpus_file)
    txt = fin.read()

for font in sorted(language.font_properties):
    SIZE, GHO, REPHA, PPU, SPACING, BOLD, ABBR = language.font_properties[font]
    font_style = f"{font} {SIZE//2}"
    image = scribe_text(txt, font_style, 50, 200, 5, 5)
    image = trim(image)
    print(f"{ABBR} \tshape:{image.shape}\tMax:{image.max():.0f} Mean:{image.mean():.0f}({image.mean()/image.max():.0%}) Min:{image.min():.0f}")
    slab_print_255(image)
