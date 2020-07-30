# Slack to Matrix Migration
Migrates Users, Channels and all the conversations from a Slack export to Matrix

Warning: It's not recommended to use anything but a fresh/empty Synapse instance for migration

However, you can configure it to import the Slack workspace to an empty federated server
and use that to effectively migrate rooms to an existing Matrix server via federation.
See 'Federated setup (import to an existing Matrix server)' below.

## Prerequisites
1. Install Python 3.7 with pip
2. Set up a Synapse Homeserver
3. Create an admin user on the Homeserver (make sure the username of the admin user does not match any existing slack user id)
4. Copy `migration_service.yaml` to somewhere reachable by your Homeserver
5. Replace the `as_token` and `hs_token` in the `migration_service.yaml` with a random string
6. Add the Application Service to your `homeserver.yaml`:
```
app_service_config_files:
  - /<path to the yaml file>/migration_service.yaml
```
7. Restart Synapse

Notes:

- Make sure the migration script can access the `/_matrix/client` api and the `/_synapse` admin api
- Other Homeserver implementations may not support timestamped massaging, see https://matrix.org/docs/spec/application_service/r0.1.0#timestamp-massaging
- You may have to increase your homserver rate limits

## Federated setup (import to an existing Matrix server)

The idea is to migrate Slack to a fresh/empty Synapse instance, that is federated with your existing Matrix homeserver.
All imported Slack users will be kicked after the migration is done, leaving only the admin user in the migrated rooms.
Invite any users from your existing Matrix homeserver to the rooms manually using the admin user.

You will need the following configuration:

```yaml
# Set to 'True' to invite all users to all rooms
invite-all: True
# Set to 'True' to invite the admin user to all rooms
create-as-admin: True
# Set to 'True' to kick all imported users from imported rooms
kick-imported-users: True
# Set to 'True' to allow rooms to be joined from other homeservers
federate-rooms: True
# Append room and displayname suffixes
room-suffix: " (slack import)"
name-suffix: " (slack import)"
```

## Running the migration
1. Run `pip3 install -r required.txt`
2. Get a zipped Export of your Slack Workspace (https://slack.com/help/articles/201658943)
3. Copy `config_example.yaml` to `config.yaml` and edit to your needs (use the `as_token` from your `migration_service.yaml`)
4. Run `python3 migrate.py`

## Cleanup
1. Remove the Application Service from your `homeserver.yaml`
2. Delete the `migration_service.yaml`
3. Reset any increased rate limits
4. Restart Synapse
