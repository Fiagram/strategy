import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Alert(_message.Message):
    __slots__ = ("id", "of_account_id", "timeframe", "symbol", "indicator", "operator", "trigger", "exp", "message", "created_at", "updated_at")
    class Timeframe(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMEFRAME_NONE: _ClassVar[Alert.Timeframe]
        TIMEFRAME_D1: _ClassVar[Alert.Timeframe]
        TIMEFRAME_W1: _ClassVar[Alert.Timeframe]
        TIMEFRAME_M1: _ClassVar[Alert.Timeframe]
    TIMEFRAME_NONE: Alert.Timeframe
    TIMEFRAME_D1: Alert.Timeframe
    TIMEFRAME_W1: Alert.Timeframe
    TIMEFRAME_M1: Alert.Timeframe
    class Indicator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INDICATOR_NONE: _ClassVar[Alert.Indicator]
        INDICATOR_CLOSE: _ClassVar[Alert.Indicator]
        INDICATOR_BOLLINGER_BANDS: _ClassVar[Alert.Indicator]
        INDICATOR_RSI: _ClassVar[Alert.Indicator]
        INDICATOR_MA10: _ClassVar[Alert.Indicator]
        INDICATOR_MA50: _ClassVar[Alert.Indicator]
        INDICATOR_MA100: _ClassVar[Alert.Indicator]
        INDICATOR_MA200: _ClassVar[Alert.Indicator]
    INDICATOR_NONE: Alert.Indicator
    INDICATOR_CLOSE: Alert.Indicator
    INDICATOR_BOLLINGER_BANDS: Alert.Indicator
    INDICATOR_RSI: Alert.Indicator
    INDICATOR_MA10: Alert.Indicator
    INDICATOR_MA50: Alert.Indicator
    INDICATOR_MA100: Alert.Indicator
    INDICATOR_MA200: Alert.Indicator
    class Operator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OPERATOR_NONE: _ClassVar[Alert.Operator]
        OPERATOR_GREATER_THAN: _ClassVar[Alert.Operator]
        OPERATOR_LESS_THAN: _ClassVar[Alert.Operator]
        OPERATOR_CROSSING_UP: _ClassVar[Alert.Operator]
        OPERATOR_CROSSING_DOWN: _ClassVar[Alert.Operator]
        OPERATOR_CROSSING: _ClassVar[Alert.Operator]
    OPERATOR_NONE: Alert.Operator
    OPERATOR_GREATER_THAN: Alert.Operator
    OPERATOR_LESS_THAN: Alert.Operator
    OPERATOR_CROSSING_UP: Alert.Operator
    OPERATOR_CROSSING_DOWN: Alert.Operator
    OPERATOR_CROSSING: Alert.Operator
    class Trigger(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TRIGGER_NONE: _ClassVar[Alert.Trigger]
        TRIGGER_ONCE: _ClassVar[Alert.Trigger]
        TRIGGER_EVERY: _ClassVar[Alert.Trigger]
    TRIGGER_NONE: Alert.Trigger
    TRIGGER_ONCE: Alert.Trigger
    TRIGGER_EVERY: Alert.Trigger
    ID_FIELD_NUMBER: _ClassVar[int]
    OF_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMEFRAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    INDICATOR_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    EXP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    of_account_id: int
    timeframe: Alert.Timeframe
    symbol: str
    indicator: Alert.Indicator
    operator: Alert.Operator
    trigger: Alert.Trigger
    exp: int
    message: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., of_account_id: _Optional[int] = ..., timeframe: _Optional[_Union[Alert.Timeframe, str]] = ..., symbol: _Optional[str] = ..., indicator: _Optional[_Union[Alert.Indicator, str]] = ..., operator: _Optional[_Union[Alert.Operator, str]] = ..., trigger: _Optional[_Union[Alert.Trigger, str]] = ..., exp: _Optional[int] = ..., message: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateAlertRequest(_message.Message):
    __slots__ = ("of_account_id", "timeframe", "symbol", "indicator", "operator", "trigger", "exp", "message")
    OF_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMEFRAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    INDICATOR_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    EXP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    of_account_id: int
    timeframe: Alert.Timeframe
    symbol: str
    indicator: Alert.Indicator
    operator: Alert.Operator
    trigger: Alert.Trigger
    exp: int
    message: str
    def __init__(self, of_account_id: _Optional[int] = ..., timeframe: _Optional[_Union[Alert.Timeframe, str]] = ..., symbol: _Optional[str] = ..., indicator: _Optional[_Union[Alert.Indicator, str]] = ..., operator: _Optional[_Union[Alert.Operator, str]] = ..., trigger: _Optional[_Union[Alert.Trigger, str]] = ..., exp: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class CreateAlertResponse(_message.Message):
    __slots__ = ("alert",)
    ALERT_FIELD_NUMBER: _ClassVar[int]
    alert: Alert
    def __init__(self, alert: _Optional[_Union[Alert, _Mapping]] = ...) -> None: ...

class GetAlertsRequest(_message.Message):
    __slots__ = ("of_account_id", "limit", "offset")
    OF_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    of_account_id: int
    limit: int
    offset: int
    def __init__(self, of_account_id: _Optional[int] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class GetAlertsResponse(_message.Message):
    __slots__ = ("alerts",)
    ALERTS_FIELD_NUMBER: _ClassVar[int]
    alerts: _containers.RepeatedCompositeFieldContainer[Alert]
    def __init__(self, alerts: _Optional[_Iterable[_Union[Alert, _Mapping]]] = ...) -> None: ...

class GetAlertRequest(_message.Message):
    __slots__ = ("of_account_id", "alert_id")
    OF_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALERT_ID_FIELD_NUMBER: _ClassVar[int]
    of_account_id: int
    alert_id: int
    def __init__(self, of_account_id: _Optional[int] = ..., alert_id: _Optional[int] = ...) -> None: ...

class GetAlertResponse(_message.Message):
    __slots__ = ("alert",)
    ALERT_FIELD_NUMBER: _ClassVar[int]
    alert: Alert
    def __init__(self, alert: _Optional[_Union[Alert, _Mapping]] = ...) -> None: ...

class UpdateAlertRequest(_message.Message):
    __slots__ = ("of_account_id", "alert_id", "timeframe", "symbol", "indicator", "operator", "trigger", "exp", "message")
    OF_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALERT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMEFRAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    INDICATOR_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    EXP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    of_account_id: int
    alert_id: int
    timeframe: Alert.Timeframe
    symbol: str
    indicator: Alert.Indicator
    operator: Alert.Operator
    trigger: Alert.Trigger
    exp: int
    message: str
    def __init__(self, of_account_id: _Optional[int] = ..., alert_id: _Optional[int] = ..., timeframe: _Optional[_Union[Alert.Timeframe, str]] = ..., symbol: _Optional[str] = ..., indicator: _Optional[_Union[Alert.Indicator, str]] = ..., operator: _Optional[_Union[Alert.Operator, str]] = ..., trigger: _Optional[_Union[Alert.Trigger, str]] = ..., exp: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class UpdateAlertResponse(_message.Message):
    __slots__ = ("alert",)
    ALERT_FIELD_NUMBER: _ClassVar[int]
    alert: Alert
    def __init__(self, alert: _Optional[_Union[Alert, _Mapping]] = ...) -> None: ...

class DeleteAlertRequest(_message.Message):
    __slots__ = ("of_account_id", "alert_id")
    OF_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALERT_ID_FIELD_NUMBER: _ClassVar[int]
    of_account_id: int
    alert_id: int
    def __init__(self, of_account_id: _Optional[int] = ..., alert_id: _Optional[int] = ...) -> None: ...

class DeleteAlertResponse(_message.Message):
    __slots__ = ("of_account_id", "alert_id")
    OF_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALERT_ID_FIELD_NUMBER: _ClassVar[int]
    of_account_id: int
    alert_id: int
    def __init__(self, of_account_id: _Optional[int] = ..., alert_id: _Optional[int] = ...) -> None: ...
