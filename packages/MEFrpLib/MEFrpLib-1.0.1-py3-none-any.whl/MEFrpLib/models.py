from typing import Union, Dict, List
from requests import Session

API_ENDPOINT = "https://api.mefrp.com"


class JSONReturnModel(object):
    def __init__(self, data: Union[Dict, List]):
        self.data: Union[Dict, List] = data["data"]
        self.message: str = data["message"]
        self.status: int = data["status"]


class TextReturnModel(object):
    def __init__(self, data: str):
        self.data: str = data


class JSONRequestModel(object):
    def __init__(
        self,
        data: Union[Dict, List],
        path: str,
        method: str,  # get post...
        bypass_proxy: bool = False,
        model: Union[JSONReturnModel, TextReturnModel] = JSONReturnModel,
    ):
        self.data = data
        self.path = path.lower()
        self.method = method
        self.bypass_proxy = bypass_proxy
        self.model = model

    def run(self) -> Union[JSONReturnModel, TextReturnModel]:
        s = APISession(self.bypass_proxy)
        r = getattr(s, self.method)(url=f"{API_ENDPOINT}{self.path}", json=self.data)
        if isinstance(self.model, TextReturnModel):
            return TextReturnModel(r.text)
        else:
            return JSONReturnModel(r.json())


class QueryRequestModel(object):
    def __init__(
        self,
        data: Union[Dict, List],
        path: str,
        method: str,  # get post...
        bypass_proxy: bool = False,
        model: Union[JSONReturnModel, TextReturnModel] = JSONReturnModel,
    ):
        self.data = data
        self.path = path.lower()
        self.method = method
        self.bypass_proxy = bypass_proxy
        self.model = model

    def run(self) -> Union[JSONReturnModel, TextReturnModel]:
        s = APISession(self.bypass_proxy)
        r = getattr(s, self.method)(url=f"{API_ENDPOINT}{self.path}", json=self.data)
        if isinstance(self.model, TextReturnModel):
            return TextReturnModel(r.text)
        else:
            return JSONReturnModel(r.json())


class AuthRequestModel(JSONRequestModel):
    def __init__(
        self,
        data: Union[Dict, List],
        path: str,
        method: str,  # get post...
        bypass_proxy: bool = False,
        model: Union[JSONReturnModel, TextReturnModel] = JSONReturnModel,
        authorization: str = "",
    ):
        super().__init__(
            data=data,
            path=path,
            method=method,
            bypass_proxy=bypass_proxy,
            model=model,
        )
        self.authorization = authorization

    def run(self) -> Union[JSONReturnModel, TextReturnModel]:
        s = APISession(self.bypass_proxy)
        s.headers.update({"Authorization": f"Bearer {self.authorization}"})
        r = getattr(s, self.method)(url=f"{API_ENDPOINT}{self.path}", json=self.data)
        if isinstance(self.model, TextReturnModel):
            return TextReturnModel(r.text)
        else:
            return JSONReturnModel(r.json())


class APISession(Session):
    def __init__(self, BYPASS_SYSTEM_PROXY=False):
        super().__init__()
        #: Trust environment settings for proxy configuration, default
        #: authentication and similar.
        self.trust_env = not BYPASS_SYSTEM_PROXY
