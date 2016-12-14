from common import *

class e_field():
    def __init__(self, amp_turns, current_object, velocity):
        """calculates the e field given a current object"""
        self.vectorized_mag = vectorize_over_points(mag)
        self.E = vectorize_over_points(self.E_field_at_point)
        self.amp_turns = amp_turns
        self.current_object = current_object
        self.velocity = velocity

    def E_field_at_point(self, point):
        return np.cross(self.velocity, self.current_object.B(point, self.amp_turns))

    def E_integrand(self, t, a, b):
    	return np.dot( self.E_field_at_point(self.r(t, a, b)), self.r_prime(t, a, b) )

    def r(self, t, a, b):
    	return np.array([0, a + t*(b-a), 0])

    def r_prime(self, t, a, b):
    	return np.array([0, (b-a), 0])
