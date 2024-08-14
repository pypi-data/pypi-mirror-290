from __future__ import annotations
from typing import Iterator, Literal, Protocol
from typing_extensions import TypeAlias
DiagnosticCode: TypeAlias = Literal['blank_line', 'special_char_line', 'paragraph', 'literal_block', 'target', 'table']

class Diagnostic:
    """A diagnostic message."""
    __slots__ = ('_message', '_code', '_line_start')

    def __init__(self, code: DiagnosticCode, message: str, line_start: int, /) -> None:
        """Initialize the diagnostic.

        :param code: The diagnostic code.
        :param message: The diagnostic message.
        :param line_start: The line number where the diagnostic starts (0-based).
        """
        self._message = message
        self._code = code
        self._line_start = line_start

    @property
    def code(self) -> DiagnosticCode:
        """The diagnostic code."""
        return self._code

    @property
    def message(self) -> str:
        """The diagnostic message."""
        return self._message

    @property
    def line_start(self) -> int:
        """The line number where the diagnostic starts."""
        return self._line_start

    def __repr__(self) -> str:
        return f'Diagnostic({self._code!r}, {self._message!r}, {self._line_start!r})'

    def as_dict(self) -> dict[str, str | int]:
        """Return the diagnostic as a dictionary."""
        return {'code': self._code, 'message': self._message, 'line_start': self._line_start}

class DiagnosticList(Protocol):
    """A list of diagnostics."""

    def __iter__(self) -> Iterator[Diagnostic]:
        ...