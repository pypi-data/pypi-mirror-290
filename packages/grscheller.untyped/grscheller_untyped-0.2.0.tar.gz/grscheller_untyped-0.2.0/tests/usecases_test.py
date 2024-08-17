# Copyright 2023-2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from typing import Any
from grscheller.untyped.nothing import Nothing, nothing  # type: ignore
from grscheller.circular_array.ca import CA

def add2(x: int|Nothing) -> int:
    return x + 2

def make_non_negative(x: int|Nothing) -> int|Nothing:
    if x >= 0:
        return x
    if x < 0:
        return 0
    return nothing

def not_nothing(x: object) -> bool:
    if x is nothing:
        return False
    else:
        return True

class Test_Builtin_Containers:
    def test_mixed_list(self) -> None:
        foo: list[int|Nothing] = [23, -5, nothing, nothing, -1, 40]

        bar: list[int|Nothing] = list(map(add2, foo))
        assert bar == [25, -3, nothing, nothing, 1, 42]

        baz: list[int|Nothing] = []
        for x in foo:
            baz.append(make_non_negative(x))
        assert baz == [23, 0, nothing, nothing, 0, 40]

        fuz = list(filter(not_nothing, foo))
        assert fuz == [23, -5, -1, 40]

        zud1 = list(filter(None, foo))
        zud2 = list(filter(None, baz))
        assert zud1 == [23, -5, -1, 40]
        assert zud2 == [23, 40]

    def test_mixed_tuples(self) -> None:
        tup0: tuple[tuple[int|Nothing, ...]|Nothing, ...] = \
            (0, 1, 2, 3), \
            (-1, 10, nothing, 30, 40, nothing, 60), \
            tuple(range(40, 81)) + (nothing, nothing), \
            nothing, \
            (99, nothing)*5

        tup1: tuple[int|Nothing, ...] = ()

        for idx in range(len(tup0)):
            tup1 += tup0[idx][2],
        assert tup1 == (2, nothing, 42, nothing, 99)

    def test_dicts(self) -> None:
        dict1 = {None:'0', ():'1', nothing:'2', 42:'42'}
        assert dict1[None] == str(0)
        assert dict1[()] == str(1)
        assert dict1[nothing] == str(2)   # comment out for grscheller.untyped
        assert dict1[Nothing()] == str(2) # PyPI version < 0.1.2
        assert dict1[42] == str(42)

        foo = Nothing()
        bar = Nothing()
        dict2 = {1: 42, 2: foo, 3: bar}
        assert dict2[1] == 42
        assert dict2[2] is Nothing()
        assert dict2[3] is Nothing()
        assert dict2[2] is dict2[3]
        assert foo is bar
        assert dict2[2] is foo
        assert dict2[2] is dict2[3]
        assert dict2[2] is dict2[2]

    def test_comparibility(self) -> None:
        cir1 = 42, CA(42, nothing)
        cir2 = 42, CA(42, nothing)
        assert cir1 == cir2  # CAs now compare with identity before equality
        assert not (cir1 is cir2)

        tup1 = 42, [42]
        tup2 = 42, [42]
        assert tup1 == tup2  # lists must compare identity before equality
        assert not (tup1 is tup2)

        tup3 = 42, [42, nothing]
        tup4 = 42, [42, nothing]
        assert tup3 == tup4
        assert not (tup3 is tup4)  # because both contain mutable objects
        assert tup3[1].pop(-1) is nothing
        assert tup4[1].pop(-1) is nothing
        tup3[1].append(100)
        tup4[1].append(200)
        assert tup3 != tup4
        tup4[1][1] -= 100
        assert tup3 == tup4

