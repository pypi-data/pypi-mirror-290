from typing import Iterable, TypeVar, overload
from functools import cmp_to_key
from .types import Skip, Insert, Inserted, Edit

@cmp_to_key
def key(x: Edit, y: Edit):
  if x.idx != y.idx:
    return x.idx - y.idx
  elif x.tag != y.tag:
    return -1 if x.tag == 'insert' else 1 # inserts first
  else:
    return 0

V =  TypeVar('V')    
def decompress(edits: Iterable[Edit[V]], start: int = 0, end: int | None = None) -> Iterable[int|Inserted[V]]:
  """Applies `edits` to `[start, end)`, returning a full iterable of indices
  - e.g. `decompress([insert(4), skip(6)], start=3, end=8) == xs `
    - `list(xs) == [3, None, 4, 5, 7] # inserted before 4, skipped 6`
  - If `end is None`, applies until last edit
  """
  i = start
  edits = sorted(edits, key=key)
  for edit in filter(lambda e: start <= e.idx < (end or float('inf')), edits):
    yield from range(i, edit.idx)
    if edit.tag == 'skip':
      i = edit.idx+1
    elif edit.tag == 'insert':
      yield Inserted(edit.value)
      i = edit.idx
    elif edit.tag == 'replace':
      yield Inserted(edit.value)
      i = edit.idx+1
  if end is not None:
    yield from range(i, end)

A = TypeVar('A')

@overload
def apply(edits: Iterable[Edit], xs: list[A], start: int = 0, *, fill: V) -> Iterable[A | V]:
  """Applies `edits` to an actual list `xs[start:]`, replacing insterts by `fill`"""
  ...
@overload
def apply(edits: Iterable[Edit[V]], xs: list[A], start: int = 0) -> Iterable[A | V]:
  """Applies `edits` to an actual list `xs[start:]`"""
  ...
def apply(edits: Iterable[Edit], xs: list[A], start: int = 0, *, fill = None): # type: ignore
  for i in decompress(edits, start=start, end=len(xs)):
    yield fill or i.value if isinstance(i, Inserted) else xs[i]