"""A fast, incremental parser for reStructuredText."""
from rst_fast_parse import diagnostics, elements
from rst_fast_parse.parse import parse_string
__version__ = '0.0.12'
__all__ = ('parse_string', 'elements', 'diagnostics')