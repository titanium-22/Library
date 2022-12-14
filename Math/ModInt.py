from typing import Union
from functools import lru_cache


class mint:

  # mod = 1000000007
  mod = 998244353

  @classmethod
  @lru_cache(maxsize=None)
  def _inv(self, a: int) -> int:
    res = 1
    b = mint.mod - 2
    while b:
      if b & 1:
        res = res * a % mint.mod
      a = a * a % mint.mod
      b >>= 1
    return res

  def __init__(self, val: int) -> None:
    self.val = val % mint.mod

  def __add__(self, other: Union[int, "mint"]) -> "mint":
    return mint(self.val + (other if isinstance(other, int) else other.val))

  def __sub__(self, other: Union[int, "mint"]) -> "mint":
    return mint(self.val - (other if isinstance(other, int) else other.val))

  def __mul__(self, other: Union[int, "mint"]) -> "mint":
    return mint(self.val * (other if isinstance(other, int) else other.val))

  def __truediv__(self, other: Union[int, "mint"]) -> "mint":
    return mint(self.val * (self._inv(other) if isinstance(other, int) else self._inv(other.val)))

  def __radd__(self, other: Union[int, "mint"]) -> "mint":
    return mint((other if isinstance(other, int) else other.val) + self.val)

  def __rsub__(self, other: Union[int, "mint"]) -> "mint":
    return mint((other if isinstance(other, int) else other.val) - self.val)

  def __rmul__(self, other: Union[int, "mint"]) -> "mint":
    return mint((other if isinstance(other, int) else other.val) * self.val)

  def __rtruediv__(self, other: Union[int, "mint"]) -> "mint":
    return mint((other if isinstance(other, int) else other.val) * self._inv(self.val))

  def __iadd__(self, other: Union[int, "mint"]) -> "mint":
    return mint(self.val + (other if isinstance(other, int) else other.val))

  def __isub__(self, other: Union[int, "mint"]) -> "mint":
    return mint(self.val - (other if isinstance(other, int) else other.val))

  def __imul__(self, other: Union[int, "mint"]) -> "mint":
    return mint(self.val * (other if isinstance(other, int) else other.val))

  def __itruediv__(self, other: Union[int, "mint"]) -> "mint":
    return mint(self.val * (self._inv(other) if isinstance(other, int) else self._inv(other.val)))

  def __eq__(self, other: Union[int, "mint"]):
    return self.val == int(other)

  def __lt__(self, other: Union[int, "mint"]):
    return self.val < int(other)

  def __le__(self, other: Union[int, "mint"]):
    return self.val <= int(other)

  def __gt__(self, other: Union[int, "mint"]):
    return self.val > int(other)

  def __ge__(self, other: Union[int, "mint"]):
    return self.val >= int(other)

  def __ne__(self, other: Union[int, "mint"]):
    return self.val != int(other)

  def __neg__(self):
    return mint(-self.val + mint.mod)

  def __pos__(self):
    return mint(self.val)

  def __int__(self):
    return self.val

  def __str__(self):
    return str(self.val)

  def __repr__(self):
    return str(self)


