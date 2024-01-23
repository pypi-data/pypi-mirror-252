# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import ClassVar

import pydantic

from .builder import BaseBuilder


class BaseResource:
    __builder__: ClassVar[BaseBuilder[Any] | None] = None
    __builder_class__: ClassVar[type[BaseBuilder[Any]]]
    __create_model__: ClassVar[type[pydantic.BaseModel]]
    __namespaced__: ClassVar[bool]

    def replacable(self) -> bool:
        raise NotImplementedError

    def replace(self, instance: pydantic.BaseModel) -> None:
        raise NotImplementedError