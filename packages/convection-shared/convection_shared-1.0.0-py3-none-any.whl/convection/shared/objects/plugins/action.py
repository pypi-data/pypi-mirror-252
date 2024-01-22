# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import typing

from convection.shared.objects.plugin import ConvectionPlugin

class ConvectionPlugin_Action(ConvectionPlugin):
    """Action Base; API for Performing Actions on Instances (Files / Users / etc)
    """

    def __init__(self, name: str, specker_root_spec: str, config: dict[str, typing.Any]) -> None:
        super().__init__(name, "plugin.action", specker_root_spec, config)
