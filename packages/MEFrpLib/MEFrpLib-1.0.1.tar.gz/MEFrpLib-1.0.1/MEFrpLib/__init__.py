# -*- coding:utf-8 -*-
"""
MEFrpLib is a Python module that helps developers use MEFrp API easily.
YOU ARE NOT ALLOWED TO USE THIS MODULE TO DO THINGS THAT VIOLATE MEFRP'S TERMS OF USE.
Copyright (c) 2024 LxHTT
"""
from .auth import (
    me_get_user_info,
    me_user_sign,
    me_get_realname_status,
    me_post_realname,
    me_node_list,
    me_get_tunnel_config,
)
from .public import (
    me_send_register_email,
    me_register,
    me_login,
    me_forgot_password,
    me_get_sponsor,
)

__version__ = "1.0.0"
