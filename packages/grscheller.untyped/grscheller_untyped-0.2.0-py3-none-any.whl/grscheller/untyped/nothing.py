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

"""#### Singleton Representing a Non-existing Value

A version of grscheller.fp.nada geared for use in less strictly
typed code.
"""

from __future__ import annotations
from typing import Any, Callable, Iterator, NewType

__all__ = [ 'Nothing', 'nothing' ]

_S = NewType('_S', tuple[tuple[()], tuple[tuple[()], tuple[tuple[()], None]]])
_sentinel: _S = _S(((), ((), ((), None))))

class Nothing():
    """
    #### Singleton semantically represents a missing value.

    * singleton nothing: nothing = Nothing() represents a non-existent value
    * returns itself for arbitrary method calls
    * returns itself if called as a Callable with arbitrary arguments
    * interpreted as an empty container by standard Python functions
    * comparison ops compare true only when 2 non-missing values compare true
      * when compared to itself behaves somewhat like IEEE Float NAN's
        * `nothing is nothing` is true
        * `nothing == nothing` is false
        * `nothing != nothing` is true
    """
    __slots__ = ()

    def __new__(cls) -> Nothing:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Nothing, cls).__new__(cls)
            cls._hash = hash((_sentinel, (_sentinel,)))
        return cls.instance

    def __iter__(self) -> Iterator:
        return iter(())

    def __hash__(self) -> int:
        return self._hash

    def __repr__(self) -> str:
        return 'nothing'

    def __bool__(self) -> bool:
        return False

    def __len__(self) -> int:
        return 0

    def __add__(self, right: Any) -> Nothing:
        return Nothing()

    def __radd__(self, left: Any) -> Nothing:
        return Nothing()

    def __mul__(self, right: Any) -> Nothing:
        return Nothing()

    def __rmul__(self, left: Any) -> Nothing:
        return Nothing()

    def __eq__(self, right: Any) -> bool:
        """Never equals anything, even itself."""
        return False

    def __ne__(self, right: Any) -> bool:
        """Always does not equal anything, even itself."""
        return True

    def __ge__(self, right: Any) -> bool:
        return False

    def __gt__(self, right: Any) -> bool:
        return False

    def __le__(self, right: Any) -> bool:
        return False

    def __lt__(self, right: Any) -> bool:
        return False

    def __getitem__(self, index: int|slice) -> Any:
        return Nothing()

    def __setitem__(self, index: int|slice, item: Any) -> None:
        return

    def __call__(*args: Any, **kwargs: Any) -> Any:
        return Nothing()

    def __getattr__(self, name: str) -> Callable[[Any], Any]:
        """Comment out for doc generation, pdoc gags on this method."""
        def method(*args: Any, **kwargs: Any) -> Any:
            return Nothing()
        return method

    def get(self, alt: Any=_sentinel) -> Any:
        """
        ##### Get an alternate value, defaults to Nada().
        """
        if alt == _sentinel:
            return Nothing()
        else:
            return alt

nothing = Nothing()
