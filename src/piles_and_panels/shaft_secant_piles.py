import os
import numpy as np
from scipy.linalg import norm
from collections import OrderedDict
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle

# Methods for secant piled shaft
def get_parameters_shaft_secant_piles(ri, n_pieces, D, L, H_drilling_platform, v=0.75, shaft_name='Shaft', print_results=True):
    """ Gets parameters for secant piles
    ri: inner shaft radius
    n_pieces: numer of piles
    D: pile diameter
    L: pile length
    v: percentage of verticality
    H_drilling_platform: height of drilling platform above top of piles
    """
    if print_results:
        print('INPUT GEOMETRY {0}...'.format(shaft_name))
        print('Inner diameter of shaft 2*ri = {:.2f} m'.format(2*ri))
        print('Numer of piles n_pieces = {}'.format(n_pieces))
        print('Pile diameter = {:.2f} m'.format(D))
        print('Pile length = {:.2f} m'.format(L))
        print('Drilling verticality = {:.2f}%'.format(v))

    a = np.pi*(2*ri + D)/n_pieces # c/c spacing between 2 neighboring piles at shaft's center line
    x0 = H_drilling_platform*v/100  # deviation at top of pile when drilling platform is above, m
    t_top = D - a - 2*x0 # overcut/ interlock
    d_top = 2*np.sqrt((D/2)**2 - (a/2)**2) # overlapped thickness
    x = x0 + L*v/100 # deviation at bottom of shaft, m
    
    if print_results:   
        print('\nOUTPUT GEOMETRY {0}...'.format(shaft_name))
        print('C/c spacing at top of shaft a = {:.2f} m'.format(a))
        print('Overcut at top of shaft t = {:.2f} cm'.format(t_top*100))
        print('Effective thickness at top of shaft d = {:.2f} cm'.format(d_top*100))
        print('Deviation at bottom of shaft dx = {:.2f} cm'.format(x*100))
    
    t_eff = t_top - 2*x # effective/overlapped thickness at toe of shaft, m
    if t_eff > 0:
        d_eff = 2*np.sqrt((D/2)*t_eff - (t_eff/2)**2) # overlapped thickness, m    
        if print_results:
            print('Overcut at bottom of shaft t_eff = {:.2f} cm'.format(t_eff*100))
            print('Effective thickness at bottom of shaft d_eff = {:.2f} cm'.format(d_eff*100))
    else:
        d_eff = np.nan
        if print_results:
            print('PILES DO NOT TOUCH IN BASE OF SHAFT!!')

    return a, t_top, d_top, x0, x, t_eff, d_eff


def plot_shaft(ri, n_pieces, D, dev_0=0.0, dev=0.0, shaft_name='Shaft'):
    angles = np.linspace(0, 2*np.pi-2*np.pi/n_pieces, n_pieces)
    r = ri + D/2
    
    x = r * np.cos(angles)
    y = r * np.sin(angles)
        
    pile_types = ['primary', 'secondary']
    #pile_colors = ['blue', 'red']
    pile_colors = ['white', 'white']
    fig, ax = plt.subplots(1, 2)
    
    # deviations
    #angles_deviation = 2*np.pi*np.random.rand(angles.size) # random angle of deviation for each of the piles
    angles_deviation = 2*np.pi*np.random.uniform(0, 1, angles.size) # random angle of deviation for each of the piles
    x0 = x + dev_0*np.cos(angles_deviation) # x top
    y0 = y + dev_0*np.sin(angles_deviation) # y top
    x = x + dev*np.cos(angles_deviation)    # x bottom
    y = y + dev*np.sin(angles_deviation)    # y bottom

    # top of shaft
    for i in range(0,len(angles),2):
        circle_p = plt.Circle((x0[i],y0[i]), D/2, facecolor=pile_colors[0], edgecolor='black', zorder=0, alpha=0.3, label=pile_types[0])
        ax[0].add_patch(circle_p)       
    for i in range(1, len(angles), 2):
        circle_s = plt.Circle((x0[i],y0[i]), D/2, facecolor=pile_colors[1], edgecolor='black', zorder=0, alpha=0.3, linewidth=2.0, label=pile_types[1])
        ax[0].add_patch(circle_s)
    
    # bottom of shaft
    for i in range(0,len(angles),2):
        circle_p = plt.Circle((x[i],y[i]), D/2, facecolor=pile_colors[0], edgecolor='black', zorder=0, alpha=0.3, label=pile_types[0])
        ax[1].add_patch(circle_p)       
    for i in range(1, len(angles), 2):
        circle_s = plt.Circle((x[i],y[i]), D/2, facecolor=pile_colors[1], edgecolor='black', zorder=0, alpha=0.3, linewidth=2.0, label=pile_types[1])
        ax[1].add_patch(circle_s)

    ax[0].set_title(shaft_name + ' at top', fontsize=8)
    ax[1].set_title(shaft_name + ' at base (deviation {0:.1f} cm)'.format(dev*100), fontsize=8)
    ax[0].tick_params(axis='both', which='major', labelsize=8)
    ax[1].tick_params(axis='both', which='major', labelsize=8)
    for axi in ax:
        axi.autoscale_view()
        axi.set_aspect('equal')
        #ax.legend()
        #handles, labels = plt.gca().get_legend_handles_labels()
        #by_label = OrderedDict(zip(labels, handles))
        #plt.legend(by_label.values(), by_label.keys())
    #plt.show()
    return fig


