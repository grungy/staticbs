#!/usr/bin/env python
from pylab import *
import scipy.integrate as integrate
from simulation_obj_polygon import *

# observation grid setup

# grid units are in meters
x = linspace(-0.1, 0.1, 100)
y = linspace(-0.1, 0.1, 100)
# z = linspace(-0.2, 0.2, 100)

## Example for how to ignore the z axis
z = zeros((100)) + 1e-2
zz = zeros(x.shape + y.shape) + 1e-2

xx, yy = meshgrid(x, y)

observation_points = rollaxis(np.array((xx, yy, zz)), 0, xx.ndim + 1)
# observation_points = np.array([[[0,0,0]]])

# current and amp turns definitions

simulation_current = 10  # amps
num_loops = 1000

amp_turns_sim = simulation_current * num_loops

# construct simulation objects
sim_obj = simulation_obj(observation_points, amp_turns_sim)

# E field line integral
# result = integrate.quad(sim_obj.E_integrand, 0, 1, args=(0, 1))
# print result

print sim_obj.get_b_obs()

sim_obj.save()
