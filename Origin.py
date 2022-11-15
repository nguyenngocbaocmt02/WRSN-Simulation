from Node import Node
import random
from Network import Network
import pandas as pd
from ast import literal_eval
from MobileCharger import MobileCharger
from Q__Learning import Q_learning
from Inma import Inma
import csv
from scipy.stats import sem, t
from scipy import mean


df = pd.read_csv("data/thaydoitileguitin.csv")
file=
for index in range(1):
    chooser_alpha = open("log/q_learning_confident3.csv", "w")
    result = csv.DictWriter(chooser_alpha, fieldnames=["nb run", "lifetime"])
    result.writeheader()
    life_time = []
    for nb_run in range(1):
        random.seed(nb_run)

        node_pos = list(literal_eval(df.node_pos[index]))
        list_node = []
        for i in range(len(node_pos)):
            location = node_pos[i]
            com_ran = df.commRange[index]
            energy = df.energy[index]
            energy_max = df.energy[index]
            prob = df.freq[index]
            node = Node(location=location, com_ran=com_ran, energy=energy, energy_max=energy_max, id=i,
                        energy_thresh=0.4 * energy, prob=prob)
            list_node.append(node)
        mc = MobileCharger(energy=df.E_mc[index], capacity=df.E_max[index], e_move=df.e_move[index],
                           e_self_charge=df.e_mc[index], velocity=df.velocity[index])
        target = [int(item) for item in df.target[index].split(',')]
        net = Network(list_node=list_node, mc=mc, target=target)
        print(len(net.node), len(net.target), max(net.target))
        q_learning = Q_learning(network=net)
        # inma = Inma()
        file_name = "log/q_learning_" + str(index) + ".csv"
       # temp = net.simulate(optimizer=q_learning, file_name=file_name)
        temp = net.simulate(optimizer=None, file_name=file_name)
        life_time.append(temp)
        result.writerow({"nb run": nb_run, "lifetime": temp})

    confidence = 0.95
    h = sem(life_time) * t.ppf((1 + confidence) / 2, len(life_time) - 1)
    result.writerow({"nb run": mean(life_time), "lifetime": h})
