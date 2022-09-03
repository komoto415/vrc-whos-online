import vrchatapi
from vrchatapi.api import authentication_api, users_api, instances_api
from dotenv import dotenv_values

config = dotenv_values(".env")

configuration = vrchatapi.Configuration(
    username = str(config['USERNAME']),
    password = str(config['PASSWORD']),
)


with vrchatapi.ApiClient(configuration) as api_client:
    # Instantiate instances of API classes
    auth_api = authentication_api.AuthenticationApi(api_client)
    usr_api = users_api.UsersApi(api_client)
    inst_api = instances_api.InstancesApi(api_client)

    try:
        current_user = auth_api.get_current_user()
        print("Logged in as:", current_user.display_name)
        print()

        for user_id in config['LOOK_FOR'].strip().split('\n'):
            user = usr_api.get_user(user_id)
            # print(user)
            print(f"User ID: {user_id}")
            print(f"Display Name:", display_name:=user.display_name)
            print(f"Username:", username:=user.username)

            print(f"User State:", user_state:=str(user.state))
            # States:
            #           'active' -> On the website
            #           'online' -> In game
            if user_state == "online":
                print(f"User Status:", user_status:=str(user.status))
                # Statuses:
                #       'join me'   -> blue
                #       'active'    -> green
                #       'ask me'    -> yellow
                #       'busy'      -> red
                print(f"Instance ID:", instance_id:=str(user.instance_id))
                if instance_id != "private":
                    print(f"World ID:", world_id:=str(user.world_id))
                    # instance = inst_api.get_instance(world_id, instance_id)
                    # print(instance)
                    # print(f"User Location:", user_location:=user.location)
                else:
                    print("User Location: In Private World")
            print(f"Last Activity:", last_activity:=user.last_activity)
            print(f"Last Login:", last_login:=user.last_login)

            print()

    except vrchatapi.ApiException as e:
        print("Exception when calling API: %s\n", e)
