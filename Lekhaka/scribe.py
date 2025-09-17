from .scribe_pango_backend import scribe_text

styles = '', ' Italic', ' Bold', ' Bold Italic'
CHARWD_OF_LINEHT = .55 # A telugu character is \approx 55% of line ht

class Scribe:
    def __init__(self, language, height, vbuffer, hbuffer, nchars_per_sample=None):
        self.language = language
        self.height = height
        self.vbuffer = vbuffer
        self.hbuffer = hbuffer
        self.scalefactor = height/96    # When rendered at the given size of the font, the slab height is ~100 px

        self.nchars_per_sample = nchars_per_sample
        self.width = None if nchars_per_sample is None else  self._calculate_width(nchars_per_sample)

    def _calculate_width(self, nchars):
        width = int(nchars * CHARWD_OF_LINEHT * self.height) + 2*self.hbuffer
        width = (((width-1)>>4)+1)<<4
        return width
        return cairocffi.ImageSurface.format_stride_for_width(cairocffi.FORMAT_A8, width)

    def get_sample_chars_width(self, nchars, width):
        # Get a random font
        fontname, rel_size, styleid = self.language.random_font()
        size = int(rel_size * self.scalefactor)
        font_style = f"{fontname} {styles[styleid]} {size}"

        # Get a random text and remove trailing spaces
        text_as_list = self.language.get_word(nchars)
        while text_as_list[-1] in ' \n':
            text_as_list.pop(-1)
        text_as_str = ''.join(text_as_list)
        text_labels = self.language.get_labels(text_as_list)

        # Render to Image
        img = scribe_text(text_as_str, font_style, self.height, width, self.hbuffer, self.vbuffer) # Text = 255

        return img, text_as_str, text_labels

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
