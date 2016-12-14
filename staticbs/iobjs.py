#!/usr/bin/env python
from common import *
import numpy as np
import scipy.constants as consts
import pprint
import copy

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
        v = np.cross(bold_r, self.unit_vector)
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

        cos_theta_1 = l1/np.sqrt(r_mag**2 + np.square(l1))
        cos_theta_2 = l2/np.sqrt(r_mag**2 + np.square(l2))

        B = (consts.mu_0/(4*consts.pi)) * \
            (current/r_mag)*(cos_theta_2 + cos_theta_1)


        return np.sqrt(B**2)

    def get_wire_points(self, num_samples):
        wire_points = make_3d_line(self.start, self.end, num_samples)
        return wire_points
