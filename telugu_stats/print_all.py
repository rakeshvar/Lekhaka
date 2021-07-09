import numpy as np
import sys
sys.path.append("..")
import telugu as language
from Lekhaka.scribe_backend_interface import scribe_text

num_styles = 50
line_ht = 120
buffer_wd = 150 * 30
buffer_ht = num_styles * line_ht

teltext = "అఈఊఏఐఔ కాఁకీంకృకేకైకోకౌః  క్ఖాగ్ఘాచ్ఛాజ్ఝా ట్ఠాడ్ఢాత్థాద్దధ్ధన్న ప్ఫాబ్భామ్మా  య్యార్రాల్లావ్వాశ్శాస్సాహ్హాక్షా  ఉత్కృష్ఠైః శార్ఙ్గిఞ్జయ ప్రత్యగ్రైః గతిర్ద్రక్ష్యసి అభిజ్ఞైః స్నిగ్ధై తత్థోచ్చైః పుష్పైః"
i= 0

data = np.zeros(shape=(buffer_ht, buffer_wd), dtype=np.uint8)

print(f"Num\tfont_name\tavg_sz")

for font_name in sorted(language.font_properties):
    [avg_sz, gho, rep, ppu, spc, abbr, has_bold] = language.font_properties[font_name]
    styles = ['', ' Italic']
    if has_bold:
        styles += [' Bold', ' Bold Italic']

    # for style in styles:
    if True:
        font_style = "{} {} {}".format(font_name, "", avg_sz)
        text = f"{i} {teltext}"
        print(f"{i}\t{font_name}\t{avg_sz}")
        slab = scribe_text(text, font_style, buffer_wd, line_ht, 10, 10, 0)
        data[i*line_ht:(i+1)*line_ht, :] = slab
        i += 1

data = 255 - data
from PIL import Image
im = Image.fromarray(data)
im.save("all.tif")
