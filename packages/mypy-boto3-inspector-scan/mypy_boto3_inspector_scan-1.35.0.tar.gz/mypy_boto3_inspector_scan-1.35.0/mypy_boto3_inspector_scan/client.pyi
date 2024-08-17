"""
Type annotations for inspector-scan service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector_scan/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_inspector_scan.client import InspectorscanClient

    session = Session()
    client: InspectorscanClient = session.client("inspector-scan")
    ```
"""

from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .literals import OutputFormatType
from .type_defs import ScanSbomResponseTypeDef

__all__ = ("InspectorscanClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class InspectorscanClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector-scan.html#Inspectorscan.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector_scan/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        InspectorscanClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector-scan.html#Inspectorscan.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector_scan/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector-scan.html#Inspectorscan.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector_scan/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector-scan.html#Inspectorscan.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector_scan/client/#close)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector-scan.html#Inspectorscan.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector_scan/client/#generate_presigned_url)
        """

    def scan_sbom(
        self, *, sbom: Mapping[str, Any], outputFormat: OutputFormatType = ...
    ) -> ScanSbomResponseTypeDef:
        """
        Scans a provided CycloneDX 1.5 SBOM and reports on any vulnerabilities
        discovered in that
        SBOM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector-scan.html#Inspectorscan.Client.scan_sbom)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector_scan/client/#scan_sbom)
        """
