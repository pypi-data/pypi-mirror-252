from __future__ import annotations

print('mysubtract 10')
from typing import Any
from .myadd import m_add

print('mysubtract 20')

def m_subtract(a:Any, b:Any)->Any:
    return a-b


def fadd()->Any:
    return m_add(1, 1)
