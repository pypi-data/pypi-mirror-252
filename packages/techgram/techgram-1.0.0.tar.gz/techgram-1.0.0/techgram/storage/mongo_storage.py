# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient


class MongoStorage:
    def __init__(self, mongo_url: str, mongo_name: str):
        try:
            self._asyncMongo = AsyncIOMotorClient(mongo_url)
            self._syncMongo = MongoClient(mongo_url)
            self.mongoName = mongo_name
        except AttributeError:
            return

    @property
    def async_Mongo(self):
        return self._asyncMongo[self.mongoName]

    @property
    def sync_Mongo(self):
        return self._syncMongo[self.mongoName]
