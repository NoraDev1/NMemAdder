
import datetime

import motor.motor_asyncio
import config


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.config = self.db.config

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            notif=True,
            session="",
            login=False,

            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason="",
                
            ),
        )
 

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)


    async def is_user_exist(self, id):
        user = await self.col.find_one({"id": int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({"id": int(user_id)})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        )
        await self.col.update_one({"id": id}, {"$set": {"ban_status": ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason,
        )
        await self.col.update_one({"id": user_id}, {"$set": {"ban_status": ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        )
        user = await self.col.find_one({"id": int(id)})
        return user.get("ban_status", default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({"ban_status.is_banned": True})
        return banned_users

    async def set_notif(self, id, notif):
        await self.col.update_one({"id": id}, {"$set": {"notif": notif}})

    async def get_notif(self, id):
        user = await self.col.find_one({"id": int(id)})
        return user.get("notif", False)

    async def get_all_notif_user(self):
        notif_users = self.col.find({"notif": True})
        return notif_users

    async def total_notif_users_count(self):
        count = await self.col.count_documents({"notif": True})
        return count

    async def set_session(self, id, session):
        await self.col.update_one({"id": id}, {"$set": {"session": session}})

    async def get_session(self, id):
        user = await self.col.find_one({"id": int(id)})
        return user.get("session")

    async def set_api(self, id, api):
        await self.col.update_one({"id": id}, {"$set": {"api": api}})

    async def get_api(self, id):
        user = await self.col.find_one({"id": int(id)})
        return user.get("api")

    async def set_hash(self, id, hash):
        await self.col.update_one({"id": id}, {"$set": {"hash": hash}})

    async def get_hash(self, id):
        user = await self.col.find_one({"id": int(id)})
        return user.get("hash")

    async def set_login(self, id, login:bool):
        await self.col.update_one({"id": id}, {"$set": {"login": login}})

    async def get_login(self, id):
        user = await self.col.find_one({"id": int(id)})
        return user.get("login")




   ########################## config data management #######################
    # def new_config(self, sleep):
    #     return dict(
    #         id = "config",
    #         sleep = sleep,

    #     )
 

    # async def add_config(self, sleep):
    #     user = self.new_config(sleep)
    #     await self.config.insert_one(user)

    # async def get_all_config(self):
    #     "get all config details"
    #     comp = self.config.find({"id": "config"})
    #     return comp

    # async def is_all_config(self):
    #     "get all config details"
    #     comp = self.config.find({"id": "config"})
    #     return True if comp else False

    async def set_fsub_channel(self, channel):
        await self.config.update_one({"id": "channel"}, {"$set": {"channel": channel}})

    async def get_fsub_channel(self):
        user = await self.config.find_one({"id": "channel"})
        return user.get("channel")

    async def set_fsub(self, status:bool):
        await self.config.update_one({"id": "fsub"}, {"$set": {"fsub": status}})

    async def get_fsub(self):
        user = await self.config.find_one({"id": "fsub"})
        return user.get("fsub")

    async def set_bcopy(self, status:bool):
        await self.config.update_one({"id": "copy"}, {"$set": {"copy": status}})

    async def get_bcopy(self):
        user = await self.config.find_one({"id": "copy"})
        return user.get("copy")
    # async def set_src(self, id, src):
    #     await self.col.update_one({"id": id}, {"$set": {"src": src}})

    # async def get_src(self, id, src):
    #     user = await self.col.find_one({"id": int(id)})
    #     return user.get("src", src)

    # async def set_dest(self, id, dest):
    #     await self.col.update_one({"id": id}, {"$set": {"dest": dest}})

    # async def get_dest(self, id, dest):
    #     user = await self.col.find_one({"id": int(id)})
    #     return user.get("dest", dest)

    # async def set_count(self, id, count):
    #     await self.col.update_one({"id": id}, {"$set": {"count": count}})

    # async def get_count(self, id, count):
    #     user = await self.col.find_one({"id": int(id)})
    #     return user.get("count", count)

    # async def set_type(self, id, type):
    #     await self.col.update_one({"id": id}, {"$set": {"type": type}})

    # async def get_type(self, id, type):
    #     user = await self.col.find_one({"id": int(id)})
    #     return user.get("type", type)


    # async def total_login(self):
    #     user = self.col.count_documents({"session":""})
    #     return user
db = Database(config.DB_URL, config.DB_NAME)