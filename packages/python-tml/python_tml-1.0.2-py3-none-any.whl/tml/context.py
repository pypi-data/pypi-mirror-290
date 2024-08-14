from __future__ import annotations

import sys
from dataclasses import dataclass, field

from tml.tags import attributes, background, foreground, is_attribute, is_background, is_foreground

_dataclass_options = {}
if sys.version_info >= (3, 10):
    _dataclass_options["slots"] = True


_sequence_template = "\033[{}m"
_reset_sequence = "\033[0m"


@dataclass(frozen=True, **_dataclass_options)
class Context:
    foreground: list[int] = field(default_factory=list)
    background: list[int] = field(default_factory=list)
    attributes: list[int] = field(default_factory=list)

    def push(self, tag: str) -> None:
        if is_foreground(tag):
            self.foreground.append(foreground[tag])
        elif is_background(tag):
            self.background.append(background[tag])
        elif is_attribute(tag):
            self.attributes.append(attributes[tag])
        else:
            raise ValueError(f"Unknown tag '{tag}'")

    def pop(self, tag: str) -> None:
        try:
            if is_foreground(tag):
                current = foreground[tag]
                expected = self.foreground.pop()
            elif is_background(tag):
                current = background[tag]
                expected = self.background.pop()
            elif is_attribute(tag):
                current = attributes[tag]
                expected = self.attributes.pop()
            else:
                raise ValueError(f"Unknown tag '{tag}'")
        except IndexError:
            expected = None

        if expected != current:
            raise ValueError(f"Unmatched closing tag '{tag}'")

    def apply(self, text: str) -> str:
        tokens = []

        if self.foreground:
            tokens.append(_sequence_template.format(self.foreground[-1]))

        if self.background:
            tokens.append(_sequence_template.format(self.background[-1]))

        for attribute in self.attributes:
            tokens.append(_sequence_template.format(attribute))

        tokens.append(text)
        tokens.append(_reset_sequence)

        return "".join(tokens)
