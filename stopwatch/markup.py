import re
from dataclasses import dataclass, field
from typing import List, Optional, get_args

from termcolor import colored
from termcolor._types import Attribute, Color
from typing_extensions import TypeGuard

_color_set = set(get_args(Color))
_attribute_set = set(get_args(Attribute))


@dataclass(frozen=True)
class State:
    tag: Optional[str] = None
    is_closing: Optional[bool] = None
    text: Optional[str] = None


@dataclass
class Style:
    color: Optional[Color] = None
    attributes: List[Attribute] = field(default_factory=list)

    def update(self, tag: str, is_closing: bool = False):
        if self._is_color(tag):
            self.color = tag if not is_closing else None
        elif self._is_attribute(tag):
            if not is_closing:
                self.attributes.append(tag)
            else:
                self.attributes.remove(tag)
        else:
            raise ValueError(f"Invalid tag {tag}")

    @staticmethod
    def _is_color(tag: str) -> TypeGuard[Color]:
        return tag in _color_set

    @staticmethod
    def _is_attribute(tag: str) -> TypeGuard[Attribute]:
        return tag in _attribute_set


def _parse(markup: str):
    position = 0
    for match in re.finditer(r"(\[\[|\]\])|\[(/?)([a-z]+)\]", markup):
        escape, is_closing, tag = match.groups()
        start_position, end_position = match.span()

        yield State(tag=None, is_closing=None, text=markup[position:start_position])

        if escape:
            yield State(tag=None, is_closing=None, text=escape[0])
        else:
            yield State(tag=tag, is_closing=bool(is_closing), text=None)

        position = end_position

    if position < len(markup):
        yield State(tag=None, is_closing=None, text=markup[position:])


def markup(markup: str) -> str:
    output = []

    style = Style()
    for state in _parse(markup):
        if state.text is not None:
            output.append(colored(state.text, color=style.color, attrs=style.attributes))
        elif state.tag is not None:
            assert state.is_closing is not None
            style.update(state.tag, is_closing=state.is_closing)

    return "".join(output)
