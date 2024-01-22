# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import re
import logging
import types
import typing
import importlib
import inspect
from sys import exit as sys_exit
from pathlib import Path

from tabulate import tabulate

from convection.shared.specker_static import StaticSpecker

def exit_invalid_cmd() -> None:
    """Invalid Command Exit
    @retval None Nothing
    Exit code 2
    """
    logging.critical("Invalid Command")
    sys_exit(2)

def get_log_levels(logger_name:typing.Union[str,None] = None) -> dict[str,int]:
    """Get Log Level for a logging.Logger, or see all registered logger levels
    @param Union[str,None] \c logger_name Logger Name. Default None. None will return all Loggers
    @retval dict[str,int] Names and Levels of each registered Logger
    """
    root_logger:logging.Logger = logging.getLogger()
    all_loggers:dict[str,typing.Union[logging.Logger,logging.PlaceHolder]] = root_logger.manager.loggerDict
    if logger_name is None:
        loggers:dict[str,int] = {}
        for registered_logger,logger in all_loggers.items():
            if not isinstance(logger,logging.Logger):
                continue
            loggers[registered_logger] = logger.level
        return loggers
    if logger_name not in all_loggers.keys():
        return {}
    req_logger:typing.Union[logging.Logger,logging.PlaceHolder] = all_loggers[logger_name]
    if not isinstance(req_logger,logging.Logger):
        return {}
    return { logger_name: req_logger.level }

def set_log_level(logger_name:str,level:int) -> bool:
    """Set Log Levels
    @param str \c logger_name Logger Name to set. Must exist
    @retval bool If level was set, or logger did not exist
    """
    loggers:dict[str,int] = get_log_levels(logger_name)
    if logger_name not in loggers.keys():
        return False
    target:logging.Logger = logging.getLogger().manager.getLogger(logger_name)
    target.setLevel(level)
    return True

def value_parser(value:typing.Union[dict,list,str]) -> typing.Any:
    """Template processor. Not DJANGO!
    @param Union[dict,list,str] \c value Content to process through templating. May be a multi level dictionary, or a single string
    @retval Any Parsed Content

    Template Format: `{{ <my configuration value> }}`

    Example:
     - `{{ global.convection.git.path }}` will return the configuration value from that entry
    """
    parser_regex:re.Pattern = re.compile(r'(\{\{\ ?((\w+\.?){1,})\ ?\}\})')
    result:typing.Any
    if isinstance(value,dict):
        result = value.copy()
        for k,v in result.items():
            result[k] = value_parser(v)
        return result
    if isinstance(value,list):
        result = value.copy()
        for i in range(0,len(result)):
            result[i] = value_parser(result[i])
        return result
    if isinstance(value,str):
        search:list[tuple[str,...]] = parser_regex.findall(value)
        if len(search) == 0:
            return value
        # new_value:str = value
        # for match in search:
        #     conf_search:str = match[1]
        #     conf_value:typing.Union[str,int,float,bool,None] = _value_finder(conf_search)
        #     if conf_value is not None:
        #         new_value = re.compile(match[0]).sub(str(conf_value),new_value)
        raise NotImplementedError("Function is incomplete")
        # return new_value
    # if type(value) in [ bool, int, float ]:
    #     return value
    raise TypeError("Invalid Value Type",type(value).__qualname__)

def get_config_types(with_auto:bool = False) -> list[str]:
    """Get Configuration File Types
    @param bool \c with_auto Whether or not to include 'auto' option
    @retval list[str] Config File Type choices
    """
    conf_choices:list[str] = ["json","yaml","toml"]
    if with_auto:
        conf_choices.append("auto")
    return conf_choices

def get_actions(obj:object) -> dict[str,typing.Callable]:
    """Get Object Methods for action map
    @param object \c obj Object to Generate for
    @retval dict[str,Callable[],None]]
    """
    action_map:dict[str,typing.Callable] = {}
    members:list[typing.Any] = inspect.getmembers(obj,predicate=inspect.ismethod)
    for m in members:
        member_name:str = m[0]
        if re.search(r'^_.*$',member_name):
            continue
        member_action:typing.Callable = m[1]
        action_map[member_name] = member_action
    return action_map

def load_types(plugin_module:str,check_type:typing.Type) -> dict[str,typing.Type]:
    """Load Types which are of check_type from known module location
    @param str \c plugin_module Plugin module path (ex: `convection.secrets.uacl`)
    @param Type \c check_type Type to verify that discovered class is a subclass of before adding to list
    @retval dict[str,Type] mapping of Type.__qualname__:Type
    """
    result:dict[str,typing.Type] = {}
    plugin_obj:types.ModuleType = importlib.import_module(plugin_module)
    classes:list[str] = dir(plugin_obj)
    for c in classes:
        obj:typing.Type = getattr(plugin_obj,c)
        if not isinstance(obj,type) or not issubclass(obj,check_type):
            continue
        if c not in result.keys():
            result[c] = obj
    return result

