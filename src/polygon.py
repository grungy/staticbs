from pylab import *
from segment import *

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

class Polygon(loop):
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


        # print self.area(self.vertices)

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

    def plot_vertices(self):
        plt.scatter(self.vertices[:,0], self.vertices[:, 1])
        plt.show()

        print "test"


if __name__ == "__main__":

    test = Polygon(20, (0,0,0), 5)
    test.plot_vertices()
