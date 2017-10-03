from pymongo import MongoClient

class Database:
    __instance = None
    def __new__(cls):
        if Database.__instance is None:
            Database.__instance = object.__new__(cls)
        Database.__instance.__client = MongoClient('localhost', 27017)
        Database.__instance.db = Database.__instance.__client.database
        Database.__instance.user_id = Database.__instance.db.user_id
        return Database.__instance

    def insert_credentials(self, user_id, credentials=None):
        creds = None if not credentials else credentials.to_json()
        if not self.get_credentials(user_id):
            Database.__instance.user_id.insert_one({"user_id": user_id, "credentials": creds})
        else:
            Database.__instance.user_id.update({"user_id": user_id}, {'$set': {"credentials": creds}})

    def get_credentials(self, user_id):
        return Database.__instance.user_id.find_one({'user_id': user_id})