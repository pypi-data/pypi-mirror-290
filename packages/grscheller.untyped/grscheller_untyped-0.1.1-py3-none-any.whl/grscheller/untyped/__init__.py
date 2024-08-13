# Copyright 2024 Geoffrey R. Scheller
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

"""
## Untyped modules

Useful modules I found difficult to implement in a strictly typed manner. Not
intended to be used with strictly typed code.

### module `grscheller.untyped.nothing`

#### class `Nothing()`

Class representing a non-existent value.

* Nothing() is a singleton
* Nothing() instances should be compared with the `is` operator, not `==`
* my[py] becomes problematic when this module is used in a strict typing context
  * implementing this module with strict typing is vastly more complicated
  * in client code my[py] keeps warning me about what I am doing
  * lots of type annotations needed, feels like early Java

#### instance variable: `nothing`

* nothing: Nothing = Nothing() is a singleton

---

"""
__version__ = "0.1.1"
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"
