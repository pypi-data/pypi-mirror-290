import html
import re
from fractions import Fraction
import nh3


def strip_html(text: str) -> str:
    return nh3.clean(text, tags=set())


def mixed_number(fraction: Fraction) -> str:
    whole = fraction.numerator // fraction.denominator
    remainder = fraction.numerator % fraction.denominator
    if whole == 0:
        return f"{fraction.numerator}/{fraction.denominator}"
    elif remainder == 0:
        return str(whole)
    else:
        return f"{whole} {remainder}/{fraction.denominator}"


def normalize_fractions(val):
    # strip out anything that looks like this: ($\d \d/\d)
    val = re.sub(r'\(\$.+\)', '', val)
    normalized = _decimal_to_fraction(_fraction_to_decimal(val))
    normalized = re.sub(r'(\d+)/(\d+)', r'\1⁄\2', normalized)
    return normalized


def collapse_whitespace(val):
    # Replace newlines, zero-width spaces, tabs, non-breaking spaces, and other whitespace characters with a space
    val = re.sub(r'[\n\r\u200B\t\xA0\s]', ' ', val)

    # Replace multiple spaces with a single space
    val = re.sub(r'\s{2,}', ' ', val)

    return val


def parse_time(val):
    if not val or val.isspace():
        return None

    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?', val)

    if not match:
        return None

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0

    return hours * 60 + minutes


def normalize_temperatures(val):
    val = _unicode_fraction_to_ascii(val)
    val = re.sub(r'(\d+) degrees F', lambda x: f"{int(x.group(1))}°F", val)
    val = re.sub(r'(\d+) degrees C', lambda x: f"{int(x.group(1))}°C", val)

    return val


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = normalize_fractions(text)
    text = normalize_temperatures(text)
    text = collapse_whitespace(text)
    text = text.strip()
    return text


def _decimal_to_fraction(val):
    def replace_decimal(match):
        d = match.groups(0)[0]
        f = mixed_number(Fraction(d).limit_denominator(8))
        return f
    result = re.sub(r'([0-9]*\.?[0-9]+)', replace_decimal, val)
    return result


def _fraction_to_decimal(val):
    def replace_fraction(s):
        i, f = s.groups(0)
        f = Fraction(f)
        return str(int(i) + float(f))
    result = re.sub(r'(?:(\d+)[-\s])?(\d+/\d+)', replace_fraction, val)
    return result


def _unicode_fraction_to_ascii(val):
    fractions = {
        "¼": "1/4",
        "⅓": "1/3",
        "½": "1/2",
        "⅖": "2/5",
        "⅗": "3/5",
        "⅘": "4/5",
        "⅙": "1/6",
        "⅐": "1/7",
        "⅛": "1/8",
        "⅑": "1/9",
        "⅒": "1/10",
        "⅚": "5/6",
        "⅜": "3/8",
        "⅝": "5/8",
        "⅞": "7/8",
        "¾": "3/4",
        "⅔": "2/3",
        "⅕": "1/5"
    }

    for unicode_frac, ascii_frac in fractions.items():
        val = val.replace(unicode_frac, ascii_frac)

    return val