def load_plugins(plugin_location:str,check_type:typing.Type) -> dict[str,typing.Type]:
    """Class / Module scanner (Plugin Scanner)
    @param str \c plugin_location Plugin root (ex:  `convection.plugins.secrets` or `convection.plugins.connectors`)
    @param Type \c check_type Type to verify that discovered class is a subclass of before adding to list
    @retval dict[str,Type] mapping of name:Type where name is the file name, (ex 'convection.plugins.secrets.generic` is `generic`)
    """
    result:dict[str,typing.Type] = {}
    try:
        plugins_root:types.ModuleType = importlib.import_module(plugin_location)
        logging.debug(f"PLUGINS ROOT: {plugins_root}")
    except ModuleNotFoundError:
        logging.warning("THERE ARE NO PLUGINS LOADED")
        return {}
    for p_str in plugins_root.__path__:
        p:Path = Path(p_str).resolve()
        if p.joinpath("specs").is_dir():
            StaticSpecker.instance.specker_instance.load_specs(p.joinpath("specs"))
        else:
            print(f"No Specs for {p_str}")
        for search_file in p.glob("*.py"):
            f:Path = Path(search_file).resolve()
            if f.name == "__init__.py" or re.search(r'^[-._].*$',f.name):
                continue
            plugin_path:str = f"{plugins_root.__package__}.{f.stem}"
            logging.debug(f"IMPORT PLUGIN PATH: {plugin_path}")
            plugin_obj:types.ModuleType = importlib.import_module(plugin_path)
            classes:list[str] = dir(plugin_obj)
            logging.debug(f"CLASSES IN PLUGIN PATH: {classes}")
            for c in classes:
                obj:typing.Type = getattr(plugin_obj,c)
                if (not isinstance(obj,type) or not issubclass(obj,check_type)) or obj == check_type:
                    continue
                if f.stem not in result.keys():
                    result[f.stem] = obj
    return result

def access_str_to_access_mode(access_mode_str:str) -> int:
    """Convert Access Mode String (short) to Access Mode Integer
    @param str \c access_mode_str Access Mode String (a string containing one or more of 'r', 'w', 'm', 'd')
    @retval int ACLObject.ACCESS_* mode
    """
    ACCESS_INVALID:int = 224
    ACCESS_NONE:int = 0
    ACCESS_READ:int = 2
    ACCESS_WRITE:int = 4
    ACCESS_MODIFY:int = 8
    ACCESS_DELETE:int = 16
    if not re.match(r'[rwmd]{1,4}',access_mode_str):
        raise ValueError(f"Unknown Access mode '{access_mode_str}', must only contain 'r', 'w', 'm', 'd', indivudally, or combined")
    result:int = ACCESS_NONE
    if "r" in access_mode_str:
        result |= ACCESS_READ
    if "w" in access_mode_str:
        result |= ACCESS_WRITE
    if "m" in access_mode_str:
        result |= ACCESS_MODIFY
    if "d" in access_mode_str:
        result |= ACCESS_DELETE
    if "I" in access_mode_str:
        result |= ACCESS_INVALID
    return result

def access_mode_to_access_str(access_mode:int,long:bool = False) -> str:
    """Convert Access Mode Integer to String
    @param int \c access_mode Access Mode to convert
    @param bool \c long Whether to print whole words or just the shorthand first letter output
    @retval str Access Mode info
    """
    ACCESS_INVALID:int = 224
    # ACCESS_NONE:int = 0
    ACCESS_READ:int = 2
    ACCESS_WRITE:int = 4
    ACCESS_MODIFY:int = 8
    ACCESS_DELETE:int = 16
    modes:list[int] = [ ACCESS_INVALID, ACCESS_READ, ACCESS_WRITE, ACCESS_MODIFY, ACCESS_DELETE ]
    mode_strs:list[str] = [ "Invalid", "Read", "Write", "Modify", "Delete" ]
    mode_str:list[str] = [ "I", "r", "w", "m", "d" ]
    output_long:list[str] = []
    output:str = ""
    for m_idx in range(0,len(modes)):
        mode:int = modes[m_idx]
        if (access_mode & mode) == mode:
            if long:
                output_long.append(mode_strs[m_idx])
            else:
                output += mode_str[m_idx]
    if long:
        output = ', '.join(output_long)
    if len(output) == 0 and long:
        return "None"
    return output

def print_console_initialization_data(data:dict[str,typing.Any]) -> None:
    """Print Data, Warnings after `initialize` Command to Console
    @param dict[str,Any] \c data Initialization result Data
    @retval None Nothing
    """
    output_rows:list[list[str]] = [["Unlock Keys"]]
    KEYDB_NOTICE:list[list[str]] = [
        ["WARNING: A new RootKey has been generated!!!"],
        ["LOSS OF THESE KEYS WILL RESULT IN DATA LOSS"],
        [""],
        ["ONE OF THESE KEYS WILL NEED TO BE PASSED TO THE SECRETS MANAGER DURING UNLOCK COMMANDS"],
        ["IT IS RECOMMENDED TO CHOOSE ONE FOR CONSTANT USE, AND STORE THE OTHERS SECURELY AWAY"],
        [""],
        ["AN UNLOCK COMMAND MUST NOW BE SENT TO CONTINUE USE"]
    ]
    for k in data["keys"]:
        output_rows.append([k])
    notice:list[list[str]] = KEYDB_NOTICE
    print(tabulate(notice,tablefmt="outline"))
    print(tabulate(output_rows,headers="firstrow",tablefmt="outline"))
    print("\n")
    access_key_id:str = data["root_access_key_id"]
    rootuser_data:list[list[str]] = [
        ["A new Root User has been generated."],
        [f"Access Key ID: {access_key_id}"],
        [""],
        ["Use this Access Key and the RSA Keypair you used via --pubkey to create your own user, then secure it away safely"]
    ]
    print(tabulate(rootuser_data,tablefmt="outline"))
