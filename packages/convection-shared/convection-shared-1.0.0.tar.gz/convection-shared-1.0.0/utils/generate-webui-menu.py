#!/usr/bin/env python3
# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import argparse
import json
import logging
from pathlib import Path
import typing
import importlib

import argstruct
from specker.loader import SpecLoader

from convection.shared.specker_static import StaticSpecker

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

    data:list[dict[str,typing.Any]] = []
    for group, commands in argstruct_obj.grouped.items():
        actions:list[dict[str,typing.Any]] = []
        if len(commands) == 0:
            continue
        for cmd, cmd_config in commands.items():
            can_cli:bool = not cmd_config.get("cli_hidden")
            can_api:bool = not cmd_config.get("api_hidden")
            if not can_api:
                continue
            action:dict[str,typing.Any] = {
                "id": cmd,
                "auth_required": cmd_config.get("auth_required"),
                "label": cmd_config.get("ui_label"),
                "tooltip": cmd_config.get("help"),
                "command": f"`this.self.api.{cmd}`",
                "callback": f"`this.self.api.{cmd}_response`"
            }
            actions.append(action)
        if len(actions) == 0:
            continue
        entry:dict[str,typing.Any] = {
            "id": group.lower().replace(' ','_'),
            "expanded": group,
            "collapsed": group[0],
            "state": True,
            "access_key": group[0].lower(),
            "actions": actions
        }
        data.append(entry)
    out:str = json.dumps(data).replace('"`','').replace('`"','').replace('[','[\n\t').replace(']},','\n]},\n')
    print(out)
# pylint: enable=duplicate-code
