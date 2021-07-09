import sys
sys.path.append("..")

from Lekhaka.scribe_backend_interface import scribe_text
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
    image = scribe_text(txt, font, 50, 200, 5, 5)
    print(ABBR)
    print(f"Images \tshape:{image.shape}\tmax:{image.max():.2f} min:{image.min():.2f}")
    slab_print_255(trim(image))
