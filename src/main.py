from auth.auth import Auth
import json
import sys, os


sync_folder_name = "My Space"
user_name = os.getlogin()

sync_folder_path = "/home/"+user_name + "/" + sync_folder_name

logs = open("logs.txt", "r+")

is_logged = len(list(logs.readlines())) != 0

def create_folder(path:str):
    
    os.chdir("/home/"+user_name)

    if sync_folder_name not in os.listdir():
        print("Creating Sync Folder...")
        os.mkdir(sync_folder_name)
        print("Your Folder has been created")
    else:
        print("Folder found " + sync_folder_path)

def show_user_details():
    atts = []

    with open("logs.txt", "r") as user:
        data = json.dumps(user.readline())
       
        return data

def show_login_menu():
    
    print("You need to login")

    email = input("Enter Email: ")
    password = input("Enter Password:")
    auth  = Auth()

    user = auth.login(email=email, password=password)
   
    if user:
        logs.write(str(user))
   

if __name__ == "__main__":
    print("Welcome To File Space") 

    while not is_logged:
        show_login_menu()

    if is_logged:
     
    
        create_folder(path="")