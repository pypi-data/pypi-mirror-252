#!/usr/bin/env python3
# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import argparse
import importlib
import logging
from pathlib import Path
import typing

from tabulate import tabulate

import argstruct

from specker.loader import SpecLoader

from convection.shared.specker_static import StaticSpecker
from convection.shared.functions import access_mode_to_access_str, access_str_to_access_mode

# pylint: disable=duplicate-code
if __name__ == "__main__":
    StaticSpecker()
    specker:SpecLoader = StaticSpecker.instance.specker_instance
    StaticSpecker.instance.specker_instance.load_specs(Path(__file__).resolve().parent.parent.joinpath("convection.secrets").joinpath("specs"))

    parser:argparse.ArgumentParser = argparse.ArgumentParser(description="Convection CLI/Conosle and API Documentation Generator")
    parser.add_argument("-v","--verbose",help="Turn on Debugging",action="store_true")
    parser.add_argument("--specker_debug",help="Turn on Debugging for Specker Specs",action="store_true")
    parser.add_argument("-p","--path",help="Path to Command Map",required=True)

    args:argparse.Namespace = parser.parse_args()
    input_args:dict[typing.Any,typing.Any] = vars(args)
    loglevel:int = logging.INFO
    if input_args["verbose"]:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel)
    input_args["loglevel"] = loglevel
    command_map:Path = Path(input_args["path"]).resolve()
    if not command_map.is_file():
        command_map_str:str = command_map.as_posix()
        print(f"Error: {command_map_str} does not exist")
    shared_path:Path = Path(importlib.import_module("convection.shared").__path__[0]).resolve()
    spec_path:Path = shared_path.joinpath("specs/")
    argstruct_obj:argstruct.ArgStruct = argstruct.ArgStruct(command_map,"toml",[spec_path])

    output:str = ""
    for group, commands in argstruct_obj.grouped.items():
        if len(commands) == 0:
            continue
        output += f"## {group}\n"
        for cmd, cmd_config in commands.items():
            can_cli:bool = not cmd_config.get("cli_hidden")
            can_api:bool = not cmd_config.get("api_hidden")
            if not can_api and not can_cli:
                continue
            output += f"### Command: `{cmd}`\n"
            output += cmd_config.get("help") + "\n\n"
            auth_flag:str = "**Y**" if cmd_config.get("auth_required") else "**N**"
            output += f"Authorization Required? {auth_flag}\n\n"
            access_method_rows:list[list[str]] = [
                [ "Access Method", "Available?" ],
                [ "CLI", "**Y**" if can_cli else "**N**" ],
                [ "API", "**Y**" if can_api else "**N**" ],
            ]
            output += tabulate(access_method_rows,headers="firstrow",tablefmt="github")
            output += "\n"
            access_mode:str = ""
            try:
                access_mode = cmd_config.get("access_mode")
            except BaseException:
                access_mode = ""
            if len(access_mode) > 0:
                access_mode_int:int = access_str_to_access_mode(access_mode)
                access_mode_str:str = access_mode_to_access_str(access_mode_int,True)
                output += f"\nUtilizes Access Modes: **{access_mode_str} ({access_mode}, integer: {str(access_mode_int)})**\n"
            arg_table:list[list[str]] = [
                [ "API Name", "CLI Flag(s)", "Description", "Required", "Type", "Default" ]
            ]
            cmd_args:dict[str,typing.Any] = cmd_config.get("args")
            for arg, arg_data in cmd_args.items():
                arg_row:list[str] = []
                arg_row.append(arg)
                if "cli_flag_names" in arg_data.keys():
                    arg_row.append(', '.join(arg_data["cli_flag_names"]))
                else:
                    arg_row.append("**NONE**")
                arg_row.append(arg_data["help"])
                arg_row.append("**Y**" if arg_data["required"] else "**N**")
                arg_row.append(arg_data["type"])
                if "default" in arg_data.keys():
                    arg_row.append(str(arg_data["default"]))
                else:
                    arg_row.append("**NONE**")
                arg_table.append(arg_row)
            if len(cmd_args) > 0:
                output += "\n"
                output += "#### Arguments\n"
                output += tabulate(arg_table,headers="firstrow",tablefmt="github")
                output += "\n\n"
            else:
                output += "\n"
    print(output)
# pylint: enable=duplicate-code
