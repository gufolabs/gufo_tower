# Pull

A Git-based installation, that is, an Environment with the **Git** installation type, requires downloading the corresponding state of the Git repository. This operation is called **Pull**.

The **Pull** operation must be performed before deploying an Environment. Once the repository state has been pulled, the same state can be deployed multiple times.

Depending on the repository state, a Pull operation may download changes to the Environment's playbooks or configuration. Therefore, **Pull must be performed before updating the NOC version or deploying changes from the repository**.

The Pull operation depends on the Environment's installation type and is currently required only for **Git** installations. Other installation types may not require a Pull operation.

The Pull operation is performed for the currently selected Environment.

To pull the repository state, select the required Environment in the Environment List and click the **Pull** button in the toolbar.

![Pull](environment-list-toolbar-pull.png)