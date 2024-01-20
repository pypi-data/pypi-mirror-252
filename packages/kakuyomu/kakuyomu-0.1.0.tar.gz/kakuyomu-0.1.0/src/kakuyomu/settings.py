import os
from typing import Final


def find_work_dir():
    cwd = os.getcwd()
    print(cwd)
    dirname = ".kakuyomu"
    while True:
        path = os.path.join(cwd, dirname)
        if os.path.exists(path):
            if os.path.isdir(path):
                return cwd
        cwd = os.path.dirname(cwd)
        if cwd == "/":
            raise FileNotFoundError(f"{dirname} not found")


class ConstMeta(type):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise TypeError(f"cannot reassign const {name!r}")
        else:
            self.__setsetattr__(name, value)

    def __delattr__(self, name: str) -> None:
        if name in self.__dict__:
            raise TypeError(f"cannot delete const {name!r}")


class URL(metaclass=ConstMeta):
    ROOT: Final[str] = "https://kakuyomu.jp"
    LOGIN: Final[str] = f"{ROOT}/login"
    MY: Final[str] = f"{ROOT}/my"
    MY_WORKS: Final[str] = f"{MY}/works"
    ANNTENA_WORKS: Final[str] = f"{ROOT}/anntena/works"


class Login(metaclass=ConstMeta):
    EMAIL_ADDRESS: Final[str] = os.environ.get("KAKUYOMU_EMAIL_ADDRESS")
    PASSWORD: Final[str] = os.environ.get("KAKUYOMU_PASSWORD")


class Config(metaclass=ConstMeta):
    # DIR: Final[str] = os.path.expanduser("~/.config/kakuyomu")
    DIR: Final[str] = find_work_dir()
    COOKIE: Final[str] = os.path.join(DIR, "cookie")


os.makedirs(Config.DIR, exist_ok=True)

if not Login.PASSWORD or not Login.EMAIL_ADDRESS:
    raise ValueError("KAKUYOMU_EMAIL_ADDRESS and KAKUYOMU_PASSWORD must be set")
