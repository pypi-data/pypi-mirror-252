# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import logging
import typing

from atckit.utilfuncs import UtilFuncs

from convection.shared.config import ConvectionConfigCore
from convection.shared.objects.metadata import ConvectionMetadata

class ConvectionObject:
    """Object Container
    """
    logger:logging.Logger
    metadata:typing.Union[ConvectionMetadata,None]
    config:ConvectionConfigCore
    _name:str
    _my_type:str

    @property
    def name(self) -> str:
        """Object Name
        @retval str Object Name
        """
        return self._name

    @property
    def my_type(self) -> str:
        """Object Type Name
        @retval str Object Type
        """
        return self._my_type

    def __init__(self,name:str,my_type:str,specker_root_spec:str,config:dict[str,typing.Any]) -> None:
        """Initializer
        @param str \c name Object Name
        @param str \c my_type Object Type Name
        @param str \c specker_root_spec Specker Spec to validate against
        @param dict[str,Any] \c config Object Configuration data
        """
        self._name = name
        self._my_type = my_type
        self.logger = UtilFuncs.create_object_logger(self)
        self.config = ConvectionConfigCore(specker_root_spec,config)
        if not hasattr(self,"metadata"):
            try:
                self.metadata = ConvectionMetadata(self.config.get_configuration_value("metadata"))
            except ValueError:
                self.metadata = None
                self.logger.debug(f"{my_type} {name} is not a versioned object")
        if self.metadata is not None:
            self.logger.debug(f"Loading {my_type}.{name} ({type(self).__qualname__}), Version: {str(self.metadata.version)}, Updated: {self.metadata.updated}")
        else:
            self.logger.debug(f"Loading {my_type}.{name} ({type(self).__qualname__}) (Not Versioned (No Metadata))")

    def get_data(self,data_name:str) -> typing.Any:
        """Object-Specific Data Getter
        @param str data_name Config Tree Name to get (starting from `groups.<group>.data.`)
        @retval Value of Data Name
        """
        return self.config.get_configuration_value(f"data.{data_name}")
