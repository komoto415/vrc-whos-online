import vrchatapi
from vrchatapi.api import authentication_api, users_api, instances_api
from dotenv import dotenv_values
import csv
from datetime import timezone, datetime
from dateutil import parser
import time
from win10toast import ToastNotifier

envs = dotenv_values(".env")

configuration = vrchatapi.Configuration(
        username=str(envs['USERNAME']),
        password=str(envs['PASSWORD']),
        )

USER_DATA = []
ONLINE = {}
API_REFRESH_TIME = 90
NOTIFICATION_DURATION = 10
MAX_LINE = 4

STATUS = {
    "join me": "blue",
    "active": "green",
    "ask me": "orange",
    "busy": "red"
    }

def poll_api():
    with vrchatapi.ApiClient(configuration) as api_client:
        # Instantiate instances of API classes
        auth_api = authentication_api.AuthenticationApi(api_client)
        usr_api = users_api.UsersApi(api_client)
        # inst_api = instances_api.InstancesApi(api_client)

        while True:
            try:
                current_user = auth_api.get_current_user()
                # print("Logged in as:", current_user.display_name)
                print("Polling API:", datetime.now().isoformat("T", "milliseconds"))
                print()

                global USER_DATA
                USER_DATA = []
                for user_id in envs["LOOK_FOR"].strip().split('\n'):
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
                    last_login = user.last_login
                    print(f"Last Login:",
                            last_login := utc_to_local(parser.parse(last_login)).isoformat("T", "milliseconds"))
                    last_activity = user.last_activity
                    print(f"Last Activity:",
                            last_activity := utc_to_local(last_activity).isoformat("T", "milliseconds"))

                    data["id"] = user_id
                    data["display_name"] = display_name
                    data["username"] = username
                    data["user_state"] = user_state
                    data["user_status"] = user_status
                    data["instance_id"] = instance_id
                    data["world_id"] = world_id
                    data["last_login"] = last_login
                    data["last_activity"] = last_activity
                    USER_DATA.append(data)
                    print()

                whos_online()
            except vrchatapi.ApiException as e:
                print("Exception when calling API: %s\n", e)

            print("Starting Sleep:", datetime.now().isoformat("T", "milliseconds"))
            print('-' * 80)
            time.sleep(API_REFRESH_TIME - ((len(ONLINE) // MAX_LINE) * NOTIFICATION_DURATION))

def whos_online():
    message = ""
    for user in USER_DATA:
        display_name = user["display_name"]
        if user["user_state"] == "online":
            times_seen_online = ONLINE.setdefault(user["id"], 0) + 1
            ONLINE[user["id"]] = times_seen_online
            # friends   -> friends
            # hidden    -> friends+
            # nothing?  -> public?????
            instance_info = "public"
            instance_id = user["instance_id"]
            if "private" in instance_id:
                instance_info = "private"
            elif "friends" in instance_id:
                instance_info = "friends"
            elif "hidden" in instance_id:
                instance_info = "friends+"
            print(online := f"{display_name} is on {STATUS[user['user_status']]} ({instance_info})")
            message += online + '\n'

        else:
            if user["id"] in ONLINE:
                print(offline := f"{display_name} has gone offline.")
                message += offline + '\n'
                del ONLINE[user["id"]]

    print()
    print(message)
    messages = [message]

    if len(ONLINE) > MAX_LINE:
        messages = []
        more_than_4 = message.split('\n')
        for i in range(len(ONLINE) % MAX_LINE):
            line = ""
            offset = i * MAX_LINE
            tail = offset + MAX_LINE
            for j in range(offset, tail):
                try:
                    new_line = more_than_4[j]
                    line += new_line + '\n'
                except IndexError as _:
                    break
            messages.append(line)

    if message == "":
        messages = ["No one is currently online"]

    """
    toast.show_toast(
        "Notification",
        "Notification body",
        duration = 20,
        icon_path = "icon.ico",
        threaded = True,
    )
    """
    for message in messages:
        print(message)
        toaster = ToastNotifier()
        toaster.show_toast(
                "Who's Online",
                message.strip(),
                icon_path=None,
                duration=NOTIFICATION_DURATION,
                )

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
        "last_login",
        ]

    with open("./logs/test_file.txt", 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None)

if __name__ == "__main__":
    poll_api()
