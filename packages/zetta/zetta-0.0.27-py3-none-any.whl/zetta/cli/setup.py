# Copyright ZettaBlock Labs 2024
import requests
import configparser
import os
import webbrowser
from zetta._utils.async_utils import synchronizer

SERVICE_SIGNIN_URL = "https://stage-app.zettablock.dev/aiweb/login"
SERVICE_GET_USER_URL = "https://neo-dev.prod.zettablock.com/v1/auth/user"
HEADERS = {
    "Authorization": ""
}

@synchronizer.create_blocking
async def setup():
    try:
        webbrowser.open(SERVICE_SIGNIN_URL)
        token = get_user_token()
        profile_data = get_user_profile(token)
        generate_profile_file(profile_data)
    except Exception as e:
        print(f"An error occurred: {e}")
    pass


def get_user_token():
    token = input("Enter the token obtained from your Zetta account:")
    return token


def get_user_profile(token):
    HEADERS['Authorization'] = token 
    response = requests.get(SERVICE_GET_USER_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def existed(d, key):
    if d[key] != "" and d[key] is not None:
        return True
    return False

def generate_profile_file(profile_data, profile_name="default"):
    config = configparser.ConfigParser()
    config[profile_name] = {}
    if existed(profile_data["data"]["profile"], "token"):
        config[profile_name]["token"] = profile_data["data"]["profile"]["token"]
    if existed(profile_data["data"]["profile"], "api_key"):
        config[profile_name]["api_key"] = profile_data["data"]["profile"]["api_key"]
    if existed(profile_data["data"]["profile"], "wallet_address"):
        config[profile_name]["wallet_address"] = profile_data["data"]["profile"]["wallet_address"]

    zetta_dir = setup_zettadir()
    file_path = os.path.join(zetta_dir, "credentials")
    with open(file_path, "w") as configfile:
        config.write(configfile)

    config[profile_name] = {}
    if existed(profile_data["data"]["user"], "id"):
        config[profile_name]["id"] = profile_data["data"]["user"]["id"]
    if existed(profile_data["data"]["user"], "tenant"):
        config[profile_name]["tenant"] = profile_data["data"]["user"]["tenant"]
    if existed(profile_data["data"]["user"], "user_name"):
        config[profile_name]["user_name"] = profile_data["data"]["user"]["user_name"]
    if existed(profile_data["data"]["user"], "email"):
        config[profile_name]["email"] = profile_data["data"]["user"]["email"]

    file_path = os.path.join(zetta_dir, "profile")
    with open(file_path, "w") as configfile:
        config.write(configfile)

    print_directory_structure(zetta_dir)


def print_directory_structure(root_dir):
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = '│   ' * level + '├── ' if level > 0 else ''
        print(f"{indent}{os.path.basename(root)}/")
        
        sub_indent = '│   ' * (level + 1) + '├── '
        for f in files:
            print(f"{sub_indent}{f}")


def setup_zettadir():
    zetta_root = os.getenv("ZETTA_ROOT")
    if not zetta_root:
        raise EnvironmentError("ZETTA_ROOT env variable is not set.")
    zetta_dir = os.path.join(zetta_root, ".zetta")
    if not os.path.exists(zetta_dir):
        os.makedirs(zetta_dir)
    return zetta_dir
