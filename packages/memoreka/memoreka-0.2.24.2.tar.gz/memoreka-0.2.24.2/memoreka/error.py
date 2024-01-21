class MobilePhoneNumberLengthError(ValueError):
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class MobilePhoneNumberInternationalTelephoneAreaCodeError(ValueError):
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg = msg

    def __str__(self) -> str:
        return self.msg
