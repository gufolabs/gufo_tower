# Working with the Node List

The **Node List** displays all Nodes currently configured for the selected [Environment](../environment/index.md).

![Node List](node-list.png)

The list contains the following columns:

| Column | Description |
| --- | --- |
| **Node** | Node name. The name must be unique within the Datacenter. |
| **Enabled** | Indicates whether the Node is enabled. Deployment is not performed on disabled Nodes. |
| **Type** | Node type. See [Node Types](node-types.md) for details. |
| **Datacenter** | Datacenter where the Node is located. See [Datacenters](../datacenter/index.md) for details. |
| **Address** | Management address of the Node. This address is used by Gufo Tower to access the Node for deployment and for communication between Nodes. |
| **Description** | Human-readable description of the Node. |

To view and configure a Node, double-click the corresponding row in the list to open the [Node Form](form.md).

## Toolbar

A toolbar above the list provides actions for managing Nodes.

![Node Toolbar](node-list-toolbar.png)

The toolbar contains the following buttons:

| Button | Description |
| --- | --- |
| **Create New** | Creates a new Node. |
| **Help** | Shows this help page. |