
class Port:
    def __init__(self, name, ip_address=None, mac_address=None, floating_ip=None):
        self.name = None
        self.set_name(name)
        self.id = None
        self.template_name = name
        self.ip_address = ip_address
        self.mac_address = mac_address  # not set
        self.floating_ip = floating_ip
        self.net_name = None

    def set_name(self, name):
        self.name = name
        split_name = name.split(':')
        if len(split_name) >= 3:
            if split_name[2] == 'input' or split_name[2] == 'in':
                self.intf_name = split_name[0][:4] + '-' + \
                                 split_name[1][:4] + '-' + \
                                 'in'
            elif split_name[2] == 'output' or split_name[2] == 'out':
                self.intf_name = split_name[0][:4] + '-' + \
                                 split_name[1][:4] + '-' + \
                                 'out'
            else:
                self.intf_name = split_name[0][:4] + '-' + \
                                 split_name[1][:4] + '-' + \
                                 split_name[2][:4]
        else:
            self.intf_name = name

    def get_short_id(self):
        return str(self.id)[:6]

    def __eq__(self, other):
        if other is None:
            return False

        if self.name == other.name and self.ip_address == other.ip_address and \
                                       self.mac_address == other.mac_address and \
                                       self.floating_ip == other.floating_ip and \
                                       self.net_name == other.net_name:
            return True
        return False

    def __hash__(self):
        return hash((self.name,
                     self.ip_address,
                     self.mac_address,
                     self.floating_ip,
                     self.net_name))
