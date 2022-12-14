from typing import Generic, Iterable, TypeVar, Union, Tuple, List
T = TypeVar("T")


class Random:

  _x, _y, _z, _w = 123456789, 362436069, 521288629, 88675123

  @classmethod
  def random(self) -> int:
    t = Random._x ^ (Random._x << 11) & 0xFFFFFFFF
    Random._x, Random._y, Random._z = Random._y, Random._z, Random._w
    Random._w = (Random._w ^ (Random._w >> 19)) ^ (t ^ (t >> 8)) & 0xFFFFFFFF
    return Random._w


class Node:

  def __init__(self, key, priority: int=-1):
    self.key = key
    self.left = None
    self.right = None
    self.priority = Random.random() if priority == -1 else priority

  def __str__(self):
    if self.left is None and self.right is None:
      return f'key:{self.key, self.priority}\n'
    return f'key:{self.key, self.priority},\n left:{self.left},\n right:{self.right}\n'


class TreapSet:

  def __init__(self, a: Iterable[T]=[]):
    self.node = None
    self.len = 0
    if a:
      a = sorted(set(a))
      self.len = len(a)
      self._build(a)

  def _build(self, a: Iterable[T]) -> None:
    def sort(l: int, r: int) -> Node:
      mid = (l + r) >> 1
      node = Node(a[mid], r[mid])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      return node
    r = sorted(Random.random() for _ in range(self.len))
    self.node = sort(0, self.len)

  def _rotate_L(self, node: Node) -> Node:
    u = node.left
    node.left = u.right
    u.right = node
    return u

  def _rotate_R(self, node: Node) -> Node:
    u = node.right
    node.right = u.left
    u.left = node
    return u

  def add(self, key: T) -> None:
    if self.node is None:
      self.node = Node(key)
      self.len += 1
      return
    node = self.node
    path = []
    di = 0
    while node is not None:
      if key == node.key:
        return False
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    if di & 1:
      path[-1].left = Node(key)
    else:
      path[-1].right = Node(key)
    while path:
      new_node = None
      node = path.pop()
      if di & 1:
        if node.left.priority < node.priority:
          new_node = self._rotate_L(node)
      else:
        if node.right.priority < node.priority:
          new_node = self._rotate_R(node)
      di >>= 1
      if new_node is not None:
        if path:
          if di & 1:
            path[-1].left = new_node
          else:
            path[-1].right = new_node
        else:
          self.node = new_node
    self.len += 1
    return True

  def discard(self, key: T) -> bool:
    node = self.node
    pnode = None
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        pnode = node
        node = node.left
      else:
        pnode = node
        node = node.right
    else:
      return False
    self.len -= 1
    while node.left is not None and node.right is not None:
      if node.left.priority < node.right.priority:
        if pnode is None:
          pnode = self._rotate_L(node)
          self.node = pnode
          continue
        new_node = self._rotate_L(node)
        if node.key < pnode.key:
          pnode.left = new_node
        else:
          pnode.right = new_node
      else:
        if pnode is None:
          pnode = self._rotate_R(node)
          self.node = pnode
          continue
        new_node = self._rotate_R(node)
        if node.key < pnode.key:
          pnode.left = new_node
        else:
          pnode.right = new_node
      pnode = new_node
    if pnode is None:
      if node.left is None:
        self.node = node.right
      else:
        self.node = node.left
      return True
    if node.left is None:
      if node.key < pnode.key:
        pnode.left = node.right
      else:
        pnode.right = node.right
    else:
      if node.key < pnode.key:
        pnode.left = node.left
      else:
        pnode.right = node.left
    return True

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        res = key
        break
      elif key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key <= node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        res = key
        break
      elif key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def to_l(self) -> List[T]:
    a = []
    if self.node is None:
      return a
    def rec(node):
      if node.left is not None:
        rec(node.left)  
      a.append(node.key)
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def get_min(self) -> T:
    node = self.node
    while node.left is not None:
      node = node.left
    return node.key

  def get_max(self) -> T:
    node = self.node
    while node.right is not None:
      node = node.right
    return node.key

  def popleft(self) -> T:
    node = self.node
    pnode = None
    while node.left is not None:
      pnode = node
      node = node.left
    self.len -= 1
    res = node.key
    if pnode is None:
      self.node = self.node.right
    else:
      pnode.left = node.right
    return res

  def pop(self) -> T:
    node = self.node
    pnode = None
    while node.right is not None:
      pnode = node
      node = node.right
    self.len -= 1
    res = node.key
    if pnode is None:
      self.node = self.node.left
    else:
      pnode.right = node.left
    return res

  def __getitem__(self, k: int) -> T:
    if k == -1 or k == self.len-1:
      return self.get_max()
    elif k == 0:
      return self.get_min()
    raise IndexError

  def __contains__(self, key: T):
    node = self.node
    while node is not None:
      if key == node.key:
        return True
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return False

  def __len__(self):
    return self.len

  def __str__(self):
    return '{' + ', '.join(map(str, self.to_l())) + '}'

  def __repr__(self):
    return 'TreapSet' + str(self)


