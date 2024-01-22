# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import typing
from convection.shared.objects.object import ConvectionObject
from convection.shared.objects.target import ConvectionTarget

class ConvectionTargetable(ConvectionObject):
    """Object that Targets can Attach to
    """

    _targets:list[ConvectionTarget]

    @property
    def targets(self) -> list[ConvectionTarget]:
        """Target Objects
        @retval list[ConvectionTarget] List of Attached Targets
        """
        return self._targets

    @property
    def target_names(self) -> list[str]:
        """Target Names
        @retval list[str] Target Names
        """
        return [ t.name for t in self._targets ]

    def attach_target(self,target:ConvectionTarget) -> None:
        """Attach Target to Object
        @param ConvectionTarget \c Target Object
        @retval None Nothing
        """
        if target.name not in self.target_names:
            self.logger.info(f"Associating Target {target.name} with {self.my_type} {self.name}")
            self._targets.append(target)

    def __init__(self, name: str, my_type: str, specker_root_spec: str, config: dict[str, typing.Any]) -> None:
        self._targets = []
        super().__init__(name, my_type, specker_root_spec, config)
