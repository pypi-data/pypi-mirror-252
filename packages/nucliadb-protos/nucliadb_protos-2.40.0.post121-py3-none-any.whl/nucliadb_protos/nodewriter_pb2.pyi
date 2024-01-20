"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import nucliadb_protos.noderesources_pb2
import nucliadb_protos.utils_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions
from nucliadb_protos.noderesources_pb2 import (
    EmptyQuery as EmptyQuery,
    EmptyResponse as EmptyResponse,
    IndexMetadata as IndexMetadata,
    IndexParagraph as IndexParagraph,
    IndexParagraphs as IndexParagraphs,
    NodeMetadata as NodeMetadata,
    ParagraphMetadata as ParagraphMetadata,
    Position as Position,
    Resource as Resource,
    ResourceID as ResourceID,
    SentenceMetadata as SentenceMetadata,
    Shard as Shard,
    ShardCleaned as ShardCleaned,
    ShardCreated as ShardCreated,
    ShardId as ShardId,
    ShardIds as ShardIds,
    ShardMetadata as ShardMetadata,
    TextInformation as TextInformation,
    VectorSentence as VectorSentence,
    VectorSetID as VectorSetID,
    VectorSetList as VectorSetList,
)

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _TypeMessage:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _TypeMessageEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_TypeMessage.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    CREATION: _TypeMessage.ValueType  # 0
    DELETION: _TypeMessage.ValueType  # 1

class TypeMessage(_TypeMessage, metaclass=_TypeMessageEnumTypeWrapper):
    """Implemented at nucliadb_object_storage"""

CREATION: TypeMessage.ValueType  # 0
DELETION: TypeMessage.ValueType  # 1
global___TypeMessage = TypeMessage

class _IndexMessageSource:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _IndexMessageSourceEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_IndexMessageSource.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PROCESSOR: _IndexMessageSource.ValueType  # 0
    WRITER: _IndexMessageSource.ValueType  # 1

class IndexMessageSource(_IndexMessageSource, metaclass=_IndexMessageSourceEnumTypeWrapper): ...

PROCESSOR: IndexMessageSource.ValueType  # 0
WRITER: IndexMessageSource.ValueType  # 1
global___IndexMessageSource = IndexMessageSource

