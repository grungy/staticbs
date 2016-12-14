#!/usr/bin/env python
from pylab import *
import scipy.integrate as integrate
import staticbs as bs
import sys

def save(data_dir='./data/', **kwargs):
    for fn in kwargs:
        print fn, kwargs[fn]
        np.save(data_dir + fn, kwargs[fn])

# def save(self, data_dir='../data/', obs_points_fn="obs_points.npy", B_fn="B.npy", E_fn="E.npy"):
#     np.save(data_dir + B_fn, self.B_obs)
#     np.save(data_dir + E_fn, self.E_obs)
#     np.save(data_dir + obs_points_fn, self.observation_points)

# print dir(static_bs_module)

# observation grid setup

# grid units are in meters
x = linspace(-0.1, 0.1, 100)
y = linspace(-0.1, 0.1, 100)
# z = linspace(-0.2, 0.2, 100)

## Example for how to ignore the z axis
z = zeros((x.shape[0])) + 1e-2
zz = zeros(x.shape + y.shape) + 1e-2

xx, yy = meshgrid(x, y)

# observation_points = rollaxis(np.array((xx, yy, zz)), 0, xx.ndim + 1)
observation_points = np.array([[[0,0,0]]])

# current and amp turns definitions

simulation_current = 10  # amps
num_loops = 1000

amp_turns = simulation_current * num_loops

# OPTIONAL water / charged particle velocity for e field calculation
velocity = np.array([0.001 ,0, 0])  # m/s

# create coil
coil_radius = 0.1  # meters
coil = bs.shapes.polygon(8, (0,0,0), coil_radius)

# make a list of all of the current segments
current_object = bs.iobjs.current_obj_list(coil.get_segments() )

#make e field object
e_field = bs.eobjs.e_field(amp_turns, current_object, velocity)

# calculate magnetic field at observation points
print "calculating B field"
B_obs = current_object.B(observation_points, amp_turns)

print "calculating E field"
E_obs = e_field.E(observation_points)


# E field line integral
# result = integrate.quad(sim_obj.E_integrand, 0, 1, args=(0, 1))
# print result

save(B_test=B_obs, E_test = E_obs, obs_points = observation_points)
