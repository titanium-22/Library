# https://github.com/titanium-22/Library/blob/main/LazyQuadraticDivision.py


from functools import reduce
from typing import Union, List, Callable, TypeVar, Generic
T = TypeVar("T")
F = TypeVar("F")


class LazyQuadraticDivision(Generic[T, F]):

  def __init__(self, n_or_a: Union[int, List], op, mapping, composition, e):
    if isinstance(n_or_a, int):
      self.n = n_or_a
      a = [e] * self.n
    else:
      a = list(n_or_a)
      self.n = len(a)
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e
    self.size = int(self.n**.5) + 1
    self.bucket_cnt = (self.n+self.size-1) // self.size
    self.data = [a[k*self.size:(k+1)*self.size] for k in range(self.bucket_cnt)]
    self.bucket_data = [reduce(self.op, v) for v in self.data]
    self.bucket_lazy = [None] * self.bucket_cnt
 
  '''Applay f to a[l:r). / O(√N)'''
  def apply(self, l: int, r: int, f: F) -> None:
    assert 0 <= l <= r <= self.n
    def _change_data(k: int, l: int, r: int) -> None:
      self._propagate(k)
      self.data[k][l:r] = [self.mapping(f, d) for d in self.data[k][l:r]]
      self.bucket_data[k] = reduce(self.op, self.data[k])
 
    k1 = l // self.size
    k2 = r // self.size
    l -= k1 * self.size
    r -= k2 * self.size
    if k1 == k2:
      if k1 < self.bucket_cnt: _change_data(k1, l, r)
    else:
      if k1 < self.bucket_cnt:
        if l == 0:
          self.bucket_lazy[k1] = f if self.bucket_lazy[k1] is None else self.composition(f, self.bucket_lazy[k1])
          self.bucket_data[k1] = self.mapping(f, self.bucket_data[k1])
        else:
          _change_data(k1, l, len(self.data[k1]))

      self.bucket_lazy[k1+1:k2] = [f if bl is None else self.composition(f, bl) for bl in self.bucket_lazy[k1+1:k2]]
      self.bucket_data[k1+1:k2] = [self.mapping(f, bd) for bd in self.bucket_data[k1+1:k2]]

      if k2 < self.bucket_cnt:
        if r == len(self.data[k2]):
          self.bucket_lazy[k2] = f if self.bucket_lazy[k2] is None else self.composition(f, self.bucket_lazy[k2])
          self.bucket_data[k2] = self.mapping(f, self.bucket_data[k2])
        else:
          _change_data(k2, 0, r)

  def all_apply(self, f: F) -> None:
    self.bucket_lazy = [f if bl is None else self.composition(f, bl) for bl in self.bucket_lazy]
 
  def _propagate(self, k: int) -> None:
    '''propagate bucket_lazy[k]. / O(√N)'''
    if k >= self.bucket_cnt or self.bucket_lazy[k] is None: return
    f = self.bucket_lazy[k]
    self.data[k] = [self.mapping(f, d) for d in self.data[k]]
    self.bucket_lazy[k] = None
 
  '''Return op([l, r)). / 0 <= l <= r <= n / O(√N)'''
  def prod(self, l: int, r: int):
    assert 0 <= l <= r <= self.n
    s = self.e
    k1 = l // self.size
    k2 = r // self.size
    l -= k1 * self.size
    r -= k2 * self.size
    self._propagate(k1)
    self._propagate(k2)
    if k1 == k2:
      s = reduce(self.op, self.data[k1][l:r], s)
    else:
      s = reduce(self.op, self.data[k1][l:], s)
      s = reduce(self.op, self.bucket_data[k1+1:k2], s)
      if k2 < self.bucket_cnt: s = reduce(self.op, self.data[k2][:r], s)
    return s
 
  '''Return op([0, n)). / O(√N)'''
  def all_prod(self):
    return reduce(self.op, self.bucket_data)
 
  def __getitem__(self, k: int) -> T:
    p = k // self.size
    # self._propagate(k)
    # return self.data[k][indx-k*self.size]
    return self.data[p][k-p*self.size] if self.bucket_lazy[p] is None else self.mapping(self.bucket_lazy[p], self.data[p][k-p*self.size])

  def __setitem__(self, indx, key):
    k = indx // self.size
    self._propagate(k)
    self.data[k][indx-k*self.size] = key
    self.bucket_data[k] = reduce(self.op, self.data[k])

  def __str__(self):
    return '[' + ', '.join(map(str, [self.__getitem__(i) for i in range(self.n)])) + ']'

  def __repr__(self):
    return 'LazyQuadraticDivision ' + str(self)
 
 
def op(s, t):
  return
 
def mapping(f, s):
  return
 
def composition(f, g):
  return
 
e = None

