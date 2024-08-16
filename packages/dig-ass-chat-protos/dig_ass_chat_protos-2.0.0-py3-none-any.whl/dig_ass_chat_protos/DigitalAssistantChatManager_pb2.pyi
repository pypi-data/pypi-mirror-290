from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalAssistantChatManagerResponse(_message.Message):
    __slots__ = ("Text", "Document")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    Text: str
    Document: bytes
    def __init__(self, Text: _Optional[str] = ..., Document: _Optional[bytes] = ...) -> None: ...

class DigitalAssistantChatManagerRequest(_message.Message):
    __slots__ = ("Text", "OuterContext", "DocType")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    OUTERCONTEXT_FIELD_NUMBER: _ClassVar[int]
    DOCTYPE_FIELD_NUMBER: _ClassVar[int]
    Text: str
    OuterContext: OuterContextItem
    DocType: str
    def __init__(self, Text: _Optional[str] = ..., OuterContext: _Optional[_Union[OuterContextItem, _Mapping]] = ..., DocType: _Optional[str] = ...) -> None: ...

class OuterContextItem(_message.Message):
    __slots__ = ("Sex", "Age", "UserId", "SessionId", "ClientId")
    SEX_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    Sex: bool
    Age: int
    UserId: str
    SessionId: str
    ClientId: str
    def __init__(self, Sex: bool = ..., Age: _Optional[int] = ..., UserId: _Optional[str] = ..., SessionId: _Optional[str] = ..., ClientId: _Optional[str] = ...) -> None: ...
