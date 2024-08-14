"""
### Sequence Edits
> Compressed representation of sequence edits
- `decompress: edits, [start, end) -> indices`
- `apply: edits, start, xs -> edited xs`
- `Edit`: skip or insert
"""
from .types import Skip, Insert, Edit, Replace
from .main import decompress, apply