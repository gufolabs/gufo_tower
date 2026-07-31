def migrate(migrator):
    (migrator.drop_column("environment", "alerta_url"),)
    migrator.drop_column("environment", "alerta_token")
