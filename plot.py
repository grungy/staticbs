#!/usr/bin/env python
from pylab import *
from mpl_toolkits.mplot3d import axes3d

def mag(vector):
	return sqrt(np.sum(square(vector), axis=-1))

def plot_linearity(B_fn, obs_points_fn="../data/obs_points_linearity.npy"):
	obs_points = np.load(obs_points_fn)
	B = np.load(B_fn)

	x = obs_points[:, 0]
	y = obs_points[:, 1]
	z = obs_points[:, 2]

	plt.subplot(2, 1, 1)
	plt.title('B field as a function of the X position')
	plt.xlabel('x position when y = 0')
	plt.plot(x[0:x.shape[0]/2], B[0:x.shape[0]/2, 0], '.')

	plt.subplot(2,1,2)
	plt.title('B field as a function of the y position')
	plt.xlabel('y position when x = 0')
	plt.plot(y[y.shape[0]/2:-1], B[y.shape[0]/2:-1, 1], '.')

	# ax4.scatter(x, y)

	# ax4.quiver(x, y,
	#        B[:, 0],
	#        B[:, 1], color='blue')

def plot_3D(B_fn, obs_points_fn="../data/obs_points.npy"):
	obs_points = np.load(obs_points_fn)
	B = np.load(B_fn)

	xx = obs_points[:, :, 0]
	yy = obs_points[:, :, 1]
	zz = obs_points[:, :, 2]

	fig3 = plt.figure()
	ax3 = fig3.gca(projection='3d')

	ax3.quiver(xx[::4, ::4], yy[::4, ::4], zz[::4, ::4],
	       B[::4, ::4, 0]/float(np.amax(B[::4, ::4, 0])),
	       B[::4, ::4, 1]/float(np.amax(B[::4, ::4, 1])),
		   B[::4, ::4, 2]/float(np.amax(B[::4, ::4, 2])), color='blue', length=0.0001)

def plot_B(B_fn, obs_points_fn="../data/obs_points.npy"):
	obs_points = np.load(obs_points_fn)
	B = np.load(B_fn)

	xx = obs_points[:, :, 0]
	yy = obs_points[:, :, 1]
	zz = obs_points[:, :, 2]

	x = xx[0, :]
	y = yy[:, 0].T

	fig1 = plt.figure()
	ax1 = fig1.gca()
	title_txt = 'XY View of the Octagon B Field'
	ax1.set_title(title_txt)
	ax1.CS = contourf(x, y, mag(B))
	ax1.quiver(xx[::4, ::4], yy[::4, ::4],
	       B[::4, ::4, 0],
	       B[::4, ::4, 1], color='white')
	plt.colorbar(ax1.CS)

def plot_E(E_fn, obs_points_fn="../data/obs_points.npy"):
	obs_points = np.load(obs_points_fn)
	E = np.load(E_fn)

	xx = obs_points[:, :, 0]
	yy = obs_points[:, :, 1]
	zz = obs_points[:, :, 2]

	x = xx[0, :]
	y = yy[:, 0].T

	fig2 = plt.figure()
	ax2 = fig2.gca()
	title_txt2 = 'XY View of the Octagon E Field'
	ax2.set_title(title_txt2)
	ax2.CS = contourf(x, y, mag(E))
	ax2.quiver(xx[::4, ::4], yy[::4, ::4],
	       E[::4, ::4, 0],
	       E[::4, ::4, 1], color='white')
	plt.colorbar(ax2.CS)

if __name__ == '__main__':

	# plot_B(sys.argv[1])
	# plot_E(sys.argv[2])
	# plot_3D(sys.argv[1])
	plot_linearity(sys.argv[1])

	plt.show()
