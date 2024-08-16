from __future__ import annotations
from typing import Iterable, Iterator, Literal, Protocol, Sequence
from typing_extensions import TypeAlias
BlockTagName: TypeAlias = Literal['section', 'transition', 'title', 'paragraph', 'blockquote', 'attribution', 'literal_block', 'line_block', 'doctest', 'bullet_list', 'enum_list', 'definition_list', 'field_list', 'option_list', 'list_item', 'link_target', 'footnote', 'citation', 'substitution_def', 'directive', 'comment', 'table_simple', 'table_grid']
_SPACE = ' '

class ElementProtocol(Protocol):

    @property
    def tagname(self) -> BlockTagName:
        """The tag name of the element."""

    @property
    def line_range(self) -> tuple[int, int]:
        """The line range of the element in the source.
        (index-based, starting from 0)
        """

    def children(self) -> Sequence[ElementProtocol]:
        """Return a list of the children of the element."""

    def debug_repr(self, indent: int=0) -> str:
        """Return a debug representation of the element.

        This takes the form of psuedo-XML, with the tag name and line range.
        """

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        """Return all elements that contain the given line."""

class ElementListProtocol(Protocol):
    """A list of elements in the document.

    It is assumed that the elements are in order of appearance in the source,
    and that the line ranges of the elements do not overlap.
    """

    def debug_repr(self, indent: int=0) -> str:
        """Return a debug representation of the list of elements."""

    def __iter__(self) -> Iterator[ElementProtocol]:
        ...

    def __getitem__(self, index: int, /) -> ElementProtocol:
        ...

    def append(self, element: ElementProtocol) -> None:
        ...

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        """Return all elements that contain the given line."""

class BasicElementList(Sequence[ElementProtocol]):

    def __init__(self) -> None:
        self._elements: list[ElementProtocol] = []

    def debug_repr(self, indent: int=0) -> str:
        text = ''
        for element in self._elements:
            text += element.debug_repr(indent) + '\n'
        return text

    def __getitem__(self, index: int, /) -> ElementProtocol:
        return self._elements[index]

    def __len__(self) -> int:
        return len(self._elements)

    def append(self, element: ElementProtocol) -> None:
        self._elements.append(element)

    def extend(self, elements: Iterable[ElementProtocol]) -> None:
        self._elements.extend(elements)

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        """Return all elements that contain the given line, in order of nesting."""
        for element in self._elements:
            if element.line_range[0] <= line <= element.line_range[1]:
                yield element
                yield from element.line_inside(line)
            if element.line_range[1] > line:
                break

class BasicElement:
    """A generic element in the document tree."""
    __slots__ = ('_tagname', '_line_range')

    def __init__(self, tagname: BlockTagName, line_range: tuple[int, int]) -> None:
        """
        :param tagname: The tag name of the element.
        :param line_range: The line range of the element in the source.
            (index-based, starting from 0)
        """
        self._tagname = tagname
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self._tagname!r}, {self._line_range})'

    def debug_repr(self, indent: int=0) -> str:
        return f'{_SPACE * indent}<{self._tagname}> {self._line_range[0]}-{self._line_range[1]}'

    @property
    def tagname(self) -> BlockTagName:
        return self._tagname

    def children(self) -> Sequence[ElementProtocol]:
        return []

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        return iter(())

class BlockQuoteElement:
    __slots__ = ('_line_range', '_children')

    def __init__(self, line_range: tuple[int, int]) -> None:
        self._children: list[ElementProtocol] = []
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

    def debug_repr(self, indent: int=0) -> str:
        text = f'{_SPACE * indent}<{self.tagname}> {self.line_range[0]}-{self.line_range[1]}'
        for child in self._children:
            text += '\n' + child.debug_repr(indent + 2)
        return text

    @property
    def tagname(self) -> BlockTagName:
        return 'blockquote'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        """Return all elements that contain the given line, in order of nesting."""
        for element in self._children:
            if element.line_range[0] <= line <= element.line_range[1]:
                yield element
                yield from element.line_inside(line)
            if element.line_range[1] > line:
                break

class ListItemElement:
    """A generic element in the document tree."""
    __slots__ = ('_line_range', '_children')

    def __init__(self, line_range: tuple[int, int]) -> None:
        """
        :param line_range: The line range of the element in the source.
            (index-based, starting from 0)
        """
        self._line_range = line_range
        self._children: list[ElementProtocol] = []

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

    @property
    def tagname(self) -> BlockTagName:
        return 'list_item'

    def debug_repr(self, indent: int=0) -> str:
        text = f'{_SPACE * indent}<list_item> {self._line_range[0]}-{self._line_range[1]}'
        for child in self._children:
            text += '\n' + child.debug_repr(indent + 2)
        return text

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        """Return all elements that contain the given line."""
        for element in self._children:
            if element.line_range[0] <= line <= element.line_range[1]:
                yield element
                yield from element.line_inside(line)
            if element.line_range[1] > line:
                break

