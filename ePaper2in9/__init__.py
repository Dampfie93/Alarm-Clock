# modules/ePaper2in9/__init__.py
from .lib.EPD    import EPD
from .lib.writer import Writer
from .fonts import freesans20    as FONT_SMALL
from .fonts import Arial72       as FONT_BIG
from .fonts import Arial72_clock as FONT_CLOCK
from .display import display, epd

__all__ = ['EPD', 'Writer', 'FONT_SMALL', 'FONT_BIG', 'FONT_CLOCK', 'display', 'epd']