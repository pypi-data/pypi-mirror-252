from dataclasses import dataclass
from typing import Optional, Tuple

import svgwrite

from fretboardgtr.base import ConfigIniter
from fretboardgtr.constants import BLACK
from fretboardgtr.elements.base import FretBoardElement


@dataclass
class StringConfig(ConfigIniter):
    """String element configuration."""

    color: str = BLACK
    width: int = 3


class String(FretBoardElement):
    """String elements to be drawn in the final fretboard."""

    def __init__(
        self,
        start_position: Tuple[float, float],
        end_position: Tuple[float, float],
        width: Optional[int] = None,
        config: Optional[StringConfig] = None,
    ):
        self.config = config if config else StringConfig()
        self.start_position = start_position
        self.end_position = end_position
        self.width = width

    def get_svg(self) -> svgwrite.base.BaseElement:
        """Convert the String to a svgwrite object.

        This maps the StringConfig configuration attributes to the svg
        attributes
        """
        if self.width is None:
            self.width = self.config.width

        line = svgwrite.shapes.Line(
            start=self.start_position,
            end=self.end_position,
            stroke=self.config.color,
            stroke_width=self.width,
        )
        return line
