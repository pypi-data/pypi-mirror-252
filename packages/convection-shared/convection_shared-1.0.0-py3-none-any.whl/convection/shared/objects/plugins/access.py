# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import typing

from convection.shared.objects.plugin import ConvectionPlugin

class ConvectionPlugin_Access(ConvectionPlugin):
    """Access Method Base; API for Connecting to Instances (VM / Bare Metal / Docker / etc)
    """

    def __init__(self, name: str, specker_root_spec:str, config: dict[str, typing.Any]) -> None:
        super().__init__(name, "plugin.access", specker_root_spec, config)

    #Define API Methods below here
    # pylint: disable=unused-argument
    def initialize(self) -> bool:
        """Initialize Access Method
        @retval bool Success / Failure
        Setup, etc
        """
        raise NotImplementedError(f"{type(self).__qualname__} does not implement initialize")

    def execute(self,target:"ConvectionTarget",action:"ConvectionPlugin_Action") -> bool: # type: ignore[name-defined]
        """Execute Method
        @param ConvectionTarget \c target Target to Perform Action on
        @param ConvectionPlugin_Action \c action Action to Perform on Target
        @retval bool Success / Failure
        """
        raise NotImplementedError(f"{type(self).__qualname__} does not implement execute")

    def cleanup(self) -> bool:
        """Access Method Cleanup
        Close / Cleanup
        @retval bool Success / Failure
        """
        raise NotImplementedError(f"{type(self).__qualname__} does not implement close")

    # pylint: enable=unused-argument
