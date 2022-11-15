import pygame
import Parameter
from scipy.spatial import distance


class Graphic:
    def __init__(self, path=None, time=None, network=None, display_width=1000, display_height=600,
                 base_x=Parameter.base[0], base_y=Parameter.base[1], network_width=2 * Parameter.base[0],
                 network_height=2 * Parameter.base[1], U=5):
        self.U = U
        self.path = path
        self.time = time
        self.axis_path = []
        self.network = network
        self.display_width = display_width
        self.display_height = display_height
        self.base = list([base_x, base_y])
        self.base_axis = list([base_x, base_y])

        self.initFrame(network_width, network_height)
        self.initScript()

    def initScript(self):

        # Cai dat kich ban

        t = distance.euclidean(self.path[0], self.base) / self.network.mc.velocity + self.time[0]
        for node in self.network.node:
            if node.location[0] == self.path[0][0] and node.location[1] == self.path[0][1]:
                if node.log_e[-1] - (t - self.time[0]) * node.avg_energy <= Parameter.min_energy:
                    node.log_e.append(Parameter.min_energy)
                    continue
                node.log_e.append(min(node.log_e[-1] + self.time[0] * self.U - t * node.avg_energy, node.energy_max))
            else:
                node.log_e.append(max(Parameter.min_energy, node.log_e[-1] - t * node.avg_energy))
        for i in range(1, len(self.path)):
            for node in self.network.node:
                t = distance.euclidean(self.path[i - 1], self.path[i]) / self.network.mc.velocity + self.time[i]
                if node.location[0] == self.path[i][0] and node.location[1] == self.path[i][1]:
                    if node.log_e[-1] - (t - self.time[i]) * node.avg_energy <= Parameter.min_energy:
                        node.log_e.append(Parameter.min_energy)
                        continue
                    node.log_e.append(
                        min(node.log_e[-1] + self.time[i] * self.U - t * node.avg_energy, node.energy_max))
                else:
                    node.log_e.append(max(Parameter.min_energy, node.log_e[-1] - t * node.avg_energy))
        t = distance.euclidean(self.path[-1], self.base) / self.network.mc.velocity
        for node in self.network.node:
            node.log_e.append(max(node.log_e[-1] - t * node.avg_energy, Parameter.min_energy))

    def initFrame(self, network_width, network_height):

        # Chuyen doi toa do
        # Thiet lap cua so game

        pygame.init()
        width = self.display_width + 45
        height = self.display_height + 45
        self.screen = pygame.display.set_mode([width, height], pygame.HWSURFACE | pygame.DOUBLEBUF)
        minx = network_width
        miny = network_width
        maxx = 0
        maxy = 0
        for node in self.network.node:
            if node.location[0] < minx:
                minx = node.location[0]
            if node.location[0] > maxx:
                maxx = node.location[0]
            if node.location[1] < miny:
                miny = node.location[1]
            if node.location[1] > maxy:
                maxy = node.location[1]
        self.base_axis[0] = self.base[0] - minx + 5
        self.base_axis[1] = self.base[1] - miny + 5
        for node in self.network.node:
            node.axis = list([node.location[0] - minx + 5, node.location[1] - miny + 5])

        scale_width = self.display_width / (maxx - minx + 5)
        scale_height = self.display_height / (maxy - miny + 5)
        self.base_axis[0] *= scale_width
        self.base_axis[1] *= scale_height
        for node in self.network.node:
            node.axis = list([node.axis[0] * scale_width, node.axis[1] * scale_height])
        self.axis_path.append(self.base_axis)
        for pos in self.path:
            for node in self.network.node:
                if node.location[0] == pos[0] and node.location[1] == pos[1]:
                    self.axis_path.append(node.axis)
        self.axis_path.append(self.base_axis)
        pygame.display.set_caption("Network simulation")
        icon = pygame.image.load('image/sensor.png')
        pygame.display.set_icon(icon)

    def play(self):

        COLOUR = (255, 255, 255)
        fpsClock = pygame.time.Clock()
        # load image
        sensorImage = self.network.node[0].original_image
        chargedSensorImage = self.network.node[0].charged_image
        baseImage = pygame.image.load('image/station.png')
        mcImage = pygame.image.load('image/mc.png')
        baseCo = self.base_axis

        # game loop
        running = True
        state = 0
        moving = False
        vector_x = 0
        vector_y = 0
        current_x = 0
        current_y = 0
        FPS = 60
        while running:

            self.screen.fill(COLOUR)

            # Ve basestation

            self.screen.blit(baseImage, baseCo)

            # Ve MC
            if not moving:
                if state == len(self.axis_path) - 1 or state == 0:
                    self.screen.blit(mcImage, [baseCo[0] + 40, baseCo[1] + 40])
                else:
                    self.screen.blit(mcImage, [self.axis_path[state][0] + 20, self.axis_path[state][1] + 20])
            else:
                current_x += vector_x
                current_y += vector_y
                print(current_x, self.axis_path[state + 1][0],current_y, self.axis_path[state + 1][1])

                if (abs(current_x - self.axis_path[state + 1][0]) <= 1 and abs(
                        current_y - self.axis_path[state + 1][1]) <= 1):

                    moving = False
                    state += 1
                    print(state)
                    continue
                else:
                    self.screen.blit(mcImage, [current_x + 20, current_y + 20])
            # Ve cac sensor

            for i in range(len(self.network.node)):
                x = self.network.node[i].axis[0]
                y = self.network.node[i].axis[1]
                if self.axis_path[state][0] == x and self.axis_path[state][1] == y:
                    self.screen.blit(chargedSensorImage, [x, y])
                else:
                    self.screen.blit(sensorImage, [x, y])
                self.network.node[i].draw_health(self.screen, state)

            # Xu li su kien

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if state < len(self.network.node[0].log_e) - 1:
                        moving = True
                        vector_x = 2*(self.axis_path[state + 1][0] - self.axis_path[state][0])/60
                        vector_y = 2*(self.axis_path[state + 1][1] - self.axis_path[state][1]) / 60
                        current_x = self.axis_path[state][0]
                        current_y = self.axis_path[state][1]

            pygame.display.update()
            fpsClock.tick(FPS)

        pygame.quit()