class ListElement:
    """A list element in the document tree."""
    __slots__ = ('_tagname', '_items')

    def __init__(self, tagname: BlockTagName, items: list[ListItemElement]) -> None:
        """
        :param tagname: The tag name of the element.
        :param line_range: The line range of the element in the source.
            (index-based, starting from 0)
        :param items: The list of items in the list.
        """
        self._tagname = tagname
        self._items = items

    def __repr__(self) -> str:
        return f'Element({self._tagname!r}, len={len(self._items)})'

    def debug_repr(self, indent: int=0) -> str:
        text = f'{_SPACE * indent}<{self._tagname}> {self.line_range[0]}-{self.line_range[1]}'
        for item in self._items:
            text += '\n' + item.debug_repr(indent + 2)
        return text

    @property
    def tagname(self) -> BlockTagName:
        return self._tagname

    @property
    def line_range(self) -> tuple[int, int]:
        return (self._items[0].line_range[0], self._items[-1].line_range[1])

    def children(self) -> Sequence[ListItemElement]:
        return self._items

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        """Return all elements that contain the given line."""
        for item in self._items:
            if item.line_range[0] <= line <= item.line_range[1]:
                yield item
                yield from item.line_inside(line)
            if item.line_range[1] > line:
                break

class TransitionElement:
    __slots__ = ('_style', '_line_range')

    def __init__(self, style: str, line_range: tuple[int, int]) -> None:
        self._style = style
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

    def debug_repr(self, indent: int=0) -> str:
        return f'{_SPACE * indent}<{self.tagname}> {self.line_range[0]}-{self.line_range[1]}'

    @property
    def tagname(self) -> BlockTagName:
        return 'transition'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
        return []

    @property
    def style(self) -> str:
        return self._style

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        return iter(())

class AttributionElement:
    __slots__ = ('_line_range',)

    def __init__(self, line_range: tuple[int, int]) -> None:
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

    def debug_repr(self, indent: int=0) -> str:
        return f'{_SPACE * indent}<{self.tagname}> {self.line_range[0]}-{self.line_range[1]}'

    @property
    def tagname(self) -> BlockTagName:
        return 'attribution'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
        return []

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        return iter(())

class SectionTitleElement:
    __slots__ = ('_overline', '_style', '_title', '_line_range')

    def __init__(self, overline: bool, style: str, title: str, line_range: tuple[int, int]) -> None:
        self._overline = overline
        self._style = style
        self._title = title
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._line_range})'

    def debug_repr(self, indent: int=0) -> str:
        return f'{_SPACE * indent}<{self.tagname} style={self.style!r}> {self.line_range[0]}-{self.line_range[1]}'

    @property
    def tagname(self) -> BlockTagName:
        return 'title'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
        return []

    @property
    def style(self) -> str:
        return self._style + '/' + self._style if self._overline else self._style

    @property
    def overline(self) -> bool:
        return self._overline

    @property
    def title(self) -> str:
        return self._title

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        return iter(())

class SectionElement:
    __slots__ = ('_title', '_children')

    def __init__(self, title: SectionTitleElement | None) -> None:
        self._title = title
        self._children: list[ElementProtocol] = []

    def __repr__(self) -> str:
        return f'Element({self.tagname!r})'

    def debug_repr(self, indent: int=0) -> str:
        text = f'{_SPACE * indent}<{self.tagname}> {self.line_range[0]}-{self.line_range[1]}'
        if self._title:
            text += '\n' + self._title.debug_repr(indent + 2)
        for child in self._children:
            text += '\n' + child.debug_repr(indent + 2)
        return text

    @property
    def tagname(self) -> BlockTagName:
        return 'section'

    @property
    def line_range(self) -> tuple[int, int]:
        start = self._title.line_range[0] if self._title else self._children[0].line_range[0] if self._children else 0
        end = self._children[-1].line_range[1] if self._children else self._title.line_range[1] if self._title else 0
        return (start, end)

    @property
    def title(self) -> SectionTitleElement | None:
        return self._title

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

    def extend(self, element: Iterable[ElementProtocol]) -> None:
        self._children.extend(element)

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        """Return all elements that contain the given line, in order of nesting."""
        for element in self._children:
            if element.line_range[0] <= line <= element.line_range[1]:
                yield element
                yield from element.line_inside(line)
            if element.line_range[1] > line:
                break

