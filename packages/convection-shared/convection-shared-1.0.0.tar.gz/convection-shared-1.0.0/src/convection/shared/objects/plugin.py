# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import typing

from atckit.version import version_locator

from convection.shared.exceptions import VersionCompatibilityError
from convection.shared.objects.plugin_metadata import ConvectionPluginMetadata
from convection.shared.objects.targetable import ConvectionTargetable
from convection.shared.objects.target import ConvectionTarget

class ConvectionPlugin(ConvectionTargetable):
    """Plugin Container
    """
    metadata:ConvectionPluginMetadata
    _compat_checked:bool

    def __init__(self, name: str, my_type: str, specker_root_spec: str, config: dict[str, typing.Any]) -> None:
        self._compat_checked = False
        super().__init__(name, my_type, specker_root_spec, config)

    def compat_check(self,in_metadata:ConvectionPluginMetadata) -> None:
        """Plugin Compatibility Checker
        @param ConvectionPluginMetadata \c in_metadata Incoming Metadata to check Version against loaded version compatibility string
        @retval None Nothing
        @raises SystemError No Metadata Object
        @raises VersionCompatibilityError Incoming Version is incompatible with Loaded version
        Sets `_compat_checked = True` after running, to allow developer to select whether or not to run compat again
        """
        self_name:str = type(self).__qualname__
        if self.metadata is None:
            raise SystemError(f"{self_name} did not have a Metadata object")
        compatible:bool = len(version_locator(self.metadata.compatibility,[str(in_metadata.version)])) > 0
        if not compatible:
            raise VersionCompatibilityError(f"Existing {self_name} (version {str(in_metadata.version)}) is not compatible with {str(self.metadata.version)}; Loaded Compat: {self.metadata.compatibility}")
        self.logger.debug(f"{self_name} Compatibility Check passed")
        if in_metadata.version != self.metadata.version:
            self.logger.warning(f"{self_name} Version has changed, its structure will be upgraded on the next write")
        self._compat_checked = True

    #Define API Methods below here
    # pylint: disable=unused-argument
    def create(self,target:ConvectionTarget) -> bool:
        """Create New on Target
        @param bool Success/Failure
        @throws NotImplementedError This function should be overwritten, do not use super()
        """
        raise NotImplementedError(f"{type(self).__qualname__} does not implement create")

    def destroy(self,target:ConvectionTarget) -> bool:
        """Destroy on Target
        @param bool Success/Failure
        @throws NotImplementedError This function should be overwritten, do not use super()
        """
        raise NotImplementedError(f"{type(self).__qualname__} does not implement destroy")

    def modify(self,target:ConvectionTarget) -> bool:
        """Modify Existing on Target
        @param bool Success/Failure
        @throws NotImplementedError This function should be overwritten, do not use super()
        """
        raise NotImplementedError(f"{type(self).__qualname__} does not implement modify")

    # pylint: enable=unused-argument