@typing_extensions.final
class OpStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Status:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _StatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[OpStatus._Status.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        OK: OpStatus._Status.ValueType  # 0
        WARNING: OpStatus._Status.ValueType  # 1
        ERROR: OpStatus._Status.ValueType  # 2

    class Status(_Status, metaclass=_StatusEnumTypeWrapper): ...
    OK: OpStatus.Status.ValueType  # 0
    WARNING: OpStatus.Status.ValueType  # 1
    ERROR: OpStatus.Status.ValueType  # 2

    STATUS_FIELD_NUMBER: builtins.int
    DETAIL_FIELD_NUMBER: builtins.int
    FIELD_COUNT_FIELD_NUMBER: builtins.int
    PARAGRAPH_COUNT_FIELD_NUMBER: builtins.int
    SENTENCE_COUNT_FIELD_NUMBER: builtins.int
    SHARD_ID_FIELD_NUMBER: builtins.int
    status: global___OpStatus.Status.ValueType
    detail: builtins.str
    field_count: builtins.int
    paragraph_count: builtins.int
    sentence_count: builtins.int
    shard_id: builtins.str
    def __init__(
        self,
        *,
        status: global___OpStatus.Status.ValueType = ...,
        detail: builtins.str = ...,
        field_count: builtins.int = ...,
        paragraph_count: builtins.int = ...,
        sentence_count: builtins.int = ...,
        shard_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["detail", b"detail", "field_count", b"field_count", "paragraph_count", b"paragraph_count", "sentence_count", b"sentence_count", "shard_id", b"shard_id", "status", b"status"]) -> None: ...

global___OpStatus = OpStatus

@typing_extensions.final
class IndexMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NODE_FIELD_NUMBER: builtins.int
    SHARD_FIELD_NUMBER: builtins.int
    TXID_FIELD_NUMBER: builtins.int
    RESOURCE_FIELD_NUMBER: builtins.int
    TYPEMESSAGE_FIELD_NUMBER: builtins.int
    REINDEX_ID_FIELD_NUMBER: builtins.int
    PARTITION_FIELD_NUMBER: builtins.int
    STORAGE_KEY_FIELD_NUMBER: builtins.int
    KBID_FIELD_NUMBER: builtins.int
    SOURCE_FIELD_NUMBER: builtins.int
    node: builtins.str
    shard: builtins.str
    """physical shard message is for"""
    txid: builtins.int
    resource: builtins.str
    typemessage: global___TypeMessage.ValueType
    reindex_id: builtins.str
    partition: builtins.str
    storage_key: builtins.str
    kbid: builtins.str
    source: global___IndexMessageSource.ValueType
    def __init__(
        self,
        *,
        node: builtins.str = ...,
        shard: builtins.str = ...,
        txid: builtins.int = ...,
        resource: builtins.str = ...,
        typemessage: global___TypeMessage.ValueType = ...,
        reindex_id: builtins.str = ...,
        partition: builtins.str | None = ...,
        storage_key: builtins.str = ...,
        kbid: builtins.str = ...,
        source: global___IndexMessageSource.ValueType = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_partition", b"_partition", "partition", b"partition"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_partition", b"_partition", "kbid", b"kbid", "node", b"node", "partition", b"partition", "reindex_id", b"reindex_id", "resource", b"resource", "shard", b"shard", "source", b"source", "storage_key", b"storage_key", "txid", b"txid", "typemessage", b"typemessage"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_partition", b"_partition"]) -> typing_extensions.Literal["partition"] | None: ...

global___IndexMessage = IndexMessage

@typing_extensions.final
class GarbageCollectorResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Status:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _StatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[GarbageCollectorResponse._Status.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        OK: GarbageCollectorResponse._Status.ValueType  # 0
        TRY_LATER: GarbageCollectorResponse._Status.ValueType  # 1

    class Status(_Status, metaclass=_StatusEnumTypeWrapper): ...
    OK: GarbageCollectorResponse.Status.ValueType  # 0
    TRY_LATER: GarbageCollectorResponse.Status.ValueType  # 1

    STATUS_FIELD_NUMBER: builtins.int
    status: global___GarbageCollectorResponse.Status.ValueType
    def __init__(
        self,
        *,
        status: global___GarbageCollectorResponse.Status.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["status", b"status"]) -> None: ...

global___GarbageCollectorResponse = GarbageCollectorResponse

@typing_extensions.final
class NewShardRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SIMILARITY_FIELD_NUMBER: builtins.int
    KBID_FIELD_NUMBER: builtins.int
    RELEASE_CHANNEL_FIELD_NUMBER: builtins.int
    similarity: nucliadb_protos.utils_pb2.VectorSimilarity.ValueType
    kbid: builtins.str
    release_channel: nucliadb_protos.utils_pb2.ReleaseChannel.ValueType
    def __init__(
        self,
        *,
        similarity: nucliadb_protos.utils_pb2.VectorSimilarity.ValueType = ...,
        kbid: builtins.str = ...,
        release_channel: nucliadb_protos.utils_pb2.ReleaseChannel.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["kbid", b"kbid", "release_channel", b"release_channel", "similarity", b"similarity"]) -> None: ...

global___NewShardRequest = NewShardRequest

@typing_extensions.final
class NewVectorSetRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    SIMILARITY_FIELD_NUMBER: builtins.int
    @property
    def id(self) -> nucliadb_protos.noderesources_pb2.VectorSetID: ...
    similarity: nucliadb_protos.utils_pb2.VectorSimilarity.ValueType
    def __init__(
        self,
        *,
        id: nucliadb_protos.noderesources_pb2.VectorSetID | None = ...,
        similarity: nucliadb_protos.utils_pb2.VectorSimilarity.ValueType = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["id", b"id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["id", b"id", "similarity", b"similarity"]) -> None: ...

global___NewVectorSetRequest = NewVectorSetRequest
