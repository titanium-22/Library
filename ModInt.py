# https://github.com/titanium-22/Library/blob/main/ModInt.py


from typing import Union
from functools import lru_cache


class ModInt:
  
  # mod = 1000000007
  mod = 998244353

  @classmethod
  @lru_cache(maxsize=None)
  def _truediv(self, a: int, b: int) -> int:
    return a * pow(b, self.mod-2, self.mod) % self.mod

  # キャッシュが当たりそうならコメントアウトする
  # @classmethod
  # @lru_cache(maxsize=None)
  def _generate(self, val: int) -> "ModInt":
    return ModInt(val)

  def __init__(self, val: int) -> None:
    self.val = val if 0 <= val and val <= self.mod else val % self.mod

  def __add__(self, other: Union[int, "ModInt"]) -> "ModInt":
    val = self.val + (other if isinstance(other, int) else other.val)
    if val > self.mod: val -= self.mod
    return self._generate(val)

  def __sub__(self, other: Union[int, "ModInt"]) -> "ModInt":
    val = self.val - (other if isinstance(other, int) else other.val)
    if val < 0: val += self.mod
    return self._generate(val)

  def __mul__(self, other: Union[int, "ModInt"]) -> "ModInt":
    val = self.val * (other if isinstance(other, int) else other.val)
    return self._generate(val)

  def __truediv__(self, other: Union[int, "ModInt"]) -> "ModInt":
    val = self._truediv(self.val, other) if isinstance(other, int) else self._truediv(self.val, other.val)
    return self._generate(val)

  def __radd__(self, other: Union[int, "ModInt"]) -> "ModInt":
    val = self.val + (other if isinstance(other, int) else other.val)
    if val > self.mod: val -= self.mod
    return self._generate(val)

  def __rsub__(self, other: Union[int, "ModInt"]) -> "ModInt":
    val = self.val - (other if isinstance(other, int) else other.val)
    if val < 0: val += self.mod
    return self._generate(val)

  def __rmul__(self, other: Union[int, "ModInt"]) -> "ModInt":
    val = self.val * (other if isinstance(other, int) else other.val)
    return self._generate(val)

  def __rtruediv__(self, other: Union[int, "ModInt"]) -> "ModInt":
    val = self._truediv(self.val, other) if isinstance(other, int) else self._truediv(self.val, other.val)
    return self._generate(val)

  def __iadd__(self, other: Union[int, "ModInt"]) -> "ModInt":
    self.val += other if isinstance(other, int) else other.val
    if self.val > self.mod:
      self.val -= self.mod
    return self

  def __isub__(self, other: Union[int, "ModInt"]) -> "ModInt":
    self.val -= other if isinstance(other, int) else other.val
    if self.val < 0:
      self.val += self.mod
    return self

  def __imul__(self, other: Union[int, "ModInt"]) -> "ModInt":
    self.val *= other if isinstance(other, int) else other.val
    return self

  def __itruediv__(self, other: Union[int, "ModInt"]) -> "ModInt":
    self.val = self._truediv(self.val, other) if isinstance(other, int) else self._truediv(self.val, other.val)
    self.val %= self.mod
    return self

  def __eq__(self, other: Union[int, "ModInt"]):
    return int(self) == int(other)

  def __lt__(self, other: Union[int, "ModInt"]):
    return int(self) < int(other)

  def __le__(self, other: Union[int, "ModInt"]):
    return int(self) <= int(other)

  def __gt__(self, other: Union[int, "ModInt"]):
    return int(self) > int(other)

  def __ge__(self, other: Union[int, "ModInt"]):
    return int(self) >= int(other)

  def __ne__(self, other: Union[int, "ModInt"]):
    return int(self) != int(other)

  def __int__(self):
    a = self.mod_div(100, 10)
    return self.val

  def __str__(self):
    return str(self.val)

  def __repr__(self):
    return str(self)

