import json
import uuid


class RedisList(object):
    redis_client = None
    key = ""
    list_key = ""

    @staticmethod
    def get_list_key(key):
        return "cpy:redis_list:list:{}".format(key)

    @staticmethod
    def get_key_key(key):
        return "cpy:redis_list:key:{}".format(key)

    def __init__(self, redis_client, key=None, overwrite=False):
        self.redis_client = redis_client
        if not key:
            self.key = str(uuid.uuid4())
        else:
            self.key = key
        key_key = self.get_key_key(self.key)
        try:
            original_key = self.redis_client.get(key_key)
        except:
            original_key = None
        if overwrite or not original_key:
            self.list_key = self.get_list_key(str(uuid.uuid4()))
            self.redis_client.set(key_key, self.list_key)
        else:
            self.list_key = original_key

    def append(self, item):
        try:
            serialized = json.dumps(item)
        except:
            raise ValueError("item is not serializable")
        self.redis_client.rpush(self.list_key, serialized)

    def get(self, idx):
        try:
            return json.loads(self.redis_client.lindex(self.list_key, idx))
        except:
            return None

    def __getitem__(self, idx):
        item = self.get(idx)
        if item is None:
            raise IndexError("No such index")

    def __iter__(self):
        return RedisListIterator(self.redis_client, self.list_key)

    def __len__(self):
        return self.redis_client.llen(self.list_key)


class RedisListIterator(object):
    key = None
    idx = 0
    redis_client = None

    def __init__(self, redis_client, key):
        self.redis_client = redis_client
        self.key = key

    def __next__(self):
        try:
            res = json.loads(self.redis_client.lindex(self.key, self.idx))
            self.idx += 1
            return res
        except:
            raise StopIteration()