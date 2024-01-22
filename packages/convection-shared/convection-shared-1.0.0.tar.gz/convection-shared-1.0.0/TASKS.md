# Convection TODO / Tasks

<sub>Definitions:</sub><br/>
<sub> - SM: Secrets Management</sub><br/>
<sub> - MA: Modularized Actions</sub><br/>
<sub> - PR: Provisioning</sub>

- [Convection TODO / Tasks](#convection-todo--tasks)
  - [1.0 Task List](#10-task-list)
    - [Core](#core)
    - [Connectivity](#connectivity)
    - [Secrets Management](#secrets-management)
    - [Provisioning](#provisioning)
    - [Modularized Actions](#modularized-actions)
    - [Management](#management)
    - [Implementation](#implementation)
  - [2.0 Task List](#20-task-list)
    - [Core](#core-1)
    - [Connectivity](#connectivity-1)
    - [Secrets Management](#secrets-management-1)
    - [Provisioning](#provisioning-1)
    - [Modularized Actions](#modularized-actions-1)
    - [Management](#management-1)
    - [Implementation](#implementation-1)


## 1.0 Task List

### Core

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| Core | Configuration Structure | 0.0.1 |                              [x] | Structure Semi-Slidified, Most items have placeholders |
| Core | Library Structure | 0.0.1 |                                    [x] | 'Plugin' based, Have subsets of classes for things like Connectors, Actions, etc |
| Core | Enable Convection-Config in Any Markup Language | 0.0.1 |          [x] | Using ATCKit UtilFunctions to allow for TOML, YAML or JSON config files |
| Core | Error Handling | 0.0.1 |                                       [ ] | |
| Core | Reporting / Logging | 0.0.1 |                                  [ ] | |
| Core | Multiprocessing and Threading | 0.0.1 |                        [x] | |
| Core | Git Clone / Checkout on Execute | 1.0.0 |                      [ ] | |
| Core | Git Tag / Branch Specifier | 1.0.0 |                           [ ] | |
| Core | Git Submodule Support | 1.0.0 |                                [ ] | |
| Core | Target Global Level Configuration | 1.0.0 |                    [ ] | |
| Core | Target Group Level Configuration | 1.0.0 |                     [ ] | |
| Core | Target Target Level Configuration | 1.0.0 |                    [ ] | |
| Core | Target Action Level Configuration | 1.0.0 |                    [ ] | |
|  |  |  |  |

### Connectivity

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| Connectivity | AWS | 1.0.0 |                                          [ ] | |
| Connectivity | ProxMox - LXC | 1.0.0 |                                [ ] | |
| Connectivity | Connector Tags generated and applied from runner, etc  [ ] | |
|  |  |  |  |

### Secrets Management

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| SM: Core | Key Rotation | 1.0.0 |                                     [x] | Rotation of Root Key, KeyMapDB, Unlock Keys |
| SM: Core | Encryption at Rest | 1.0.0 |                               [x] | Data always Encrypted. Only Unencrypted for Reading / Modifying |
| SM: Core | Permissions / Access Management | 1.0.0 |                  [x] | ACLs stored in AuthDB, Multiple ACL types, and controls |
| SM: Core | User ACL Granularity (Per secret) | 1.0.0 |                [x] | |
| SM: Core | Automatic Secrets Rotation | 1.0.0 |                       [x] | Multiple Keys Generated for Each Store, Each Write causes a Rotation of the keys in the KeySet |
| SM: Arbitrary | Storage | 1.0.0 |                                     [x] | Generic Secrets Store; Key/Value store |
| SM: Arbitrary | Retrieval | 1.0.0 |                                   [x] | Generic Secrets Store; Key/Value store |
| SM: RSA Keys | Generation | 1.0.0 |                                   [ ] | |
| SM: RSA Keys | Client Public Key Gathering | 1.0.0 |                  [ ] | |
| SM: RSA Keys | Client Private Key Gathering | 1.0.0 |                 [ ] | |
| SM: RSA Keys | Key Distribution to Targets | 1.0.0 |                  [ ] | |
| SM: TLS Certs | Generation | 1.0.0 |                                  [ ] | |
| SM: TLS Certs | Act as Certificate Authority | 1.0.0 |                [ ] | |
| SM: TLS Certs | Multi Level CA (Configurable) | 1.0.0 |               [ ] | |
| SM: TLS Certs | Cert Distribution to Targets | 1.0.0 |                [ ] | |
| SM: TLS Certs | Client Cert Bundle Gathering | 1.0.0 |                [ ] | |
| SM: Password | Generation | 1.0.0 |                                   [x] | Provided by PassDB Secrets Plugin |
| SM: Password | Client Password Gathering | 1.0.0 |                    [x] | PassDB Plugin allows for Generation or Storage of existing passwords |
| SM: Password | Password Distribution to Targets | 1.0.0 |             [ ] | |
|  |  |  |  |

### Provisioning

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| PR: Instance | Create | 1.0.0 |                                       [ ] | |
| PR: Instance | Destroy | 1.0.0 |                                      [ ] | |
|  |  |  |  |

### Modularized Actions

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| MA: Files | Copy Files (Local, Target, Remote) | 1.0.0 |              [ ] | |
| MA: Files | Read Files | 1.0.0 |                                      [ ] | |
| MA: Files | Delete Files | 1.0.0 |                                    [ ] | |
| MA: Files | Execute Files | 1.0.0 |                                   [ ] | |
|  |  |  |  |

### Management

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| Management: Package | OS Package Management | 1.0.0 |                 [ ] | |
| Management: Package | OS Package Repo Management | 1.0.0 |            [ ] | |
| Management: Service | Start/Stop/Restart Services | 1.0.0 |           [ ] | |
| Management: Service | Enable/Disable Services | 1.0.0 |               [ ] | |
| Management: Firewall | Firewall Configuration | 1.0.0 |               [ ] | |
| Management: IAM | Local Users | 1.0.0 |                               [ ] | |
| Management: IAM | SSH Keys From SM | 1.0.0 |                          [ ] | |
| Management: IAM | Passwords from SM | 1.0.0 |                         [ ] | |
| Management: IAM | Database Users | 1.0.0 |                            [ ] | |
|  |  |  |  |

### Implementation

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| Implementation: Database | Configuration | 1.0.0 |                    [ ] | |
| Implementation: Database | Create/Destroy | 1.0.0 |                   [ ] | |
| Implementation: Webserver | Host Configuration | 1.0.0 |              [ ] | |
| Implementation: Webserver | Enable/Disable Host | 1.0.0 |             [ ] | |
|  |  |  |  |

## 2.0 Task List

### Core

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| Core | Managing Connectivity Environments | 2.0.0 |                  [ ] | |
| Core | WebHook Triggerable | 2.0.0 |                                 [ ] | |
| Core | WebHook Sendable | 2.0.0 |                                    [ ] | |
|  |  |  |  |

### Connectivity

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| Connectivity | GCP | 2.0.0 |                                         [ ] | |
| Connectivity | Azure | 2.0.0 |                                       [ ] | |
| Connectivity | ESX | 2.0.0 |                                         [ ] | |
| Connectivity | HyperV | 2.0.0 |                                      [ ] | |
| Connectivity | ProxMox - QEMU | 2.0.0 |                              [ ] | |
|  |  |  |  |

### Secrets Management

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| SM: Core | Garbage Collection | 2.0.0 |                               [ ] | Investigate and ensure secure objects are GC'd properly |
| SM: GPG | Generation | 2.0.0 |                                        [ ] | |
| SM: GPG | Signing | 2.0.0 |                                           [ ] | |
| SM: GPG | Verification | 2.0.0 |                                      [ ] | |
| SM: GPG | Client Public Key Gathering | 2.0.0 |                       [ ] | |
| SM: GPG | Client Private Key Gathering | 2.0.0 |                      [ ] | |
| SM: GPG | GPG Public Key Distribution to Targets | 2.0.0 |            [ ] | |
| SM: GPG | GPG Private Key Distribution to Targets | 2.0.0 |           [ ] | |
| SM: GPG | GPG Key Server | 2.0.0 |                                    [ ] | |
| SM: ENC | On the Fly Encryption/Decryption | 2.0.0 |                  [ ] | |
| SM: SSH | PAM Auth Module for RSA Keys | 2.0.0 |                      [ ] | |
|  |  |  |  |

### Provisioning

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| PR: Instance | Modify Instance Stateful | 2.0.0 |                     [ ] | |
| PR: Instance | Gather Instance State | 2.0.0 |                        [ ] | |
| PR: Imaging | Create Image for Connector | 2.0.0 |                    [ ] | |
| PR: Imaging | Image Management for Connector | 2.0.0 |                [ ] | |
|  |  |  |  |

### Modularized Actions

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| MA: Files | Create/Update Files, with Templating | 2.0.0 |            [ ] | |
| MA: Files | Set File Permissions | 2.0.0 |                            [ ] | |
|  |  |  |  |

### Management

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| Management: Package | Library Management for Python | 2.0.0 |         [ ] | |
| Management: Package | Library Management for Rust? | 3.0.0 |          [ ] | |
| Management: Package | Library Management for Go? | 3.0.0 |            [ ] | |
| Management: Package | Library Management for NodeJS? | 3.0.0 |        [ ] | |
| Management: Service | Add/Remove Services | 2.0.0 |                   [ ] | |
|  |  |  |  |

### Implementation

| Feature | Sub Feature  | Target Version | Complete | Comments |
| --------| -----------  | -------------- | -------- | -------- |
| Implementation: Database | Import/Export Database | 2.0.0 |           [ ] | |
| Implementation: Webserver | Content Deploy to Hosts | 3.0.0 | [ ] | |
