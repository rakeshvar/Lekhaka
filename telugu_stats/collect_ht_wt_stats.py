import numpy as np
import sys
sys.path.append("..")

import telugu
import telugu as language
from Lekhaka.scribe_pango_backend import scribe_text

max_ht, max_wd = 0, 0
tot_ht, tot_wd = 128, 1280


def trimmed_ht_wd(img): # H x W
    good_rows = np.where(np.sum(img, axis=1) > 0)[0]  # (H,)
    good_cols = np.where(np.sum(img, axis=0) > 0)[0]  # (W,)
    try:
        ht = good_rows.max() - good_rows.min() + 1
        wd = good_cols.max() - good_cols.min() + 1
        return ht, wd
    except:
        return 0, 0


print("font", "style", "size", "aksharas", "labels", "chars", "ht", "wd", sep='\t')


for font_name in sorted(language.font_properties):
    [avg_sz, gho, rep, ppu, spc, has_bold, abbr] = language.font_properties[font_name]
    styles = ['', ' Italic', ' Bold', ' Bold Italic']

    for style in [""]:
        for size in range(avg_sz - 10, avg_sz + 11, 2):
            for n_aksharas in range(3, 21, 3):
                font_style = "{} {} {}".format(font_name, style, size)
                aksharas = telugu.get_word(n_aksharas)
                text = ''.join(aksharas)
                slab = scribe_text(text, font_style, tot_ht, tot_wd, 10, 10)
                labels = language.get_labels(aksharas)
                ht, wd = trimmed_ht_wd(slab)
                print(font_name, style, size, n_aksharas, len(labels), len(text), ht, wd, sep='\t')

                if max_ht < ht: max_ht = ht
                if max_wd < wd: max_wd = wd

print(f"Maximimum Height:{max_ht} Width:{max_wd}")
print(f"Image Height:{tot_ht}, Width{tot_wd}")

print("font", "style", "size", "ht", "wd", sep='\t')
for font_name in sorted(language.font_properties):
    [avg_sz, gho, rep, ppu, spc, has_bold, abbr] = language.font_properties[font_name]
    styles = ['', ' Italic', ' Bold', ' Bold Italic']

    for style in styles:
        for size in range(avg_sz - 10, avg_sz + 11, 2):
            font_style = "{} {} {}".format(font_name, style, size)
            slab = scribe_text('అ', font_style, tot_ht, tot_ht, 10, 10)
            ht, wd = trimmed_ht_wd(slab)
            print(font_name, style, size, ht, wd, sep='\t')
