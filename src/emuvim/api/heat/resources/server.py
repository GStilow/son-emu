
class Server:
    def __init__(self,name, id=None, flavor=None, image=None, command=None, nw_list=None):
        self.name = name
        self.id = id          # not set
        self.flavor = flavor
        self.image = image
        self.command = command
        self.ports = list()
