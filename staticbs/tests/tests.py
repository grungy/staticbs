from unittest import TestCase

import staticbs as bs
import numpy as np
import scipy.constants as consts

class bstest(TestCase):

    def test_coil_center(self):
        observation_points = np.array([[[0,0,0]]])
        # current and amp turns definitions
        simulation_current = 10  # amps
        num_loops = 1000
        amp_turns = simulation_current * num_loops

        coil_radius = 0.1  # meters
        coil = bs.shapes.polygon(8, (0,0,0), coil_radius)
        current_object = bs.iobjs.current_obj_list(coil.get_segments() )

        B_obs = current_object.B(observation_points, amp_turns)
        calc_result = 0.6283185307179585
        diff = (bs.common.mag(B_obs) - calc_result)
        print diff
        self.assertTrue( diff/calc_result  <= 0.01 ) #  1% error acceptable

    def test_coil_axial_distance(self):
        # page 9-9 in MIT guide
        observation_points = np.array([[[0,0,5]]])
        # current and amp turns definitions
        simulation_current = 10  # amps
        num_loops = 1000
        amp_turns = simulation_current * num_loops

        coil_radius = 0.1  # meters
        coil = bs.shapes.polygon(8, (0,0,0), coil_radius)
        current_object = bs.iobjs.current_obj_list(coil.get_segments() )

        B_obs = current_object.B(observation_points, amp_turns)
        analytical_result = (consts.mu_0 * amp_turns * coil_radius**2) / \
            (2 * (coil_radius**2 + observation_points[0, 0, 2]))**(3/2)
        diff = (bs.common.mag(B_obs) - analytical_result)
        self.assertTrue( diff  <= 0.01 * analytical_result ) #  1% error acceptable

    def test_ampere(self):
        # compare with ampere's law
        radius = 0.05
        observation_points = np.array([[[0, radius, 0]]])
        # current and amp turns definitions
        simulation_current = 10  # amps
        num_loops = 1000
        amp_turns = simulation_current * num_loops

        start = np.array([0, 0, 0])
        end = np.array([0, 0, 0.1])
        line = bs.iobjs.straight_wire(start, end)
        current_object = bs.iobjs.current_obj_list( [line] )

        B_obs = current_object.B(observation_points, amp_turns)
        ampere_result = (consts.mu_0 * amp_turns ) / \
            (2 * np.pi * radius)
        diff = (bs.common.mag(B_obs) - ampere_result)
        self.assertTrue( diff  <= 0.01 * ampere_result ) #  1% error acceptable
