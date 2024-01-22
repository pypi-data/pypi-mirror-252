# Convection IaC

Convection IaC - The Provisioner Infrastructure as Code Project

 - [IaC](src/convection_core/README.md)
 - [Secrets Management](src/convection.secrets/README.md)
 - [Server Core](src/convection_server/README.md)
 - [Plugins](src/convection.plugins/README.md)

## About

The Convection Project, at is core, is a take on Infrastructure as Code that isnt actually Infrastructure as Config. Of course, there is ambiguity between what IaC means, but it originally meant **Infrastrucutre as Code**. Many of todays orchestration and automation tools are in the name of 'Infrastructure as Code' but actually devolve into managing configuration files all day due to the billion layers of abstraction we have placed on everything. And worse, having to do pragmatic things in a configuration file, like yaml, is just abusive to the configuration file format. Convection is a real pragmatic approach to IaC, providing a real programming language (Python) with a set of tools to create infrastructure and orchestration through a unified pragmatic approach.

The Convection Project is be made up of multiple tools. As mentioned, at its core, is the IaC process. To support secure storage, a Secrets Manager also exists within this project. There are also other tools that will be implemented in the future.

### Future

Additional tools will be created to complete this suite, including a System Image Creator and Manager. See [TASKS.md](TASKS.md) for an ongoing roadmap
