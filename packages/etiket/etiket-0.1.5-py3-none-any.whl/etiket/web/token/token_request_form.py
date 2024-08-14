from typing import Annotated, Union
from fastapi.param_functions import Form

class OAuth2TokenRequestForm:
    def __init__(
        self, *,
        grant_type: Annotated[Union[str, None], Form(regex="password|refresh_token")] = None,
        username: Annotated[str, Form()] = "",
        password: Annotated[str, Form()] = "",
        refresh_token: Annotated[str, Form()] = "",
        scope: Annotated[str, Form()] = "",
        client_id: Annotated[Union[str, None], Form()] = None,
        client_secret: Annotated[Union[str, None], Form()] = None,
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.refresh_token = refresh_token
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret