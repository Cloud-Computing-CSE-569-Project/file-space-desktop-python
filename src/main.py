from auth.auth import Auth
import json
import sys, os
from core.watcher import Watcher
from core.indexer import Indexer
from config.aws import Services
import uuid

sync_folder_name = "My Space"
user_name = os.getlogin()

sync_folder_path = "/home/" + user_name + "/" + sync_folder_name
sync_folder_name_cloud = str(uuid.uuid4())
logs = open("logs.txt", "r+")

is_logged = len(list(logs.readlines())) != 0


def create_folder(path: str):

    os.chdir("/home/" + user_name)

    if sync_folder_name not in os.listdir():
        print("Creating Sync Folder Locally...")
        os.mkdir(sync_folder_name)
        print("Your Folder has been created")
        print("=============================")
        print("Creating Sync Folder Remotely")

        try:

            response = Services.s3.put_object(
                Bucket="file-storage-global113245-dev",
                Key="sync_folders/" + sync_folder_name_cloud + "/",
            )
            print(response)
        except Exception as e:
            print(e)
    else:
        print("Your sync folder is " + sync_folder_path)


def show_user_details():
    atts = []

    with open("logs.txt", "r") as user:
        data = json.dumps(user.readline())

        return data


def show_login_menu():

    print("You need to login")

    email = input("Enter Email: ")
    password = input("Enter Password:")
    auth = Auth()

    user = auth.login(email=email, password=password)

    if user:
        logs.write(str(user))


if __name__ == "__main__":
    print("Welcome To File Space")
    my_indexer = Indexer()
    my_watcher = Watcher(
        sync_folder_path=sync_folder_path,
        indexer=my_indexer,
        user_sync_folder=sync_folder_name_cloud,
    )

    while not is_logged:
        show_login_menu()

    if is_logged:
        create_folder(path="")
        my_watcher.start_sync()
