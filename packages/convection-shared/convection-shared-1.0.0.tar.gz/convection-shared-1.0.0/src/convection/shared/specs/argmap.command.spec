{
    "auth_required": {
        "type": "bool",
        "required": true,
        "default": true,
        "comment": "Whether or not Command requires to be authorized"
    },
    "ui_label": {
        "type": "str",
        "required": true,
        "comment": "WebUI Label"
    },
    "help": {
        "type": "str",
        "required": true,
        "comment": "Command Help"
    },
    "cli_hidden": {
        "required": false,
        "type": "bool",
        "default": false,
        "comment": "Hide from CLI"
    },
    "api_hidden": {
        "required": false,
        "type": "bool",
        "default": true,
        "comment": "Hide from API"
    },
    "access_mode": {
        "required": true,
        "type": "str",
        "default": "",
        "format": "^[rwmd]{0,4}?$",
        "comment": "Convection Secrets Manager, Access Mode, short string",
        "example": "rw"
    },
    "args": {
        "type": "dict",
        "required": false,
        "default": {},
        "comment": "Command Argument configurations",
        "spec_chain": "argmap.command.args-root"
    },
    "group": {
        "type": "str",
        "required": false,
        "default": "",
        "comment": "Command 'group' name for organization"
    }
}