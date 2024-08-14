from chalk._gen.chalk.aggregate.v1 import backfill_pb2 as _backfill_pb2
from chalk._gen.chalk.aggregate.v1 import timeseries_pb2 as _timeseries_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class PlanAggregateBackfillRequest(_message.Message):
    __slots__ = ("params",)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _backfill_pb2.AggregateBackfillUserParams
    def __init__(
        self,
        params: _Optional[
            _Union[_backfill_pb2.AggregateBackfillUserParams, _Mapping]
        ] = ...,
    ) -> None: ...

class PlanAggregateBackfillResponse(_message.Message):
    __slots__ = ("series", "estimate", "params", "backfill", "errors")
    SERIES_FIELD_NUMBER: _ClassVar[int]
    ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    BACKFILL_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    series: _containers.RepeatedCompositeFieldContainer[
        _timeseries_pb2.AggregateTimeSeries
    ]
    estimate: _backfill_pb2.AggregateBackfillEstimate
    params: _backfill_pb2.AggregateBackfillUserParams
    backfill: _backfill_pb2.AggregateBackfill
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        series: _Optional[
            _Iterable[_Union[_timeseries_pb2.AggregateTimeSeries, _Mapping]]
        ] = ...,
        estimate: _Optional[
            _Union[_backfill_pb2.AggregateBackfillEstimate, _Mapping]
        ] = ...,
        params: _Optional[
            _Union[_backfill_pb2.AggregateBackfillUserParams, _Mapping]
        ] = ...,
        backfill: _Optional[_Union[_backfill_pb2.AggregateBackfill, _Mapping]] = ...,
        errors: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetAggregatesRequest(_message.Message):
    __slots__ = ("for_features",)
    FOR_FEATURES_FIELD_NUMBER: _ClassVar[int]
    for_features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, for_features: _Optional[_Iterable[str]] = ...) -> None: ...

class GetAggregatesResponse(_message.Message):
    __slots__ = ("series", "errors")
    SERIES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    series: _containers.RepeatedCompositeFieldContainer[
        _timeseries_pb2.AggregateTimeSeries
    ]
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        series: _Optional[
            _Iterable[_Union[_timeseries_pb2.AggregateTimeSeries, _Mapping]]
        ] = ...,
        errors: _Optional[_Iterable[str]] = ...,
    ) -> None: ...
