class DictList(object):
    objects = {}
    head = 0
    tail = 0

    def __init__(self, items=None):
        if items:
            for item in items:
                self.push_back(item)

    def push_back(self, item):
        self.objects[self.tail] = item
        self.tail += 1

    def push_front(self, item):
        self.head -= 1
        self.objects[self.head] = item

    def pop_back(self):
        if self.__len__() == 0:
            return None
        self.tail -= 1
        item = self.objects[self.tail]
        del self.objects[self.tail]
        return item

    def pop_front(self):
        if self.__len__() == 0:
            return None
        item = self.objects[self.head]
        del self.objects[self.head]
        self.head += 1
        return item

    def append(self, item):
        self.push_back(item)

    def pop(self):
        return self.pop_back()

    def get(self, idx, default=None, raise_exception=False):
        if idx < 0:
            idx += self.__len__()
        try:
            item = self.objects[self.head + idx]
        except KeyError:
            if raise_exception:
                raise IndexError("No such index")
            return default
        return item

    def __getitem__(self, idx):
        return self.get(idx, raise_exception=True)

    def __iter__(self):
        return DictListIterator(self)
    
    def __len__(self):
        return self.tail - self.head
    

class DictListIterator(object):
    dict_list = None
    idx = 0
    
    def __init__(self, dict_list: DictList):
        self.dict_list = dict_list
    
    def __next__(self):
        try:
            item = self.dict_list[self.idx]
            self.idx += 1
            return item
        except IndexError:
            raise StopIteration()

