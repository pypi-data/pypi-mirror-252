import time
from typing import Any, List

from ..openapi.api_config import APIConfig
from .base import Base
from ..exceptions import BlissRESTError

from ..openapi.services.Hardware_service import (
    RegisterHardwareResource_post_register_post,
    HardwaresResource_get_get,
    HardwareResource_get__string_id__get,
    HardwareResource_post__string_id__post,
    HardwareResource_put__string_id__put,
)
from ..openapi.models.RegisterHardwareSchema import RegisterHardwareSchema
from ..openapi.models.CallObjectFunction import CallObjectFunction
from ..openapi.models.SetObjectProperty import SetObjectProperty


class HardwareObject:
    """A `HardwareObject`

    Properties are mapped to python properties:
        print(omega.position)
        omega.velocity = 2000

    Functions can be directly called:
        omega.move(10)

    """

    _update_interval = 0.2

    def __init__(self, address: str, api_config: APIConfig):
        self._last_status_time = 0
        self._state = None
        self._api_config = api_config
        self._address = address

        self._get_status()

    def __str__(self):
        properties = "".join(
            [
                f"  {property}:\t{value}\n"
                for property, value in self._state.properties.items()
            ]
        )
        callables = ", ".join(self._state.callables)

        errors = ""
        if self.errors:
            errors = f"! Errors: \n  {self.errors}"

        return f"""Address: {self._address} ({self.type})
{errors}
Properties:
{properties}

Callables:
  {callables}

"""

    @property
    def type(self):
        return self._state.type

    @property
    def errors(self):
        return self._state.errors

    def __getattr__(self, item):
        state = object.__getattribute__(self, "_state")
        if state:
            get_status = object.__getattribute__(self, "_get_status")
            get_status()
            state = object.__getattribute__(self, "_state")
            if item in state.properties:
                return state.properties[item]

            if item in state.callables:
                make_callable = object.__getattribute__(self, "_make_callable")
                return make_callable(item)

        return super().__getattribute__(item)

    def __setattr__(self, item: str, value: Any):
        if hasattr(self, "_state"):
            if self._state:
                if item in self._state.properties:
                    self._set(item, value)

        return super().__setattr__(item, value)

    def _make_callable(self, function: str):
        return lambda value=None: self._call(function=function, value=value)

    def _get_status(self):
        now = time.time()
        if now - self._last_status_time > self._update_interval:
            self._state = HardwareResource_get__string_id__get(
                id=self._address, api_config_override=self._api_config
            )
            self._last_status_time = now

    def _call(self, function: str, value: Any):
        return HardwareResource_post__string_id__post(
            id=self._address,
            data=CallObjectFunction(function=function, value=value),
            api_config_override=self._api_config,
        )

    def _set(self, property: str, value: Any):
        return HardwareResource_put__string_id__put(
            id=self._address,
            data=SetObjectProperty(property=property, value=value),
            api_config_override=self._api_config,
        )


class Hardware(Base):
    def __str__(self):
        objects = "".join([f"  {address}\n" for address in self.available])
        return f"Hardware:\n{objects}"

    @property
    def available(self):
        """List the currently available `HardwareObjects`"""
        response = HardwaresResource_get_get(api_config_override=self._api_config)
        return [result.id for result in response.results]

    def register(self, *addresses: List[str]):
        """Register a `HardwareObject` with blissterm"""
        return RegisterHardwareResource_post_register_post(
            data=RegisterHardwareSchema(ids=addresses),
            api_config_override=self._api_config,
        )

    def get(self, address: str):
        """Get a hardware object from its beacon `address`"""
        if address not in self.available:
            try:
                print(f"Object `{address}` not yet available, trying to register it...")
                self.register(address)
            except BlissRESTError:
                raise KeyError(
                    f"Object `{address}` not available, are you are sure it exists in beacon?"
                )

        return HardwareObject(address=address, api_config=self._api_config)
