# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     user.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/12
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class UserPathSuffix(Enum):
    user_special = '/user/getNewIsSpecialUser'
    user_settings = '/user/setting/get'
    friend_recommend = '/relation/friend/recommend'
    user_profile = '/user/get'


class UserHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_user_special(self, json: dict) -> dict:
        """获取用户特权信息"""
        return self.http_client.send_request(method="post", path=UserPathSuffix.user_special.value, json=json)

    def get_user_settings(self, json: dict) -> dict:
        """获取用户设置信息"""
        return self.http_client.send_request(method="post", path=UserPathSuffix.user_settings.value, json=json)

    def get_user_friend_recommend(self, json: dict) -> dict:
        """获取用户朋友推荐信息"""
        return self.http_client.send_request(method="post", path=UserPathSuffix.friend_recommend.value, json=json)

    def get_user_profile(self, json: dict) -> dict:
        """获取用户个人资料"""
        return self.http_client.send_request(method="post", path=UserPathSuffix.user_profile.value, json=json)
