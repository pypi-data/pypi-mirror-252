# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import typing

from convection.shared.objects.object import ConvectionObject

class ConvectionInstance(ConvectionObject):
    """Target Instance Object
    """

    def __init__(self, name: str, config: dict[str, typing.Any]) -> None:
        super().__init__(name, "instance", "instance", config)
