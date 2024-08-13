# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: intrusion_zone.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from biostarPython.service import zone_pb2 as zone__pb2
from biostarPython.service import action_pb2 as action__pb2
from biostarPython.service import device_pb2 as device__pb2
from biostarPython.service import card_pb2 as card__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14intrusion_zone.proto\x12\x13gsdk.intrusion_zone\x1a\nzone.proto\x1a\x0c\x61\x63tion.proto\x1a\x0c\x64\x65vice.proto\x1a\ncard.proto\"<\n\x06Member\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\r\n\x05input\x18\x02 \x01(\r\x12\x11\n\toperation\x18\x03 \x01(\r\"y\n\x05Input\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0c\n\x04port\x18\x02 \x01(\r\x12+\n\nswitchType\x18\x03 \x01(\x0e\x32\x17.gsdk.device.SwitchType\x12\x10\n\x08\x64uration\x18\x04 \x01(\r\x12\x11\n\toperation\x18\x05 \x01(\r\"<\n\x06Output\x12\r\n\x05\x65vent\x18\x01 \x01(\r\x12#\n\x06\x61\x63tion\x18\x02 \x01(\x0b\x32\x13.gsdk.action.Action\"\xb2\x02\n\x08ZoneInfo\x12\x0e\n\x06zoneID\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08\x64isabled\x18\x03 \x01(\x08\x12\x10\n\x08\x61rmDelay\x18\x04 \x01(\r\x12\x12\n\nalarmDelay\x18\x05 \x01(\r\x12\x0f\n\x07\x64oorIDs\x18\x06 \x03(\r\x12\x10\n\x08groupIDs\x18\x07 \x03(\r\x12%\n\x05\x63\x61rds\x18\x08 \x03(\x0b\x32\x16.gsdk.card.CSNCardData\x12,\n\x07members\x18\t \x03(\x0b\x32\x1b.gsdk.intrusion_zone.Member\x12*\n\x06inputs\x18\n \x03(\x0b\x32\x1a.gsdk.intrusion_zone.Input\x12,\n\x07outputs\x18\x0b \x03(\x0b\x32\x1b.gsdk.intrusion_zone.Output\"\x1e\n\nGetRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\";\n\x0bGetResponse\x12,\n\x05zones\x18\x01 \x03(\x0b\x32\x1d.gsdk.intrusion_zone.ZoneInfo\"5\n\x10GetStatusRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0f\n\x07zoneIDs\x18\x02 \x03(\r\":\n\x11GetStatusResponse\x12%\n\x06status\x18\x01 \x03(\x0b\x32\x15.gsdk.zone.ZoneStatus\"L\n\nAddRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12,\n\x05zones\x18\x02 \x03(\x0b\x32\x1d.gsdk.intrusion_zone.ZoneInfo\"\r\n\x0b\x41\x64\x64Response\"2\n\rDeleteRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0f\n\x07zoneIDs\x18\x02 \x03(\r\"\x10\n\x0e\x44\x65leteResponse\"$\n\x10\x44\x65leteAllRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\"\x13\n\x11\x44\x65leteAllResponse\"A\n\rSetArmRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0f\n\x07zoneIDs\x18\x02 \x03(\r\x12\r\n\x05\x61rmed\x18\x03 \x01(\x08\"\x10\n\x0eSetArmResponse\"E\n\x0fSetAlarmRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12\x0f\n\x07zoneIDs\x18\x02 \x03(\r\x12\x0f\n\x07\x61larmed\x18\x03 \x01(\x08\"\x12\n\x10SetAlarmResponse*\x98\x02\n\x04\x45num\x12!\n\x1d\x46IRST_ENUM_VALUE_MUST_BE_ZERO\x10\x00\x12\x15\n\x11\x44\x45\x46\x41ULT_ARM_DELAY\x10\n\x12\x17\n\x13\x44\x45\x46\x41ULT_ALALM_DELAY\x10\x05\x12\x0e\n\nMAX_ALARMS\x10\x05\x12\x16\n\x11MAX_ACCESS_GROUPS\x10\x80\x01\x12\r\n\tMAX_DOORS\x10@\x12\x0f\n\x0bMAX_MEMBERS\x10@\x12\x0e\n\tMAX_CARDS\x10\x80\x01\x12\x0f\n\nMAX_INPUTS\x10\x80\x01\x12\x10\n\x0bMAX_OUTPUTS\x10\x80\x01\x12\x14\n\x0fMAX_NAME_LENGTH\x10\x90\x01\x12\x12\n\rMAX_ARM_DELAY\x10\xff\x01\x12\x14\n\x0fMAX_ALARM_DELAY\x10\xff\x01\x1a\x02\x10\x01*J\n\tInputType\x12\x0e\n\nINPUT_NONE\x10\x00\x12\x0e\n\nINPUT_CARD\x10\x01\x12\r\n\tINPUT_KEY\x10\x02\x12\x0e\n\tINPUT_ALL\x10\xff\x01*\x92\x01\n\rOperationType\x12\x12\n\x0eOPERATION_NONE\x10\x00\x12\x11\n\rOPERATION_ARM\x10\x01\x12\x14\n\x10OPERATION_DISARM\x10\x02\x12\x14\n\x10OPERATION_TOGGLE\x10\x03\x12\x13\n\x0fOPERATION_ALARM\x10\x04\x12\x19\n\x15OPERATION_CLEAR_ALARM\x10\x08\x32\xdf\x04\n\x12IntrusionAlarmZone\x12H\n\x03Get\x12\x1f.gsdk.intrusion_zone.GetRequest\x1a .gsdk.intrusion_zone.GetResponse\x12Z\n\tGetStatus\x12%.gsdk.intrusion_zone.GetStatusRequest\x1a&.gsdk.intrusion_zone.GetStatusResponse\x12H\n\x03\x41\x64\x64\x12\x1f.gsdk.intrusion_zone.AddRequest\x1a .gsdk.intrusion_zone.AddResponse\x12Q\n\x06\x44\x65lete\x12\".gsdk.intrusion_zone.DeleteRequest\x1a#.gsdk.intrusion_zone.DeleteResponse\x12Z\n\tDeleteAll\x12%.gsdk.intrusion_zone.DeleteAllRequest\x1a&.gsdk.intrusion_zone.DeleteAllResponse\x12Q\n\x06SetArm\x12\".gsdk.intrusion_zone.SetArmRequest\x1a#.gsdk.intrusion_zone.SetArmResponse\x12W\n\x08SetAlarm\x12$.gsdk.intrusion_zone.SetAlarmRequest\x1a%.gsdk.intrusion_zone.SetAlarmResponseBD\n!com.supremainc.sdk.intrusion_zoneP\x01Z\x1d\x62iostar/service/intrusionZoneb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'intrusion_zone_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n!com.supremainc.sdk.intrusion_zoneP\001Z\035biostar/service/intrusionZone'
  _globals['_ENUM']._loaded_options = None
  _globals['_ENUM']._serialized_options = b'\020\001'
  _globals['_ENUM']._serialized_start=1260
  _globals['_ENUM']._serialized_end=1540
  _globals['_INPUTTYPE']._serialized_start=1542
  _globals['_INPUTTYPE']._serialized_end=1616
  _globals['_OPERATIONTYPE']._serialized_start=1619
  _globals['_OPERATIONTYPE']._serialized_end=1765
  _globals['_MEMBER']._serialized_start=97
  _globals['_MEMBER']._serialized_end=157
  _globals['_INPUT']._serialized_start=159
  _globals['_INPUT']._serialized_end=280
  _globals['_OUTPUT']._serialized_start=282
  _globals['_OUTPUT']._serialized_end=342
  _globals['_ZONEINFO']._serialized_start=345
  _globals['_ZONEINFO']._serialized_end=651
  _globals['_GETREQUEST']._serialized_start=653
  _globals['_GETREQUEST']._serialized_end=683
  _globals['_GETRESPONSE']._serialized_start=685
  _globals['_GETRESPONSE']._serialized_end=744
  _globals['_GETSTATUSREQUEST']._serialized_start=746
  _globals['_GETSTATUSREQUEST']._serialized_end=799
  _globals['_GETSTATUSRESPONSE']._serialized_start=801
  _globals['_GETSTATUSRESPONSE']._serialized_end=859
  _globals['_ADDREQUEST']._serialized_start=861
  _globals['_ADDREQUEST']._serialized_end=937
  _globals['_ADDRESPONSE']._serialized_start=939
  _globals['_ADDRESPONSE']._serialized_end=952
  _globals['_DELETEREQUEST']._serialized_start=954
  _globals['_DELETEREQUEST']._serialized_end=1004
  _globals['_DELETERESPONSE']._serialized_start=1006
  _globals['_DELETERESPONSE']._serialized_end=1022
  _globals['_DELETEALLREQUEST']._serialized_start=1024
  _globals['_DELETEALLREQUEST']._serialized_end=1060
  _globals['_DELETEALLRESPONSE']._serialized_start=1062
  _globals['_DELETEALLRESPONSE']._serialized_end=1081
  _globals['_SETARMREQUEST']._serialized_start=1083
  _globals['_SETARMREQUEST']._serialized_end=1148
  _globals['_SETARMRESPONSE']._serialized_start=1150
  _globals['_SETARMRESPONSE']._serialized_end=1166
  _globals['_SETALARMREQUEST']._serialized_start=1168
  _globals['_SETALARMREQUEST']._serialized_end=1237
  _globals['_SETALARMRESPONSE']._serialized_start=1239
  _globals['_SETALARMRESPONSE']._serialized_end=1257
  _globals['_INTRUSIONALARMZONE']._serialized_start=1768
  _globals['_INTRUSIONALARMZONE']._serialized_end=2375
# @@protoc_insertion_point(module_scope)
