# Tests for Sukoon iPython kernel
# Each test is some code, followed by a comment indicating the expected response
# Expected responses start with "##"


x = 3 + 2
## x = 5

y = 4
z = 5
## y = 4
## z = 5

import math
x = math.sqrt(4.0)
## x = 2.0

x, y = 6, 7
## x = 6
## y = 7

def f():
    value = 345
    return value
## value = 345
