import sys
from typing import (
    Dict,
    List,
    Literal,
    SupportsIndex,
    Tuple,
    TypeVar,
    Union,
    overload,
    Callable,
    Optional,
)

from ._common import Coordinate, RectValue, Sequence

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

if sys.version_info >= (3, 9):
    from collections.abc import Collection, Iterator
else:
    from typing import Collection, Iterator

_N = TypeVar("_N", int, float)
_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")

_RectTypeCompatible_co = TypeVar("_RectTypeCompatible_co", bound=RectValue, covariant=True)

class _GenericRect(Collection[_N]):
    @property
    def x(self) -> _N: ...
    @x.setter
    def x(self, value: float) -> None: ...
    @property
    def y(self) -> _N: ...
    @y.setter
    def y(self, value: float) -> None: ...
    @property
    def top(self) -> _N: ...
    @top.setter
    def top(self, value: float) -> None: ...
    @property
    def left(self) -> _N: ...
    @left.setter
    def left(self, value: float) -> None: ...
    @property
    def bottom(self) -> _N: ...
    @bottom.setter
    def bottom(self, value: float) -> None: ...
    @property
    def right(self) -> _N: ...
    @right.setter
    def right(self, value: float) -> None: ...
    @property
    def topleft(self) -> Tuple[_N, _N]: ...
    @topleft.setter
    def topleft(self, value: Coordinate) -> None: ...
    @property
    def bottomleft(self) -> Tuple[_N, _N]: ...
    @bottomleft.setter
    def bottomleft(self, value: Coordinate) -> None: ...
    @property
    def topright(self) -> Tuple[_N, _N]: ...
    @topright.setter
    def topright(self, value: Coordinate) -> None: ...
    @property
    def bottomright(self) -> Tuple[_N, _N]: ...
    @bottomright.setter
    def bottomright(self, value: Coordinate) -> None: ...
    @property
    def midtop(self) -> Tuple[_N, _N]: ...
    @midtop.setter
    def midtop(self, value: Coordinate) -> None: ...
    @property
    def midleft(self) -> Tuple[_N, _N]: ...
    @midleft.setter
    def midleft(self, value: Coordinate) -> None: ...
    @property
    def midbottom(self) -> Tuple[_N, _N]: ...
    @midbottom.setter
    def midbottom(self, value: Coordinate) -> None: ...
    @property
    def midright(self) -> Tuple[_N, _N]: ...
    @midright.setter
    def midright(self, value: Coordinate) -> None: ...
    @property
    def center(self) -> Tuple[_N, _N]: ...
    @center.setter
    def center(self, value: Coordinate) -> None: ...
    @property
    def centerx(self) -> _N: ...
    @centerx.setter
    def centerx(self, value: float) -> None: ...
    @property
    def centery(self) -> _N: ...
    @centery.setter
    def centery(self, value: float) -> None: ...
    @property
    def size(self) -> Tuple[_N, _N]: ...
    @size.setter
    def size(self, value: Coordinate) -> None: ...
    @property
    def width(self) -> _N: ...
    @width.setter
    def width(self, value: float) -> None: ...
    @property
    def height(self) -> _N: ...
    @height.setter
    def height(self, value: float) -> None: ...
    @property
    def w(self) -> _N: ...
    @w.setter
    def w(self, value: float) -> None: ...
    @property
    def h(self) -> _N: ...
    @h.setter
    def h(self, value: float) -> None: ...
    __hash__: None  # type: ignore
    __safe_for_unpickling__: Literal[True]
    @overload
    def __init__(
        self, left: float, top: float, width: float, height: float
    ) -> None: ...
    @overload
    def __init__(self, left_top: Coordinate, width_height: Coordinate) -> None: ...
    @overload
    def __init__(self, single_arg: RectValue) -> None: ...
    @overload
    def __init__(self) -> None: ...
    def __len__(self) -> Literal[4]: ...
    def __iter__(self) -> Iterator[_N]: ...
    @overload
    def __getitem__(self, i: SupportsIndex) -> _N: ...
    @overload
    def __getitem__(self, s: slice) -> List[_N]: ...
    @overload
    def __setitem__(self, key: int, value: float) -> None: ...
    @overload
    def __setitem__(self, key: slice, value: Union[float, RectValue]) -> None: ...
    def __copy__(self) -> Self: ...
    copy = __copy__
    @overload
    def move(self, x: float, y: float, /) -> Self: ...
    @overload
    def move(self, move_by: Coordinate, /) -> Self: ...
    @overload
    def move_ip(self, x: float, y: float, /) -> None: ...
    @overload
    def move_ip(self, move_by: Coordinate, /) -> None: ...
    def move_to(self, **kwargs: Union[float, Coordinate]) -> Self: ...
    @overload
    def inflate(self, x: float, y: float, /) -> Self: ...
    @overload
    def inflate(self, inflate_by: Coordinate, /) -> Self: ...
    @overload
    def inflate_ip(self, x: float, y: float, /) -> None: ...
    @overload
    def inflate_ip(self, inflate_by: Coordinate, /) -> None: ...
    @overload
    def scale_by(self, x: float, y: float = ...) -> Self: ...
    @overload
    def scale_by(self, scale_by: Coordinate) -> Self: ...
    @overload
    def scale_by_ip(self, x: float, y: float = ...) -> None: ...
    @overload
    def scale_by_ip(self, scale_by: Coordinate) -> None: ...
    @overload
    def update(self, left: float, top: float, width: float, height: float, /) -> None: ...
    @overload
    def update(self, left_top: Coordinate, width_height: Coordinate, /) -> None: ...
    @overload
    def update(self, single_arg: RectValue, /) -> None: ...
    @overload
    def clamp(self, rect: RectValue, /) -> Self: ...
    @overload
    def clamp(self, left_top: Coordinate, width_height: Coordinate, /) -> Self: ...
    @overload
    def clamp(self, left: float, top: float, width: float, height: float, /) -> Self: ...
    @overload
    def clamp_ip(self, rect: RectValue, /) -> None: ...
    @overload
    def clamp_ip(self, left_top: Coordinate, width_height: Coordinate, /) -> None: ...
    @overload
    def clamp_ip(
        self, left: float, top: float, width: float, height: float, /
    ) -> None: ...
    @overload
    def clip(self, rect: RectValue, /) -> Self: ...
    @overload
    def clip(self, left_top: Coordinate, width_height: Coordinate, /) -> Self: ...
    @overload
    def clip(self, left: float, top: float, width: float, height: float, /) -> Self: ...
    @overload
    def clipline(
        self, x1: float, x2: float, x3: float, x4: float, /
    ) -> Union[Tuple[Tuple[_N, _N], Tuple[_N, _N]], Tuple[()]]: ...
    @overload
    def clipline(
        self, first_coordinate: Coordinate, second_coordinate: Coordinate, /
    ) -> Union[Tuple[Tuple[_N, _N], Tuple[_N, _N]], Tuple[()]]: ...
    @overload
    def clipline(
        self, rect_arg: RectValue, /
    ) -> Union[Tuple[Tuple[_N, _N], Tuple[_N, _N]], Tuple[()]]: ...
    @overload
    def union(self, rect: RectValue, /) -> Self: ...
    @overload
    def union(self, left_top: Coordinate, width_height: Coordinate, /) -> Self: ...
    @overload
    def union(self, left: float, top: float, width: float, height: float, /) -> Self: ...
    @overload
    def union_ip(self, rect: RectValue, /) -> None: ...
    @overload
    def union_ip(self, left_top: Coordinate, width_height: Coordinate, /) -> None: ...
    @overload
    def union_ip(
        self, left: float, top: float, width: float, height: float, /
    ) -> None: ...
    def unionall(self, rect: Sequence[_RectTypeCompatible_co], /) -> Self: ...
    def unionall_ip(self, rect_sequence: Sequence[_RectTypeCompatible_co], /) -> None: ...
    @overload
    def fit(self, rect: RectValue, /) -> Self: ...
    @overload
    def fit(self, left_top: Coordinate, width_height: Coordinate, /) -> Self: ...
    @overload
    def fit(self, left: float, top: float, width: float, height: float, /) -> Self: ...
    def normalize(self) -> None: ...
    def __contains__(self, rect: Union[RectValue, _N], /) -> bool: ...  # type: ignore[override]
    @overload
    def contains(self, rect: RectValue, /) -> bool: ...
    @overload
    def contains(self, left_top: Coordinate, width_height: Coordinate, /) -> bool: ...
    @overload
    def contains(
        self, left: float, top: float, width: float, height: float, /
    ) -> bool: ...
    @overload
    def collidepoint(self, x: float, y: float, /) -> bool: ...
    @overload
    def collidepoint(self, x_y: Coordinate, /) -> bool: ...
    @overload
    def colliderect(self, rect: RectValue, /) -> bool: ...
    @overload
    def colliderect(self, left_top: Coordinate, width_height: Coordinate, /) -> bool: ...
    @overload
    def colliderect(
        self, left: float, top: float, width: float, height: float, /
    ) -> bool: ...
    def collidelist(self, rect_list: Sequence[_RectTypeCompatible_co], /) -> int: ...
    def collidelistall(self, rect_list: Sequence[_RectTypeCompatible_co], /) -> List[int]: ...
    def collideobjectsall(
        self, objects: Sequence[_T], key: Optional[Callable[[_T], RectValue]] = None
    ) -> List[_T]: ...
    def collideobjects(
        self, objects: Sequence[_T], key: Optional[Callable[[_T], RectValue]] = None
    ) -> Optional[_T]: ...
    @overload
    def collidedict(
        self, rect_dict: Dict[_RectTypeCompatible_co, _V], values: Literal[False] = False
    ) -> Optional[Tuple[_RectTypeCompatible_co, _V]]: ...
    @overload
    def collidedict(
        self, rect_dict: Dict[_K, _RectTypeCompatible_co], values: Literal[True]
    ) -> Optional[Tuple[_K, _RectTypeCompatible_co]]: ...
    @overload
    def collidedictall(
        self, rect_dict: Dict[_RectTypeCompatible_co, _V], values: Literal[False] = False
    ) -> List[Tuple[_RectTypeCompatible_co, _V]]: ...
    @overload
    def collidedictall(
        self, rect_dict: Dict[_K, _RectTypeCompatible_co], values: Literal[True]
    ) -> List[Tuple[_K, _RectTypeCompatible_co]]: ...

# Rect confirms to the Collection ABC, since it also confirms to
# Sized, Iterable and Container ABCs
class Rect(_GenericRect[int]):
    ...
    
class FRect(_GenericRect[float]):
    ...

RectType = Rect
FRectType = FRect
