import re
import unicodedata
from html import unescape
from urllib.parse import unquote
import json
import numpy as np

from .primitives import MaterialsEntity

_multi_ws_regex = re.compile(r"\ +")
_gibberish = re.compile(r"[!\"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~]{5,}")
_html_tag_regex = re.compile(
    "<math[^>]*>.*?</math(s)?>|</?.[^>]+>|<div[^>]*>|</div>|<dl[^>]*>|</dl>|<dt[^>]*>|</dt>|"
    "<dd[^>]*>|</dd>|<ul[^>]*>|</ul>|<li[^>]*>|</li>|<ol[^>]*>|</ol>|"
    "<span[^>]*>|</span>||<!--[^!]*-->|"
    "<u>|</u>|<i>|</i>|<b>|</b>|<br ?/>|<tr[^>]*>|</tr>|<td[^>]*>|</td>"
)
SENT_PAT = re.compile(
    r"(^\d{1,4}[、\.．])|(\s\d{1,4}[、\.．])|(\n\d{1,4}[、\.．])|(\\n\d{1,4}[、\.．])"
)


class NumpyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, np.int64) or isinstance(o, np.float64):
            return o.item()
        return super().default(o)


def parse_list_str(s):
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    return [x.strip() for x in s.split(",")]


def unique_count(x):
    return sorted(
        list(zip(*np.unique(x, return_counts=True))), key=lambda x: x[1], reverse=True
    )


def replace_symbol(text):
    conv_dict = {
        ".mu.": "μ",
        ".deg.": "°",
        ".degree.": "°",
        ".omega.": "Ω",
        ".ang.": "Å",
        ".alpha.": "α",
        ".beta.": "β",
        ".delta.": "δ",
        ".pi.": "π",
        ".gamma.": "γ",
        ".eta.": "η",
        ".multidot.": ".",
        ".sub.": "<sub>",
        ".sup.": "<sup>",
        ".ltoreq.": "≤",
        ".gtoreq.": "≥",
        ".noteq.": "≠",
        ".theta.": "θ",
        ".epsilon.": "ε",
        ".sigma.": "σ",
        ".phi.": "φ",
        ".lambda.": "λ",
        ".tau.": "τ",
        ".prime.": "'",
        ".MU.": "μ",
        ".DEG.": "°",
        ".DEGREE.": "°",
        ".OMEGA.": "Ω",
        ".ANG.": "Å",
        ".ALPHA.": "α",
        ".BETA.": "β",
        ".DELTA.": "δ",
        ".PI.": "π",
        ".GAMMA.": "γ",
        ".ETA.": "η",
        ".MULTIDOT.": ".",
        ".SUB.": "<sub>",
        ".SUP.": "<sup>",
        ".LTOREQ.": "≤",
        ".GTOREQ.": "≥",
        ".NOTEQ.": "≠",
        ".THETA.": "θ",
        ".EPSILON.": "ε",
        ".SIGMA.": "σ",
        ".PHI.": "φ",
        ".LAMBDA.": "λ",
        ".TAU.": "τ",
        ".PRIME.": "'",
    }

    for k, v in conv_dict.items():
        text = text.replace(k, v)

    return text


def clean_text(text):
    # normalize unicode
    a = unicodedata.normalize("NFC", text)
    # format text such as '%29 and &lt;'
    b = unescape(unquote(a))
    # # replace math symbols
    c = replace_symbol(b)
    # # remove html tag
    d = _html_tag_regex.sub("", c)
    # # # remove gibberish
    e = _gibberish.sub(" ", d)
    # # # merge multiple whitespaces
    f = _multi_ws_regex.sub(" ", e)
    return f


def split_train_dev_test(
    data, train_ratio=0.9, dev_ratio=0.05, test_ratio=0.05, seed=42
):
    np.random.seed(seed)
    np.random.shuffle(data)
    train_size = int(len(data) * train_ratio)
    dev_size = int(len(data) * dev_ratio)
    train_data = data[:train_size]
    dev_data = data[train_size : train_size + dev_size]
    test_data = data[train_size + dev_size :]
    return train_data, dev_data, test_data


def print_coloured_spans(text, start_offset, end_offset, label):
    entity2colour = {
        MaterialsEntity.ENT: "\033[93m",  # yellow
        MaterialsEntity.PRP: "\033[91m",  # red
        MaterialsEntity.MES: "\033[94m",  # blue
        MaterialsEntity.UNT: "\033[92m",  # green
        MaterialsEntity.AUT: "\033[95m",  # magenta
    }
    span_text = text[start_offset:end_offset]
    span_colour = entity2colour.get(label, "\033[0m")
    print("{}{}\033[0m".format(span_colour, span_text), end="")
