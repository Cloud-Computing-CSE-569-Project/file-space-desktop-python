from auth.auth import Auth
import json
import sys, os
from core.watcher import Watcher
from core.indexer import Indexer
from config.aws import Services
from config.db import DBConnector

import uuid

sync_folder_name = "My Space"
user_name = os.getlogin()

sync_folder_path = "/home/" + user_name + "/" + sync_folder_name

logs = "logs.txt"


def create_folder(sync_folder: str):

    os.chdir("/home/" + user_name)

    if sync_folder_name not in os.listdir():
     
        print("Creating Sync Folder Locally...")
        os.mkdir(sync_folder_name)
        print("Your Folder has been created")
        print("=============================")
        print("Creating Sync Folder Remotely")

        try:

            Services.s3.put_object(
                Bucket="file-storage-global113245-dev",
                Key="sync_folders/" + sync_folder + "/",
            )
            print("Folder Created on the Cloud - You can access via your phone")
        except Exception as e:
            print(e)
        
        print("Creating Database....")
        connector = DBConnector()
        connector.create_table()
    
    else:
        print("Your sync folder is " + sync_folder_path)


def show_user_details():
    atts = []

    with open(logs, "r") as user:
        data = eval(user.read())
        return data


def show_login_menu():
    f = open(logs, "r+")
    print("You need to login")

    email = input("Enter Email: ")
    password = input("Enter Password:")
    auth = Auth()

    user = auth.login(email=email, password=password)

    if "Username" in user.keys():
        f.write(str(user))
        f.close()
    return True


if __name__ == "__main__":

    print("Welcome To File Space")
    my_indexer = Indexer()

    f = open(logs, "r")
    is_logged = len(list(f.readlines())) != 0
    print(is_logged)

    while not is_logged:
        is_logged = show_login_menu()

    print("Logged")
    if is_logged:
        user_details = show_user_details()
        user_id = user_details["Username"]
        name = [
            name["Value"]
            for name in user_details["UserAttributes"]
            if name["Name"] == "name"
        ]
        sync_folder_name_cloud = user_id
        print("Welcome " + name[0])

        my_watcher = Watcher(
            sync_folder_path=sync_folder_path,
            indexer=my_indexer,
            user_sync_folder=sync_folder_name_cloud,
        )
        create_folder(sync_folder=user_id)
        my_watcher.start_sync()

        """ bucket = Services.s3.Bucket(Services.bucket_name)
        for obj in bucket.objects.filter(Prefix="sync_folders/{0}".format(user_id)):
            print(obj.owner) """

    f.close()
