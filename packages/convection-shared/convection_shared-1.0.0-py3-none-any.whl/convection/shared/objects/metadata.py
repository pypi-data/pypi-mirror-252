# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import typing

from atckit.version import Version

class ConvectionMetadata:
    """Convection Metadata Container
    """

    _version:Version
    _compatibility:str
    _author:str
    _updated:int

    @property
    def version(self) -> Version:
        """Version Information
        @retval Version Version Info
        """
        return self._version

    @property
    def author(self) -> str:
        """Author Information
        @retval str Author Info
        """
        return self._author

    @property
    def updated(self) -> int:
        """Updated Date Information
        @retval int Date Last Updated
        """
        return self._updated

    @property
    def compatibility(self) -> str:
        """Version Compatibility Matcher
        @retval str Compatibility Version Search String
        """
        return self._compatibility

    def __init__(self,metadata:dict[str,typing.Any]) -> None:
        for k,v in metadata.items():
            setattr(self,f"_{k}",v)

    def get(self) -> dict[str,typing.Any]:
        """Get Metadata as dictionary
        @retval dict[str,Any] Metadata
        """
        return {
            "version": str(self.version),
            "compatibility": self.compatibility,
            "author": self.author,
            "updated": self.updated
        }
