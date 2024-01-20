"""Package to create printable sheets for print and play games."""
from .measure import A1, A2, A3, A4, A5, LETTER, HALF_LETTER, LEGAL, JUNIOR_LEGAL, TABLOID
from .measure import MINI_USA, MINI_CHIMERA, MINI_EURO, STANDARD_USA, CHIMERA, EURO,  STANDARD, MAGNUM_COPPER
from .measure import MAGNUM_SPACE, SMALL_SQUARE,  SQUARE, MAGNUM_SILVER, MAGNUM_GOLD, TAROT
from .measure import Coordinates, Point, Size, mm, cm, inch
from .card import Card, CardImage
from .deck import Deck
from .sheet import Sheet
from .output import sheet_output, sheet_pdf_output
from .filters import MultipleFilter, StraightenFilter, InpaintFilter, CropFilter
from .processing import inpaint, straighten, crop
from .template import Template, svg_file_to_image, svg_content_to_image
from .definition import Definition, DefinitionError


__version__ = "v0.1.0b3"


__all__ = [
    A1, A2, A3, A4, A5, LETTER, HALF_LETTER, LEGAL, JUNIOR_LEGAL, TABLOID,
    MINI_USA, MINI_CHIMERA, MINI_EURO, STANDARD_USA, CHIMERA, EURO,  STANDARD, MAGNUM_COPPER,
    MAGNUM_SPACE, SMALL_SQUARE,  SQUARE, MAGNUM_SILVER, MAGNUM_GOLD, TAROT,
    Coordinates, Point, Size, mm, cm, inch,
    Card, CardImage,
    Deck,
    Sheet,
    sheet_output, sheet_pdf_output,
    MultipleFilter, StraightenFilter, InpaintFilter, CropFilter,
    inpaint, straighten, crop,
    Template, svg_file_to_image, svg_content_to_image,
    Definition, DefinitionError
]
