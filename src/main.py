from auth.auth import Auth
import os
from config.aws import Services

from core.watcher import Watcher
from db.db import engine, logins
from sqlalchemy import text
sync_folder_name = "My Space"
user_name = os.getlogin()

sync_folder_path = "/home/" + user_name + "/" + sync_folder_name


def create_folder(sync_folder: str, token: str):

    os.chdir("/home/" + user_name)

    if sync_folder_name not in os.listdir():

        print("Creating Sync Folder Locally...")
        os.mkdir(sync_folder_name)
        print("Your Folder has been created")
        print("=============================")
        print("Creating Sync Folder Remotely")

        try:

            Services.s3.Bucket(Services.bucket_name).put_object(
                Key=sync_folder + "/"
            )
            print("Folder Created on the Cloud")

        except Exception as e:
            print(e)

        #db.create_table()

        attr = {"device": user_name, "sync_folder": sync_folder}

        update = str([attr])
        response = Services.cognito.update_user_attributes(
            UserAttributes=[
                {"Name": "custom:desktop", "Value": update},
            ],
            AccessToken=token,
        )
    else:
        print("Your sync folder is " + sync_folder_path)


def show_login_menu():
    print("You need to login")

    email = input("Enter Email: ")
    password = input("Enter Password:")
    auth = Auth()

    token = auth.login(email=email, password=password)

    if token == "":
        return False
    return True


def main_screen():
    token = logins[0][-1]
    user_details = Auth().get_user_info(token=token)
    sync_folder_name_cloud = "protected/{0}/sync_folders/{1}".format(user_details["cog_id"], user_name)
    print("Welcome " + user_details["name"])

    my_watcher = Watcher(
            sync_folder=sync_folder_path,
            sync_folder_remote=sync_folder_name_cloud,
            user=user_details,
    )

    create_folder(sync_folder=sync_folder_name_cloud, token=token)
    my_watcher.sync()  # 726374143976

if __name__ == "__main__":
    #db = DBConnector()
    #db.create_login_table()
    print("Welcome To File Space")

    logins = engine.execute(text("select * from logins")).fetchall()
    is_logged = len(logins) != 0

    if is_logged:
      main_screen()
    else:
        while not is_logged:
            is_logged = show_login_menu()
            print("You Are logged!")
            os.system("exit")
