import logging
from .config import AbstractConfiguration


class Position:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Size:
    def __init__(self, w, h):
        self._w = w
        self._h = h

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h


class WavePainter:
    """
    WavePainter is a class that allows us to override the drawing logic more easily and by just specifying a new draw function
    to any child class, as well as overriding the svg XML tag template with custom strings,
    without having to change the entire structure of draw code.
    """

    def __init__(self, sample_list: list[float], config: AbstractConfiguration):
        self.sample_list = sample_list
        self.align = config.align
        self.config = config
        self.height = config.height
        self.width = config.step_width
        self.elements = None

    def template(self):
        """
        The default painter's svg template which rounds up the creation of drawing
        """
        return f'<svg baseProfile="tiny" height="100%" preserveAspectRatio="{self.config.preserve_aspect_ratio}" version="1.2" viewBox="0 0 {self.width} {self.height}" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs/>{self.elements}</svg>'

    def draw(self):
        """
        The default painter's draw function. Creates a simple bar waveform, nothing too complicated
        """

        def bottom(sample: float, i: int, c: AbstractConfiguration):
            """
            bottom position bar helper function to calculate size and position
            """
            pos = (i * (c.width), (1 - sample) * c.height)
            size = (c.width - c.gap, sample * c.height)
            return Position(pos[0], pos[1]), Size(size[0], size[1])

        def center(sample: float, i: int, c: AbstractConfiguration):
            """
            center position bar helper function to calculate size and position
            """
            pos = (i * (c.width), (0.5 * c.height) - (0.5 * sample * c.height))
            size = (c.width - c.gap, sample * c.height)
            return Position(pos[0], pos[1]), Size(size[0], size[1])

        def per_sample(s, i, align_callable, config):
            """
            per-sample processor that calls the given callback function based on the alignment and
            outputs an SVG element as string for each sample value
            """
            pos, size = align_callable(s, i, config)
            return f'<rect width="{size.w}" height="{size.w}" x="{pos.x}" y="{pos.y}" rx="{config.rounded}" ry="{config.rounded}" fill="{config.color}" />'

        if self.align == "bottom":
            align_callable = bottom
        elif self.align == "center":
            align_callable = center
        else:
            logging.warn("Missing alignment, using 'center' alignment as default")
            align_callable = center
        self.elements = ""
        for i, s in enumerate(self.sample_list):
            self.elements += per_sample(s, i, align_callable, self.config)
        return self

    def to_string(self):
        """
        To be called to finish the drawing, after draw is finished, to print the loose svg string into a
        conforming svg XML tag.
        Note that both self.template and self.draw can be overriden by child classes, hence they both can deviate
        from the default draw function (and template, respectively), but this function serves as the common basis
        all children to call in order to finish the drawing
        """
        return self.draw().template()
