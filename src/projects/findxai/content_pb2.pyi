from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExtractContentFromLinksRequest(_message.Message):
    __slots__ = ("links",)
    LINKS_FIELD_NUMBER: _ClassVar[int]
    links: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, links: _Optional[_Iterable[str]] = ...) -> None: ...

class ExtractContentFromLinksReponse(_message.Message):
    __slots__ = ("contents",)
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    contents: _containers.RepeatedCompositeFieldContainer[ExtractedContent]
    def __init__(self, contents: _Optional[_Iterable[_Union[ExtractedContent, _Mapping]]] = ...) -> None: ...

class ExtractedContent(_message.Message):
    __slots__ = ("link", "title", "content")
    LINK_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    link: str
    title: str
    content: str
    def __init__(self, link: _Optional[str] = ..., title: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...
