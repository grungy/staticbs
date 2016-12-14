import numpy as np
from iobjs import *

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

class polygon(loop):
    def __init__(self, n_sides, center, radius):
        self.n_sides = n_sides
        self.center = np.array(center)
        self.radius = radius  # circumradius -- goes to a vertex points
        self.v_straight_length = radius * 2.0

        self.phi = (360.0 / self.n_sides) * (np.pi / 180)

        self.prime_vector = np.matrix([self.center + np.array([0, self.radius, 0])])

        theta = self.phi

        self.rot_matrix_arr = [np.matrix([[np.cos(theta), -np.sin(theta), 0],\
                                [np.sin(theta), np.cos(theta), 0],
                                [0, 0, 1]]) for theta in -np.arange(0, 2*np.pi, theta)]
        self.vertices = np.array(self.rot_matrix_arr * self.prime_vector.T)

        self.segments = self.create_segments(self.vertices)

    def area(self, vertices):
        x = vertices[:, 0]
        y = vertices[:, 1]

        area = 0.0
        num_points = len(x)
        j = num_points - 1

        for i in range(0, num_points):
            area = area +  (x[j] + x[i]) * (y[j] - y[i])
            j = i

        return area / 2.0


class octagon(loop):
    def __init__(self, h_straight_length_percent, v_straight_length_percent, vertical_axis, horizontal_axis, height):
        # height is the total height of the stack at the point where you start depositing the current layer
        # thickness later on is the height of the layer being currently deposited
        self.theta = 45 * np.pi/180  # radians
        self.h_straight_length_percent = h_straight_length_percent
        self.v_straight_length_percent = v_straight_length_percent
        self.horizontal_axis = horizontal_axis
        self.vertical_axis = vertical_axis
        self.height = height

        self.h_straight_length = self.horizontal_axis * self.h_straight_length_percent
        self.v_straight_length = self.vertical_axis * self.v_straight_length_percent

        # print "h_straight_length: ", self.h_straight_length
        # print "v_straight_length: ", self.v_straight_length

        self.vertices = self.calculate_vertices()
        # print self.vertices
        # print self.area(self.vertices)
        #
        # fig, ax = plt.subplots()
        # plt.scatter(self.vertices[:,0], self.vertices[:,1])
        # circle = plt.Circle((0,0), 0.1,fill=False)
        # ax.add_artist(circle)
        # plt.show()

        self.segments = self.create_segments(self.vertices)

    def area(self, vertices):
        x = vertices[:, 0]
        y = vertices[:, 1]

        area = 0.0
        num_points = len(x)
        j = num_points - 1

        for i in range(0, num_points):
            area = area +  (x[j] + x[i]) * (y[j] - y[i])
            j = i

        return area / 2.0
    def calculate_vertices(self):

        center = (0, 0, self.height)
        x = center[0]
        y = center[1]
        z = center[2]

        v1 = (x - self.h_straight_length/2.0, y - self.vertical_axis / 2.0, z)
        v2 = (x - self.horizontal_axis / 2.0, y - self.v_straight_length / 2.0, z)
        v3 = (x - self.horizontal_axis / 2.0, y + self.v_straight_length / 2.0, z)
        v4 = (x - self.h_straight_length / 2.0, y + self.vertical_axis / 2.0, z)
        v5 = (x + self.h_straight_length / 2.0, y + self.vertical_axis / 2.0, z)
        v6 = (x + self.horizontal_axis / 2.0, y + self.v_straight_length / 2.0, z)
        v7 = (x + self.horizontal_axis / 2.0, y - self.v_straight_length / 2.0, z)
        v8 = (x + self.h_straight_length / 2.0, y - self.vertical_axis / 2.0, z)

        vertices = np.array([v1, v2, v3, v4, v5, v6, v7, v8])
        # print "vertices: ", vertices
        return vertices