class LinkTargetElement:
    __slots__ = ('_name', '_norm_name', '_target', '_target_indirect', '_line_range')

    def __init__(self, name: str, normed_name: str, target: str, target_indirect: bool, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._target = target
        self._target_indirect = target_indirect
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

    def debug_repr(self, indent: int=0) -> str:
        name = ''
        if self._norm_name:
            name = f' name={self._norm_name!r}'
        target = ''
        if self._target:
            if self._target_indirect:
                target = f' refname={self._target!r}'
            else:
                target = f' refuri={self._target!r}'
        return f'{_SPACE * indent}<{self.tagname}{name}{target}> {self.line_range[0]}-{self.line_range[1]}'

    @property
    def tagname(self) -> BlockTagName:
        return 'link_target'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
        return []

    @property
    def name(self) -> str:
        """The raw name of the target."""
        return self._name

    @property
    def normed_name(self) -> str:
        """The normalised name of the target."""
        return self._norm_name

    @property
    def target(self) -> tuple[bool, str]:
        return (self._target_indirect, self._target)

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        return iter(())

class CitationElement:
    __slots__ = ('_name', '_norm_name', '_line_range', '_children')

    def __init__(self, name: str, normed_name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._children: list[ElementProtocol] = []
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

    def debug_repr(self, indent: int=0) -> str:
        text = f'{_SPACE * indent}<{self.tagname} name={self._norm_name!r}> {self.line_range[0]}-{self.line_range[1]}'
        for child in self._children:
            text += '\n' + child.debug_repr(indent + 2)
        return text

    @property
    def tagname(self) -> BlockTagName:
        return 'citation'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    @property
    def name(self) -> str:
        """The raw name of the target."""
        return self._name

    @property
    def normed_name(self) -> str:
        """The normalised name of the target."""
        return self._norm_name

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        """Return all elements that contain the given line, in order of nesting."""
        for element in self._children:
            if element.line_range[0] <= line <= element.line_range[1]:
                yield element
                yield from element.line_inside(line)
            if element.line_range[1] > line:
                break

class FootnoteElement:
    __slots__ = ('_name', '_norm_name', '_line_range', '_children')

    def __init__(self, name: str, normed_name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._children: list[ElementProtocol] = []
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

    def debug_repr(self, indent: int=0) -> str:
        text = f'{_SPACE * indent}<{self.tagname} name={self._norm_name!r}> {self.line_range[0]}-{self.line_range[1]}'
        for child in self._children:
            text += '\n' + child.debug_repr(indent + 2)
        return text

    @property
    def tagname(self) -> BlockTagName:
        return 'footnote'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    @property
    def name(self) -> str:
        """The raw name of the target."""
        return self._name

    @property
    def normed_name(self) -> str:
        """The normalised name of the target."""
        return self._norm_name

    def children(self) -> Sequence[ElementProtocol]:
        return self._children

    def append(self, element: ElementProtocol) -> None:
        self._children.append(element)

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        """Return all elements that contain the given line, in order of nesting."""
        for element in self._children:
            if element.line_range[0] <= line <= element.line_range[1]:
                yield element
                yield from element.line_inside(line)
            if element.line_range[1] > line:
                break

class SubstitutionDefElement:
    __slots__ = ('_name', '_norm_name', '_line_range')

    def __init__(self, name: str, normed_name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._norm_name = normed_name
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._norm_name!r}, {self._line_range})'

    def debug_repr(self, indent: int=0) -> str:
        return f'{_SPACE * indent}<{self.tagname} name={self._norm_name!r}> {self.line_range[0]}-{self.line_range[1]}'

    @property
    def tagname(self) -> BlockTagName:
        return 'substitution_def'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
        return []

    @property
    def name(self) -> str:
        """The raw name of the target."""
        return self._name

    @property
    def normed_name(self) -> str:
        """The normalised name of the target."""
        return self._norm_name

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        return iter(())

class DirectiveElement:
    __slots__ = ('_name', '_line_range')

    def __init__(self, name: str, line_range: tuple[int, int]) -> None:
        self._name = name
        self._line_range = line_range

    def __repr__(self) -> str:
        return f'Element({self.tagname!r}, {self._name!r}, {self._line_range})'

    def debug_repr(self, indent: int=0) -> str:
        return f'{_SPACE * indent}<{self.tagname} name={self.name!r}> {self.line_range[0]}-{self.line_range[1]}'

    @property
    def tagname(self) -> BlockTagName:
        return 'directive'

    @property
    def line_range(self) -> tuple[int, int]:
        return self._line_range

    def children(self) -> Sequence[ElementProtocol]:
        return []

    @property
    def name(self) -> str:
        return self._name

    def line_inside(self, line: int) -> Iterable[ElementProtocol]:
        return iter(())