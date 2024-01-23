# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from typing import Any
from typing import AsyncContextManager
from typing import AsyncIterable
from typing import cast
from typing import overload
from typing import Generator
from typing import Iterable
from typing import Literal
from typing import TypeVar
from typing import TYPE_CHECKING

import pydantic
from canonical.exceptions import DoesNotExist
from canonical.exceptions import Duplicate
from canonical.exceptions import Stale
from ..annotations import APIResourceType
from ..annotations import Reference
if TYPE_CHECKING:
    from ..objectmeta import ObjectMeta


B = TypeVar('B')
T = TypeVar('T', bound=APIResourceType)


class BaseResourceRepository:
    DoesNotExist = DoesNotExist
    Duplicate = Duplicate
    Stale = Stale

    class Cursor(AsyncIterable[B]):
        def __await__(self) -> Generator[Any, Any, list[B]]:
            ...

    def all(self, model: type[B]) -> Cursor[B]:
        raise NotImplementedError

    def query(
        self,
        model: type[B],
        filters: Iterable[tuple[str, str, Any]] | None = None,
        sort: Iterable[str] | None = None,
        namespace: str | None = None,
        limit: int | None = None,
        kind: str | None = None,
        page_size: int = 10,
        keys: list[Any] | None = None,
        **_: Any
    ) -> Cursor[B]:
        raise NotImplementedError

    async def allocate(self, obj: type[Any]) -> int:
        raise NotImplementedError

    async def exists(
        self,
        key: Reference | Iterable[tuple[str, str, Any]],
        model: Any
    ) -> bool:
        raise NotImplementedError

    @overload
    async def get(
        self,
        key: Reference,
        model: type[T],
        *,
        require: Literal[True]
    ) -> T:
        ...

    @overload
    async def get(
        self,
        key: Reference,
        model: type[T] | None,
        *,
        require: Literal[True] = True
    ) -> T:
        ...

    @overload
    async def get(
        self,
        key: Reference,
        model: type[T] | None,
        *,
        require: Literal[False] = False
    ) -> T | None:
        ...

    async def get(
        self,
        key: Reference,
        model: type[T] | None = None,
        *,
        require: bool = True
    ) -> T | None:
        model = cast(type[T] | None, key.get_model())
        if model is None:
            raise TypeError(
                f"Model should be attached to {type(key).__name__} "
                "or provided with the `model` parameter."
            )
        obj = await self.reference(key, model)
        if obj is None and require:
            raise self.DoesNotExist
        return cast(T | None, obj)

    async def persist(
        self,
        model: type[pydantic.BaseModel],
        instance: T,
        transaction: Any = None
    ) -> T:
        assert instance.metadata.is_attached()
        new = instance
        try:
            old = await self.get(instance.key, type(instance))
        except self.DoesNotExist:
            old = None
        new = await self.persist_model(instance, old=old, transaction=transaction)
        return new

    async def persist_metadata(
        self,
        metadata: ObjectMeta[Any],
        transaction: Any | None = None
    ) -> None:
        dao = metadata.dao()
        await self.put(dao.key, dao, transaction=transaction)

    async def persist_model(
        self,
        new: T,
        old: T | None = None,
        transaction: Any = None
    ) -> T:
        if old and old.metadata.generation != new.metadata.generation:
            raise Stale
        updated, changed = new.update(old) # type: ignore
        if not changed:
            return new
        await self.put(updated.key, updated, transaction=transaction)
        await self.persist_metadata(updated.metadata, transaction=transaction)
        return updated

    async def put(
        self,
        key: Reference,
        dao: pydantic.BaseModel,
        transaction: Any | None = None
    ) -> None:
        raise NotImplementedError(key)

    async def reference(self, key: Reference, model: type[T]) -> T | None:
        raise NotImplementedError

    async def restore(self, instance: T) -> T:
        return instance

    async def on_persisted(self, new: T, old: T | None, transaction: Any | None = None):
        pass

    def transaction(self, transaction: Any | None = None) -> AsyncContextManager[Any]:
        raise NotImplementedError