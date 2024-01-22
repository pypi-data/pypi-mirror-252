# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import typing

from convection.shared.objects.object import ConvectionObject
from convection.shared.objects.instance import ConvectionInstance

class ConvectionTarget(ConvectionObject):
    """Target Object
    """
    _actions:list["ConvectionPlugin_Action"] # type: ignore[name-defined]
    _instances:list[ConvectionInstance]
    _access_method:"ConvectionPlugin_Access" # type: ignore[name-defined]

    have_connector:bool
    have_group:bool
    _have_accessor:bool

    @property
    def have_accessor(self) -> bool:
        """Accessor Configured Check
        @retval bool Whether Accessor has been set
        """
        return self._have_accessor

    @property
    def access_method(self) -> "ConvectionPlugin_Access": # type: ignore[name-defined]
        """Attached Instance Access Method
        @retval ConvectionPlugin_Access Instance Access Method
        """
        return self._access_method

    @property
    def actions(self) -> list["ConvectionPlugin_Action"]: # type: ignore[name-defined]
        """Attached Actions
        @retval list[ConvectionPlugin_Action] List of Attached Actions
        """
        return self._actions

    @property
    def instance_names(self) -> list[str]:
        """Instance Name list
        @retval list[str] List of Instance Names
        """
        return [ i.name for i in self._instances ]

    @property
    def action_names(self) -> list[str]:
        """Action Name list
        @retval list[str] List of Action Names
        """
        return [ a.name for a in self._actions ]

    def __init__(self, name: str, config: dict[str, typing.Any]) -> None:
        self.have_connector = False
        self.have_group = False
        self._have_accessor = False
        self._instances = []
        self._actions = []
        super().__init__(name, "target", "target", config)

    def attach_access_method(self,method:"ConvectionPlugin_Access") -> None: # type: ignore[name-defined]
        """Attach Access Method
        @param ConvectionPlugin_Access \c method Access Method Plugin
        @retval None Nothing
        """
        self._have_accessor = True
        self._access_method = method

    def attach_instance(self,instance:ConvectionInstance) -> None:
        """Attach Instance
        @param ConvectionInstance \c instance Instance to Attach
        @retval None Nothing
        """
        if instance.name not in self.instance_names:
            self._instances.append(instance)

    def detach_instance(self,instance:typing.Union[ConvectionInstance,str]) -> bool:
        """Remove Instance
        @param Union[ConvectionInstance,str] \c instance Instance Name or Instance Object
        @retval bool Whether Instance existed or not
        """
        instance_name:str = "UNKNOWN"
        if isinstance(instance,ConvectionInstance):
            instance_name = instance.name
        elif isinstance(instance,str):
            instance_name = instance
        try:
            i_idx:int = self.instance_names.index(instance_name)
        except ValueError:
            return False
        self._instances.pop(i_idx)
        return True

    def attach_action(self,action:"ConvectionPlugin_Action") -> None: # type: ignore[name-defined]
        """Attach Action
        @param ConvectionPlugin_Action \c action Action to Attach
        @retval None Nothing
        """
        if action.name not in self.action_names:
            self._actions.append(action)

    def detach_action(self,action:typing.Union["ConvectionPlugin_Action",str]) -> bool: # type: ignore[name-defined]
        """Remove Action
        @param Union[ConvectionPlugin_Access,str] \c action Action Name or Action Object
        @retval bool Whether Action existed or not
        """
        action_name:str = "UNKNOWN"
        # pylint: disable=isinstance-second-argument-not-valid-type
        if isinstance(action,"ConvectionPlugin_Action"): # type: ignore[arg-type]
            action_name = action.name # type: ignore[union-attr] # Because of the quoted defined name
        # pylint: enable=isinstance-second-argument-not-valid-type
        elif isinstance(action,str):
            action_name = action
        try:
            i_idx:int = self.action_names.index(action_name)
        except ValueError:
            return False
        self._actions.pop(i_idx)
        return True
