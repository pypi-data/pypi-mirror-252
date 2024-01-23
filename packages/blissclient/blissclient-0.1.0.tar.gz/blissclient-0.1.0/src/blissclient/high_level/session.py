from typing import Any

from .base import Base
from ..openapi.models.CallFunction import CallFunction
from ..openapi.models.UpdateScanSavingBody import UpdateScanSavingBody
from ..openapi.models.ScanSaving import ScanSaving
from ..openapi.services.Session_service import (
    CallFunctionResource_post__session_name__call_post,
    CallFunctionStateResource_get__session_name__call__call_id__get,
    CallFunctionStateResource_delete__session_name__call__call_id__delete,
    ScanSavingResource_get__session_name__scan_saving_get,
    ScanSavingResource_patch__session_name__scan_saving_patch,
)


class Session(Base):
    def __init__(self, session_name: str):
        self._session_name = session_name
        super().__init__()

    def __str__(self):
        return f"Session: {self.session_name}"

    @property
    def session_name(self):
        """The current session name"""
        return self._session_name

    def call(
        self,
        function: str,
        *args,
        call_async: bool = False,
        object_name: str = None,
        **kwargs,
    ):
        """Call a function in the session

        Kwargs:
            call_async: Allows the function to be called asynchronously
            object_name: Call a function on an object

        Returns:
            If `call_async` is `false`, returns the function return value
            If `call_async` is `true`, returns the `call_id` uuid
        """
        response = CallFunctionResource_post__session_name__call_post(
            self._session_name,
            CallFunction(
                call_async=call_async,
                function=function,
                args=args,
                kwargs=kwargs,
                object=object_name,
            ),
            api_config_override=self._api_config,
        )

        if call_async:
            return response.call_id
        else:
            return response.return_value

    def state(self, call_id: str):
        """Get the state of a function call from its `call_id`"""
        state = CallFunctionStateResource_get__session_name__call__call_id__get(
            self._session_name,
            call_id=call_id,
            api_config_override=self._api_config,
        )

        return state

    def kill(self, call_id: str):
        """Kill a currently asynchronously running function from its `call_id`"""
        CallFunctionStateResource_delete__session_name__call__call_id__delete(
            self._session_name, call_id=call_id, api_config_override=self._api_config
        )
        return True

    @property
    def scan_saving(self):
        """Get the current `SCAN_SAVING` configuration"""

        class ScanSavingRepr(ScanSaving):
            def __str__(self):
                return "Scan Saving:\n" + "\n".join(
                    [f"  {field}:\t{value}" for field, value in self]
                )

        scan_saving = ScanSavingResource_get__session_name__scan_saving_get(
            self._session_name, api_config_override=self._api_config
        )
        return ScanSavingRepr(**scan_saving.dict())

    def update_scan_saving(self, parameter: str, value: Any):
        """Update a `SCAN_SAVING property"""
        return ScanSavingResource_patch__session_name__scan_saving_patch(
            self._session_name,
            data=UpdateScanSavingBody(**{parameter: value}),
            api_config_override=self._api_config,
        )
