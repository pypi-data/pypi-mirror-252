# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast
from typing import Any
from typing import ClassVar
from typing import Self
from typing import TypeVar

from .apiresource import APIResource
from .apiversionedmeta import APIVersionedMeta
from .bases import BaseRootResource
from .builders import APIRootResourceClassBuilder


T = TypeVar('T', bound=APIResource[Any])


class APIRootResource(BaseRootResource[T]):
    __builder_class__ = APIRootResourceClassBuilder
    __descriptor_class__: ClassVar[type[APIVersionedMeta[Any]]] = APIVersionedMeta
    __meta__: ClassVar[Any]

    @classmethod
    def model_input(cls, data: dict[str, Any]):
        return cls.__create_model__.model_validate(data)

    def __init_subclass__(cls, **kwargs: Any):
        if kwargs:
            kwargs.setdefault('kind', cls.__name__)
            kwargs.setdefault('namespaced', False)
            meta = cls.__descriptor_class__.model_validate({
                **kwargs,
                'root': True
            })
            meta.contribute_to_class(cls, {})
        return super().__init_subclass__()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        if kwargs and not kwargs.get('abstract'):
            cls.__builder__ = cls.__builder_class__(cls, **kwargs)
            cls.build_class(cast(Any, cls.__builder__))
        return super().__pydantic_init_subclass__(**kwargs)

    @classmethod
    def build_class(cls, builder: APIRootResourceClassBuilder[Self]) -> None:
        cls.__create_model__ = builder.build_create_model()

    @classmethod
    def is_namespaced(cls):
        return cls.__namespaced__

    @property
    def key(self):
        return self.root.get_object_ref(self.__meta__).with_model(type(self))

    @property
    def kind(self) -> str:
        return self.root.kind

    @property
    def metadata(self):
        return self.root.metadata

    def update(self, old: Self | None) -> tuple[Self, bool]:
        if old is None:
            return self.model_validate(self.model_dump()), True
        root, changed = self.root.update(old.root)
        return self.model_validate(root.model_dump()), changed