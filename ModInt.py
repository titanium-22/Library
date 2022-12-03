# https://github.com/titanium-22/Library/blob/main/ModInt.py


from typing import Union
from functools import lru_cache


class SubModInt:
  
  # mod = 1000000007
  mod = 998244353

  @classmethod
  @lru_cache(maxsize=None)
  def _truediv(self, a: int, b: int) -> int:
    return a * pow(b, self.mod-2, self.mod) % self.mod

  def __init__(self, val: int) -> None:
    self.val = val if 0 <= val and val <= self.mod else val % self.mod

  def __add__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self.val + (other if isinstance(other, int) else other.val)
    if val > self.mod: val -= self.mod
    return SubModInt(val)

  def __sub__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self.val - (other if isinstance(other, int) else other.val)
    if val < 0: val += self.mod
    return SubModInt(val)

  def __mul__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self.val * (other if isinstance(other, int) else other.val)
    return SubModInt(val)

  def __truediv__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self._truediv(self.val, other) if isinstance(other, int) else self._truediv(self.val, other.val)
    return SubModInt(val)

  def __radd__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self.val + (other if isinstance(other, int) else other.val)
    if val > self.mod: val -= self.mod
    return SubModInt(val)

  def __rsub__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self.val - (other if isinstance(other, int) else other.val)
    if val < 0: val += self.mod
    return SubModInt(val)

  def __rmul__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self.val * (other if isinstance(other, int) else other.val)
    return SubModInt(val)

  def __rtruediv__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self._truediv(self.val, other) if isinstance(other, int) else self._truediv(self.val, other.val)
    return SubModInt(val)

  def __iadd__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self.val + (other if isinstance(other, int) else other.val)
    if val > self.mod: val -= self.mod
    return SubModInt(val)

  def __isub__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self.val - (other if isinstance(other, int) else other.val)
    if val < 0: val += self.mod
    return SubModInt(val)

  def __imul__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self.val * (other if isinstance(other, int) else other.val)
    return SubModInt(val)

  def __itruediv__(self, other: Union[int, "SubModInt"]) -> "SubModInt":
    val = self._truediv(self.val, other) if isinstance(other, int) else self._truediv(self.val, other.val)
    return SubModInt(val)

  def __eq__(self, other: Union[int, "SubModInt"]):
    return int(self) == int(other)

  def __lt__(self, other: Union[int, "SubModInt"]):
    return int(self) < int(other)

  def __le__(self, other: Union[int, "SubModInt"]):
    return int(self) <= int(other)

  def __gt__(self, other: Union[int, "SubModInt"]):
    return int(self) > int(other)

  def __ge__(self, other: Union[int, "SubModInt"]):
    return int(self) >= int(other)

  def __ne__(self, other: Union[int, "SubModInt"]):
    return int(self) != int(other)
  
  def __int__(self):
    return self.val

  def __str__(self):
    return str(self.val)

  def __repr__(self):
    return str(self)


@lru_cache(maxsize=None)
def ModInt(val: int) -> "SubModInt":
  return SubModInt(val)

