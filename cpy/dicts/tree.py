class NodeTypes(object):
    OBJECT = 'object'
    DICT = 'dict'
    TUPLE = 'tuple'
    LIST = 'list'
    NONE = 'none'


class Node(object):
    node_type = NodeTypes.OBJECT
    children = None
    val = None

    def __init__(self, obj):
        if isinstance(obj, dict):
            self.node_type = NodeTypes.DICT
            self.children = {}
            for key, val in obj.items():
                self.children[key] = Node(val)
        elif isinstance(obj, list) or isinstance(obj, tuple):
            if isinstance(obj, list):
                self.node_type = NodeTypes.LIST
            elif isinstance(obj, tuple):
                self.node_type = NodeTypes.TUPLE
            self.children = []
            for item in obj:
                self.children.append(Node(item))
        elif obj is None:
            self.node_type = NodeTypes.NONE
        else:
            self.val = obj

    def decode(self):
        if self.node_type == NodeTypes.NONE:
            return None
        if self.node_type == NodeTypes.DICT:
            return {key: val.decode() for key, val in self.children.items()}
        if self.node_type == NodeTypes.LIST:
            return [child.decode() for child in self.children]
        if self.node_type == NodeTypes.TUPLE:
            res = tuple()
            for child in self.children:
                res = res + (child.decode(),)
            return res
        return self.val

    def get(self, *args):
        if not args:
            return self
        if self.node_type == NodeTypes.OBJECT or self.node_type == NodeTypes.NONE:
            return self.val
        return self.children[args[0]].get(*args[1:])

    def set(self, val, *args):
        if not args:
            raise Exception("You can't modify the root")
        if self.node_type == NodeTypes.OBJECT or self.node_type == NodeTypes.NONE:
            raise Exception("Non-iterable object has no children")
        if len(args) == 1:
            self.children[args[0]] = Node(val)
        else:
            self.children[args[0]].set(val, *args[1:])

    def delete(self, *args):
        if not args:
            raise Exception("You can't modify the root")
        if self.node_type == NodeTypes.OBJECT or self.node_type == NodeTypes.NONE:
            raise Exception("Non-iterable object has no children")
        if len(args) == 1:
            del self.children[args[0]]
        else:
            self.children[args[0]].delete(*args[1:])


class ObjectTree(object):
    root = None

    def __init__(self, val):
        self.root = Node(val)

    def get(self, *args):
        return self.root.get(*args)

    def set(self, val, *args):
        if not args:
            self.root = Node(val)
        else:
            self.root.set(val, *args)

    def delete(self, *args):
        if not args:
            self.root = None
        else:
            self.root.delete(*args)