# Plot shaft 3D
def data_for_cylinder_2_points(p0, p1, R):
    """ Gets grid data for cylinder
    """
    v = p1 - p0
    mag = norm(v)
    v = v/mag # unit vector
    
    #make some vector not in the same direction as v
    not_v = np.array([1, 0, 0])
    if (v == not_v).all():
        not_v = np.array([0, 1, 0])
    #make vector perpendicular to v
    n1 = np.cross(v, not_v)
    #normalize n1
    n1 /= norm(n1)
    #make unit vector perpendicular to v and n1
    n2 = np.cross(v, n1)
    #surface ranges over t from 0 to length of axis and 0 to 2*pi
    t = np.linspace(0, mag, 10)
    theta = np.linspace(0, 2 * np.pi, 20)
    #use meshgrid to make 2d arrays
    t, theta = np.meshgrid(t, theta)
    #generate coordinates for surface
    X, Y, Z = [p0[i] + v[i] * t + R * np.sin(theta) * n1[i] + R * np.cos(theta) * n2[i] for i in [0, 1, 2]]

    return X, Y, Z

    
def plot_cylinder_2points(axis, point0, point1, radius, color='blue'):
    """ Plots a cylinder by connecting 2 points
    """
    Xc, Yc, Zc = data_for_cylinder_2_points(point0, point1, radius)
    axis.plot_surface(Xc, Yc, Zc, color=color)
    #plot axis
    axis.plot(*zip(point0, point1), color = 'red')
 

def plot_shaft_3d(ri, n_pieces, D, L, dev0=0.0, dev=0.0, shaft_name='Shaft'):
    """ Plots shaft in 3D with random drilling deviation
    dev0: maxinum deviation at top of pile [m]
    dev: maxinum deviation at base of pile [m]"""
    angles = np.linspace(0, 2*np.pi-2*np.pi/n_pieces, n_pieces)
    r = ri + D/2   
    x = r * np.cos(angles)
    y = r * np.sin(angles)
    
    # deviations
    #angles_deviation = 2*np.pi*np.random.rand(angles.size) # random angle of deviation for each of the piles
    angles_deviation = 2*np.pi*np.random.uniform(0,1,angles.size) # random angle of deviation for each of the piles
    x_dev0 = x + dev0*np.cos(angles_deviation) # x top
    y_dev0 = y + dev0*np.sin(angles_deviation) # y top
    x_dev = x + dev*np.cos(angles_deviation)    # x bottom
    y_dev = y + dev*np.sin(angles_deviation)    # y bottom
    
    fig = plt.figure()
    #ax = fig.gca(projection='3d')
    ax = fig.add_subplot(projection='3d')
    
    for i in range(0,len(angles),2):
        point0 = np.array([x_dev[i], y_dev[i], 0])          # bottom
        point1 = np.array([x_dev0[i], y_dev0[i], L])        # top
        plot_cylinder_2points(ax, point0, point1, D/2)
        
    for i in range(1, len(angles), 2):
        point0 = np.array([x_dev[i], y_dev[i], 0])  # bottom
        point1 = np.array([x_dev0[i], y_dev0[i], L])          # top
        plot_cylinder_2points(ax, point0, point1, D/2, color='orange')
        
    ax.set_title(shaft_name + ' 3D', fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=8)
    #ax.set_aspect('equal')
    set_axis_equal_3d(ax)
    #plt.show()
    return fig
    
    
def set_axis_equal_3d(ax):
    """ Sets equal aspect ratio
    """
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)