"""A fast, incremental parser for reStructuredText."""
from rst_fast_parse import diagnostics, elements
from rst_fast_parse.parse import nest_sections, parse_string
__version__ = '0.0.14'
__all__ = ('parse_string', 'nest_sections', 'elements', 'diagnostics')