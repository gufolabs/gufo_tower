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

<style>
.ansible-tag {
    padding: .2em .6em .3em;
    font-size: 75%;
    font-weight: bold;
    line-height: 1;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    border-radius: 1em;
}

.ansible-ok-tag {
    background-color: #2ecc71;
}

.ansible-changed-tag {
    background-color: #f1c40f;
}

.ansible-unreachable-tag {
    background-color: #7f8c8d;
}

.ansible-failed-tag {
    background-color: #c0392b;
}
</style>

| Result | Description |
| --- | --- |
| <div class="ansible-tag ansible-ok-tag">x</div> | Task completed successfully without changes. |
| <div class="ansible-tag ansible-changed-tag">x</div> | Task completed successfully with changes. |
| <div class="ansible-tag ansible-unreachable-tag">x</div>| Task was skipped. |
| <div class="ansible-tag ansible-failed-tag">x</div> | Task failed. |