from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRequest(_message.Message):
    __slots__ = ("c2coff", "cr", "date_restrict", "exact_terms", "exclude_terms", "file_type", "filter", "gl", "high_range", "hl", "hq", "img_color_type", "img_dominant_color", "img_size", "img_type", "language", "link_site", "low_range", "lr", "num", "or_terms", "q", "rights", "safe", "search_type", "site_search", "site_search_filter", "sort", "start")
    C2COFF_FIELD_NUMBER: _ClassVar[int]
    CR_FIELD_NUMBER: _ClassVar[int]
    DATE_RESTRICT_FIELD_NUMBER: _ClassVar[int]
    EXACT_TERMS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_TERMS_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    GL_FIELD_NUMBER: _ClassVar[int]
    HIGH_RANGE_FIELD_NUMBER: _ClassVar[int]
    HL_FIELD_NUMBER: _ClassVar[int]
    HQ_FIELD_NUMBER: _ClassVar[int]
    IMG_COLOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    IMG_DOMINANT_COLOR_FIELD_NUMBER: _ClassVar[int]
    IMG_SIZE_FIELD_NUMBER: _ClassVar[int]
    IMG_TYPE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LINK_SITE_FIELD_NUMBER: _ClassVar[int]
    LOW_RANGE_FIELD_NUMBER: _ClassVar[int]
    LR_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    OR_TERMS_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    RIGHTS_FIELD_NUMBER: _ClassVar[int]
    SAFE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    SITE_SEARCH_FIELD_NUMBER: _ClassVar[int]
    SITE_SEARCH_FILTER_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    c2coff: str
    cr: str
    date_restrict: str
    exact_terms: str
    exclude_terms: str
    file_type: str
    filter: str
    gl: str
    high_range: str
    hl: str
    hq: str
    img_color_type: str
    img_dominant_color: str
    img_size: str
    img_type: str
    language: str
    link_site: str
    low_range: str
    lr: str
    num: int
    or_terms: str
    q: str
    rights: str
    safe: str
    search_type: str
    site_search: str
    site_search_filter: str
    sort: str
    start: int
    def __init__(self, c2coff: _Optional[str] = ..., cr: _Optional[str] = ..., date_restrict: _Optional[str] = ..., exact_terms: _Optional[str] = ..., exclude_terms: _Optional[str] = ..., file_type: _Optional[str] = ..., filter: _Optional[str] = ..., gl: _Optional[str] = ..., high_range: _Optional[str] = ..., hl: _Optional[str] = ..., hq: _Optional[str] = ..., img_color_type: _Optional[str] = ..., img_dominant_color: _Optional[str] = ..., img_size: _Optional[str] = ..., img_type: _Optional[str] = ..., language: _Optional[str] = ..., link_site: _Optional[str] = ..., low_range: _Optional[str] = ..., lr: _Optional[str] = ..., num: _Optional[int] = ..., or_terms: _Optional[str] = ..., q: _Optional[str] = ..., rights: _Optional[str] = ..., safe: _Optional[str] = ..., search_type: _Optional[str] = ..., site_search: _Optional[str] = ..., site_search_filter: _Optional[str] = ..., sort: _Optional[str] = ..., start: _Optional[int] = ...) -> None: ...

class SearchResult(_message.Message):
    __slots__ = ("title", "link", "snippet")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    SNIPPET_FIELD_NUMBER: _ClassVar[int]
    title: str
    link: str
    snippet: str
    def __init__(self, title: _Optional[str] = ..., link: _Optional[str] = ..., snippet: _Optional[str] = ...) -> None: ...

class SearchResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[SearchResult]
    def __init__(self, results: _Optional[_Iterable[_Union[SearchResult, _Mapping]]] = ...) -> None: ...

class DeactivateKeysRequest(_message.Message):
    __slots__ = ("api_keys", "force_delete")
    API_KEYS_FIELD_NUMBER: _ClassVar[int]
    FORCE_DELETE_FIELD_NUMBER: _ClassVar[int]
    api_keys: _containers.RepeatedScalarFieldContainer[str]
    force_delete: bool
    def __init__(self, api_keys: _Optional[_Iterable[str]] = ..., force_delete: bool = ...) -> None: ...

class DeactivateKeysResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ActivateKeysRequest(_message.Message):
    __slots__ = ("api_keys",)
    API_KEYS_FIELD_NUMBER: _ClassVar[int]
    api_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, api_keys: _Optional[_Iterable[str]] = ...) -> None: ...

class ActivateKeysResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class KeyInfo(_message.Message):
    __slots__ = ("id", "name", "api_key", "search_engine_id", "is_active", "daily_queries", "status_code", "error_msg", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    SEARCH_ENGINE_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DAILY_QUERIES_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    api_key: str
    search_engine_id: str
    is_active: bool
    daily_queries: int
    status_code: int
    error_msg: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., api_key: _Optional[str] = ..., search_engine_id: _Optional[str] = ..., is_active: bool = ..., daily_queries: _Optional[int] = ..., status_code: _Optional[int] = ..., error_msg: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class AddKeysRequest(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[KeyInfo]
    def __init__(self, data: _Optional[_Iterable[_Union[KeyInfo, _Mapping]]] = ...) -> None: ...

class AddKeysResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKeysRequest(_message.Message):
    __slots__ = ("api_keys",)
    API_KEYS_FIELD_NUMBER: _ClassVar[int]
    api_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, api_keys: _Optional[_Iterable[str]] = ...) -> None: ...

class GetKeysResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[KeyInfo]
    def __init__(self, results: _Optional[_Iterable[_Union[KeyInfo, _Mapping]]] = ...) -> None: ...
