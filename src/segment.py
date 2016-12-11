#!/usr/bin/env python
from pylab import *
import scipy.constants as consts
import pprint
import copy
from mpl_toolkits.mplot3d import Axes3D


def vectorize_over_points(func):
    def vectorized_func(a, *args, **kwargs):
        r = array(tuple(func(p, *args, **kwargs) for p in a.reshape(-1, 3)))
        return r.reshape(a.shape[:-1] + r.shape[1:])
    return vectorized_func


class current_obj_list(list):
    def B(self, points, current):
        return np.sum((i.B(points, current) for i in self), axis=0)


class loop:
    """creates straight wire segments from points. It closes the loop if it is left open.
    Current flows in the order the points are given."""
    def __init__(self, I, points):
        self.vertices = points
        self.segments = self.create_segments(self.vertices)

    def create_segments(self, points):
        wire_list = []
        for i in range(0, len(points)):
            if (i+1) == len(points):
                wire_list.append(straight_wire(points[i], points[0]))

            else:
                wire_list.append(straight_wire(points[i], points[i+1]))

        return copy.deepcopy(wire_list)

    def get_segments(self):
        return copy.deepcopy(self.segments)

class octagon(loop):
    def __init__(self, h_straight_length_percent, v_straight_length_percent, vertical_axis, horizontal_axis, height):
        # height is the total height of the stack at the point where you start depositing the current layer
        # thickness later on is the height of the layer being currently deposited
        self.theta = 45 * pi/180  # radians
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


class straight_wire:

    def __init__(self, start, end):
        self.start = start  # xyz tuple
        self.end = end  # xyz tuple
        self.unit_vector = (end-start)/mag(end-start)
        self.B = vectorize_over_points(self.B_at_point)

    def perpendicular_vector(self, observation_point, start, end):
        # source point is origin
        bold_r = observation_point - start
        wire_vector = (start - end)
        wv_unit_v = wire_vector / mag( wire_vector )

        # in the direction of the unit vector
        r_prime = np.dot(bold_r, wv_unit_v)
        r_prime_vector = r_prime * wv_unit_v

        r = bold_r - r_prime_vector
        return r

    def magnetic_field_direction_at_point(self, observation_point):
        bold_r = observation_point - self.start
        # r_prime = dot(bold_r, self.unit_vector)
        # r_prime_vector = r_prime*self.unit_vector
        v = cross(bold_r, self.unit_vector)
        return v / mag(v)

    def B_at_point(self, observation_point, current):
        return self.magnetic_field_direction_at_point(observation_point) * \
            self.magnetic_field_magnitude_at_point(observation_point, current)

    def magnetic_field_magnitude_at_point(self, observation_point, current):
        """ current in amps, points in meters, returns Teslas
         current flows from start to end of wire"""
        start = self.start
        end = self.end

        r = self.perpendicular_vector(observation_point, start, end)

        r_mag = mag(r)

        unit_vector = (end - start) / mag( end - start)
        l1 = np.dot( (observation_point - start), unit_vector )
        l2 = np.dot( (observation_point- end), -1*unit_vector )
        
        cos_theta_1 = l1/sqrt(r_mag**2 + square(l1))
        cos_theta_2 = l2/sqrt(r_mag**2 + square(l2))

        B = (consts.mu_0/(4*consts.pi)) * \
            (current/r_mag)*(cos_theta_2 + cos_theta_1)


        return np.sqrt(B**2)

    def get_wire_points(self, num_samples):
        wire_points = make_3d_line(self.start, self.end, num_samples)
        return wire_points

class moving_conductor:

    def __init__(self, velocity):
        self.velocity = velocity
        self.E = vectorize_over_points(self.E_field_at_point)

    def E_field_at_point(self, B):
        return np.cross(self.velocity, B)

def mag(vector):
    return sqrt(np.sum(square(vector), axis=-1))
