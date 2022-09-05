import vrchatapi
from vrchatapi.api import authentication_api, users_api, instances_api
from dotenv import dotenv_values
import csv
from datetime import datetime, timezone

envs = dotenv_values(".env")

configuration = vrchatapi.Configuration(
        username=str(envs['USERNAME']),
        password=str(envs['PASSWORD']),
        )

user_data = []

def main():
    with vrchatapi.ApiClient(configuration) as api_client:
        # Instantiate instances of API classes
        auth_api = authentication_api.AuthenticationApi(api_client)
        usr_api = users_api.UsersApi(api_client)
        inst_api = instances_api.InstancesApi(api_client)

        try:
            current_user = auth_api.get_current_user()
            print("Logged in as:", current_user.display_name)
            print()

            for user_id in envs['LOOK_FOR'].strip().split('\n'):
                data = {}
                user = usr_api.get_user(user_id)
                # print(user)
                print(f"User ID: {user_id}")
                print(f"Display Name:", display_name := user.display_name)
                print(f"Username:", username := user.username)
                print(f"User State:", user_state := str(user.state))
                # States:
                #           'active' -> On the website
                #           'online' -> In game
                # if user_state == "online":
                print(f"User Status:", user_status := str(user.status))
                # Statuses:
                #       'join me'   -> blue
                #       'active'    -> green
                #       'ask me'    -> yellow
                #       'busy'      -> red
                print(f"Instance ID:", instance_id := str(user.instance_id))
                print(f"World ID:", world_id := str(user.world_id))
                last_activity = user.last_activity
                print(f"Last Activity:",
                        last_activity := utc_to_local(last_activity).isoformat("T", "milliseconds"))
                print(f"Last Login:", last_login := user.last_login)

                data["id"] = user_id
                data["display_name"] = display_name
                data["username"] = username
                data["user_state"] = user_state
                data["user_status"] = user_status
                data["instance_id"] = instance_id
                data["world_id"] = world_id
                data["last_activity"] = last_activity
                data["lost_login"] = last_login
                user_data.append(data)
                print()

        except vrchatapi.ApiException as e:
            print("Exception when calling API: %s\n", e)
    [print(data) for data in user_data]
    write_to_csv(user_data)

def write_to_csv(data):
    fieldnames = [
        "id",
        "display_name",
        "username",
        "user_state",
        "user_status",
        "instance_id",
        "world_id",
        "last_activity",
        "lost_login",
        ]

    with open("test_file.txt", 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None)

if __name__ == "__main__":
    main()
