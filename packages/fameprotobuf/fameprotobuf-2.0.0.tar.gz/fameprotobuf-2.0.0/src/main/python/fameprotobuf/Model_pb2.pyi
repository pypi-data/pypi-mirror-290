from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModelData(_message.Message):
    __slots__ = ("name", "version", "packages")
    class JavaPackages(_message.Message):
        __slots__ = ("agent", "dataItem", "portable")
        AGENT_FIELD_NUMBER: _ClassVar[int]
        DATAITEM_FIELD_NUMBER: _ClassVar[int]
        PORTABLE_FIELD_NUMBER: _ClassVar[int]
        agent: _containers.RepeatedScalarFieldContainer[str]
        dataItem: _containers.RepeatedScalarFieldContainer[str]
        portable: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, agent: _Optional[_Iterable[str]] = ..., dataItem: _Optional[_Iterable[str]] = ..., portable: _Optional[_Iterable[str]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PACKAGES_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    packages: ModelData.JavaPackages
    def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ..., packages: _Optional[_Union[ModelData.JavaPackages, _Mapping]] = ...) -> None: ...
