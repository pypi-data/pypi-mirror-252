# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import logging
from pathlib import Path
import typing

from deepmerge.merger import Merger

from specker.loader import SpecLoader
from atckit.utilfuncs import UtilFuncs

from convection.shared.specker_static import StaticSpecker

class ConvectionConfigCore:
    """Configuration Loader/Getter
    """

    logger:logging.Logger
    _configuration:dict[typing.Any,typing.Any]
    _specker:SpecLoader

    @property
    def specker_instance(self) -> SpecLoader:
        """Specker object for static instance
        @retval SpecLoader Specker Object
        """
        return self._specker

    def __init__(self,specker_root_spec:str,target_config:typing.Union[Path,dict[typing.Any,typing.Any]],override_type:str = "auto") -> None:
        try:
            getattr(self,"logger")
        except BaseException:
            self.logger = UtilFuncs.create_object_logger(self)
        try:
            self._specker = StaticSpecker.instance.specker_instance
        except AttributeError:
            StaticSpecker()
            self._specker = StaticSpecker.instance.specker_instance
            StaticSpecker.instance.specker_instance.load_specs(Path(__file__).resolve().parent.parent.joinpath("convection.secrets").joinpath("specs"))

        default_config:dict[str,typing.Any] = {}
        default_config = self._specker.defaults(specker_root_spec)
        merger:Merger = Merger([
                (list, ["prepend"]),
                (dict, ["merge"]),
            ],
            ["override"],
            ["override_if_not_empty"]
        )
        root_config:dict[str,typing.Any] = {}
        if isinstance(target_config,Path):
            root_config = UtilFuncs.load_sfile(target_config,override_type)
        else:
            root_config = target_config

        self._configuration = merger.merge(default_config,root_config)
        spec_check:bool = self._specker.compare(specker_root_spec,self.get_configuration_value(None))
        if not spec_check:
            raise SyntaxError("Config Validation Failed")

    def validate_config(self,spec_name:str,config:dict[typing.Any,typing.Any]) -> bool:
        """Explicitly Validate Configuration Block
        @param str \c spec_name Name of Spec to use for validation
        @param dict[Any,Any] \c config Configuration block to Validate
        @retval bool Validation Result
        """
        result:bool = self._specker.compare(spec_name,config)
        return result

    def get_configuration_value(self,config_name:typing.Union[str,None]) -> typing.Any:
        """Get Configuration Value
        @param str \c or \c None \c config_name Name of configuration value to get
        @param bool \c processed Whether to process value and return the rendered result (True), or the raw result (False)
        @retval Any Configuration value, if it exists
        @throws ValueError Cannot find a key of the requested config tree
        @throws IndexError Index in configuration list is out of range
        @throws TypeError Attempting to scan a part of the config tree that is not a list or dict
        """
        if config_name is None:
            return self._configuration
        config_tree:list[str] = config_name.split('.')
        current_branch:typing.Union[list,dict[typing.Any,typing.Any],str,int,bool] = self._configuration.copy()
        traversed_tree:list[str] = []
        for i in range(0,len(config_tree)):
            tree_part:str = config_tree[i]
            if isinstance(current_branch,dict):
                if tree_part not in current_branch.keys():
                    raise ValueError("Cannot Locate branch of configuration",'.'.join(traversed_tree),tree_part)
                current_branch = current_branch[tree_part]
            elif isinstance(current_branch,list):
                branch_idx:int = int(tree_part)
                if branch_idx >= len(current_branch):
                    raise IndexError("Branch of Configuration out of Index Range",'.'.join(traversed_tree),tree_part)
                current_branch = current_branch[branch_idx]
            else:
                if i != len(config_tree):
                    raise TypeError("Attempt to traverse configuration tree on non-traversable type",'.'.join(traversed_tree),tree_part,type(current_branch).__name__)
                return current_branch
            traversed_tree.append(tree_part)
        return current_branch

    # pylint: disable=unused-argument
    def config_loader_callback(self,target:Path,cbargs:dict[str,typing.Any]) -> None:
        """Config Loader
        Callback for loading additional config files after initial load
        @param Path \c target Target Config file to load
        @param dict[str,Any] \c cbargs Callback args; NOT USED
        @retval None Nothing
        """
        configuration:dict[typing.Any,typing.Any] = UtilFuncs.load_sfile(target)
        original_conf:dict[typing.Any,typing.Any] = self._configuration.copy()
        merger = Merger([
                (list, ["prepend"]),
                (dict, ["merge"]),
            ],
            ["override"],
            ["override_if_not_empty"]
        )
        self._configuration = merger.merge(original_conf,configuration)
    # pylint: enable=unused-argument

class ConvectionConfiguration(ConvectionConfigCore):
    """Convection Primary Configuration Container
    """
    instance:"ConvectionConfiguration"

    _command_line:dict[str,typing.Any]

    @staticmethod
    def set_instance(instance:"ConvectionConfiguration") -> None:
        """Set Static Configuration Instance
        @retval None Nothing
        """
        ConvectionConfiguration.instance = instance

    def __init__(self,call_args:dict[str,typing.Any]) -> None:
        """Initializer
        @param dict[str,Any] \c call_args Calling Arguments
        @throws ValueError Invalid Input Override Type
        """
        self.logger = UtilFuncs.create_object_logger(self)
        ConvectionConfiguration.set_instance(self)
        if call_args["input_type"] not in [ "yaml", "json", "toml", "auto" ]:
            raise ValueError("Input type is invalid",call_args["input_type"])
        self._command_line = call_args
        config_file:Path = Path(self.get_commandline_arg("config")).resolve()
        config_root:Path = config_file.parent
        self._command_line["config_root"] = config_root
        super().__init__("root",config_file,self.get_commandline_arg("input_type"))

    def get_loglevel(self) -> int:
        """Get Configured Log Level
        @retval int logging.<level>
        """
        result:int = -1
        result_str:str = ""
        try:
            result_str = self.get_configuration_value("global.reporting.log.level")
        except BaseException:
            self.logger.debug("Could not locate option `global.reporting.log.level, falling back to commandline level")
        if result == -1:
            result = self.get_commandline_arg("loglevel")
        else:
            if result_str == "DEBUG":
                result = logging.DEBUG
            elif result_str == "INFO":
                result = logging.INFO
            elif result_str == "WARNING":
                result = logging.WARNING
            elif result_str == "ERROR":
                result = logging.ERROR
            elif result_str == "CRITICAL":
                result = logging.CRITICAL
            else:
                self.logger.error("Invalid Value for global.reporting.log.level, defaulting to INFO")
                result = logging.INFO
        return result

    def get_commandline_arg(self,arg_name:str) -> typing.Any:
        """Get Commandline Argument
        @param str \c arg_name Name of Commandline Argument to get
        @retval Any Value of Argument, if exists. None if not set
        """
        if arg_name not in self._command_line.keys():
            return None
        return self._command_line[arg_name]
