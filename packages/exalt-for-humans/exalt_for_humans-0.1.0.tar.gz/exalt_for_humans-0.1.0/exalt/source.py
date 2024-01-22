""" Syntax Highlighted Source Images

"""


from pathlib import Path
from typing import Optional


import pyvips

from loguru import logger
from rich.console import Console
from rich.syntax import Syntax


class Source:
    def __init__(
        self,
        path: Path | str,
        begin: int = 0,
        count: int = -1,
        title: str = None,
        line_numbers: bool = False,
        padding: int = 1,
        theme: Optional[str] = None,
    ) -> None:
        """
        path: Path - source code
        begin: int - line number, defaults to 0
        count: int - line number, defaults to end
        title: str - embedded title, defaults to file name
        line_numbers: bool - show line numbers in image
        padding: int - padding around image in columns/rows
        theme: str - color theme applied to syntax highlighting
        """

        self.path: Path = Path(path).resolve()
        self.begin: int = begin
        self.count: int = len(self.text) if count == -1 else count
        self.title: str = title or f"{self.path.name}"
        self.line_numbers: bool = line_numbers
        self.padding: int = padding
        self.theme: str = theme

    @property
    def extent(self) -> slice:
        try:
            return self._extent
        except AttributeError:
            pass
        self._extent = slice(self.begin, self.begin + self.count)
        return self._extent

    @property
    def text(self) -> list[str]:
        try:
            return self._text
        except AttributeError:
            pass
        self._text = self.path.read_text().splitlines()
        return self._text

    @property
    def svg(self) -> str:
        try:
            return self._svg
        except AttributeError:
            pass

        code = "\n".join(self.text[self.extent])

        width = max(len(line) for line in self.text[self.extent])

        logger.debug(f"max {width=}")

        if width % 10:
            width += 10 - (width % 10)

        if self.line_numbers:
            width += 5
            logger.debug(f"line number {width=}")

        lexer = Syntax.guess_lexer(self.path.name, code)

        code = Syntax(
            code,
            lexer=lexer,
            start_line=self.extent.start,
            line_numbers=self.line_numbers,
            padding=self.padding,
            theme=self.theme,
        )

        with open("/dev/null", "w") as devnull:
            with Console(file=devnull, width=width, record=True) as console:
                console.print(code)
                self._svg = console.export_svg(title=self.title)

        return self._svg

    @property
    def image(self) -> pyvips.Image:
        try:
            return self._image
        except AttributeError:
            pass

        self._image = pyvips.Image.svgload_buffer(bytes(self.svg, encoding="utf-8"))
        return self._image

    def save(self, path: Path) -> None:
        """ """

        self.image.write_to_file(path)
