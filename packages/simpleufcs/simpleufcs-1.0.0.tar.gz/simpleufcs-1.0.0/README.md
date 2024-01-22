# simpleufcs

A simple ~~(and ugly)~~ Uniform Function Call Syntax (UFCS) implementation in python.

## Usage

Installation:

```sh
pip install simpleufcs
```

```py
from simpleufcs import UFCS
UFCS([3, 2, 1]).sorted(key=lambda x: x <= 1).map(lambda x: x * 2).list().print()
```

## benchmark

In the [benchmark](./benchmark.py), the UFCS implementation is about 3 times slower than the built-in method.

| bench | ufcs                | builtin              |
| ----- | ------------------- | -------------------- |
| 1     | 0.02407699999457691 | 0.006241800001589581 |
