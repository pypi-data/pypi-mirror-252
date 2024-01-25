from enum import Enum

import skia

from iceberg import Bounds, Drawable
from iceberg.core.properties import FontStyle


class SimpleText(Drawable):
    """Draw a simple text. This has no line wrapping.

    Args:
        text: The text to draw.
        font_style: The font style to use.
    """

    text: str
    font_style: FontStyle

    def setup(self) -> None:
        self._skia_font = self.font_style.get_skia_font()
        self._skia_paint = self.font_style.get_skia_paint()
        self._height = self._skia_font.getSize()
        self._width = self._skia_font.measureText(self.text, paint=self._skia_paint)
        self._spacing = self._skia_font.getSpacing()

        self._bounds = Bounds(
            left=0,
            top=0,
            right=self._width,
            bottom=self._spacing,
        )

    @property
    def bounds(self) -> Bounds:
        return self._bounds

    def draw(self, canvas: skia.Canvas) -> None:
        canvas.drawString(self.text, 0, self._height, self._skia_font, self._skia_paint)


class Text(Drawable):
    """Main text class with line wrapping.

    Args:
        text: The text to draw.
        font_style: The font style to use.
        align: The alignment of the text.
        width: The width of the text. If not specified, no line wrapping will be done.
        line_spacing: The line spacing of the text.
    """

    class Align(Enum):
        LEFT = 0
        RIGHT = 1
        CENTER = 2

    text: str
    font_style: FontStyle
    align: Align = Align.LEFT
    width: float = None
    line_spacing: float = 0.9

    def __init__(
        self,
        text: str,
        font_style: FontStyle,
        align: Align = Align.LEFT,
        width: float = None,
        line_spacing: float = 0.9,
    ):
        self.init_from_fields(
            text=text,
            font_style=font_style,
            align=align,
            width=width,
            line_spacing=line_spacing,
        )

    def setup(self) -> None:
        self._skia_font = self.font_style.get_skia_font()
        self._skia_paint = self.font_style.get_skia_paint()
        self._line_height = self.font_style.size
        self._spacing = self._skia_font.getSpacing()

        self._space_width = self._skia_font.measureText(" ", paint=self._skia_paint)

        # Wrap the text.
        self._lines = []
        self._width = 0
        self._height = 0

        if self.width is None:
            # No wrapping is needed. Split the text into lines.
            self._lines = self.text.split("\n")
            self._width = max(
                self._skia_font.measureText(line, paint=self._skia_paint)
                for line in self._lines
            )
        else:
            # Wrap the text.
            pre_lines = self.text.split("\n")

            for pre_line in pre_lines:
                words = pre_line.split(" ")
                line = ""
                for word in words:
                    if (
                        self._skia_font.measureText(line + word, paint=self._skia_paint)
                        > self.width
                    ):
                        self._lines.append(line)
                        self._width = max(
                            self._width,
                            self._skia_font.measureText(line, paint=self._skia_paint),
                        )
                        line = word + " "
                    else:
                        line += word + " "
                self._lines.append(line)

            self._width = max(
                self._width,
                self._skia_font.measureText(line, paint=self._skia_paint),
            )

        # Calculate the height of the text using the line spacing.
        # The last line does not need extra spacing.
        # `line_spacing` is the ratio of the line height to the line spacing.
        self._height = (
            self._spacing + (len(self._lines) - 1) * self._spacing * self.line_spacing
        )

    @property
    def bounds(self) -> Bounds:
        return Bounds(
            left=0,
            top=0,
            right=self._width,
            bottom=self._height,
        )

    def draw(self, canvas: skia.Canvas):
        # Draw the text.
        y = self._spacing
        for line in self._lines:
            x = 0
            if self.align == Text.Align.RIGHT:
                x = self._width - self._skia_font.measureText(
                    line, paint=self._skia_paint
                )
            elif self.align == Text.Align.CENTER:
                x = (
                    self._width
                    - self._skia_font.measureText(line, paint=self._skia_paint)
                ) / 2

            canvas.drawString(
                line,
                x,
                y - (self._spacing - self._line_height),
                self._skia_font,
                self._skia_paint,
            )
            y += self._spacing * self.line_spacing
