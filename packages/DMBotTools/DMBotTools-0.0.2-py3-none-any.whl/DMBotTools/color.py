import warnings
from typing import Any, Tuple


class Color:
    __slots__ = ['_r', '_g', '_b', '_a']
    
    def __init__(self, r: int, g: int, b: int, a: int) -> None:
        self._r = r
        self._g = g
        self._b = b
        self._a = a

    def __hash__(self) -> int:
        return hash((self._r, self._g, self._b, self._a))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Color):
            return self._r == other._r and self._g == other._g and self._b == other._b and self._a == other._a
        
        return False

    def __iter__(self):
        return iter((self._r, self._g, self._b, self._a))

    def __getitem__(self, index):
        return (self._r, self._g, self._b, self._a)[index]
    
    def __setitem__(self, index, value):
        if index == 0:
            self.r = value
        elif index == 1:
            self.g = value
        elif index == 2:
            self.b = value
        elif index == 3:
            self.a = value
        else:
            raise IndexError("Index out of range")
    
    def __str__(self) -> str:
        return f"{self.r}_{self.g}_{self.b}_{self.a}"

    def __repr__(self) -> str:
        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"

    @property
    def r(self) -> int:
        return self._r
    
    @r.setter
    def r(self, value: int) -> None:
        if not (0 <= value <= 255):
            raise ValueError("Invalid value for r. It must be between 0 and 255")
        
        self._r = value
    
    @property
    def g(self) -> int:
        return self._g
    
    @g.setter
    def g(self, value: int) -> None:
        if not (0 <= value <= 255):
            raise ValueError("Invalid value for g. It must be between 0 and 255")
        
        self._g = value
    
    @property
    def b(self) -> int:
        return self._b
    
    @b.setter
    def b(self, value: int) -> None:
        if not (0 <= value <= 255):
            raise ValueError("Invalid value for b. It must be between 0 and 255")
        
        self._b = value
    
    @property
    def a(self) -> int:
        return self._a
    
    @a.setter
    def a(self, value: int) -> None:
        if not (0 <= value <= 255):
            raise ValueError("Invalid value for a. It must be between 0 and 255")
        
        self._a = value

    @staticmethod
    def from_tuple(value: Tuple[int, int, int, int]) -> "Color":
        warnings.warn("from_tuple is deprecated, use Color(*value) instead", DeprecationWarning, stacklevel=2)
        return Color(value[0], value[1], value[2], value[3])
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        warnings.warn("to_tuple is deprecated, use tuple(color) or list(color) instead", DeprecationWarning, stacklevel=2)
        return (self.r, self.g, self.r, self.a)
