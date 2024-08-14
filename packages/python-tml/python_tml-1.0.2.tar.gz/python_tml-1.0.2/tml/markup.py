import sys
from typing import IO, Any, Optional

from tml.context import Context
from tml.parser import parse


def markup(text: str) -> str:
    tokens = []

    context = Context()
    for state in parse(text):
        if state.text is not None:
            tokens.append(context.apply(state.text))
        elif state.tag is not None:
            if not state.is_closing:
                context.push(state.tag)
            else:
                context.pop(state.tag)

    return "".join(tokens)


def mprint(
    *values: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[IO[str]] = None,
    flush: bool = False,
) -> None:
    if sep is None:
        sep = " "

    if end is None:
        end = "\n"

    if file is None:
        file = sys.stdout

    text = sep.join(str(value) for value in values)
    text = markup(text)

    print(text, sep=sep, end=end, file=file, flush=flush)
