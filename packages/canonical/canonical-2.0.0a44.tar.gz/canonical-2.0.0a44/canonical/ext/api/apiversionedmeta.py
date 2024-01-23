# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import Literal
from typing import TypeVar
from typing import TYPE_CHECKING

import pydantic
from pydantic.fields import FieldInfo

from .apimodelinspector import APIModelInspector
from .types import APIVersion
if TYPE_CHECKING:
    from .apimodel import APIModel


T = TypeVar('T', bound='APIModel')


class APIVersionedMeta(pydantic.BaseModel, Generic[T]):
    model_config = {'populate_by_name': True}
    inspector: ClassVar[APIModelInspector] = APIModelInspector()
    _model: type[T] | None = pydantic.PrivateAttr(default=None)

    #api_version: str
    api_group: str = pydantic.Field(alias='group')
    #base_path: str
    kind: str
    namespaced: bool
    plural: str | None
    short: str | None = None
    version: str
    root: bool = False

    @property
    def api_version(self) -> APIVersion:
        v = f'{self.api_group}/{self.version}'\
            if self.api_group\
            else self.version
        return APIVersion(v)

    @property
    def base_path(self) -> str:
        p = f'{self.api_version}'
        if self.namespaced:
            p = f'{p}/namespaces/{{namespace}}'
        return f'{p}/{self.plural}'

    @property
    def model(self) -> type[T]:
        assert self._model
        return self.model

    def contribute_to_class(
        self,
        cls: type[T],
        fields: dict[str, FieldInfo],
        root: tuple[type[Any], ...] | None = None
    ):
        setattr(cls, '__meta__', self)
        if fields:
            fields['api_version'].annotation = Literal[f'{self.api_version}']
            fields['api_version'].default = self.api_version
            fields['kind'].annotation = Literal[f'{self.kind}']
            fields['kind'].default = self.kind

    def get_url(self, detail: bool = False, subpath: str | None = None) -> str:
        path = f'{self.base_path}'
        if detail:
            path = f'{path}/{{name}}'
        path = f'/{path}'
        if subpath:
            path = f'{path}{subpath}'
        return path