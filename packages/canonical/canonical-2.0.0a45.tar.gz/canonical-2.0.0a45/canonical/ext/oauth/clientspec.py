# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Generic
from typing import TypeVar

import pydantic

from canonical.ext.api import APIModelField
from canonical.ext.api import ResourceSpec
from canonical.ext.crypto import EncryptionResult


RefType = TypeVar('RefType')


class ClientSpec(ResourceSpec, Generic[RefType]):
    client_id: str = pydantic.Field(
        default=...,
        alias='clientId',
        title='Client ID',
        description=(
            "The OAuth 2.x/OpenID Connect client identifier."
        ),
        max_length=64
    )

    client_secret: EncryptionResult | str = APIModelField(
        default=...,
        alias='clientSecret',
        title='Client secret',
        description=(
            "The OAuth 2.x/OpenID Connect client secret."
        ),
        max_length=64,
        encrypt=True
    )

    provider: RefType = pydantic.Field(
        default=...,
        description=(
            "A local reference to an OAuth 2.x/OpenID Connect provider."
        )
    )

    def must_encrypt(self, attname: str) -> bool:
        return attname == 'client_secret'