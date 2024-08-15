from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExecutionData(_message.Message):
    __slots__ = ("versions", "simulation", "configuration")
    class Versions(_message.Message):
        __slots__ = ("fameProtobuf", "fameIo", "fameCore", "python", "jvm", "os")
        FAMEPROTOBUF_FIELD_NUMBER: _ClassVar[int]
        FAMEIO_FIELD_NUMBER: _ClassVar[int]
        FAMECORE_FIELD_NUMBER: _ClassVar[int]
        PYTHON_FIELD_NUMBER: _ClassVar[int]
        JVM_FIELD_NUMBER: _ClassVar[int]
        OS_FIELD_NUMBER: _ClassVar[int]
        fameProtobuf: str
        fameIo: str
        fameCore: str
        python: str
        jvm: str
        os: str
        def __init__(self, fameProtobuf: _Optional[str] = ..., fameIo: _Optional[str] = ..., fameCore: _Optional[str] = ..., python: _Optional[str] = ..., jvm: _Optional[str] = ..., os: _Optional[str] = ...) -> None: ...
    class Simulation(_message.Message):
        __slots__ = ("start", "durationInMS", "ticks")
        START_FIELD_NUMBER: _ClassVar[int]
        DURATIONINMS_FIELD_NUMBER: _ClassVar[int]
        TICKS_FIELD_NUMBER: _ClassVar[int]
        start: str
        durationInMS: int
        ticks: int
        def __init__(self, start: _Optional[str] = ..., durationInMS: _Optional[int] = ..., ticks: _Optional[int] = ...) -> None: ...
    class Configuration(_message.Message):
        __slots__ = ("coreCount", "outputProcess", "outputInterval")
        CORECOUNT_FIELD_NUMBER: _ClassVar[int]
        OUTPUTPROCESS_FIELD_NUMBER: _ClassVar[int]
        OUTPUTINTERVAL_FIELD_NUMBER: _ClassVar[int]
        coreCount: int
        outputProcess: int
        outputInterval: int
        def __init__(self, coreCount: _Optional[int] = ..., outputProcess: _Optional[int] = ..., outputInterval: _Optional[int] = ...) -> None: ...
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    versions: ExecutionData.Versions
    simulation: ExecutionData.Simulation
    configuration: ExecutionData.Configuration
    def __init__(self, versions: _Optional[_Union[ExecutionData.Versions, _Mapping]] = ..., simulation: _Optional[_Union[ExecutionData.Simulation, _Mapping]] = ..., configuration: _Optional[_Union[ExecutionData.Configuration, _Mapping]] = ...) -> None: ...
