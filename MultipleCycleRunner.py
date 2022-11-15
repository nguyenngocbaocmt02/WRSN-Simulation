import os

import docx
from Node import Node
import random
from Network import Network
import pandas as pd
from ast import literal_eval
from MobileCharger import MobileCharger
import csv
import Parameter as para


def getTextDocx(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return fullText


def getTextTxt(filename):
    tmp = open(filename)
    return tmp.readlines()


df = pd.read_csv("data/thaydoitileguitin.csv")
path = 'D:/lab/WRSN_Simulation-master/WRSN_Simulation-master/my_data/data'
path_result = 'D:/lab/WRSN_Simulation-master/WRSN_Simulation-master/my_data/simulate'
path_log = 'D:/lab/WRSN_Simulation-master/WRSN_Simulation-master/my_data/log'
max_time = 3000
for file_name in os.listdir(path):
    print(path + '/' + file_name)
    data = getTextTxt(path + '/' + file_name)
    chooser_alpha = open("log/q_learning_confident3.csv", "w")
    result = csv.DictWriter(chooser_alpha, fieldnames=["nb run", "lifetime"])
    result.writeheader()
    life_time = []
    for nb_run in range(1):
        random.seed(nb_run)
        node_pos = list(literal_eval(df.node_pos[0]))
        list_node = []
        i = 0
        for dataline in data[0:]:
            print(dataline)
            if dataline == "": break
            temp = tuple(map(float, dataline.split("\t")[:2]))
            location = list([temp[0], temp[1]])
            com_ran = 90
            energy = 10800.0
            energy_max = 10800.0
            prob = 0.3

            node = Node(location=location, com_ran=com_ran, energy=energy, energy_max=energy_max, id=i,
                        energy_thresh=0.4 * energy, prob=prob)
            list_node.append(node)
            i = i + 1
        mc = MobileCharger(energy=108000.0, capacity=108000.0, e_move=1.0,
                           e_self_charge=df.e_mc[0], velocity=5.0)
        target = []
        for i in range(len(list_node) + 1):
            target.append(i)
        net = Network(list_node=list_node, mc=mc, target=target)
        temp = net.simulate_only(optimizer=None, file_name=file_name, maxtime=max_time)

        q = (path_result + '/' + file_name).replace('docx', 'txt')
        q1 = (path_log + '/' + file_name).replace('docx', 'txt')
        out = open(q, 'w')
        out1 = open(q1, 'w')
        out.write(str(para.base[0]) + ' ' + str(para.base[1]) + '\n')
        count_disconnected = 0
        count_weak = 0
        for i in range(len(list_node)):
            list_node[i].avg_energy = (float)(list_node[i].energy_max - list_node[i].energy) / max_time
            if list_node[i].avg_energy > 0.8 or list_node[i].energy < 5000:
                list_node[i].avg_energy = 0.5 + 0.3 * random.random()
                list_node[i].energy = 7000 + random.random() * 1000
            if list_node[i].energy_max == list_node[i].energy:
                count_disconnected += 1
                continue
            if (list_node[i].energy - para.min_energy) / list_node[i].avg_energy < 72000:
                count_weak += 1

        for i in range(len(list_node)):
            if list_node[i].energy_max == list_node[i].energy:
                list_node[i].energy = 7500 + random.random() * 1500
                list_node[i].avg_energy = 0.01 + 0.69 * random.random()
                if (list_node[i].energy - para.min_energy) / list_node[i].avg_energy < 72000:
                    count_weak += 1

        for i in range(len(list_node)):
            out.write(str(list_node[i].location[0]) + ' ' + str(list_node[i].location[1]) + ' ' + str(
                "{:.4f}".format(list_node[i].avg_energy)) + ' ' + str("{:.4f}".format(list_node[i].energy)) + '\n')
        out1.write("The number of disconnected node: " + str(count_disconnected) + '\n')
        out1.write("The number of risky node: " + str(count_weak) + '\n')
        out1.close()
        out.close()
