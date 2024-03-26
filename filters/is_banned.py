from aiogram.filters import Filter
from aiogram import types
from utility.db import *

class IsBannedFilter(Filter):
    def __init__(self):
        pass
    async def __call__(self,message:types.Message)->bool:
        banned_users = [user[1] for user in getAllBannedUsers()]
        if(message.from_user.id in banned_users):
            return True
        else: return False