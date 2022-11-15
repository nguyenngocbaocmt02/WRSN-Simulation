from scipy.spatial import distance
import numpy as np
import Parameter as para
import math


class Inma:
    def __init__(self):
        self.x = 0

    def update(self, network=None):
        request_list = network.mc.list_request
        if not len(request_list):
            return network.mc.current, 0
        id_list = np.asarray([request["id"] for request in request_list])
        t = [(network.node[request["id"]].energy / request["avg_energy"]) for request in request_list]
        time_move = np.asarray([distance.euclidean(network.mc.current, network.node[request["id"]].location) / network.mc.velocity
                     for request in request_list])
        p = para.alpha / para.beta ** 2
        time_charge = np.asarray([
            (network.node[request["id"]].energy_max - network.node[request["id"]].energy) / (p - request["avg_energy"])
            for request in request_list])
        x = time_move + time_charge
        arg_min = np.argmin(x)
        next_location = network.node[id_list[arg_min]].location
        print(next_location, t[arg_min])
        return next_location, t[arg_min]
