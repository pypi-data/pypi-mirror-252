from __future__ import annotations

from typing import Any


def m_add(a:Any, b:Any)->Any:
    return m_subtract(a+b,0)

print('myadd 10')

from .mysubtract import m_subtract


print('myadd 20')


