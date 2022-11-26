# https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeMultiSet.py


import sys
from typing import Union, Generic, Iterable, List, TypeVar
T = TypeVar("T")


class Node:

  def __init__(self, key, val) -> None:
    self.key = key
    self.size = 1
    self.val = val
    self.valsize = val
    self.left = None
    self.right = None

  def __str__(self) -> str:
    if self.left is None and self.right is None:
      return f'key:{self.key, self.size, self.val, self.valsize}\n'
    return f'key:{self.key, self.size, self.val, self.valsize},\n left:{self.left},\n right:{self.right}\n'


class SplayTreeMultiSet(Generic[T]):

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.node = None
    if a:
      self._build(a)

  def _build(self, a: Iterable[T]) -> None:
    def sort(l: int, r: int):
      if l == r: return None
      mid = (l + r) >> 1
      node = Node(a[mid])
      node.left = sort(l, mid)
      node.right = sort(mid+1, r)
      self._update(node)
      return node
    aa = sorted(a)
    a = [aa[0]]
    for i in range(1, len(aa)):
      if aa[i] != a[-1]:
        a.append(aa[i])
    self.node = sort(0, len(a))

  def _update(self, node: Node) -> None:
    node.size = 1
    node.valsize = node.val
    if node.left is not None:
      node.size += node.left.size
      node.valsize += node.left.valsize
    if node.right is not None:
      node.size += node.right.size
      node.valsize += node.right.valsize

  def _splay(self, path: List[Node], di: int) -> Node:
    for _ in range(len(path)>>1):
      node = path.pop()
      pnode = path.pop()
      if di&1 == di>>1&1:
        if di&1 == 1:
          tmp = node.left
          node.left = tmp.right
          tmp.right = node
          pnode.left = node.right
          node.right = pnode
        else:
          tmp = node.right
          node.right = tmp.left
          tmp.left = node
          pnode.right = node.left
          node.left = pnode
      else:
        if di&1 == 1:
          tmp = node.left
          node.left = tmp.right
          pnode.right = tmp.left
          tmp.right = node
          tmp.left = pnode
        else:
          tmp = node.right
          node.right = tmp.left
          pnode.left = tmp.right
          tmp.left = node
          tmp.right = pnode
      self._update(pnode)
      self._update(node)
      self._update(tmp)
      if not path:
        return tmp
      di >>= 2
      if di & 1 == 1:
        path[-1].left = tmp
      else:
        path[-1].right = tmp
    gnode = path[0]
    if di & 1 == 1:
      node = gnode.left
      gnode.left = node.right
      node.right = gnode
      self._update(node.right)
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
      self._update(node.left)
    self._update(node)
    return node

  def _set_search_splay(self, key: T) -> None:
    node = self.node
    if node is None or node.key == key: return
    path = []
    di = 0
    while node is not None:
      if node.key == key:
        break
      elif key < node.key:
        path.append(node)
        di = di << 1 | 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)

  def _set_kth_elm_splay(self, k: int) -> None:
    if k < 0:
      k += self.__len__()
    # assert 0 <= k < self.__len__()
    now = 0
    di = 0
    node = self.node
    path = []
    while True:
      s = now if node.left is None else now + node.left.valsize
      t = s + node.val
      if s <= k < t:
        if path:
          self.node = self._splay(path, di)
        break
      elif t > k:
        path.append(node)
        di = di<<1|1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
        now = t

  def _set_kth_elm_tree_splay(self, k: int) -> None:
    if k < 0:
      k += self.__len__()
    # assert 0 <= k < self.__len__()
    now = 0
    di = 0
    node = self.node
    path = []
    while True:
      t = now if node.left is None else now + node.left.size
      if t == k:
        if path:
          self.node = self._splay(path, di)
        break
      elif t > k:
        path.append(node)
        di = di<<1|1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
        now = t + 1

  def _get_min_splay(self, node: Node) -> Node:
    if node is None or node.left is None:
      return node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
    return self._splay(path, (1<<len(path))-1)

  def _get_max_splay(self, node: Node) -> Node:
    if node is None or node.right is None:
      return node
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
    return self._splay(path, 0)

  '''Add a key. / O(logN)'''
  def add(self, key: T, val: int=1) -> None:
    if self.node is None:
      self.node = Node(key, val)
      return True
    self._set_search_splay(key)
    if self.node.key == key:
      self.node.val += val
      self._update(self.node)
      return
    node = Node(key, val)
    if key < self.node.key:
      node.left = self.node.left
      node.right = self.node
      self.node.left = None
      self._update(node.right)
    else:
      node.left = self.node
      node.right = self.node.right
      self.node.right = None
      self._update(node.left)
    self._update(node)
    self.node = node
    return

  '''Discard a key. / O(logN)'''
  def discard(self, key: T, val: int=1) -> bool:
    if self.node is None: return False
    self._set_search_splay(key)
    if self.node.key != key: return False
    if self.node.val > val:
      self.node.val -= val
      self._update(self.node)
      return True
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_min_splay(self.node.right)
      node.left = self.node.left
      self._update(node.left)
      self.node = node
    return True

  def discar_all(self, key: T) -> bool:
    return self.discar(key, self.count(key))

  def count(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    return self.node.val if self.node.key == key else 0

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    path = []
    di = 0
    res = None
    while node is not None:
      if node.key == key:
        res = key
        break
      elif key < node.key:
        path.append(node)
        di = di << 1 | 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        res = node.key
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    path = []
    di = 0
    res = None
    while node is not None:
      if node.key == key:
        break
      elif key < node.key:
        path.append(node)
        di = di << 1 | 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        res = node.key
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    path = []
    di = 0
    res = None
    while node is not None:
      if node.key == key:
        res = node.key
        break
      elif key < node.key:
        path.append(node)
        di = di << 1 | 1
        res = node.key
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: T) -> Union[T, None]:
    node = self.node
    if node is None: return None
    path = []
    di = 0
    res = None
    while node is not None:
      if node.key == key:
        break
      elif key < node.key:
        path.append(node)
        di = di << 1 | 1
        res = node.key
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    else:
      if path:
        path.pop()
        di >>= 1
    if path:
      self.node = self._splay(path, di)
    return res

  '''Count the number of elements < key. / O(logN)'''
  def index(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.valsize
    if self.node.key < key:
      res += self.node.val
    return res

  '''Count the number of elements <= key. / O(logN)'''
  def index_right(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.valsize
    if self.node.key <= key:
      res += self.node.val
    return res

  '''Return and Remove max element or a[p]. / O(logN)'''
  def pop(self, p: int=-1) -> T:
    if p == -1:
      node = self._get_max_splay(self.node)
      self.node = node.left
      return node.key
    if p < 0:
      p += self.__len__()
    self._set_kth_elm_splay(p)
    res = self.node.key
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_min_splay(self.node.right)
      node.left = self.node.left
      self.node = node
      self._update(self.node.left)
    return res

  '''Return and Remove min element. / O(logN)'''
  def popleft(self) -> T:
    node = self._get_min_splay(self.node)
    self.node = node.right
    return node.key

  '''Return List of self. / O(N)'''
  def to_l(self) -> List[T]:
    if sys.getrecursionlimit() < self.__len__():
      sys.setrecursionlimit(self.__len__()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.extend([node.key]*node.val)
      if node.right is not None:
        rec(node.right)
    a = []
    if self.node is not None:
      rec(self.node)
    return a

  def get_elm(self, p: int) -> T:
    self._set_kth_elm_tree_splay(p)
    return self.node.key

  def items(self):
    for i in range(self.len_elm()):
      self._set_kth_elm_tree_splay(i)
      yield self.node.key, self.node.val

  def keys(self):
    for i in range(self.len_elm()):
      self._set_kth_elm_tree_splay(i)
      yield self.node.key

  def values(self):
    for i in range(self.len_elm()):
      self._set_kth_elm_tree_splay(i)
      yield self.node.val

  def len_elm(self) -> int:
    return 0 if self.node is None else self.node.size

  def show_items(self) -> None:
    print('{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.items())) + '}')

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self.__getitem__(-i-1)

  def __contains__(self, key: T) -> bool:
    self._set_search_splay(key)
    return self.node is not None and self.node.key == key

  def __getitem__(self, p) -> T:
    if p < 0:
      p += self.__len__()
    self._set_kth_elm_splay(p)
    return self.node.key

  def __len__(self):
    return 0 if self.node is None else self.node.valsize

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.to_l())) + '}'

  def __repr__(self):
    return 'SplayTreeSet ' + str(self)


