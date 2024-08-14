from .color import Color
from .styles import STYLES
import re

_STYLES = {}
for k, v in STYLES.items():
    if isinstance(v, dict):
        for _k1, v1 in v.items():
            _STYLES[f'{v1}'] = k
    else:
        _STYLES[f'{v}'] = k


def _load0(info: tuple[str, str, str]):
    if info[-1]:
        return Color(info[-1])
    style = {}
    for v in info[0].split(';'):
        if v in _STYLES:
            style[_STYLES[v]] = int(v)
    return Color(info[1], _style=style)

def _load(text: str):
    reg = r'\033\[(\d+(?:;\d+)*)m(.*?)\033\[0m|([^\033\[\d;]+)'
    groups = re.findall(reg, text)
    if groups:
        if len(groups) == 1:
            return _load0(groups[0])
        children = []
        for group in groups:
            children.append(_load0(group))
        return Color('', _children=children)
    else:
        return Color(text)


def color(content: str | Color):
    if isinstance(content, Color):
        return content
    else:
        return _load(content)
