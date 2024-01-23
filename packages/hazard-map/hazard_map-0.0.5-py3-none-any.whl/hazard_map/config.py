import re

ZERO_PADDING_DIGITS = 2
RENDERING_DPI = 480

NODE_MATCHER = re.compile(r'^(?P<kind>H|CA|CO)-?(?P<number>\d+)$')
MAPPING_MATCHER = re.compile('^\s*[Y]\s*$', re.I)
