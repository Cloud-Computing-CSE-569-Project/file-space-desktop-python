from auth.auth import Auth
import json
import sys, os
from core.indexer import Indexer
from config.aws import Services
import boto3
from config.db import DBConnector
from models.user import User
import requests
from core.watcher import Watcher
from queue import Queue
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
                Key="sync_folders/" + sync_folder + "/"
            )
            print("Folder Created on the Cloud")

        except Exception as e:
            print(e)

        print("Creating Database....")
        db.create_table()

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

    print(token)
    if token == "":
        return False
    return True


if __name__ == "__main__":
    db = DBConnector()
    db.create_login_table()
    print("Welcome To File Space")
    my_indexer = Indexer()

    logins = db.fetch_logins()
    is_logged = len(logins) != 0

    while not is_logged:
        is_logged = show_login_menu()

    if is_logged:
        token = logins[0][-1]
        user_details = Auth().get_user_info(token=token)
        sync_folder_name_cloud = user_details["sync_folder_name"]
        print("Welcome " + user_details["name"])
     
        my_watcher = Watcher(
            sync_folder = sync_folder_path,
            sync_folder_remote = sync_folder_name_cloud,
            user = user_details
        )

        create_folder(sync_folder=sync_folder_name_cloud, token=token)
        my_watcher.sync()  # 726374143976
