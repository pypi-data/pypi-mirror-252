import os
from locker import Locker

CONFIG_DEFAULT_SECTION = 'General'

LOCKER_ACCESS_KEY_ID = "f63ab764-7174-4309-8e01-b4263ad55e4d"
LOCKER_ACCESS_SECRET_KEY = "/kfEOLNKHCAw0PiOE18LhZMeexXIIzqwjcOlC6dc0+0="


class Config:
    def __init__(self):
        self.locker = Locker(access_key_id=LOCKER_ACCESS_KEY_ID, secret_access_key=LOCKER_ACCESS_SECRET_KEY)
        self.set_attr()

    def set_attr(self):
        secrets = self.locker.list()
        for arg in secrets:
            setattr(self, arg['key'].lower(), arg['value'])


config = Config()


print(config)
