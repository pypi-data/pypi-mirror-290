# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: time.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from biostarPython.service import err_pb2 as err__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ntime.proto\x12\tgsdk.time\x1a\terr.proto\"\x1e\n\nGetRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\"\x1e\n\x0bGetResponse\x12\x0f\n\x07GMTTime\x18\x01 \x01(\x04\"/\n\nSetRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0f\n\x07GMTTime\x18\x02 \x01(\x04\"\r\n\x0bSetResponse\"5\n\x0fSetMultiRequest\x12\x11\n\tdeviceIDs\x18\x01 \x03(\r\x12\x0f\n\x07GMTTime\x18\x02 \x01(\x04\"A\n\x10SetMultiResponse\x12-\n\x0c\x64\x65viceErrors\x18\x01 \x03(\x0b\x32\x17.gsdk.err.ErrorResponse\"6\n\nTimeConfig\x12\x10\n\x08timeZone\x18\x01 \x01(\x05\x12\x16\n\x0esyncWithServer\x18\x02 \x01(\x08\"$\n\x10GetConfigRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\":\n\x11GetConfigResponse\x12%\n\x06\x63onfig\x18\x01 \x01(\x0b\x32\x15.gsdk.time.TimeConfig\"K\n\x10SetConfigRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12%\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x15.gsdk.time.TimeConfig\"\x13\n\x11SetConfigResponse\"Q\n\x15SetConfigMultiRequest\x12\x11\n\tdeviceIDs\x18\x01 \x03(\r\x12%\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x15.gsdk.time.TimeConfig\"G\n\x16SetConfigMultiResponse\x12-\n\x0c\x64\x65viceErrors\x18\x01 \x03(\x0b\x32\x17.gsdk.err.ErrorResponse\"\xb1\x01\n\x08WeekTime\x12\x0c\n\x04year\x18\x01 \x01(\r\x12\x1f\n\x05month\x18\x02 \x01(\x0e\x32\x10.gsdk.time.Month\x12#\n\x07ordinal\x18\x03 \x01(\x0e\x32\x12.gsdk.time.Ordinal\x12#\n\x07weekday\x18\x04 \x01(\x0e\x32\x12.gsdk.time.Weekday\x12\x0c\n\x04hour\x18\x05 \x01(\r\x12\x0e\n\x06minute\x18\x06 \x01(\r\x12\x0e\n\x06second\x18\x07 \x01(\r\"o\n\x0b\x44STSchedule\x12&\n\tstartTime\x18\x01 \x01(\x0b\x32\x13.gsdk.time.WeekTime\x12$\n\x07\x65ndTime\x18\x02 \x01(\x0b\x32\x13.gsdk.time.WeekTime\x12\x12\n\ntimeOffset\x18\x03 \x01(\x05\"6\n\tDSTConfig\x12)\n\tschedules\x18\x01 \x03(\x0b\x32\x16.gsdk.time.DSTSchedule\"\'\n\x13GetDSTConfigRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\"<\n\x14GetDSTConfigResponse\x12$\n\x06\x63onfig\x18\x01 \x01(\x0b\x32\x14.gsdk.time.DSTConfig\"M\n\x13SetDSTConfigRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12$\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x14.gsdk.time.DSTConfig\"\x16\n\x14SetDSTConfigResponse\"S\n\x18SetDSTConfigMultiRequest\x12\x11\n\tdeviceIDs\x18\x01 \x03(\r\x12$\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x14.gsdk.time.DSTConfig\"J\n\x19SetDSTConfigMultiResponse\x12-\n\x0c\x64\x65viceErrors\x18\x01 \x03(\x0b\x32\x17.gsdk.err.ErrorResponse*r\n\x04\x45num\x12!\n\x1d\x46IRST_ENUM_VALUE_MUST_BE_ZERO\x10\x00\x12\x1b\n\x0eMIN_DST_OFFSET\x10\xe0\xc7\xff\xff\xff\xff\xff\xff\xff\x01\x12\x13\n\x0eMAX_DST_OFFSET\x10\xa0\x38\x12\x15\n\x11MAX_DST_SCHEDULES\x10\x02*\xe1\x01\n\x05Month\x12\x11\n\rMONTH_JANUARY\x10\x00\x12\x12\n\x0eMONTH_FEBRUARY\x10\x01\x12\x0f\n\x0bMONTH_MARCH\x10\x02\x12\x0f\n\x0bMONTH_APRIL\x10\x03\x12\r\n\tMONTH_MAY\x10\x04\x12\x0e\n\nMONTH_JUNE\x10\x05\x12\x0e\n\nMONTH_JULY\x10\x06\x12\x10\n\x0cMONTH_AUGUST\x10\x07\x12\x13\n\x0fMONTH_SEPTEMBER\x10\x08\x12\x11\n\rMONTH_OCTOBER\x10\t\x12\x12\n\x0eMONTH_NOVEMBER\x10\n\x12\x12\n\x0eMONTH_DECEMBER\x10\x0b*\x9d\x01\n\x07Weekday\x12\x12\n\x0eWEEKDAY_SUNDAY\x10\x00\x12\x12\n\x0eWEEKDAY_MONDAY\x10\x01\x12\x13\n\x0fWEEKDAY_TUESDAY\x10\x02\x12\x15\n\x11WEEKDAY_WEDNESDAY\x10\x03\x12\x14\n\x10WEEKDAY_THURSDAY\x10\x04\x12\x12\n\x0eWEEKDAY_FRIDAY\x10\x05\x12\x14\n\x10WEEKDAY_SATURDAY\x10\x06*\xe7\x01\n\x07Ordinal\x12\x11\n\rORDINAL_FIRST\x10\x00\x12\x12\n\x0eORDINAL_SECOND\x10\x01\x12\x11\n\rORDINAL_THIRD\x10\x02\x12\x12\n\x0eORDINAL_FOURTH\x10\x03\x12\x11\n\rORDINAL_FIFTH\x10\x04\x12\x11\n\rORDINAL_SIXTH\x10\x05\x12\x13\n\x0fORDINAL_SEVENTH\x10\x06\x12\x12\n\x0eORDINAL_EIGHTH\x10\x07\x12\x11\n\rORDINAL_NINTH\x10\x08\x12\x11\n\rORDINAL_TENTH\x10\t\x12\x19\n\x0cORDINAL_LAST\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x32\xa0\x05\n\x04Time\x12\x34\n\x03Get\x12\x15.gsdk.time.GetRequest\x1a\x16.gsdk.time.GetResponse\x12\x34\n\x03Set\x12\x15.gsdk.time.SetRequest\x1a\x16.gsdk.time.SetResponse\x12\x43\n\x08SetMulti\x12\x1a.gsdk.time.SetMultiRequest\x1a\x1b.gsdk.time.SetMultiResponse\x12\x46\n\tGetConfig\x12\x1b.gsdk.time.GetConfigRequest\x1a\x1c.gsdk.time.GetConfigResponse\x12\x46\n\tSetConfig\x12\x1b.gsdk.time.SetConfigRequest\x1a\x1c.gsdk.time.SetConfigResponse\x12U\n\x0eSetConfigMulti\x12 .gsdk.time.SetConfigMultiRequest\x1a!.gsdk.time.SetConfigMultiResponse\x12O\n\x0cGetDSTConfig\x12\x1e.gsdk.time.GetDSTConfigRequest\x1a\x1f.gsdk.time.GetDSTConfigResponse\x12O\n\x0cSetDSTConfig\x12\x1e.gsdk.time.SetDSTConfigRequest\x1a\x1f.gsdk.time.SetDSTConfigResponse\x12^\n\x11SetDSTConfigMulti\x12#.gsdk.time.SetDSTConfigMultiRequest\x1a$.gsdk.time.SetDSTConfigMultiResponseB1\n\x17\x63om.supremainc.sdk.timeP\x01Z\x14\x62iostar/service/timeb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'time_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\027com.supremainc.sdk.timeP\001Z\024biostar/service/time'
  _globals['_ENUM']._serialized_start=1410
  _globals['_ENUM']._serialized_end=1524
  _globals['_MONTH']._serialized_start=1527
  _globals['_MONTH']._serialized_end=1752
  _globals['_WEEKDAY']._serialized_start=1755
  _globals['_WEEKDAY']._serialized_end=1912
  _globals['_ORDINAL']._serialized_start=1915
  _globals['_ORDINAL']._serialized_end=2146
  _globals['_GETREQUEST']._serialized_start=36
  _globals['_GETREQUEST']._serialized_end=66
  _globals['_GETRESPONSE']._serialized_start=68
  _globals['_GETRESPONSE']._serialized_end=98
  _globals['_SETREQUEST']._serialized_start=100
  _globals['_SETREQUEST']._serialized_end=147
  _globals['_SETRESPONSE']._serialized_start=149
  _globals['_SETRESPONSE']._serialized_end=162
  _globals['_SETMULTIREQUEST']._serialized_start=164
  _globals['_SETMULTIREQUEST']._serialized_end=217
  _globals['_SETMULTIRESPONSE']._serialized_start=219
  _globals['_SETMULTIRESPONSE']._serialized_end=284
  _globals['_TIMECONFIG']._serialized_start=286
  _globals['_TIMECONFIG']._serialized_end=340
  _globals['_GETCONFIGREQUEST']._serialized_start=342
  _globals['_GETCONFIGREQUEST']._serialized_end=378
  _globals['_GETCONFIGRESPONSE']._serialized_start=380
  _globals['_GETCONFIGRESPONSE']._serialized_end=438
  _globals['_SETCONFIGREQUEST']._serialized_start=440
  _globals['_SETCONFIGREQUEST']._serialized_end=515
  _globals['_SETCONFIGRESPONSE']._serialized_start=517
  _globals['_SETCONFIGRESPONSE']._serialized_end=536
  _globals['_SETCONFIGMULTIREQUEST']._serialized_start=538
  _globals['_SETCONFIGMULTIREQUEST']._serialized_end=619
  _globals['_SETCONFIGMULTIRESPONSE']._serialized_start=621
  _globals['_SETCONFIGMULTIRESPONSE']._serialized_end=692
  _globals['_WEEKTIME']._serialized_start=695
  _globals['_WEEKTIME']._serialized_end=872
  _globals['_DSTSCHEDULE']._serialized_start=874
  _globals['_DSTSCHEDULE']._serialized_end=985
  _globals['_DSTCONFIG']._serialized_start=987
  _globals['_DSTCONFIG']._serialized_end=1041
  _globals['_GETDSTCONFIGREQUEST']._serialized_start=1043
  _globals['_GETDSTCONFIGREQUEST']._serialized_end=1082
  _globals['_GETDSTCONFIGRESPONSE']._serialized_start=1084
  _globals['_GETDSTCONFIGRESPONSE']._serialized_end=1144
  _globals['_SETDSTCONFIGREQUEST']._serialized_start=1146
  _globals['_SETDSTCONFIGREQUEST']._serialized_end=1223
  _globals['_SETDSTCONFIGRESPONSE']._serialized_start=1225
  _globals['_SETDSTCONFIGRESPONSE']._serialized_end=1247
  _globals['_SETDSTCONFIGMULTIREQUEST']._serialized_start=1249
  _globals['_SETDSTCONFIGMULTIREQUEST']._serialized_end=1332
  _globals['_SETDSTCONFIGMULTIRESPONSE']._serialized_start=1334
  _globals['_SETDSTCONFIGMULTIRESPONSE']._serialized_end=1408
  _globals['_TIME']._serialized_start=2149
  _globals['_TIME']._serialized_end=2821
# @@protoc_insertion_point(module_scope)
