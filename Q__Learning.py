import numpy as np
from scipy.spatial import distance

from Node_Method import find_receiver
from Q_learning_method import init_function, action_function, q_max_function, reward_function


class Q_learning:
    def __init__(self, init_func=init_function, nb_action=81, action_func=action_function, network=None):
        self.action_list = action_func(nb_action=nb_action)
        self.q_table = init_func(nb_action=nb_action)
        self.state = nb_action
        self.charging_time = [0.0 for _ in self.action_list]
        self.reward = np.asarray([0.0 for _ in self.action_list])
        self.reward_max = [0.0 for _ in self.action_list]

    def update(self, network, alpha=0.5, gamma=0.5, q_max_func=q_max_function, reward_func=reward_function):
        if not len(network.mc.list_request):
            return self.action_list[self.state], 0.0
        self.set_reward(reward_func=reward_func, network=network)
        self.q_table[self.state] = (1 - alpha) * self.q_table[self.state] + alpha * (
                self.reward + gamma * self.q_max(q_max_func))
        self.choose_next_state(network)
        if self.state == len(self.action_list) - 1:
            charging_time = (network.mc.capacity - network.mc.energy) / network.mc.e_self_charge
        else:
            charging_time = self.charging_time[self.state]
        print("next state =", self.action_list[self.state], self.state, charging_time)
        # print(self.charging_time)
        return self.action_list[self.state], charging_time

    def q_max(self, q_max_func=q_max_function):
        return q_max_func(q_table=self.q_table, state=self.state)

    def set_reward(self, reward_func=reward_function, network=None):
        first = np.asarray([0.0 for _ in self.action_list], dtype=float)
        second = np.asarray([0.0 for _ in self.action_list], dtype=float)
        third = np.asarray([0.0 for _ in self.action_list], dtype=float)
        for index, row in enumerate(self.q_table):
            temp = reward_func(network=network, q_learning=self, state=index, receive_func=find_receiver)
            first[index] = temp[0]
            second[index] = temp[1]
            third[index] = temp[2]
            self.charging_time[index] = temp[3]
        first = first / np.sum(first)
        second = second / np.sum(second)
        third = third / np.sum(third)
        self.reward = first + second + third
        self.reward_max = list(zip(first, second, third))

    def choose_next_state(self, network):
        # next_state = np.argmax(self.q_table[self.state])
        if network.mc.energy < 10:
            self.state = len(self.q_table) - 1
        else:
            self.state = np.argmax(self.q_table[self.state])
            # print(self.reward_max[self.state])
            # print(self.action_list[self.state])
