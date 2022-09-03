# Step 1. We begin with creating a Configuration, which contains the username and password for authentication.
import vrchatapi
from vrchatapi.api import authentication_api, users_api
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

    try:
        # Step 3. Calling getCurrentUser on Authentication API logs you in if the user isn't already logged in.
        current_user = auth_api.get_current_user()
        print("Logged in as:", current_user.display_name)
        print()

        for user_id in config['LOOK_FOR'].split('\n'):
            user = usr_api.get_user(user_id)
            print(f"User ID: {user_id}")
            print(f"Display Name:", display_name:=user.display_name)
            print(f"Username:", username:=user.username)

            # State:    'active' -> On the website
            #           'online' -> In game
            print(f"User State:", user_state:=user.state)
            if str(user_state) == "online":
                print(f"User Status:", user_status:=user.status)
                print(f"User Location:", user_location:=user.location)
            print(f"Last Activity:", last_activity:=user.last_activity)
            print(f"Last Login:", last_login:=user.last_login)

            print()

    except vrchatapi.ApiException as e:
        print("Exception when calling API: %s\n", e)
