from fameprotobuf import Contract_pb2 as _Contract_pb2
from fameprotobuf import Field_pb2 as _Field_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InputData(_message.Message):
    __slots__ = ("runId", "simulation", "timeSeries", "agent", "contract", "schema", "stringSets")
    class SimulationParam(_message.Message):
        __slots__ = ("startTime", "stopTime", "randomSeed")
        STARTTIME_FIELD_NUMBER: _ClassVar[int]
        STOPTIME_FIELD_NUMBER: _ClassVar[int]
        RANDOMSEED_FIELD_NUMBER: _ClassVar[int]
        startTime: int
        stopTime: int
        randomSeed: int
        def __init__(self, startTime: _Optional[int] = ..., stopTime: _Optional[int] = ..., randomSeed: _Optional[int] = ...) -> None: ...
    class TimeSeriesDao(_message.Message):
        __slots__ = ("seriesId", "seriesName", "timeSteps", "values")
        SERIESID_FIELD_NUMBER: _ClassVar[int]
        SERIESNAME_FIELD_NUMBER: _ClassVar[int]
        TIMESTEPS_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        seriesId: int
        seriesName: str
        timeSteps: _containers.RepeatedScalarFieldContainer[int]
        values: _containers.RepeatedScalarFieldContainer[float]
        def __init__(self, seriesId: _Optional[int] = ..., seriesName: _Optional[str] = ..., timeSteps: _Optional[_Iterable[int]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...
    class AgentDao(_message.Message):
        __slots__ = ("id", "className", "field", "metadata")
        ID_FIELD_NUMBER: _ClassVar[int]
        CLASSNAME_FIELD_NUMBER: _ClassVar[int]
        FIELD_FIELD_NUMBER: _ClassVar[int]
        METADATA_FIELD_NUMBER: _ClassVar[int]
        id: int
        className: str
        field: _containers.RepeatedCompositeFieldContainer[_Field_pb2.NestedField]
        metadata: str
        def __init__(self, id: _Optional[int] = ..., className: _Optional[str] = ..., field: _Optional[_Iterable[_Union[_Field_pb2.NestedField, _Mapping]]] = ..., metadata: _Optional[str] = ...) -> None: ...
    class StringSetDao(_message.Message):
        __slots__ = ("name", "value", "metadata")
        class StringSetEntry(_message.Message):
            __slots__ = ("name", "metadata")
            NAME_FIELD_NUMBER: _ClassVar[int]
            METADATA_FIELD_NUMBER: _ClassVar[int]
            name: str
            metadata: str
            def __init__(self, name: _Optional[str] = ..., metadata: _Optional[str] = ...) -> None: ...
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        METADATA_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: _containers.RepeatedCompositeFieldContainer[InputData.StringSetDao.StringSetEntry]
        metadata: str
        def __init__(self, name: _Optional[str] = ..., value: _Optional[_Iterable[_Union[InputData.StringSetDao.StringSetEntry, _Mapping]]] = ..., metadata: _Optional[str] = ...) -> None: ...
    RUNID_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_FIELD_NUMBER: _ClassVar[int]
    TIMESERIES_FIELD_NUMBER: _ClassVar[int]
    AGENT_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    STRINGSETS_FIELD_NUMBER: _ClassVar[int]
    runId: int
    simulation: InputData.SimulationParam
    timeSeries: _containers.RepeatedCompositeFieldContainer[InputData.TimeSeriesDao]
    agent: _containers.RepeatedCompositeFieldContainer[InputData.AgentDao]
    contract: _containers.RepeatedCompositeFieldContainer[_Contract_pb2.ProtoContract]
    schema: str
    stringSets: _containers.RepeatedCompositeFieldContainer[InputData.StringSetDao]
    def __init__(self, runId: _Optional[int] = ..., simulation: _Optional[_Union[InputData.SimulationParam, _Mapping]] = ..., timeSeries: _Optional[_Iterable[_Union[InputData.TimeSeriesDao, _Mapping]]] = ..., agent: _Optional[_Iterable[_Union[InputData.AgentDao, _Mapping]]] = ..., contract: _Optional[_Iterable[_Union[_Contract_pb2.ProtoContract, _Mapping]]] = ..., schema: _Optional[str] = ..., stringSets: _Optional[_Iterable[_Union[InputData.StringSetDao, _Mapping]]] = ...) -> None: ...
