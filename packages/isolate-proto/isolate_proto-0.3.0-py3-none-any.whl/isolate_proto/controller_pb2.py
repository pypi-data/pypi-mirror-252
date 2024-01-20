# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: controller.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from isolate.connections.grpc.definitions import common_pb2 as common__pb2
from isolate.server.definitions import server_pb2 as server__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x10\x63ontroller.proto\x12\ncontroller\x1a\x0c\x63ommon.proto\x1a\x0cserver.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1cgoogle/protobuf/struct.proto"\xde\x01\n\tHostedMap\x12,\n\x0c\x65nvironments\x18\x01 \x03(\x0b\x32\x16.EnvironmentDefinition\x12\x42\n\x14machine_requirements\x18\x02 \x01(\x0b\x32\x1f.controller.MachineRequirementsH\x00\x88\x01\x01\x12#\n\x08\x66unction\x18\x03 \x01(\x0b\x32\x11.SerializedObject\x12!\n\x06inputs\x18\x04 \x03(\x0b\x32\x11.SerializedObjectB\x17\n\x15_machine_requirements"\xf6\x01\n\tHostedRun\x12,\n\x0c\x65nvironments\x18\x01 \x03(\x0b\x32\x16.EnvironmentDefinition\x12\x42\n\x14machine_requirements\x18\x02 \x01(\x0b\x32\x1f.controller.MachineRequirementsH\x00\x88\x01\x01\x12#\n\x08\x66unction\x18\x03 \x01(\x0b\x32\x11.SerializedObject\x12*\n\nsetup_func\x18\x04 \x01(\x0b\x32\x11.SerializedObjectH\x01\x88\x01\x01\x42\x17\n\x15_machine_requirementsB\r\n\x0b_setup_func"\x88\x01\n\x14\x43reateUserKeyRequest\x12\x35\n\x05scope\x18\x01 \x01(\x0e\x32&.controller.CreateUserKeyRequest.Scope\x12\x12\n\x05\x61lias\x18\x02 \x01(\tH\x00\x88\x01\x01"\x1b\n\x05Scope\x12\t\n\x05\x41\x44MIN\x10\x00\x12\x07\n\x03\x41PI\x10\x01\x42\x08\n\x06_alias";\n\x15\x43reateUserKeyResponse\x12\x12\n\nkey_secret\x18\x01 \x01(\t\x12\x0e\n\x06key_id\x18\x02 \x01(\t"\x15\n\x13ListUserKeysRequest"B\n\x14ListUserKeysResponse\x12*\n\tuser_keys\x18\x01 \x03(\x0b\x32\x17.controller.UserKeyInfo"&\n\x14RevokeUserKeyRequest\x12\x0e\n\x06key_id\x18\x01 \x01(\t"\x17\n\x15RevokeUserKeyResponse"\x93\x01\n\x0bUserKeyInfo\x12\x0e\n\x06key_id\x18\x01 \x01(\t\x12.\n\ncreated_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x35\n\x05scope\x18\x03 \x01(\x0e\x32&.controller.CreateUserKeyRequest.Scope\x12\r\n\x05\x61lias\x18\x04 \x01(\t"\xb1\x01\n\x0fHostedRunResult\x12\x0e\n\x06run_id\x18\x01 \x01(\t\x12\x30\n\x06status\x18\x02 \x01(\x0b\x32\x1b.controller.HostedRunStatusH\x00\x88\x01\x01\x12\x12\n\x04logs\x18\x03 \x03(\x0b\x32\x04.Log\x12,\n\x0creturn_value\x18\x04 \x01(\x0b\x32\x11.SerializedObjectH\x01\x88\x01\x01\x42\t\n\x07_statusB\x0f\n\r_return_value"\x80\x01\n\x0fHostedRunStatus\x12\x30\n\x05state\x18\x01 \x01(\x0e\x32!.controller.HostedRunStatus.State";\n\x05State\x12\x0f\n\x0bIN_PROGRESS\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\x14\n\x10INTERNAL_FAILURE\x10\x02"\x82\x03\n\x13MachineRequirements\x12\x14\n\x0cmachine_type\x18\x01 \x01(\t\x12\x17\n\nkeep_alive\x18\x02 \x01(\x05H\x00\x88\x01\x01\x12\x17\n\nbase_image\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x19\n\x0c\x65xposed_port\x18\x04 \x01(\x05H\x02\x88\x01\x01\x12\x16\n\tscheduler\x18\x05 \x01(\tH\x03\x88\x01\x01\x12\x37\n\x11scheduler_options\x18\x08 \x01(\x0b\x32\x17.google.protobuf.StructH\x04\x88\x01\x01\x12\x1d\n\x10max_multiplexing\x18\x06 \x01(\x05H\x05\x88\x01\x01\x12\x1c\n\x0fmax_concurrency\x18\t \x01(\x05H\x06\x88\x01\x01\x42\r\n\x0b_keep_aliveB\r\n\x0b_base_imageB\x0f\n\r_exposed_portB\x0c\n\n_schedulerB\x14\n\x12_scheduler_optionsB\x13\n\x11_max_multiplexingB\x12\n\x10_max_concurrency"\xf5\x03\n\x1aRegisterApplicationRequest\x12,\n\x0c\x65nvironments\x18\x01 \x03(\x0b\x32\x16.EnvironmentDefinition\x12\x42\n\x14machine_requirements\x18\x02 \x01(\x0b\x32\x1f.controller.MachineRequirementsH\x00\x88\x01\x01\x12#\n\x08\x66unction\x18\x03 \x01(\x0b\x32\x11.SerializedObject\x12*\n\nsetup_func\x18\x04 \x01(\x0b\x32\x11.SerializedObjectH\x01\x88\x01\x01\x12\x1d\n\x10\x61pplication_name\x18\x05 \x01(\tH\x02\x88\x01\x01\x12\x37\n\tauth_mode\x18\x06 \x01(\x0e\x32\x1f.controller.ApplicationAuthModeH\x03\x88\x01\x01\x12 \n\x0fmax_concurrency\x18\x07 \x01(\x05\x42\x02\x18\x01H\x04\x88\x01\x01\x12.\n\x08metadata\x18\x08 \x01(\x0b\x32\x17.google.protobuf.StructH\x05\x88\x01\x01\x42\x17\n\x15_machine_requirementsB\r\n\x0b_setup_funcB\x13\n\x11_application_nameB\x0c\n\n_auth_modeB\x12\n\x10_max_concurrencyB\x0b\n\t_metadata"7\n\x1dRegisterApplicationResultType\x12\x16\n\x0e\x61pplication_id\x18\x01 \x01(\t"z\n\x19RegisterApplicationResult\x12\x12\n\x04logs\x18\x01 \x03(\x0b\x32\x04.Log\x12>\n\x06result\x18\x02 \x01(\x0b\x32).controller.RegisterApplicationResultTypeH\x00\x88\x01\x01\x42\t\n\x07_result"\xc2\x01\n\x18UpdateApplicationRequest\x12\x18\n\x10\x61pplication_name\x18\x01 \x01(\t\x12\x17\n\nkeep_alive\x18\x02 \x01(\x05H\x00\x88\x01\x01\x12\x1d\n\x10max_multiplexing\x18\x03 \x01(\x05H\x01\x88\x01\x01\x12\x1c\n\x0fmax_concurrency\x18\x04 \x01(\x05H\x02\x88\x01\x01\x42\r\n\x0b_keep_aliveB\x13\n\x11_max_multiplexingB\x12\n\x10_max_concurrency"D\n\x17UpdateApplicationResult\x12)\n\nalias_info\x18\x01 \x01(\x0b\x32\x15.controller.AliasInfo"f\n\x0fSetAliasRequest\x12\r\n\x05\x61lias\x18\x01 \x01(\t\x12\x10\n\x08revision\x18\x02 \x01(\t\x12\x32\n\tauth_mode\x18\x03 \x01(\x0e\x32\x1f.controller.ApplicationAuthMode"\x10\n\x0eSetAliasResult"#\n\x12\x44\x65leteAliasRequest\x12\r\n\x05\x61lias\x18\x01 \x01(\t"%\n\x11\x44\x65leteAliasResult\x12\x10\n\x08revision\x18\x01 \x01(\t"\x14\n\x12ListAliasesRequest";\n\x11ListAliasesResult\x12&\n\x07\x61liases\x18\x01 \x03(\x0b\x32\x15.controller.AliasInfo"\xbf\x01\n\tAliasInfo\x12\r\n\x05\x61lias\x18\x01 \x01(\t\x12\x10\n\x08revision\x18\x02 \x01(\t\x12\x32\n\tauth_mode\x18\x03 \x01(\x0e\x32\x1f.controller.ApplicationAuthMode\x12\x17\n\x0fmax_concurrency\x18\x04 \x01(\x05\x12\x18\n\x10max_multiplexing\x18\x05 \x01(\x05\x12\x12\n\nkeep_alive\x18\x06 \x01(\x05\x12\x16\n\x0e\x61\x63tive_runners\x18\x07 \x01(\x05">\n\x10SetSecretRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\x05value\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_value"\x13\n\x11SetSecretResponse"\x14\n\x12ListSecretsRequest"^\n\x06Secret\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x35\n\x0c\x63reated_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x88\x01\x01\x42\x0f\n\r_created_time":\n\x13ListSecretsResponse\x12#\n\x07secrets\x18\x01 \x03(\x0b\x32\x12.controller.Secret"(\n\x17ListAliasRunnersRequest\x12\r\n\x05\x61lias\x18\x01 \x01(\t"C\n\x18ListAliasRunnersResponse\x12\'\n\x07runners\x18\x01 \x03(\x0b\x32\x16.controller.RunnerInfo"Y\n\nRunnerInfo\x12\x11\n\trunner_id\x18\x01 \x01(\t\x12\x1a\n\x12in_flight_requests\x18\x02 \x01(\x05\x12\x1c\n\x14\x65xpiration_countdown\x18\x03 \x01(\x05*:\n\x13\x41pplicationAuthMode\x12\x0b\n\x07PRIVATE\x10\x00\x12\n\n\x06PUBLIC\x10\x01\x12\n\n\x06SHARED\x10\x02\x32\xc8\x08\n\x11IsolateController\x12=\n\x03Run\x12\x15.controller.HostedRun\x1a\x1b.controller.HostedRunResult"\x00\x30\x01\x12=\n\x03Map\x12\x15.controller.HostedMap\x1a\x1b.controller.HostedRunResult"\x00\x30\x01\x12V\n\rCreateUserKey\x12 .controller.CreateUserKeyRequest\x1a!.controller.CreateUserKeyResponse"\x00\x12S\n\x0cListUserKeys\x12\x1f.controller.ListUserKeysRequest\x1a .controller.ListUserKeysResponse"\x00\x12V\n\rRevokeUserKey\x12 .controller.RevokeUserKeyRequest\x1a!.controller.RevokeUserKeyResponse"\x00\x12h\n\x13RegisterApplication\x12&.controller.RegisterApplicationRequest\x1a%.controller.RegisterApplicationResult"\x00\x30\x01\x12`\n\x11UpdateApplication\x12$.controller.UpdateApplicationRequest\x1a#.controller.UpdateApplicationResult"\x00\x12\x45\n\x08SetAlias\x12\x1b.controller.SetAliasRequest\x1a\x1a.controller.SetAliasResult"\x00\x12N\n\x0b\x44\x65leteAlias\x12\x1e.controller.DeleteAliasRequest\x1a\x1d.controller.DeleteAliasResult"\x00\x12N\n\x0bListAliases\x12\x1e.controller.ListAliasesRequest\x1a\x1d.controller.ListAliasesResult"\x00\x12J\n\tSetSecret\x12\x1c.controller.SetSecretRequest\x1a\x1d.controller.SetSecretResponse"\x00\x12P\n\x0bListSecrets\x12\x1e.controller.ListSecretsRequest\x1a\x1f.controller.ListSecretsResponse"\x00\x12_\n\x10ListAliasRunners\x12#.controller.ListAliasRunnersRequest\x1a$.controller.ListAliasRunnersResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "controller_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _REGISTERAPPLICATIONREQUEST.fields_by_name["max_concurrency"]._options = None
    _REGISTERAPPLICATIONREQUEST.fields_by_name[
        "max_concurrency"
    ]._serialized_options = b"\030\001"
    _globals["_APPLICATIONAUTHMODE"]._serialized_start = 3727
    _globals["_APPLICATIONAUTHMODE"]._serialized_end = 3785
    _globals["_HOSTEDMAP"]._serialized_start = 156
    _globals["_HOSTEDMAP"]._serialized_end = 378
    _globals["_HOSTEDRUN"]._serialized_start = 381
    _globals["_HOSTEDRUN"]._serialized_end = 627
    _globals["_CREATEUSERKEYREQUEST"]._serialized_start = 630
    _globals["_CREATEUSERKEYREQUEST"]._serialized_end = 766
    _globals["_CREATEUSERKEYREQUEST_SCOPE"]._serialized_start = 729
    _globals["_CREATEUSERKEYREQUEST_SCOPE"]._serialized_end = 756
    _globals["_CREATEUSERKEYRESPONSE"]._serialized_start = 768
    _globals["_CREATEUSERKEYRESPONSE"]._serialized_end = 827
    _globals["_LISTUSERKEYSREQUEST"]._serialized_start = 829
    _globals["_LISTUSERKEYSREQUEST"]._serialized_end = 850
    _globals["_LISTUSERKEYSRESPONSE"]._serialized_start = 852
    _globals["_LISTUSERKEYSRESPONSE"]._serialized_end = 918
    _globals["_REVOKEUSERKEYREQUEST"]._serialized_start = 920
    _globals["_REVOKEUSERKEYREQUEST"]._serialized_end = 958
    _globals["_REVOKEUSERKEYRESPONSE"]._serialized_start = 960
    _globals["_REVOKEUSERKEYRESPONSE"]._serialized_end = 983
    _globals["_USERKEYINFO"]._serialized_start = 986
    _globals["_USERKEYINFO"]._serialized_end = 1133
    _globals["_HOSTEDRUNRESULT"]._serialized_start = 1136
    _globals["_HOSTEDRUNRESULT"]._serialized_end = 1313
    _globals["_HOSTEDRUNSTATUS"]._serialized_start = 1316
    _globals["_HOSTEDRUNSTATUS"]._serialized_end = 1444
    _globals["_HOSTEDRUNSTATUS_STATE"]._serialized_start = 1385
    _globals["_HOSTEDRUNSTATUS_STATE"]._serialized_end = 1444
    _globals["_MACHINEREQUIREMENTS"]._serialized_start = 1447
    _globals["_MACHINEREQUIREMENTS"]._serialized_end = 1833
    _globals["_REGISTERAPPLICATIONREQUEST"]._serialized_start = 1836
    _globals["_REGISTERAPPLICATIONREQUEST"]._serialized_end = 2337
    _globals["_REGISTERAPPLICATIONRESULTTYPE"]._serialized_start = 2339
    _globals["_REGISTERAPPLICATIONRESULTTYPE"]._serialized_end = 2394
    _globals["_REGISTERAPPLICATIONRESULT"]._serialized_start = 2396
    _globals["_REGISTERAPPLICATIONRESULT"]._serialized_end = 2518
    _globals["_UPDATEAPPLICATIONREQUEST"]._serialized_start = 2521
    _globals["_UPDATEAPPLICATIONREQUEST"]._serialized_end = 2715
    _globals["_UPDATEAPPLICATIONRESULT"]._serialized_start = 2717
    _globals["_UPDATEAPPLICATIONRESULT"]._serialized_end = 2785
    _globals["_SETALIASREQUEST"]._serialized_start = 2787
    _globals["_SETALIASREQUEST"]._serialized_end = 2889
    _globals["_SETALIASRESULT"]._serialized_start = 2891
    _globals["_SETALIASRESULT"]._serialized_end = 2907
    _globals["_DELETEALIASREQUEST"]._serialized_start = 2909
    _globals["_DELETEALIASREQUEST"]._serialized_end = 2944
    _globals["_DELETEALIASRESULT"]._serialized_start = 2946
    _globals["_DELETEALIASRESULT"]._serialized_end = 2983
    _globals["_LISTALIASESREQUEST"]._serialized_start = 2985
    _globals["_LISTALIASESREQUEST"]._serialized_end = 3005
    _globals["_LISTALIASESRESULT"]._serialized_start = 3007
    _globals["_LISTALIASESRESULT"]._serialized_end = 3066
    _globals["_ALIASINFO"]._serialized_start = 3069
    _globals["_ALIASINFO"]._serialized_end = 3260
    _globals["_SETSECRETREQUEST"]._serialized_start = 3262
    _globals["_SETSECRETREQUEST"]._serialized_end = 3324
    _globals["_SETSECRETRESPONSE"]._serialized_start = 3326
    _globals["_SETSECRETRESPONSE"]._serialized_end = 3345
    _globals["_LISTSECRETSREQUEST"]._serialized_start = 3347
    _globals["_LISTSECRETSREQUEST"]._serialized_end = 3367
    _globals["_SECRET"]._serialized_start = 3369
    _globals["_SECRET"]._serialized_end = 3463
    _globals["_LISTSECRETSRESPONSE"]._serialized_start = 3465
    _globals["_LISTSECRETSRESPONSE"]._serialized_end = 3523
    _globals["_LISTALIASRUNNERSREQUEST"]._serialized_start = 3525
    _globals["_LISTALIASRUNNERSREQUEST"]._serialized_end = 3565
    _globals["_LISTALIASRUNNERSRESPONSE"]._serialized_start = 3567
    _globals["_LISTALIASRUNNERSRESPONSE"]._serialized_end = 3634
    _globals["_RUNNERINFO"]._serialized_start = 3636
    _globals["_RUNNERINFO"]._serialized_end = 3725
    _globals["_ISOLATECONTROLLER"]._serialized_start = 3788
    _globals["_ISOLATECONTROLLER"]._serialized_end = 4884
# @@protoc_insertion_point(module_scope)
