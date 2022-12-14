# https://github.com/titanium-22/Library/blob/main/Heap/IntervalHeap.py
from typing import Generic, Iterable, TypeVar
T = TypeVar("T")


class IntervalHeap(Generic[T]):

  def __init__(self, a: Iterable[T]=[]):
    self._data = list(a)
    self._heapify()

  def _heapify(self) -> None:
    n = len(self._data)
    for i in range(n-1, -1, -1):
      if i & 1 and self._data[i-1] < self._data[i]:
        self._data[i-1], self._data[i] = self._data[i], self._data[i-1]
      k = self._down(i)
      self._up(k, i)

  def add(self, key: T) -> None:
    self._data.append(key)
    self._up(len(self._data)-1)

  def pop_min(self) -> T:
    if len(self._data) < 3:
      res = self._data.pop()
    else:
      self._data[1], self._data[-1] = self._data[-1], self._data[1]
      res = self._data.pop()
      k = self._down(1)
      self._up(k)
    return res

  def pop_max(self) -> T:
    if len(self._data) < 2:
      res = self._data.pop()
    else:
      self._data[0], self._data[-1] = self._data[-1], self._data[0]
      res = self._data.pop()
      self._up(self._down(0))
    return res

  def get_min(self) -> T:
    return self._data[0] if len(self._data) < 2 else self._data[1]

  def get_max(self) -> T:
    return self._data[0]

  def __len__(self):
    return len(self._data)

  def __bool__(self):
    return len(self._data) > 0

  def _parent(self, k):
    return ((k>>1)-1) & ~1

  def _down(self, k: int) -> int:
    n = len(self._data)
    if k & 1:
      while 2*k+1 < n:
        c = 2*k+3
        if n <= c or self._data[c-2] < self._data[c]:
          c -= 2
        if c < n and self._data[c] < self._data[k]:
          self._data[k], self._data[c] = self._data[c], self._data[k]
          k = c
        else:
          break
    else:
      while 2*k+2 < n:
        c = 2*k+4
        if n <= c or self._data[c] < self._data[c-2]:
          c -= 2
        if c < n and self._data[k] < self._data[c]:
          self._data[k], self._data[c] = self._data[c], self._data[k]
          k = c
        else:
          break
    return k

  def _up(self, k: int, root: int=1) -> int:
    if (k|1) < len(self._data) and self._data[k&~1] < self._data[k|1]:
      self._data[k&~1], self._data[k|1] = self._data[k|1], self._data[k&~1]
      k ^= 1
    while root < k:
      p = self._parent(k)
      if not self._data[p] < self._data[k]:
        break
      self._data[p], self._data[k] = self._data[k], self._data[p]
      k = p
    while root < k:
      p = self._parent(k) | 1
      if not self._data[k] < self._data[p]:
        break
      self._data[p], self._data[k] = self._data[k], self._data[p]
      k = p
    return k

  def __str__(self):
    return '[' + ', '.join(map(str, sorted(self._data))) + ']'


