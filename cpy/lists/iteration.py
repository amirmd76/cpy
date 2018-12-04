class ListIterator(object):
    objects_list = None
    indices = None
    idx = 0

    def __init__(self, objects_list, indices=None):
        self.objects_list = objects_list
        self.indices = indices

    def __next__(self):
        try:
            index = self.idx
            if self.indices:
                index = self.indices[self.idx]
            item = self.objects_list[index]
            self.idx += 1
            return item
        except IndexError:
            raise StopIteration()


class ListSubSequence(object):
    objects_list = None
    indices = None

    def __init__(self, objects_list, indices=None):
        self.objects_list = objects_list
        self.indices = indices

    def __iter__(self):
        return ListIterator(self.objects_list, self.indices)

    def __len__(self):
        if self.indices:
            return len(self.indices)
        return len(self.objects_list)

    def __getitem__(self, idx):
        try:
            index = idx
            if self.indices:
                index = self.indices[idx]
            return self.objects_list[index]
        except Exception:
            raise IndexError("No such index")
