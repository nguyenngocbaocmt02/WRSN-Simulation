import pygame
import Parameter
from Node import Node
from Network import Network
from MobileCharger import MobileCharger
from scipy.spatial import distance


class MyNode(Node, pygame.sprite.Sprite):
    def __init__(self, location=None, com_ran=None, sen_ran=None, energy=None, prob=Parameter.prob, avg_energy=0.0,
                 len_cp=100, id=None, is_active=True, energy_max=None, energy_thresh=None, axis=None,
                 log_e=[]):
        super().__init__(location, com_ran, sen_ran, energy, prob, avg_energy, len_cp, id, is_active, energy_max,
                         energy_thresh)
        self.log_e = []
        self.original_image = pygame.image.load('image/sensor.png')
        self.charged_image = pygame.image.load('image/charged_sensor.png')
        self.health = energy
        self.axis = axis
        self.log_e.append(self.energy)

    def draw_health(self, surf, state):
        self.rect = self.original_image.get_rect(center=self.axis)
        health_rect = pygame.Rect(0, 0, self.original_image.get_width(), 5)
        health_rect.midbottom = self.rect.centerx + 16, self.rect.top + 58.5
        max_health = 10800
        self.draw_health_bar(surf, health_rect.topleft, health_rect.size,
                             (192, 192, 192), (255, 255, 255), self.log_e[state] / max_health)

    def draw_health_bar(self, surf, pos, size, borderC, backC, progress):
        pygame.draw.rect(surf, backC, (*pos, *size))
        pygame.draw.rect(surf, borderC, (*pos, *size), 1)
        innerPos = (pos[0] + 1, pos[1] + 1)
        innerSize = ((size[0] - 2) * progress, size[1] - 2)
        rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
        if progress > 0.67:
            pygame.draw.rect(surf, (0, 255, 0), rect)
        elif progress > 0.33:
            pygame.draw.rect(surf, (255, 255, 102), rect)
        else:
            pygame.draw.rect(surf, (255, 0, 0), rect)