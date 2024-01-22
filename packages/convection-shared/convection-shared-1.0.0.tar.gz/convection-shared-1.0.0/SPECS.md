# Configuration Options

- [Configuration Options](#configuration-options)
  - [Spec for root](#spec-for-root)
  - [Spec for global](#spec-for-global)
  - [Spec for global.reporting](#spec-for-globalreporting)
  - [Spec for global.reporting.log](#spec-for-globalreportinglog)
  - [Spec for global.secrets](#spec-for-globalsecrets)
  - [Spec for global.secrets.client](#spec-for-globalsecretsclient)
  - [Spec for global.secrets.client.network](#spec-for-globalsecretsclientnetwork)
  - [Spec for global.secrets.client.auth](#spec-for-globalsecretsclientauth)
  - [Spec for plugin](#spec-for-plugin)
  - [Spec for metadata](#spec-for-metadata)
  - [Spec for metadata.plugin](#spec-for-metadataplugin)
  - [Spec for plugin.access](#spec-for-pluginaccess)
  - [Spec for plugin.action](#spec-for-pluginaction)
  - [Spec for plugin.connector](#spec-for-pluginconnector)
  - [Spec for commandmap.root](#spec-for-commandmaproot)
  - [Spec for commandmap.command.args-root](#spec-for-commandmapcommandargs-root)
  - [Spec for commandmap.commands](#spec-for-commandmapcommands)
  - [Spec for commandmap.command](#spec-for-commandmapcommand)
  - [Spec for commandmap.command.args](#spec-for-commandmapcommandargs)
  - [Spec for target](#spec-for-target)
  - [Spec for group](#spec-for-group)
  - [Spec for anyitem](#spec-for-anyitem)

Auto generated from .spec files
## Spec for root

Option: `global` - Global Options
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `global`

## Spec for global

Option: `reporting` - Reporting and Logging configuration
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `global.reporting`

Option: `secrets` - Secrets Configuration
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `global.secrets`

## Spec for global.reporting

Option: `log` - Logging Configuration
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `global.reporting.log`

## Spec for global.reporting.log

Option: `level` - Log Verbosity Level
 - Type: str
 - Required: True
 - Default: ERROR
 - Acceptable Values: DEBUG, INFO, WARNING, ERROR, CRITICAL

Option: `file` - Log File Path
 - Type: file
 - Required: False
 - Default: ./convection.log

## Spec for global.secrets

Option: `client` - Secrets Client Configuration
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `global.secrets.client`

## Spec for global.secrets.client

Option: `use_network` - Toggle Convection Secrets Manager connection over socket or network
 - Type: bool
 - Required: True
 - Default: False

Option: `tls_ca` - TLS CA Cert for Connection
 - Type: file:exist
 - Required: True
 - Default: ./config/ca.pem

Option: `socket_path` - Socket filename for IPC communication
 - Type: file
 - Required: True
 - Default: /var/run/convection.secrets.sock

Option: `network` - Convection Secrets Manager Network Configuration
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `global.secrets.client.network`

Option: `auth` - Convection Secrets Manager Client Auth Data
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `global.secrets.client.auth`

Option: `log_file` - Log File Path
 - Type: file
 - Required: True
 - Default: ./convection-secrets.client.log

## Spec for global.secrets.client.network

Option: `target_ip` - IP or Hostname Secrets Manager is listening on
 - Type: str
 - Required: True
 - Default: 127.0.0.1

Option: `target_port` - Port number to connect to Secrets Manager
 - Type: int
 - Required: True
 - Default: 9670

## Spec for global.secrets.client.auth

Option: `access_key_id` - Convection Secrets Manager User Access Key ID
 - Type: str
 - Required: True

Option: `private_key` - Convection Secrets Manager User Private Key (Path)
 - Type: file:exist
 - Required: True
 - Default: ./config/secrets_auth.key

Option: `key_password` - Private Key Password (If Used)
 - Type: str
 - Required: False
 - Default: 

## Spec for plugin

Option: `metadata` - Plugin Metadata
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `metadata`

## Spec for metadata

Option: `version` - Object Version
 - Type: str
 - Required: True
 - Example: ['1.0.0']

Option: `author` - Object Author
 - Type: str
 - Required: True
 - Example: ['AccidentallyTheCable <cableninja@cableninja.net>']

Option: `updated` - Date Object Updated
 - Type: int
 - Required: True
 - Example: [20230808]

Option: `compatibility` - Version Compatibility Search String
 - Type: str
 - Required: True
 - Example: <=:1.0,>:2.0

Option: `plugin` - Plugin Object Metadata
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `metadata.plugin`

## Spec for metadata.plugin

Option: `type` - Plugin Type
 - Type: str
 - Required: False
 - Acceptable Values: Connector, Access, Secret, Action

Option: `name` - Plugin Name
 - Type: str
 - Required: False

Option: `description` - Plugin Description
 - Type: str
 - Required: False

## Spec for plugin.access

Option: `metadata` - Plugin Metadata
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `metadata`

Option: `data` - Access Data Definitions
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

Option: `env` - ENV Variables
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

Option: `options` - Access Configuration Options (Access Method Dependent)
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

Option: `__any_item__` - Allow Any item for plugins
 - Type: any
 - Required: False

## Spec for plugin.action

Option: `metadata` - Plugin Metadata
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `metadata`

Option: `data` - Action Data Definitions
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

Option: `env` - ENV Variables
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

## Spec for plugin.connector

Option: `metadata` - Plugin Metadata
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `metadata`

Option: `data` - Connector Data Definitions
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

Option: `env` - ENV Variables
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

## Spec for commandmap.root

Option: `commands` - Command Map Information
 - Type: dict
 - Required: True
 - Default: {}
 - Example: {'auth_required': True, 'args': {'myarg': {'type': 'str', 'cli_flag_names': ['-M', '--my-arg'], 'required': True, 'help': 'My Argument'}, 'otherarg': {'type': 'str', 'cli_flag_names': ['-z', '--other-arg'], 'required': True, 'help': 'My Other Argument'}}}
 - Additionally Validates With: `commandmap.commands`

## Spec for commandmap.command.args-root

Option: `__any_item__` - Data Definition
 - Type: any
 - Required: False
 - Additionally Validates With: `commandmap.command.args`

## Spec for commandmap.commands

Option: `__any_item__` - Command Data
 - Type: dict
 - Required: False
 - Additionally Validates With: `commandmap.command`

## Spec for commandmap.command

Option: `auth_required` - Whether or not Command requires to be authorized
 - Type: bool
 - Required: True
 - Default: True

Option: `help` - Command Help
 - Type: str
 - Required: True

Option: `cli_hidden` - Hide from CLI
 - Type: bool
 - Required: False
 - Default: False

Option: `api_hidden` - Hide from API
 - Type: bool
 - Required: False
 - Default: True

Option: `access_mode` - Convection Secrets Manager, Access Mode, short string
 - Type: str
 - Required: True
 - Default: 
 - Acceptable Format: ^[rwmd]{1,4}?$
 - Example: rw

Option: `args` - Command Argument configurations
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `commandmap.command.args-root`

## Spec for commandmap.command.args

Option: `type` - Argument value type
 - Type: str
 - Required: True
 - Acceptable Values: any, str, int, list, dict, float, bool

Option: `required` - Whether or not Argument is required
 - Type: bool
 - Required: True
 - Default: False

Option: `default` - Default Argument Value
 - Type: any
 - Required: False

Option: `help` - Argument Help Text
 - Type: str
 - Required: True

Option: `cli_flag_names` - Commandline Flag Name(s)
 - Type: list
 - Required: True
 - Example: ['--my-arg', '-M']

Option: `multi` - Whether or not to set `nargs='+'`
 - Type: bool
 - Required: False
 - Default: False

## Spec for target

Option: `data` - Target Data Definitions
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

Option: `env` - ENV Variables
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

Option: `options` - Target Configuration Options (Dependent on connector type)
 - Type: dict
 - Required: True
 - Default: {}
 - Additionally Validates With: `anyitem`

## Spec for group

Option: `data` - Group Data Definitions
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

Option: `env` - ENV Variables
 - Type: dict
 - Required: False
 - Default: {}
 - Additionally Validates With: `anyitem`

## Spec for anyitem

Option: `__any_item__` - Data Definition
 - Type: any
 - Required: False
