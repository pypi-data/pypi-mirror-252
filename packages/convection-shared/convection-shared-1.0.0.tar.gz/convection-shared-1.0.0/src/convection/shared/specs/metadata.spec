{
    "version": {
        "required": true,
        "type": "str",
        "comment": "Object Version",
        "example": [ "1.0.0" ]
    },
    "author": {
        "required": true,
        "type": "str",
        "comment": "Object Author",
        "example": [ "AccidentallyTheCable <cableninja@cableninja.net>" ]
    },
    "updated": {
        "required": true,
        "type": "int",
        "comment": "Date Object Updated",
        "example": [ 20230808 ]
    },
    "compatibility": {
        "required": true,
        "type": "str",
        "comment": "Version Compatibility Search String",
        "example": "<=:1.0,>:2.0"
    },
    "plugin": {
        "required": false,
        "type": "dict",
        "default": {},
        "comment": "Plugin Object Metadata",
        "spec_chain": "metadata.plugin"
    }
}