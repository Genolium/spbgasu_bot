from aiogram.filters import Filter
from aiogram import types
from os import getenv
from dotenv import find_dotenv,load_dotenv
from utility.db import *

class IsAdminIDFilter(Filter):
    def __init__(self):
        pass
    async def __call__(self,message:types.Message)->bool:
        admin_ids = [user[0] for user in get_all_admins()]
        if(message.from_user.id in admin_ids):
            return True
        else: return False