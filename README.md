# Slack to Matrix Migration
Migrates Users, Channels and all the conversations from a Slack export to Matrix

Warning: It's not recommended to use anything but a fresh/empty Synapse instance for migration

## Prerequisites
1. Install Python 3.7 with pip
2. Set up a Synapse Homeserver (other Homeserver implementations may not support timestamped massaging, see https://matrix.org/docs/spec/application_service/r0.1.0#timestamp-massaging)
3. Create an admin user on the Homeserver (make sure the username of the admin user does not match any existing slack user id)
4. Copy `migration_service.yaml` to somewhere reachable by your Homeserver
5. Replace the `as_token` and `hs_token` in the `migration_service.yaml` with a random string
6. Add the Application Service to your `homeserver.yaml`:
```
app_service_config_files:
  - /<path to the yaml file>/migration_service.yaml
```
7. Restart Synapse

## Running the migration
1. Run `pip3 install -r required.txt`
2. Get a zipped Export of your Slack Workspace (https://slack.com/help/articles/201658943)
3. Copy `config_example.yaml` to `config.yaml` and edit to your needs (use the `as_token` from your `migration_service.yaml`)
4. Run `python3 migrate.py`

## Cleanup
1. Remove the Application Service from your `homeserver.yaml`
2. Delete the `migration_service.yaml`
3. Restart Synapse
