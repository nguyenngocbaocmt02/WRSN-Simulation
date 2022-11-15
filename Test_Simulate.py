import pygame
import Parameter
from Node import Node
from Network import Network
from MobileCharger import MobileCharger
from scipy.spatial import distance
from MyNode import MyNode
from Graphic import Graphic

file = open('D:\lab\WRSN_Simulation-master\WRSN_Simulation-master\my_data\simulate\10.txt', 'r')
data = file.readlines()
list_node = []
i = 0
for dataline in data[1:]:
    if dataline == "": break
    temp = tuple(map(float, dataline.split('\t')[:4]))
    location = list([temp[0], temp[1]])
    com_ran = 160
    energy = temp[2]
    energy_max = 10800.0
    avg_energy = temp[3] * 5
    prob = 0.3
    node = MyNode(location=location, com_ran=com_ran, energy=energy, energy_max=energy_max, id=i,
                  energy_thresh=0.4 * energy, prob=prob, avg_energy=avg_energy)
    list_node.append(node)
    i = i + 1
mc = MobileCharger(energy=108000.0, capacity=108000.0, e_move=1.0,
                   e_self_charge=2, velocity=5.0)
target = []
time = []
path = []
for i in range(len(list_node) + 1):
    target.append(i)
for i in range(len(list_node)):
    time.append(200)
    path.append(list_node[i].location)
net = Network(list_node=list_node, mc=mc, target=target)

graphic = Graphic(network=net, path=path, time=time)
graphic.play()
