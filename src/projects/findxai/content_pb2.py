# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: content.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'content.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rcontent.proto\x12\x10google.search.v1\"/\n\x1e\x45xtractContentFromLinksRequest\x12\r\n\x05links\x18\x01 \x03(\t\"V\n\x1e\x45xtractContentFromLinksReponse\x12\x34\n\x08\x63ontents\x18\x01 \x03(\x0b\x32\".google.search.v1.ExtractedContent\"@\n\x10\x45xtractedContent\x12\x0c\n\x04link\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t2\x8f\x01\n\x0e\x43ontentService\x12}\n\x17\x45xtractContentFromLinks\x12\x30.google.search.v1.ExtractContentFromLinksRequest\x1a\x30.google.search.v1.ExtractContentFromLinksReponseB\x10Z\x0epkg/contentsvcb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'content_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\016pkg/contentsvc'
  _globals['_EXTRACTCONTENTFROMLINKSREQUEST']._serialized_start=35
  _globals['_EXTRACTCONTENTFROMLINKSREQUEST']._serialized_end=82
  _globals['_EXTRACTCONTENTFROMLINKSREPONSE']._serialized_start=84
  _globals['_EXTRACTCONTENTFROMLINKSREPONSE']._serialized_end=170
  _globals['_EXTRACTEDCONTENT']._serialized_start=172
  _globals['_EXTRACTEDCONTENT']._serialized_end=236
  _globals['_CONTENTSERVICE']._serialized_start=239
  _globals['_CONTENTSERVICE']._serialized_end=382
# @@protoc_insertion_point(module_scope)
