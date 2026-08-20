# Application URL Structure

Gufo Tower uses an internal URL structure for navigation between application components. These URLs are used exclusively for navigation within the application and are not related to requests sent to the server or to the server-side API.

Each application component registers the URLs it handles using the `router.push()` method and the `Route` class. The registered routes define the internal navigation structure of the application.

For example, an application component can register a URL as follows:

```javascript
router.push(
    new Route(/^\/environment\/(\d+)\/node$/, node_list_logic.on_route)
);
```

The `Route` defines the URL pattern and the handler responsible for displaying the corresponding application component. The `router.push()` call registers the route with the application router.

Navigation to a registered application component is performed using `navigation.navigate()`:

```javascript
navigation.navigate(`/environment/${env_id}/node`);
```

The application URL structure is as follows:

| URL                             | Description                                     |
| ------------------------------- | ----------------------------------------------- |
| `/`                             | Home dashboard                                  |
| `/change-password`              | Change password form                            |
| `/datacenter`                   | Datacenter list                                 |
| `/datacenter/(\d+)`             | Datacenter form for the specified item          |
| `/datacenter/new`               | Create new datacenter form                      |
| `/environment`                  | Environment list                                |
| `/environment/(\d+)`            | Environment form for the specified item         |
| `/environment/(\d+)/deploy`     | Deploy the specified environment                |
| `/environment/(\d+)/inventory`  | Ansible inventory for the specified environment |
| `/environment/(\d+)/node`       | Node list for the specified environment         |
| `/environment/(\d+)/node/(\d+)` | Node form for the specified item                |
| `/environment/(\d+)/node/new`   | Create new node form                            |
| `/environment/(\d+)/pool`       | Pool list for the specified environment         |
| `/environment/(\d+)/pool/(\d+)` | Pool form for the specified item                |
| `/environment/(\d+)/pool/new`   | Create new pool form                            |
| `/environment/(\d+)/role`       | Role list for the specified environment         |
| `/environment/(\d+)/role/(\d+)` | Role form for the specified item                |
| `/environment/(\d+)/role/new`   | Create new role form                            |
| `/environment/(\d+)/service`    | Service list for the specified environment      |
| `/environment/new`              | Create new environment form                     |
| `/login`                        | Login form                                      |
| `/settings`                     | Settings form                                   |
