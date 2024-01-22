import atexit as _atexit
from typing import (
    Callable as _Callable,
    Concatenate as _Concatenate,
    ParamSpec as _ParamSpec,
    TypeVar as _TypeVar,
)
from easydrive import (
    Controller as _Controller,
    Vehicle as _Vehicle,
    TrackPiece,
    TrackPieceType,
    Lights,
    Lane3,
    Lane4
)
from anki.errors import *
from concurrent.futures import TimeoutError


_T = _TypeVar('_T')
_P = _ParamSpec('_P')

_control = _Controller()
_vehicle: _Vehicle|None = None


@_atexit.register
def _cleanup_vehicle():
    _control.disconnect_all()

def _raise_vehicle_not_found():
    if _vehicle is None:
        raise RuntimeError("There is no vehicle connected. Did you forget to call connect?")

def _wrap_vehicle(method: _Callable[_Concatenate[_Vehicle, _P], _T]) -> _Callable[_P, _T]:
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        _raise_vehicle_not_found()
        # Can't type hint an exception-based type guard. Static checkers thing _vehicle may be None
        return method(_vehicle, *args, **kwargs)
    return wrapper

def _wrap_vehicle_property(name: str):
    def wrapper():
        _raise_vehicle_not_found()
        return getattr(_vehicle, name)
    return wrapper


def connect(vehicle_id: int|None=None):
    global _vehicle
    _vehicle = _control.connect_one(vehicle_id)
    return _vehicle


wait_for_track_change = _wrap_vehicle(_Vehicle.wait_for_track_change)
set_speed = _wrap_vehicle(_Vehicle.set_speed)
stop = _wrap_vehicle(_Vehicle.stop)
change_lane = _wrap_vehicle(_Vehicle.change_lane)
change_position = _wrap_vehicle(_Vehicle.change_position)
get_lane = _wrap_vehicle(_Vehicle.get_lane)
align_to_start = _wrap_vehicle(_Vehicle.align_to_start)
get_current_track_piece: _Callable[[], TrackPiece] = _wrap_vehicle_property("current_track_piece")
get_map: _Callable[[], tuple[TrackPiece]|None] = _wrap_vehicle_property("map")
get_road_offset: _Callable[[], float|None] = _wrap_vehicle_property("road_offset")
get_speed: _Callable[[], int] = _wrap_vehicle_property("speed")
get_current_lane3: _Callable[[], Lane3|None] = _wrap_vehicle_property("current_lane3")
get_current_lane4: _Callable[[], Lane4|None] = _wrap_vehicle_property("current_lane4")
get_vehicle_id: _Callable[[], int] = _wrap_vehicle_property("id")

scan = _wrap_vehicle(_control.scan)  # This seems dirty, but it's actually legal
