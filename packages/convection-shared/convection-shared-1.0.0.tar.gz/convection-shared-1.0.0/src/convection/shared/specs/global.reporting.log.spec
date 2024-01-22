{
    "level": {
        "type": "str",
        "required": true,
        "default": "ERROR",
        "values": [ "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" ],
        "comment": "Log Verbosity Level"
    },
    "file": {
        "type": "file",
        "required": false,
        "default": "./convection.log",
        "comment": "Log File Path"
    }
}