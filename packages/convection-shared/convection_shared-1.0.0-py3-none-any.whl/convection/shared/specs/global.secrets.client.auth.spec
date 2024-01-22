{
    "access_key_id": {
        "type": "str",
        "required": true,
        "comment": "Convection Secrets Manager User Access Key ID"
    },
    "private_key": {
        "type": "file:exist",
        "required": true,
        "default": "./config/secrets_auth.key",
        "comment": "Convection Secrets Manager User Private Key (Path)"
    },
    "key_password": {
        "type": "str",
        "required": false,
        "default": "",
        "comment": "Private Key Password (If Used)"
    }
}