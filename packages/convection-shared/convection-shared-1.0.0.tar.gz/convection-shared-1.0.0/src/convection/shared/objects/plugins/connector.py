# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import typing

from convection.shared.objects.plugin import ConvectionPlugin
from convection.shared.objects.target import ConvectionTarget

class ConvectionPlugin_Connector(ConvectionPlugin):
    """Connector Base; API for Connecting to Providers (Cloud / VM / etc)
    """

    def __init__(self, name: str, specker_root_spec:str, config: dict[str, typing.Any]) -> None:
        super().__init__(name, "plugin.connector", specker_root_spec, config)

    def attach_target(self, target: ConvectionTarget) -> None:
        """Attach Target for Connector
        @param ConvectionTarget \c target Target to Attach
        @retval None Nothing
        """
        target.have_connector = True
        super().attach_target(target)
        return None

    #Define API Methods below here
    # pylint: disable=unused-argument

    def connect(self) -> bool:
        """Connect / Authenticate
        @param bool Success/Failure
        @throws NotImplementedError This function should be overwritten, do not use super()
        """
        raise NotImplementedError(f"{type(self).__qualname__} does not implement connect")

    def disconnect(self) -> bool:
        """Disconnect / Deauth
        @param bool Success/Failure
        @throws NotImplementedError This function should be overwritten, do not use super()
        """
        raise NotImplementedError(f"{type(self).__qualname__} does not implement disconnect")

    def status(self) -> bool:
        """Connection / Authentication Status
        @param bool Success/Failure
        @throws NotImplementedError This function should be overwritten, do not use super()
        """
        raise NotImplementedError(f"{type(self).__qualname__} does not implement status")

    def info(self) -> bool:
        """Gather Information about Instance on Connector
        @param bool Success/Failure
        @throws NotImplementedError This function should be overwritten, do not use super()
        """
        raise NotImplementedError(f"{type(self).__qualname__} does not implement info")

    # pylint: enable=unused-argument
