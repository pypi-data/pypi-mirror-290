from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

BUNDLED: ResourceEntryFlag
COMPRESSED: ResourceEntryFlag
DESCRIPTOR: _descriptor.FileDescriptor
ENCRYPTED: ResourceEntryFlag
EXCLUDED: ResourceEntryFlag
HASH_MD5: HashAlgorithm
HASH_SHA1: HashAlgorithm
HASH_SHA256: HashAlgorithm
HASH_SHA512: HashAlgorithm
HASH_UNKNOWN: HashAlgorithm
SIGN_RSA: SignAlgorithm
SIGN_UNKNOWN: SignAlgorithm

class HashDigest(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: ClassVar[int]
    data: bytes
    def __init__(self, data: Optional[bytes] = ...) -> None: ...

class ManifestData(_message.Message):
    __slots__ = ["engine_versions", "header", "resources"]
    ENGINE_VERSIONS_FIELD_NUMBER: ClassVar[int]
    HEADER_FIELD_NUMBER: ClassVar[int]
    RESOURCES_FIELD_NUMBER: ClassVar[int]
    engine_versions: _containers.RepeatedCompositeFieldContainer[HashDigest]
    header: ManifestHeader
    resources: _containers.RepeatedCompositeFieldContainer[ResourceEntry]
    def __init__(self, header: Optional[Union[ManifestHeader, Mapping]] = ..., engine_versions: Optional[Iterable[Union[HashDigest, Mapping]]] = ..., resources: Optional[Iterable[Union[ResourceEntry, Mapping]]] = ...) -> None: ...

class ManifestFile(_message.Message):
    __slots__ = ["archive_identifier", "data", "signature", "version"]
    ARCHIVE_IDENTIFIER_FIELD_NUMBER: ClassVar[int]
    DATA_FIELD_NUMBER: ClassVar[int]
    SIGNATURE_FIELD_NUMBER: ClassVar[int]
    VERSION_FIELD_NUMBER: ClassVar[int]
    archive_identifier: bytes
    data: bytes
    signature: bytes
    version: int
    def __init__(self, data: Optional[bytes] = ..., signature: Optional[bytes] = ..., archive_identifier: Optional[bytes] = ..., version: Optional[int] = ...) -> None: ...

class ManifestHeader(_message.Message):
    __slots__ = ["project_identifier", "resource_hash_algorithm", "signature_hash_algorithm", "signature_sign_algorithm"]
    PROJECT_IDENTIFIER_FIELD_NUMBER: ClassVar[int]
    RESOURCE_HASH_ALGORITHM_FIELD_NUMBER: ClassVar[int]
    SIGNATURE_HASH_ALGORITHM_FIELD_NUMBER: ClassVar[int]
    SIGNATURE_SIGN_ALGORITHM_FIELD_NUMBER: ClassVar[int]
    project_identifier: HashDigest
    resource_hash_algorithm: HashAlgorithm
    signature_hash_algorithm: HashAlgorithm
    signature_sign_algorithm: SignAlgorithm
    def __init__(self, resource_hash_algorithm: Optional[Union[HashAlgorithm, str]] = ..., signature_hash_algorithm: Optional[Union[HashAlgorithm, str]] = ..., signature_sign_algorithm: Optional[Union[SignAlgorithm, str]] = ..., project_identifier: Optional[Union[HashDigest, Mapping]] = ...) -> None: ...

class ResourceEntry(_message.Message):
    __slots__ = ["compressed_size", "dependants", "flags", "hash", "size", "url", "url_hash"]
    COMPRESSED_SIZE_FIELD_NUMBER: ClassVar[int]
    DEPENDANTS_FIELD_NUMBER: ClassVar[int]
    FLAGS_FIELD_NUMBER: ClassVar[int]
    HASH_FIELD_NUMBER: ClassVar[int]
    SIZE_FIELD_NUMBER: ClassVar[int]
    URL_FIELD_NUMBER: ClassVar[int]
    URL_HASH_FIELD_NUMBER: ClassVar[int]
    compressed_size: int
    dependants: _containers.RepeatedScalarFieldContainer[int]
    flags: int
    hash: HashDigest
    size: int
    url: str
    url_hash: int
    def __init__(self, hash: Optional[Union[HashDigest, Mapping]] = ..., url: Optional[str] = ..., url_hash: Optional[int] = ..., size: Optional[int] = ..., compressed_size: Optional[int] = ..., flags: Optional[int] = ..., dependants: Optional[Iterable[int]] = ...) -> None: ...

class HashAlgorithm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SignAlgorithm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ResourceEntryFlag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
