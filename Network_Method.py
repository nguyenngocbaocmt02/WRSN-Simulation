import random
from Package import Package


def uniform_com_func(net):
    for node in net.node:
        if node.id in net.target and random.random() <= node.prob and node.is_active:
            package = Package()
            node.send(net, package)
            # print(package.path)
    return True


def to_string(net):
    min_energy = 10 ** 10
    min_node = -1
    for node in net.node:
        if node.energy < min_energy:
            min_energy = node.energy
            min_node = node
    min_node.print_node()


def count_package_function(net):
    count = 0
    for target_id in net.target:
        package = Package(is_energy_info=True)
        net.node[target_id].send(net, package)
        if package.path[-1] == -1:
            count += 1
    return count
