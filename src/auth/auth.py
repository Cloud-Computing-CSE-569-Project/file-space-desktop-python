import os
from config.aws import Services

USER_POOL_ID = os.getenv("USER_POOL_ID")
CLIENT_ID = os.getenv("DESKTOP_CLIENT_ID")
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
            token = response["AuthenticationResult"]["AccessToken"]

            user = Services.cognito.get_user(AccessToken=token)
            return user
        except Exception as e:
            return e.args

    def get_session(self):
        try:
            return Services.cognito_id.get_id(IdentityPoolId=IDENTITY_POOL_ID)
        except Exception as e:
            return e.args
