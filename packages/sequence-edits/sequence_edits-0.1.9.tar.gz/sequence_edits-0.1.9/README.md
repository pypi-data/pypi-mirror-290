# Sequence Edits

> Compressed representation of sequence edits


## Edits

```python
class Skip:
  id: int
  tag = 'skip'

class Insert:
  idx: int
  value: T
  tag = 'insert'

Edit = Skip | Insert
```

All edits are applied w.r.t. the original list. So, order of edits only affects the order in which values are insterted to a same index.

## Usage

```python
import sequence_edits as se

edits = [
  se.Insert(idx=1, value='the'),
  se.Skip(idx=4)
]
xs = ['And',      'earth', 'was', 'without', 'no', 'form']
list(se.apply(edits, xs))
#  ['And', 'the', 'earth', 'was', 'without',       'form']
```