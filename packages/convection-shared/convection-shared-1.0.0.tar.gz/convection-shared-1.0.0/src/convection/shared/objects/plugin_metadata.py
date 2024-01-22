# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import typing
from convection.shared.objects.metadata import ConvectionMetadata


class ConvectionPluginMetadata(ConvectionMetadata):
    """Convection Plugin Metadata, Plugin Type, Name, Description additions"""

    _name:str
    _type:str
    _description:str

    @property
    def name(self) -> str:
        """Plugin Name
        @retval str Plugin Name
        """
        return self._name

    @property
    def type(self) -> str:
        """Plugin Type
        @retval str Plugin Type
        """
        return self._type

    @property
    def description(self) -> str:
        """Plugin Description
        @retval str Plugin Description
        """
        return self._description

    def __init__(self, metadata: dict[str, typing.Any]) -> None:
        for k,v in metadata["plugin"].items():
            setattr(self,f"_{k}",v)
        super().__init__(metadata)

    def get(self) -> dict[str, typing.Any]:
        """Get Metadata as Dictionary
        @retval dict[str,Any] Metadata data
        """
        metadata:dict[str,typing.Any] = super().get()
        metadata["plugin"] = {
            "name": self.name,
            "type": self.type,
            "description": self.description
        }
        return metadata
