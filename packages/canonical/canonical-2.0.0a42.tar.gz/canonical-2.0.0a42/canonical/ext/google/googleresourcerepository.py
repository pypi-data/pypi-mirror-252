# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import logging
from typing import AsyncIterable
from typing import Any
from typing import Iterable
from typing import Mapping
from typing import Any
from typing import TypeVar

import pydantic
from google.cloud.datastore import Client

from canonical.protocols import ITransaction
from canonical.ext.api import APIVersionedMeta
from canonical.ext.api import DefaultInspector
from canonical.ext.api import ObjectReference
from canonical.ext.api import UIDReference
from canonical.ext.api.bases import BaseReference
from canonical.ext.api.annotations import Reference
from canonical.ext.api.annotations import APIResourceType
from canonical.ext.resource import BaseResourceRepository
from .basedatastorestorage import BaseDatastoreStorage
from .protocols import IDatastoreKey
from .protocols import IDatastoreEntity


T = TypeVar('T', bound=APIResourceType)


class GoogleDatastoreResourceRepository(BaseResourceRepository):
    backend: BaseDatastoreStorage
    inspector = DefaultInspector
    logger: logging.Logger = logging.getLogger('uvicorn')

    def __init__(self, backend: BaseDatastoreStorage) -> None:
        self.backend = backend

    def all(self, model: type[T], namespace: str | None = None) -> AsyncIterable[T]:
        return self.query(model=model, namespace=namespace)

    def get_entity_name(self, key: ObjectReference | UIDReference | type[T] | APIVersionedMeta[Any]) -> str:
        if not isinstance(key, (ObjectReference, UIDReference, APIVersionedMeta)):
            key = self.inspector.inspect(key)
        name = f'{key.api_group}/{key.kind}'
        if not key.api_group:
            name = key.kind
        return name

    def model_factory(
        self,
        key: IDatastoreKey,
        entity: Mapping[str, Any],
        model: type[T]
    ) -> T:
        return model.model_validate(dict(entity))

    def resource_key(
        self,
        key: Reference,
        parent: IDatastoreKey |None = None,
        namespace: str | None = None
    ) -> IDatastoreKey:
        assert isinstance(key, (ObjectReference, UIDReference))
        return self.backend.entity_key(
            self.get_entity_name(key),
            key.as_name(),
            parent=parent,
            namespace=namespace
        )

    def query(
        self,
        model: type[T],
        filters: Iterable[tuple[str, str, Any]] | None = None,
        sort: Iterable[str] | None = None,
        namespace: str | None = None,
        limit: int | None = None,
        kind: str | None = None,
        page_size: int = 10,
        keys: list[Any] | None = None,
        **_: Any
    ) -> AsyncIterable[T]:
        return self.backend.query(
            model=model,
            filters=filters,
            sort=sort,
            namespace=namespace,
            limit=limit,
            kind=kind or self.get_entity_name(model),
            page_size=page_size,
            keys=keys
        )
        

    async def allocate(self, obj: type[APIResourceType]) -> int:
        k = self.get_entity_name(obj)
        i = await self.backend.allocate_identifier(k)
        self.logger.info("Allocated identifier (kind: %s, uid: %s)", k, i)
        return i

    async def exists(self, key: Reference | Iterable[tuple[str, str, Any]], model: type[T]) -> bool:
        assert isinstance(key, BaseReference), type(key)
        q = self.backend.query(
            model=model,
            namespace=key.get_namespace(),
            keys=[self.resource_key(key, namespace=key.get_namespace())],
            page_size=1
        )
        return await q.exists()

    async def get_entity_by_key(self, key: IDatastoreKey) -> IDatastoreEntity | None:
        return await self.backend.get_entity_by_key(key)

    async def reference(self, key: Reference, model: type[T]) -> T | None:
        k = self.resource_key(key, namespace=key.get_namespace())
        e = await self.get_entity_by_key(key=k)
        instance = None
        if e is not None:
            instance = await self.restore(self.model_factory(k, dict(e), model))
        return instance

    def transaction(self, transaction: Any | None = None):
        return self.backend.transaction(transaction)

    async def persist_entity(
        self,
        client: Client | ITransaction,
        entity: IDatastoreEntity
    ) -> IDatastoreEntity:
        return await self.backend.run_in_executor(functools.partial(client.put, entity)) # type: ignore

    async def put(
        self,
        key: Reference,
        dao: pydantic.BaseModel,
        transaction: Any | None = None
    ) -> None:
        await self.persist_entity(
            client=transaction or self.backend.client,
            entity=self.backend.entity_factory(
                key=self.resource_key(key),
                obj=dao
            )
        )