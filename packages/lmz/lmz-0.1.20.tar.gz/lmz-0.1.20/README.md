# listmapzip

provides a few functions that should be part of python3


## Install
```
pip install lmz
conda install -c conda-forge
```

## Example

```Python
from lmz import Map,Zip,Filter,Grouper,Range,Transpose,Flatten,iterselect

# Map
>>> def add(x,y=4): return x+y
>>> Map(add, range(3),y=2)
[2, 3, 4]

>>> Grouper(range(10),3)
[(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, None, None)]


# Flatten
>>> z=Grouper(range(10),3)
>>> Flatten(z)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, None, None]

>>> Transpose(z)
[(0, 3, 6, 9), (1, 4, 7, None), (2, 5, 8, None)]

>>> Range(z)
[0, 1, 2, 3]

>>> iterselect(iter(range(10)),4)
4

# Zip and Filter work as expected
```

