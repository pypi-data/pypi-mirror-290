from fameprotobuf import Services_pb2 as _Services_pb2
from fameprotobuf import InputFile_pb2 as _InputFile_pb2
from fameprotobuf import ExecutionData_pb2 as _ExecutionData_pb2
from fameprotobuf import Model_pb2 as _Model_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataStorage(_message.Message):
    __slots__ = ("input", "output", "execution", "model")
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    input: _InputFile_pb2.InputData
    output: _Services_pb2.Output
    execution: _ExecutionData_pb2.ExecutionData
    model: _Model_pb2.ModelData
    def __init__(self, input: _Optional[_Union[_InputFile_pb2.InputData, _Mapping]] = ..., output: _Optional[_Union[_Services_pb2.Output, _Mapping]] = ..., execution: _Optional[_Union[_ExecutionData_pb2.ExecutionData, _Mapping]] = ..., model: _Optional[_Union[_Model_pb2.ModelData, _Mapping]] = ...) -> None: ...
