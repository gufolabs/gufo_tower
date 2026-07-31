def migrate(migrator):
    migrator.add_index("datacenter", ("name",), unique=True)
    migrator.add_index("environment", ("name",), unique=True)
    migrator.add_index(
        "node",
        (
            "environment_id",
            "datacenter_id",
            "name",
        ),
        unique=True,
    )
    migrator.add_index("user", ("name",), unique=True)
    migrator.add_index(
        "role",
        (
            "environment_id",
            "name",
        ),
        unique=True,
    )
