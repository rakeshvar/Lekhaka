import cairocffi
from .scribe_backend_interface import scribe_text

styles = '', ' Italic', ' Bold', ' Bold Italic'
CHARWD_OF_LINEHT = .55 # A telugu character is \approx 55% of line ht

class Scribe:
    def __init__(self, language, height, vbuffer, hbuffer, nchars_per_sample=None):
        self.language = language
        self.height = height
        self.vbuffer = vbuffer
        self.hbuffer = hbuffer
        self.scalefactor = height/96                           # When rendered at given size, slab height is ~100 px

        self.nchars_per_sample = nchars_per_sample
        self.width = None if nchars_per_sample is None else  self._calculate_width(nchars_per_sample)

    def _calculate_width(self, nchars):
        width = int(nchars * CHARWD_OF_LINEHT * self.height) + 2*self.hbuffer
        return cairocffi.ImageSurface.format_stride_for_width(cairocffi.FORMAT_A8, width)

    def get_sample_chars_width(self, nchars, width):
        fontname, rel_size, styleid = self.language.random_font()
        text_as_list = self.language.get_word(nchars)
        text_as_str = ''.join(text_as_list)
        size = int(rel_size * self.scalefactor)
        font_style = f"{fontname} {styles[styleid]} {size}"
        img = scribe_text(text_as_str, font_style, width, self.height, self.hbuffer, self.vbuffer)
        return img, text_as_str, self.language.get_labels(text_as_list)

    def __call__(self, nchars=None):
        if nchars is None:
            assert self.nchars_per_sample is not None
            return self.get_sample_chars_width(self.nchars_per_sample, self.width)
        else:
            return self.get_sample_chars_width(nchars, self._calculate_width(nchars))

    def __str__(self):
        return f"Scribe:" \
               f"\n\tLanguage = {self.language}" \
               f"\n\tChars per Sample = {self.nchars_per_sample}" \
               f"\n\tHeight = {self.height} Buffer = {self.vbuffer}" \
               f"\n\tWidth = {self.width} Buffer = {self.hbuffer}" \
               f"\n\tScale Factor = {self.scalefactor}"
