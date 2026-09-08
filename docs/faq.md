---
hide:
    - navigation
---
# FAQ

## Getting Started with Tower

### Why Do I Need Tower?

Tower simplifies the deployment and management of complex, multi-node NOC installations.

### Why Tower if Thor exists?

Thor is focused on Docker-based NOC deployments, while Tower is focused on deploying and managing NOC on bare-metal servers and virtual machines.

### How to install Tower?

Install Tower using:

```shell
curl https://sh.gufolabs.com/tower | sh -s -- venv
```

Complete setup instructions are available in the [Installation Guide](installation.md).

### How to upgrade Tower?

Tower can be upgraded using the standard Python package management tools. See the [Installation Guide](installation.md) for details.

### How quickly can I deploy NOC with Tower?

Deployment time depends on the node configuration, network, and NOC installation. For an initial deployment, plan for approximately one hour.

### Is Tower production-ready?

Yes. Tower is designed and supported for production use.

## Requirements and Platforms

### Which operating systems can Tower install NOC on?

This depends on the NOC version being installed. See the documentation for the selected NOC version for its supported operating systems.

### What are the requirements for Tower?

Tower has minimal resource requirements. It requires Python on the host and only a small amount of disk space and memory for Tower itself. NOC resource requirements depend on the deployed NOC configuration.

### Does Tower work on Linux?

Yes. Linux is supported.

### Does Tower work on FreeBSD?

Yes. FreeBSD is supported.

### Does Tower work on macOS?

Yes. macOS is supported.

### Does Tower work on Windows?

Windows is not supported.

## Architecture and Design

### What is Tower?

Tower is a web interface and configuration database for managing NOC deployments. It uses Ansible to execute deployment playbooks on NOC nodes.

In other words, Tower provides a convenient configuration interface for NOC's Ansible-based deployment system.

### Is Tower a NOC distribution?

No. Tower is a tool for managing NOC installations. Tower can, however, download and install NOC distributions on managed nodes.

### Does Tower require Docker?

No. Docker is not required. Tower can run natively in a Python virtual environment.

A Docker-based version of Tower is also available when containerized deployment is preferred.

### What Is an Environment?

An Environment represents a separate NOC installation, such as a production, development, or test environment. Tower can manage multiple independent Environments.

### What Is a Node?

A Node is a server managed by Tower on which one or more NOC services are deployed.

### How many NOC nodes can Tower manage?

Tower is designed to manage NOC infrastructure of any size, from a single node to clusters of hundreds of nodes.

### How does Tower deploy NOC nodes?

A managed NOC node only needs SSH access and a user account that Tower can use.

Tower handles the rest of the deployment process automatically.

### Can Tower manage multiple NOC installations?

Yes. Tower can manage multiple independent NOC installations.

Each **Environment** represents a separate NOC installation and can contain its own configuration and nodes.

## Configuration and Operations

### Where does Tower store its configuration?

Tower stores its data in the `data` directory of the Tower installation environment.

### What format does Tower use to store its configuration?

Tower uses SQLite as its configuration database.

### Can I upgrade NOC without losing data?

Yes. Tower can be used both to install and to upgrade NOC installations while preserving their existing data.

### Can I use Tower to manage different NOC configurations?

Yes. Each Tower Environment represents a separate NOC installation and can have its own configuration.

### What Are the Requirements for a Node?

A managed Node must:

- Be accessible from Tower via SSH.
- Have a user that Tower can use for remote operations.
- Allow the required privileged operations, typically through `sudo`.
- Have Python installed for Ansible operations.
- Run a Linux or FreeBSD operating system supported by the NOC version being deployed.

### Can Tower configure virtual machines automatically?

Yes. Tower can provide node-specific configuration through cloud-init. A virtual machine can retrieve its configuration from Tower during the first boot and configure itself automatically.

### What Do the Deployment Options Mean?

Deployment options let you control what Tower does during a deployment and how much diagnostic information it produces. In most cases, the default options are sufficient; the additional options are useful for troubleshooting, maintenance, or more controlled deployments.

