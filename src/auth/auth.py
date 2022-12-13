import os
from config.aws import Services
import uuid
import sys
from config.db import DBConnector
from models.login import Login
from models.user import User

USER_POOL_ID = "us-east-2_M1Eh4E3MA"  # os.getenv("USER_POOL_ID")
CLIENT_ID = "4rmavund0ekutqevh36li6ehta"  # os.getenv("DESKTOP_CLIENT_ID")
CLIENT_SECRET = os.getenv("DESKTOP_CLIENT_SECRET")
IDENTITY_POOL_ID = os.getenv("IDENTITY_POOL_ID")
BUCKET_ID = os.getenv("BUCKET_ID")


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

    def get_session(self):
        try:
            return Services.cognito_id.get_id(IdentityPoolId=IDENTITY_POOL_ID)
        except Exception as e:
            return e.args

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
                    ],
                    "quota_used": [
                        attr["Value"]
                        for attr in user["UserAttributes"]
                        if attr["Name"] == "custom:quota_used"
                    ],
                    "desktop": [
                        attr["Value"]
                        for attr in user["UserAttributes"]
                        if attr["Name"] == "custom:desktop"
                    ],
                }
        except Exception as e:
            print(e)

    def _save_login(self, token):
        db = DBConnector()

        user = Services.cognito.get_user(AccessToken=token)

        login_details = Login(username=user["Username"], access_token=token)

        print("Login ", db.create_login(login_details))

    def signup(self, user: User):
        """"
            Singup new user
        """ ""
        return user
