import numpy as np
import sys
sys.path.append("..")

import telugu
import telugu as language
from Lekhaka.scribe_backend_interface import scribe_text

max_ht, max_wd = 0, 0
buffer_wd, buffer_ht = 1280, 128


def ht_wd(img):
    good_rows = np.where(np.sum(img, axis=1) > 0)[0]
    good_cols = np.where(np.sum(img, axis=0) > 0)[0]
    return good_rows.max()-good_rows.min()+1,  good_cols.max()-good_cols.min()+1


print("font", "style", "size", "aksharas", "labels", "chars", "ht", "wd", sep='\t')


for font_name in sorted(language.font_properties):
    [avg_sz, gho, rep, ppu, spc, abbr, has_bold] = language.font_properties[font_name]
    styles = ['', ' Italic']
    if has_bold:
        styles += [' Bold', ' Bold Italic']

    for style in [""]:
        for size in range(avg_sz - 10, avg_sz + 11, 2):
            for n_aksharas in range(3, 21, 3):
                font_style = "{} {} {}".format(font_name, style, size)
                aksharas = telugu.get_word(n_aksharas)
                text = ''.join(aksharas)
                slab = scribe_text(text, font_style, buffer_wd, buffer_ht, 10, 10, 0)
                labels = language.get_labels(aksharas)
                ht, wd = ht_wd(slab)
                print(font_name, style, size, n_aksharas, len(labels), len(text), ht, wd, sep='\t')

                if max_ht < ht: max_ht = ht
                if max_wd < wd: max_wd = wd

print(max_wd, max_ht)
print(buffer_wd, buffer_ht)

print("font", "style", "size", "ht", "wd", sep='\t')
for font_name in sorted(language.font_properties):
    [avg_sz, gho, rep, ppu, spc, abbr, has_bold] = language.font_properties[font_name]
    styles = ['', ' Italic']
    if has_bold:
        styles += [' Bold', ' Bold Italic']

    for style in styles:
        for size in range(avg_sz - 10, avg_sz + 11, 2):
            font_style = "{} {} {}".format(font_name, style, size)
            slab = scribe_text('అ', font_style, buffer_ht, buffer_ht, 10, 10, 0)
            ht, wd = ht_wd(slab)
            print(font_name, style, size, ht, wd, sep='\t')
