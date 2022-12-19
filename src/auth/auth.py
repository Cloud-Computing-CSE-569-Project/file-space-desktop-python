import os
from config.aws import Services
import uuid
import sys
from models.login import Login
from models.user import User
from pathlib import Path
from dotenv import load_dotenv
from db.db import engine, logins
from sqlalchemy import text
load_dotenv()

USER_POOL_ID = os.getenv("USER_POOL_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("DESKTOP_CLIENT_SECRET")
IDENTITY_POOL_ID = os.getenv("IDENTITY_POOL_ID")
BUCKET_ID = os.getenv("BUCKET_NAME")


class Auth:
    def login(self, email: str, password: str):
        try:
            response = Services.cognito.initiate_auth(
                ClientId=CLIENT_ID,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": email, "PASSWORD": password},
            )

            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                token = response["AuthenticationResult"]["AccessToken"]
                self._save_login(token=token)
            return token
        except Exception as e:
            return e.args[-1]

    def get_user_info(self, token):

        try:
            user = Services.cognito.get_user(AccessToken=token)

            if user:
                return {
                    "sync_folder_name": user["Username"],
                    "name": [
                        attr["Value"]
                        for attr in user["UserAttributes"]
                        if attr["Name"] == "name"
                    ][0],
                    "email": [
                        attr["Value"]
                        for attr in user["UserAttributes"]
                        if attr["Name"] == "email"
                    ][0],
                    "limit_quota": [
                        attr["Value"]
                        for attr in user["UserAttributes"]
                        if attr["Name"] == "custom:limit_quota"
                    ][0],
                    "quota_used": [
                        attr["Value"]
                        for attr in user["UserAttributes"]
                        if attr["Name"] == "custom:quota_used"
                    ],
                    "desktop": [
                        attr["Value"]
                        for attr in user["UserAttributes"]
                        if attr["Name"] == "custom:desktop"
                    ][0],
                    "username": [
                        attr["Value"]
                        for attr in user["UserAttributes"]
                        if attr["Name"] == "sub"
                    ][0],
                    "cog_id": [
                        attr["Value"]
                        for attr in user["UserAttributes"]
                        if attr["Name"] == "custom:cog_id"
                    ][0],

                }
        except Exception as e:
            print(e)

    def _save_login(self, token):

        user = Services.cognito.get_user(AccessToken=token)

        login_details = Login(username=user["Username"], access_token=token)
        
        query = """ Insert into logins(username, isLogged, accessToken) values ('{0}','{1}', '{2}')""".format(
            login_details.username, login_details.is_logged, login_details.access_token
        )
        engine.execute(text(query))

    def signup(self, user: User):
        """"
            Singup new user
        """ ""
        return user
