symbols = itos = [
  "\n",   "\u001e",   " ",
  "!",   "#",   "$",   "%",   "&",   "(",   ")",   "*",   "+",   ",",   "-",   ".",   "/",
  "0",   "1",   "2",   "3",   "4",   "5",   "6",   "7",   "8",   "9",
  ":",   ";",   "<",   "=",   ">",   "?",   "@",   "[",   "\\",   "]",   "^",   "_", "{",   "}",   "~",
  "A",
  "।",   "॥",
  "ఁ",   "ం",   "ః",
  "అ",   "ఆ",   "ఇ",   "ఈ",   "ఉ",   "ఊ",   "ఋ",   "ఌ",   "ఎ",   "ఏ",   "ఐ",   "ఒ",   "ఓ",   "ఔ",
  "క",   "ఖ",   "గ",   "ఘ",   "ఙ",
  "చ",   "ఛ",   "జ",   "ఝ",   "ఞ",
  "ట",   "ఠ",   "డ",   "ఢ",   "ణ",
  "త",   "థ",   "ద",   "ధ",   "న",
  "ప",   "ఫ",   "బ",   "భ",   "మ",
  "య",   "ర",   "ఱ",   "ల",   "ళ",   "వ",
  "శ",   "ష",   "స",   "హ",
  "ఽ",
  "ా",   "ి",   "ీ",   "ు",   "ూ",   "ృ",   "ౄ",   "ె",   "ే",   "ై",   "ొ",   "ో",   "ౌ",   "్",
  "ౘ",   "ౙ",
  "ౠ",   "ౡ",
  "ౢ",   "ౣ",
  "౦",   "౧",   "౨",   "౩",   "౪",   "౫",   "౬",   "౭",   "౮",   "౯",
  "‌",   "—",   "‘",   "’",   "“",   "”",
  "₹"
]

eng = ["a", "A", "B", "b", "C", "c", "D", "d", "e", "E", "f", "F", "g", "G", "h", "H", "i", "I", "j", "J", "k", "K", "l", "L", "M", "m", "n", "N", "o", "O", "P", "p", "Q", "q", "R", "r", "S", "s", "t", "T", "U", "u", "v", "V", "w", "W", "X", "x", "Y", "y", "z", "Z",]

stoi = {ch:idx for idx, ch in enumerate(itos)}

def stoi_safe(ch):
    try:
        return stoi[ch]
    except KeyError as e:
        if ch in eng:
            return stoi["A"]
        else:
            raise e

def get_labels(text):
    """
    A basic conversion of unicode telugu text to list of labels (indices)
    Looks each unicode character separately.
    If not found in all_chars, throws error.
    """
    return [stoi_safe(char) for char in text]


def get_chars(labels):
    """
    It converts labels to unicode telugu text.
    It is the inverse of get_labels.
    :param labels: list of labels
    :return: list of int
    """
    return [itos[i] for i in labels]
