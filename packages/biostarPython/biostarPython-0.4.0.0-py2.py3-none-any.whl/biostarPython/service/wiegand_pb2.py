# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wiegand.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from biostarPython.service import device_pb2 as device__pb2
from biostarPython.service import err_pb2 as err__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rwiegand.proto\x12\x0cgsdk.wiegand\x1a\x0c\x64\x65vice.proto\x1a\terr.proto\"_\n\x0bParityField\x12\x11\n\tparityPos\x18\x01 \x01(\r\x12/\n\nparityType\x18\x02 \x01(\x0e\x32\x1b.gsdk.wiegand.WiegandParity\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\"t\n\rWiegandFormat\x12\x10\n\x08\x66ormatID\x18\x01 \x01(\r\x12\x0e\n\x06length\x18\x02 \x01(\r\x12\x10\n\x08IDFields\x18\x03 \x03(\x0c\x12/\n\x0cparityFields\x18\x04 \x03(\x0b\x32\x19.gsdk.wiegand.ParityField\"\xf3\x02\n\rWiegandConfig\x12\'\n\x04mode\x18\x01 \x01(\x0e\x32\x19.gsdk.wiegand.WiegandMode\x12\x18\n\x10useWiegandBypass\x18\x02 \x01(\x08\x12\x13\n\x0buseFailCode\x18\x03 \x01(\x08\x12\x10\n\x08\x66\x61ilCode\x18\x04 \x01(\r\x12\x15\n\routPulseWidth\x18\x05 \x01(\r\x12\x18\n\x10outPulseInterval\x18\x06 \x01(\r\x12,\n\x07\x66ormats\x18\x07 \x03(\x0b\x32\x1b.gsdk.wiegand.WiegandFormat\x12\x31\n\x0cslaveFormats\x18\x08 \x03(\x0b\x32\x1b.gsdk.wiegand.WiegandFormat\x12.\n\tCSNFormat\x18\t \x01(\x0b\x32\x1b.gsdk.wiegand.WiegandFormat\x12\x36\n\x10useWiegandUserID\x18\n \x01(\x0e\x32\x1c.gsdk.wiegand.WiegandOutType\"$\n\x10GetConfigRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\"@\n\x11GetConfigResponse\x12+\n\x06\x63onfig\x18\x01 \x01(\x0b\x32\x1b.gsdk.wiegand.WiegandConfig\"Q\n\x10SetConfigRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12+\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x1b.gsdk.wiegand.WiegandConfig\"\x13\n\x11SetConfigResponse\"W\n\x15SetConfigMultiRequest\x12\x11\n\tdeviceIDs\x18\x01 \x03(\r\x12+\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x1b.gsdk.wiegand.WiegandConfig\"G\n\x16SetConfigMultiResponse\x12-\n\x0c\x64\x65viceErrors\x18\x01 \x03(\x0b\x32\x17.gsdk.err.ErrorResponse\"a\n\x12WiegandTamperInput\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0c\n\x04port\x18\x02 \x01(\r\x12+\n\nswitchType\x18\x03 \x01(\x0e\x32\x17.gsdk.device.SwitchType\"/\n\rWiegandOutput\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0c\n\x04port\x18\x02 \x01(\r\"\xf7\x01\n\x11WiegandDeviceInfo\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x35\n\x0btamperInput\x18\x02 \x01(\x0b\x32 .gsdk.wiegand.WiegandTamperInput\x12\x31\n\x0credLEDOutput\x18\x03 \x01(\x0b\x32\x1b.gsdk.wiegand.WiegandOutput\x12\x33\n\x0egreenLEDOutput\x18\x04 \x01(\x0b\x32\x1b.gsdk.wiegand.WiegandOutput\x12\x31\n\x0c\x62uzzerOutput\x18\x05 \x01(\x0b\x32\x1b.gsdk.wiegand.WiegandOutput\"-\n\x13SearchDeviceRequest\x12\x16\n\x0eparentDeviceID\x18\x01 \x01(\r\"0\n\x14SearchDeviceResponse\x12\x18\n\x10wiegandDeviceIDs\x18\x01 \x03(\r\"`\n\x10SetDeviceRequest\x12\x16\n\x0eparentDeviceID\x18\x01 \x01(\r\x12\x34\n\x0b\x64\x65viceInfos\x18\x02 \x03(\x0b\x32\x1f.gsdk.wiegand.WiegandDeviceInfo\"\x13\n\x11SetDeviceResponse\"*\n\x10GetDeviceRequest\x12\x16\n\x0eparentDeviceID\x18\x01 \x01(\r\"I\n\x11GetDeviceResponse\x12\x34\n\x0b\x64\x65viceInfos\x18\x01 \x03(\x0b\x32\x1f.gsdk.wiegand.WiegandDeviceInfo*\xd5\x02\n\x04\x45num\x12!\n\x1d\x46IRST_ENUM_VALUE_MUST_BE_ZERO\x10\x00\x12\x1b\n\x17\x44\x45\x46\x41ULT_OUT_PULSE_WIDTH\x10(\x12\x1f\n\x1a\x44\x45\x46\x41ULT_OUT_PULSE_INTERVAL\x10\x90N\x12\x17\n\x13MIN_OUT_PULSE_WIDTH\x10\x14\x12\x17\n\x13MAX_OUT_PULSE_WIDTH\x10\x64\x12\x1b\n\x16MIN_OUT_PULSE_INTERVAL\x10\xc8\x01\x12\x1c\n\x16MAX_OUT_PULSE_INTERVAL\x10\xa0\x9c\x01\x12\x11\n\rMAX_ID_FIELDS\x10\x04\x12\x15\n\x11MAX_PARITY_FIELDS\x10\x04\x12\x1b\n\x16MAX_WIEGAND_FIELD_BITS\x10\x80\x02\x12\x1b\n\x17MAX_WIEGAND_FIELD_BYTES\x10 \x12\x17\n\x13MAX_WIEGAND_FORMATS\x10\x10\x1a\x02\x10\x01*L\n\x0bWiegandMode\x12\x13\n\x0fWIEGAND_IN_ONLY\x10\x00\x12\x14\n\x10WIEGAND_OUT_ONLY\x10\x01\x12\x12\n\x0eWIEGAND_IN_OUT\x10\x02*Y\n\rWiegandParity\x12\x17\n\x13WIEGAND_PARITY_NONE\x10\x00\x12\x16\n\x12WIEGAND_PARITY_ODD\x10\x01\x12\x17\n\x13WIEGAND_PARITY_EVEN\x10\x02*_\n\x0eWiegandOutType\x12\x1b\n\x17WIEGAND_OUT_UNSPECIFIED\x10\x00\x12\x17\n\x13WIEGAND_OUT_CARD_ID\x10\x01\x12\x17\n\x13WIEGAND_OUT_USER_ID\x10\x02\x32\xf5\x03\n\x07Wiegand\x12L\n\tGetConfig\x12\x1e.gsdk.wiegand.GetConfigRequest\x1a\x1f.gsdk.wiegand.GetConfigResponse\x12L\n\tSetConfig\x12\x1e.gsdk.wiegand.SetConfigRequest\x1a\x1f.gsdk.wiegand.SetConfigResponse\x12[\n\x0eSetConfigMulti\x12#.gsdk.wiegand.SetConfigMultiRequest\x1a$.gsdk.wiegand.SetConfigMultiResponse\x12U\n\x0cSearchDevice\x12!.gsdk.wiegand.SearchDeviceRequest\x1a\".gsdk.wiegand.SearchDeviceResponse\x12L\n\tSetDevice\x12\x1e.gsdk.wiegand.SetDeviceRequest\x1a\x1f.gsdk.wiegand.SetDeviceResponse\x12L\n\tGetDevice\x12\x1e.gsdk.wiegand.GetDeviceRequest\x1a\x1f.gsdk.wiegand.GetDeviceResponseB7\n\x1a\x63om.supremainc.sdk.wiegandP\x01Z\x17\x62iostar/service/wiegandb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'wiegand_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\032com.supremainc.sdk.wiegandP\001Z\027biostar/service/wiegand'
  _globals['_ENUM']._loaded_options = None
  _globals['_ENUM']._serialized_options = b'\020\001'
  _globals['_ENUM']._serialized_start=1749
  _globals['_ENUM']._serialized_end=2090
  _globals['_WIEGANDMODE']._serialized_start=2092
  _globals['_WIEGANDMODE']._serialized_end=2168
  _globals['_WIEGANDPARITY']._serialized_start=2170
  _globals['_WIEGANDPARITY']._serialized_end=2259
  _globals['_WIEGANDOUTTYPE']._serialized_start=2261
  _globals['_WIEGANDOUTTYPE']._serialized_end=2356
  _globals['_PARITYFIELD']._serialized_start=56
  _globals['_PARITYFIELD']._serialized_end=151
  _globals['_WIEGANDFORMAT']._serialized_start=153
  _globals['_WIEGANDFORMAT']._serialized_end=269
  _globals['_WIEGANDCONFIG']._serialized_start=272
  _globals['_WIEGANDCONFIG']._serialized_end=643
  _globals['_GETCONFIGREQUEST']._serialized_start=645
  _globals['_GETCONFIGREQUEST']._serialized_end=681
  _globals['_GETCONFIGRESPONSE']._serialized_start=683
  _globals['_GETCONFIGRESPONSE']._serialized_end=747
  _globals['_SETCONFIGREQUEST']._serialized_start=749
  _globals['_SETCONFIGREQUEST']._serialized_end=830
  _globals['_SETCONFIGRESPONSE']._serialized_start=832
  _globals['_SETCONFIGRESPONSE']._serialized_end=851
  _globals['_SETCONFIGMULTIREQUEST']._serialized_start=853
  _globals['_SETCONFIGMULTIREQUEST']._serialized_end=940
  _globals['_SETCONFIGMULTIRESPONSE']._serialized_start=942
  _globals['_SETCONFIGMULTIRESPONSE']._serialized_end=1013
  _globals['_WIEGANDTAMPERINPUT']._serialized_start=1015
  _globals['_WIEGANDTAMPERINPUT']._serialized_end=1112
  _globals['_WIEGANDOUTPUT']._serialized_start=1114
  _globals['_WIEGANDOUTPUT']._serialized_end=1161
  _globals['_WIEGANDDEVICEINFO']._serialized_start=1164
  _globals['_WIEGANDDEVICEINFO']._serialized_end=1411
  _globals['_SEARCHDEVICEREQUEST']._serialized_start=1413
  _globals['_SEARCHDEVICEREQUEST']._serialized_end=1458
  _globals['_SEARCHDEVICERESPONSE']._serialized_start=1460
  _globals['_SEARCHDEVICERESPONSE']._serialized_end=1508
  _globals['_SETDEVICEREQUEST']._serialized_start=1510
  _globals['_SETDEVICEREQUEST']._serialized_end=1606
  _globals['_SETDEVICERESPONSE']._serialized_start=1608
  _globals['_SETDEVICERESPONSE']._serialized_end=1627
  _globals['_GETDEVICEREQUEST']._serialized_start=1629
  _globals['_GETDEVICEREQUEST']._serialized_end=1671
  _globals['_GETDEVICERESPONSE']._serialized_start=1673
  _globals['_GETDEVICERESPONSE']._serialized_end=1746
  _globals['_WIEGAND']._serialized_start=2359
  _globals['_WIEGAND']._serialized_end=2860
# @@protoc_insertion_point(module_scope)
