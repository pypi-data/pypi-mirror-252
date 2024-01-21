from .models import (
    JSONReturnModel,
    JSONRequestModel,
)


def me_send_register_email(email: str, bypass_proxy: bool = False) -> JSONReturnModel:
    return JSONRequestModel(
        data={"email": email},
        path="/api/v4/public/verify/register/email",
        method="POST",
        bypass_proxy=bypass_proxy,
        model=JSONReturnModel,
    ).run()


def me_register(
    email: str, username: str, password: str, code: int, bypass_proxy: bool = False
):
    return JSONRequestModel(
        data={"email": email, "username": username, "password": password, "code": code},
        path="/api/v4/public/verify/register",
        method="POST",
        bypass_proxy=bypass_proxy,
        model=JSONReturnModel,
    ).run()


def me_login(username: str, password: str, bypass_proxy: bool = False):
    return JSONRequestModel(
        data={"username": username, "password": password},
        path="/api/v4/public/verify/login",
        method="POST",
        bypass_proxy=bypass_proxy,
        model=JSONReturnModel,
    ).run()


def me_forgot_password(email: str, username: str, bypass_proxy: bool = False):
    return JSONRequestModel(
        data={"email": email, "username": username},
        path="/api/v4/public/verify/forgot_password",
        method="POST",
        bypass_proxy=bypass_proxy,
        model=JSONReturnModel,
    ).run()


def me_get_sponsor(bypass_proxy: bool = False) -> JSONReturnModel:
    return JSONRequestModel(
        data={},
        path="/api/v4/public/info/sponsor",
        method="GET",
        bypass_proxy=bypass_proxy,
        model=JSONReturnModel,
    ).run()
