# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import typing

from convection.shared.objects.target import ConvectionTarget
from convection.shared.objects.targetable import ConvectionTargetable

class ConvectionGroup(ConvectionTargetable):
    """Group Object
    """

    def __init__(self, name: str, config: dict[str, typing.Any]) -> None:
        super().__init__(name, "group", "group", config)

    def attach_target(self, target: ConvectionTarget) -> None:
        """Attach Target to Group
        @param ConvectionTarget \c target Target Object
        @retval None Nothing
        """
        target.have_group = True
        super().attach_target(target)