- **Install Everything** — install or update all NOC components.
- **Run pre-deploy checks** — verify that the environment is ready for deployment before making changes.
- **Run post-deploy tests** — verify that the deployment completed successfully.
- **Restart quick** — stop all NOC services and start them again. This provides the fastest restart but causes a complete service interruption.
- **Restart gentle** — restart NOC services one by one to reduce the impact of the restart.
- **Be verbose** — enable Ansible verbose output (`-v`) for troubleshooting.
- **Be extremely verbose** — enable maximum Ansible debug output (`-vvvv`) for detailed troubleshooting.
- **Show secrets in deploy log** — include normally hidden secret values in the deployment log. Use this only when necessary for troubleshooting.

### Can Tower and NOC run on the same server?

Yes. Running Tower and NOC on the same server is perfectly fine for single-node NOC installations.

For larger or multi-node installations, it is recommended to run Tower on a separate server to isolate the management system from the NOC infrastructure.

### Can I use my own Ansible playbooks with Tower?

Yes. Tower supports extending NOC deployments with **Extra Roles**. Extra Roles are added by providing a Git repository URL containing your Ansible roles, allowing you to extend the deployment without modifying the standard NOC deployment playbooks.

### What does the "SSE 4.2" error mean?

If you see an error indicating that **SSE 4.2** is not supported, ClickHouse is being installed on an **amd64 Node** whose CPU does not expose the required instruction set.

This issue only applies to **amd64** systems. If the Node is a virtual machine, enable **SSE 4.2** in the VM's CPU settings in your virtualization platform and restart the virtual machine. Then run the deployment again.

### Can I Run Deployments from the Command Line?

Yes. After the initial configuration, deployments can be performed directly from the command line instead of using the web interface.

Tower uses Ansible playbooks for deployments, so you can run the same playbooks manually and use Ansible options such as tags to perform specific operations.

For example, you can run the complete deployment:

```shell
cd <tower data>/cache/<environment id>/playbooks

export ANSIBLE_SSH_PIPELINING=1 ANSIBLE_HOST_KEY_CHECKING=1 PYTHONUNBUFFERED=1 NOC_ENV=<environment name>

ansible-playbook -i /opt/tower/bin/tower-inv site.yml -f 50
```

You can also run specific operations using tags. For example, to update NOC sources:

```shell
ansible-playbook -i /opt/tower/bin/tower-inv site.yml -f 6 --tags get_source
```

Or to update the configuration and perform a gentle restart:

```shell
ansible-playbook -i /opt/tower/bin/tower-inv site.yml -f 6 --tags config,sort_restart
```

This provides direct access to the underlying Ansible deployment system and can be useful for automation, troubleshooting, or performing specific deployment operations.

## Support and License

### What is the license of Tower?

Tower's license is synchronized with the NOC license.

As a deliberate design decision, wherever the use of NOC is permitted, the use of Tower is permitted as well.

### Where can I get support?

Please use GitHub Issues for bugs or Discussions for feature requests.

### Can I help the NOC project financially?

Yes, you can support our work via [GitHub Sponsors](https://github.com/sponsors/gufolabs) or [Buy Me a Coffee](https://www.buymeacoffee.com/dvolodin).

Your contributions help us continue developing and maintaining NOC and the Gufo ecosystem.

## About Gufo

### What does "Gufo" mean?

*Gufo* means *the Owl* in Italian.

### Why the owls?

We love owls and the viable parts of our technologies were proven at the project named "the Owl".

### What is "Gufo Labs"?

[Gufo Labs](https://gufolabs.com/) is the Italian company specialized in network and IT consulting and software research.

### What is "Gufo Stack"?

We've extracted core components behind [NOC](https://getnoc.com/) and released them as independent packages, available under the terms of the 3-clause BSD license.

Our software shares common code quality standards and is battle-proven under high load. We hope our key components will help engineers and developers build reliable networks and robust network management software.

See [more details](https://gufolabs.com/products/gufo-stack/).
