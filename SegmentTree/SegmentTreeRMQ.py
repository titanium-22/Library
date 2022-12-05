# https://github.com/titanium-22/Library/blob/main/SegmentTree/SegmentTreeRMQ.py


from typing import Generic, Iterable, TypeVar, Union
T = TypeVar("T")


class SegmentTreeRMQ(Generic[T]):

  '''Build a new SegmentTree. / O(N)'''
  def __init__(self, _n_or_a: Union[int, Iterable[T]], _e: T=float('inf')) -> None:
    self._e = _e
    if isinstance(_n_or_a, int):
      self._n = _n_or_a
      self._log  = (self._n-1).bit_length()
      self._size = 1 << self._log
      self._data  = [self._e] * (self._size<<1)
    else:
      _n_or_a = list(_n_or_a)
      self._n = len(_n_or_a)
      self._log  = (self._n-1).bit_length()
      self._size = 1 << self._log
      self._data = [self._e] * (self._size<<1)
      self._data[self._size:self._size+self._n] = _n_or_a
      for i in range(self._size-1, 0, -1):
        self._data[i] = self._data[i<<1] if self._data[i<<1] < self._data[i<<1|1] else self._data[i<<1|1]

  '''Change a[k] into x. / O(logN)'''
  def set(self, k: int, val: T) -> None:
    assert 0 <= k < self._n
    k += self._size
    self._data[k] = val
    for _ in range(self._log):
      k >>= 1
      self._data[k] = self._data[k<<1] if self._data[k<<1] < self._data[k<<1|1] else self._data[k<<1|1]

  '''Return a[k]. / O(1)'''
  def get(self, key: int) -> T:
    assert 0 <= key < self._n
    return self._data[key+self._size]

  '''Return op([l, r)). / 0 <= l <= r <= n / O(logN)'''
  def prod(self, l: int, r: int) -> T:
    assert 0 <= l <= r <= self._n
    l += self._size
    r += self._size
    res = self._e
    while l < r:
      if l & 1:
        if res > self._data[l]:
          res = self._data[l]
        l += 1
      if r & 1:
        r ^= 1
        if res > self._data[r]:
          res = self._data[r]
      l >>= 1
      r >>= 1
    return res

  '''Return min([0, n)). / O(1)'''
  def all_prod(self) -> T:
    return self._data[1]

  '''Find the largest index R s.t. f([l, R)) == True. / O(logN)'''
  def max_right(self, l: int, f=lambda lr: lr):
    # assert 0 <= l <= self._n
    # assert f(self._e)
    if l == self._n:
      return self._n 
    l += self._size
    tmp = self._e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(min(tmp, self._data[l])):
        while l < self._size:
          l <<= 1
          if f(min(tmp, self._data[l])):
            tmp = min(tmp, self._data[l])
            l += 1
        return l - self._size
      tmp = min(tmp, self._data[l])
      l += 1
      if l & -l == l:
        break
    return self._n

  '''Find the smallest index L s.t. f([L, r)) == True. / O(logN)'''
  def min_left(self, r: int, f=lambda lr: lr):
    # assert 0 <= r <= self._n 
    # assert f(self._e)
    if r == 0:
      return 0 
    r += self._size
    tmp = self._e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(min(self._data[r], tmp)):
        while r < self._size:
          r = r<<1|1
          if f(min(self._data[r], tmp)):
            tmp = min(self.dat[r], tmp)
            r -= 1
        return r + 1 - self._size
      tmp = min(self._data[r], tmp)
      if r & -r == r:
        break 
    return 0

  '''Debug. / O(N)'''
  def show(self) -> None:
    print('<SegmentTreeRMQ> [\n' + '\n'.join(['  ' + ' '.join(map(str, [self._data[(1<<i)+j] for j in range(1<<i)])) for i in range(self._log+1)]) + '\n]')

  def __getitem__(self, k: int):
    return self.get(k)

  def __setitem__(self, k: int, key):
    self.set(k, key)

  def __str__(self):
    return '[' + ', '.join(map(str, [self.get(i) for i in range(self._n)])) + ']'

  def __repr__(self):
    return 'SegmentTreeRMQ ' + str(self)

