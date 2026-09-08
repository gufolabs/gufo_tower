# Tower Capabilities

Tower Capabilities provide a playbook with information about the capabilities supported by the Tower instance running the deployment.

Capabilities allow a playbook to determine whether the current Tower instance provides all the functionality required to perform the deployment.

## Capabilities

Capabilities are currently represented as a list of capability identifiers:

* `ansible_l1` — provides Ansible 2.9.
* `inventory_v1` — provides inventory schema version 1.

The list may be extended as new Tower capabilities are introduced.

## Inventory

Tower passes the capabilities to the deployment inventory through the `all.vars.caps` variable:

```yaml
all:
  vars:
    caps:
      - ansible_l1
      - inventory_v1
```

## Default Capabilities

If `all.vars.caps` is not defined, the playbook must assume that the Tower instance provides the following capabilities:

* `ansible_l1`
* `inventory_v1`

The playbook should check the required capabilities at the beginning of the deployment and fail if any required capability is not available.
