# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from typing import cast
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import Self

import pydantic
import pydantic.fields

from canonical.lib.types import ResourceName
from .apimodelfieldinfo import APIModelFieldInfo
from .apimodelinspector import APIModelInspector
from .builders import APIModelClassBuilder


__all__: list[str] = [
    'APIModel'
]


class APIModel(pydantic.BaseModel):
    inspector: ClassVar[APIModelInspector] = APIModelInspector()
    model_config = {'populate_by_name': True}
    __builder__: ClassVar[APIModelClassBuilder[Any] | None] = None
    __builder_class__: ClassVar[type[APIModelClassBuilder[Any]]] = APIModelClassBuilder
    __create_model__: ClassVar[type[pydantic.BaseModel]]
    __update_model__: ClassVar[type[pydantic.BaseModel]]
    __stored_model__: ClassVar[type[Self]]
    __output_model__: ClassVar[type[pydantic.BaseModel]]
    __origin_fields__: ClassVar[dict[str, APIModelFieldInfo]] = {}
    __metadata_class__: ClassVar[type[pydantic.BaseModel] | None] = None
    __mode__: ClassVar[str] = 'domain'
    __namespaced__: ClassVar[bool] = False
    __params__: ClassVar[dict[str, Any]]
    _dirty: bool = pydantic.PrivateAttr(default=False)
    _parent: pydantic.BaseModel | None = pydantic.PrivateAttr(default=None)

    @classmethod
    def build_class(cls, builder: Any, **kwargs: Any):
        builder = cast(APIModelClassBuilder['APIModel'], builder)
        builder.contribute_annotations()

    @classmethod
    def contribute_to_class(
        cls,
        parent: type[APIModel],
        attname: str,
        field: pydantic.fields.FieldInfo
    ) -> None:
        """Hook to execute when this model is an attribute on
        a new class.
        """
        pass

    @classmethod
    def model_input(cls, data: dict[str, Any]):
        return cls.__create_model__.model_validate(data)

    @classmethod
    def model_input_json(cls, buf: str | bytes):
        return cls.__create_model__.model_validate_json(buf)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        if not cls.inspector.is_concrete(cls):
            return
        origin = cls.__pydantic_generic_metadata__.get('origin')
        if kwargs.get('abstract') or origin is not None:
            return
        if kwargs:
            cls.__namespaced__ = kwargs.pop('namespaced', cls.__namespaced__)
        cls.__builder__ = cls.__builder_class__(
            model=cls,
            metadata_class=cls.__metadata_class__,
            namespaced=cls.__namespaced__,
            **kwargs
        )
        cls.build_class(cls.__builder__, **kwargs)
        cls.__builder__.construct()

    def __init_subclass__(cls, **kwargs: Any):
        for Base in cls.__bases__:
            if Base in (pydantic.BaseModel, Generic):
                super().__init_subclass__()
                continue
            #super().__init_subclass__(**kwargs)

    @property
    def parent(self) -> APIModel | None:
        return cast(APIModel, self._parent)

    def add_to_parent(self, parent: APIModel):
        self._parent = parent

    def get_resource_name(self) -> ResourceName:
        """Return the :class:`ResourceName` where the
        resource may be found."""
        raise NotImplementedError

    def get_url(self) -> str:
        """Return the URL where the resource may be found."""
        raise NotImplementedError

    def is_attached(self) -> bool:
        return self._parent is not None

    def model_post_init(self, _: Any) -> None:
        for attname in self.model_fields:
            v = getattr(self, attname)
            if not isinstance(v, APIModel):
                continue
            v.add_to_parent(self)

    def replace(self, instance: pydantic.BaseModel):
        """Replaces all fields of `self` with corresponding fields of
        `instance.
        """
        for attname, field in self.model_fields.items():
            if attname not in instance.model_fields:
                continue
            adapter = pydantic.TypeAdapter(field.annotation)
            ours = getattr(self, attname)
            theirs = cleaned = getattr(instance, attname, None)
            if not isinstance(theirs, pydantic.BaseModel):
                cleaned = adapter.validate_python(theirs)
            if not field.frozen:
                # TODO: must actually raise an exception if the value is
                # different, but it needs to integrate with FastAPIs
                # request validation.
                if isinstance(cleaned, pydantic.BaseModel) and isinstance(ours, APIModel):
                    ours.replace(cleaned)
                    continue
                self.replace_field(attname, ours, theirs)

    def replace_field(self, attname: str, ours: Any, theirs: Any):
        if ours != theirs:
            setattr(self, attname, theirs)