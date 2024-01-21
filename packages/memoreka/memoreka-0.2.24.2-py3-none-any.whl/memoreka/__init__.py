import json
import time

import requests

import moa.error


class MoaUser:
    def __init__(self, phone: str, pwd: str, server: str = "https://api.memoreka.com") -> None:
        """
        初始化一个妙花笔记用户对象
        :param phone: 手机号，格式为 "+86 11451419198"
        :param pwd: 密码
        :param server: 服务器，默认为 https://api.memoreka.com
        """
        if len(phone) != 15:
            raise moa.error.MobilePhoneNumberLengthError(
                f"手机号码长度或格式错误，正确格式应为 \"+86 11451419198\" 而参数为 \"{phone}\""
            )
        if not phone.startswith("+86 "):
            raise moa.error.MobilePhoneNumberInternationalTelephoneAreaCodeError(
                f"国际电话区号错误，应恒定为 \"+86 \" 而传入的是 \"{phone[:4]}\""
            )
        self.phone: str = phone
        self.pwd: str = pwd
        self.server: str = server
        self.jk: str or None = None  # 个人兑换码
        self.name: str or None = None  # （猜测）用户名，目前恒定为空
        self.token: str or None = None
        self.secret: str or None = None
        self.expired: int or None = None  # （猜测）token/secret 过期时间
        self.login_time: int or None = None
        self.login()

    def __str__(self) -> str:
        return (f"(phone={self.phone}, pwd={self.pwd}, server={self.server}, jk={self.jk}, name={self.name}, "
                f"token={self.token}, secret={self.secret}, expired={self.expired}, login_time={self.login_time})")

    def __repr__(self) -> str:
        return self.__str__()

    def request_api(self, method: str, path: str, params: dict) -> dict:
        """
        向 API 发起请求
        :param method: HTTP 请求方法，如 "GET", "POST" 等
        :param path: API 路径，如 "/auth/pass_login"
        :param params: API 传参，如 {"a": "b", "c": 114514}
        :return: API 返回结果
        """
        if self.login_time is not None and self.login_time > self.expired:  # 此处因为短路机制不会报错
            self.login()
        return requests.request(
            method=method,
            url=f"{self.server}{path}",
            data=json.dumps(params),
            headers={
                "User-Agent": "Dart/3.2 (dart.io)",  # 妙花笔记使用 Flutter 编写
                "lang": "zh",
                "version": "0.2.24",  # 本版本的库编写时基于该版本的 APP 进行抓包研究
                "Accept-encoding": "gzip",
                "meta": "eyJvcyI6ImFuZHJvaWQiLCJ2ZXIiOiJYaWFvbWkvdmFuZ29naC92YW5nb2doOjEyL1NLUTEuMjExMDA2LjAwMS9WMTMuMC"
                        "4zLjAuU0pWQ05YTTp1c2VyL3JlbGVhc2Uta2V5c19SRUxfMTJfMzFfMjAyMi0wNS0wMSIsImJyYW5kIjoiWGlhb21pIiwi"
                        "bW9kZWwiOiJ2YW5nb2doX00yMDAySjlFX3ZhbmdvZ2giLCJwaHlzaWNhbCI6dHJ1ZX0=",  # 追踪参数，此处为 小米10青春版
                "client": "moa",  # moa 是 妙花笔记 的英文缩写
                "Content-Type": "application/json, charset=utf-8",
                "role": "user",
                "did": self.jk if self.jk is not None else "",
                "token": self.token if self.token is not None else ""

            }
        ).json()

    def login(self) -> None:
        pass_login = self.request_api(
            method="POST",
            path="/auth/pass_login",
            params={
                "phone": self.phone,
                "pass": self.pwd
            }
        )
        try:
            self.jk = pass_login["jk"]
            self.name = pass_login["name"]
            self.token = pass_login["token"]
            self.secret = pass_login["secret"]
            self.expired = pass_login["expired"]
        except KeyError:
            raise ValueError(
                f"手机号或密码错误，以下为调试日志：\n"
                f"phone = {self.phone}\n"
                f"pwd = {self.pwd}\n"
                f"API_Result = {pass_login}"
            )
        self.login_time = time.time_ns() // 1000



