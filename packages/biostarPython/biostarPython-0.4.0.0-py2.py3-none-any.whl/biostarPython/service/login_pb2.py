# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: login.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0blogin.proto\x12\ngsdk.login\"\"\n\x0cLoginRequest\x12\x12\n\ntenantCert\x18\x01 \x01(\t\"!\n\rLoginResponse\x12\x10\n\x08jwtToken\x18\x01 \x01(\t\">\n\x11LoginAdminRequest\x12\x17\n\x0f\x61\x64minTenantCert\x18\x01 \x01(\t\x12\x10\n\x08tenantID\x18\x02 \x01(\t\"&\n\x12LoginAdminResponse\x12\x10\n\x08jwtToken\x18\x01 \x01(\t\"\x0f\n\rLogoutRequest\"\x10\n\x0eLogoutResponse2\xd3\x01\n\x05Login\x12<\n\x05Login\x12\x18.gsdk.login.LoginRequest\x1a\x19.gsdk.login.LoginResponse\x12K\n\nLoginAdmin\x12\x1d.gsdk.login.LoginAdminRequest\x1a\x1e.gsdk.login.LoginAdminResponse\x12?\n\x06Logout\x12\x19.gsdk.login.LogoutRequest\x1a\x1a.gsdk.login.LogoutResponseB3\n\x18\x63om.supremainc.sdk.loginP\x01Z\x15\x62iostar/service/loginb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'login_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\030com.supremainc.sdk.loginP\001Z\025biostar/service/login'
  _globals['_LOGINREQUEST']._serialized_start=27
  _globals['_LOGINREQUEST']._serialized_end=61
  _globals['_LOGINRESPONSE']._serialized_start=63
  _globals['_LOGINRESPONSE']._serialized_end=96
  _globals['_LOGINADMINREQUEST']._serialized_start=98
  _globals['_LOGINADMINREQUEST']._serialized_end=160
  _globals['_LOGINADMINRESPONSE']._serialized_start=162
  _globals['_LOGINADMINRESPONSE']._serialized_end=200
  _globals['_LOGOUTREQUEST']._serialized_start=202
  _globals['_LOGOUTREQUEST']._serialized_end=217
  _globals['_LOGOUTRESPONSE']._serialized_start=219
  _globals['_LOGOUTRESPONSE']._serialized_end=235
  _globals['_LOGIN']._serialized_start=238
  _globals['_LOGIN']._serialized_end=449
# @@protoc_insertion_point(module_scope)
