# Deploy

**Deploy** is the process of applying changes to the NOC nodes. It can be used during installation, configuration, and NOC version updates.

To start a deployment, select the required Environment and click the **Deploy** button in the Environment List toolbar.

![Deploy](environment-list-toolbar-deploy.png)

The Deploy panel opens and displays the deployment progress and results.

## Deploy Toolbar

The toolbar provides controls for managing and monitoring the deployment.

![Deploy Toolbar](deploy-toolbar.png)

The toolbar contains the following elements:

| Element | Description |
| --- | --- |
| **Back** | Back to the environment list. |
| **Deploy Recap** | Displays a summary of deployment tasks by their result. |
| **Deploy Status** | Displays the current deployment status. |
| **Elapsed Time** | Displays the time elapsed since the deployment started. |

## Deploy Recap

**Deploy Recap** provides a summary of the deployment results. Each result is displayed as a number with a colored indicator.

| Result | Description |
| --- | --- |
| 🟢 **12** | Task completed successfully without changes. |
| 🟡 **5** | Task completed successfully with changes. |
| ⚪ **3** | Task was skipped. |
| 🔴 **1** | Task failed. |