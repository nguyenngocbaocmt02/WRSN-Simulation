import Parameter as para


class Package:
    def __init__(self, is_energy_info=False):
        self.path = []
        self.is_energy_info = is_energy_info
        self.size = self.get_size()
        self.is_success = False

    def get_size(self):
        return para.b if not self.is_energy_info else para.b_energy

    def update_path(self, node_id):
        self.path.append(node_id)
