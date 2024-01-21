from .models import (
    JSONReturnModel,
    AuthRequestModel,
    TextReturnModel,
)


def me_get_user_info(authorization: str, bypass_proxy: bool = False) -> JSONReturnModel:
    return AuthRequestModel(
        data={},
        path="/api/v4/auth/user",
        method="GET",
        bypass_proxy=bypass_proxy,
        model=JSONReturnModel,
        authorization=authorization,
    ).run()


def me_user_sign(authorization: str, bypass_proxy: bool = False) -> JSONReturnModel:
    return AuthRequestModel(
        data={},
        path="/api/v4/auth/sign",
        method="GET",
        bypass_proxy=bypass_proxy,
        model=JSONReturnModel,
        authorization=authorization,
    ).run()


def me_get_realname_status(
    authorization: str, bypass_proxy: bool = False
) -> JSONReturnModel:
    return AuthRequestModel(
        data={},
        path="/api/v4/auth/realname/get",
        method="GET",
        bypass_proxy=bypass_proxy,
        model=JSONReturnModel,
        authorization=authorization,
    ).run()


def me_post_realname(
    authorization: str, idcard: str, name: str, bypass_proxy: bool = False
) -> JSONReturnModel:
    return AuthRequestModel(
        data={"idcard": idcard, "name": name},
        path="/api/v4/auth/realname/post",
        method="POST",
        bypass_proxy=bypass_proxy,
        model=JSONReturnModel,
        authorization=authorization,
    ).run()


def me_node_list(authorization: str, bypass_proxy: bool = False) -> JSONReturnModel:
    return AuthRequestModel(
        data={},
        path="/api/v4/auth/node/list",
        method="GET",
        bypass_proxy=bypass_proxy,
        model=JSONReturnModel,
        authorization=authorization,
    ).run()


def me_get_tunnel_config(
    authorization: str, id: int, bypass_proxy: bool = False
) -> JSONReturnModel:
    return AuthRequestModel(
        data={},
        path=f"/api/v4/auth/conf/node/{id}",
        method="GET",
        bypass_proxy=bypass_proxy,
        model=TextReturnModel,
        authorization=authorization,
    ).run()
