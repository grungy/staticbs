#!/usr/bin/env python
import numpy as np
from polygon import *
from probe_board import *

def vectorize_over_points(func):
    def vectorized_func(a, *args, **kwargs):
        r = array(tuple(func(p, *args, **kwargs) for p in a.reshape(-1, 3)))
        return r.reshape(a.shape[:-1] + r.shape[1:])
    return vectorized_func

def mag(vector):
    return sqrt(np.sum(square(vector), axis=-1))

class simulation_obj():
    def __init__(self, observation_points, amp_turns):
        """takes a probe board and a current object and combines them together"""
        self.vectorized_mag = vectorize_over_points(mag)
        self.E = vectorize_over_points(self.E_field_at_point)

        self.observation_points = observation_points

        # sea water velocity

        self.velocity = np.array([0.001 ,0, 0])  # m/s

        # create probe board
        self.probe_board = probe_board()

        # create coil
        self.coil_height = 71.374e-3  # meters
        # self.coil_height = 50.8e-3  # meters
        self.coil_horizontal_axis = 50.8e-3  # meters

        self.coil1 = Polygon(8, (0,0,-0.01), self.coil_height)
        self.coil2 = Polygon(8, (0,0,0), self.coil_height)

        self.padding = self.coil_height_chk()

        # center the points around the origin
        self.global_pad_locations = self.probe_board.pad_locations \
         - self.coil1.v_straight_length/2.0 + self.padding

        # create the current object
        self.amp_turns = amp_turns

        self.current_object = current_obj_list(self.coil1.get_segments() + self.coil2.get_segments())

        # calculate magnetic field at observation points
        self.B_obs = self.current_object.B(self.observation_points, self.amp_turns)

        self.E_obs = self.E(self.observation_points)

    def coil_height_chk(self):

    	padding = (self.coil1.v_straight_length - \
    	self.probe_board.pad_height) / 2.0

    	assert padding > 0.0  # make sure the loop is bigger than all of the pads
    	return padding

    def E_field_at_point(self, point):
        return np.cross(self.velocity, self.current_object.B(point, self.amp_turns))

    def E_integrand(self, t):
    	# print "t: ", t
    	# print "r(t): ", self.r(t)
    	# print self.E_field_at_point(self.r(t))
    	return np.dot( self.E_field_at_point(self.r(t)), self.r_prime(t) )

    def r(self, t):
    	a = self.global_pad_locations[0]
    	b = self.global_pad_locations[1]
    	return np.array([0, a + t*(b-a), 0])

    def r_prime(self, t):
    	a = self.global_pad_locations[0]
    	b = self.global_pad_locations[1]
    	return np.array([0, (b-a), 0])

    def save(self):
        np.save("../data/B.npy", self.B_obs)
        np.save("../data/E.npy", self.E_obs)
        np.save("../data/obs_points.npy", self.observation_points)

    def get_b_obs(self):
        return self.B_obs
