import json
import uuid

from cpy.lists.iteration import ListIterator


class RedisList(object):
    redis_client = None
    key = ""
    list_key = ""
    key_key = ""
    commitable = False

    @staticmethod
    def get_list_key(key):
        return "cpy:redis_list:list:{}".format(key)

    @staticmethod
    def get_key_key(key):
        return "cpy:redis_list:key:{}".format(key)

    def __init__(self, redis_client, key=None, overwrite=False, commit=True):
        self.redis_client = redis_client
        if not key:
            self.key = str(uuid.uuid4())
        else:
            self.key = key
        key_key = self.get_key_key(self.key)
        self.key_key = key_key
        try:
            original_key = self.redis_client.get(key_key)
        except:
            original_key = None
        if overwrite or not original_key:
            self.list_key = self.get_list_key(str(uuid.uuid4()))
            if commit:
                self.redis_client.set(key_key, self.list_key)
            else:
                self.commitable = True
        else:
            self.list_key = original_key

    def append(self, item):
        try:
            serialized = json.dumps(item)
        except:
            raise ValueError("item is not serializable")
        self.redis_client.rpush(self.list_key, serialized)

    def commit(self):
        if self.commitable:
            self.redis_client.set(self.key_key, self.list_key)

    def get(self, idx):
        try:
            return json.loads(self.redis_client.lindex(self.list_key, idx))
        except:
            return None

    def __getitem__(self, idx):
        item = self.get(idx)
        if item is None:
            raise IndexError("No such index")
        return item

    def __iter__(self):
        return ListIterator(self)

    def __len__(self):
        return self.redis_client.llen(self.list_key)
