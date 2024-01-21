# qrio

> A QR handling module for writing and reading QR.

## example

```python
from qrio import encode, decode

data = "hello world"

print(data == decode(encode(data.encode())).decode())
```