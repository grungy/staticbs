#!/usr/bin/env python
from pylab import *
from mpl_toolkits.mplot3d import axes3d

def mag(vector):
	return sqrt(np.sum(square(vector), axis=-1))

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

	plot_B(sys.argv[1])
	plot_E(sys.argv[2])
	# plot_3D(sys.argv[1])

	plt.show()
