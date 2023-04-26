import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D  # for rotation around center of rectangle


def get_parameters_shaft_diaphragm_panels(D, L, H_drilling_platform, v=0.5):
    """ Gets parameters for secant piled wall
    D: pannel thickness [m]
    di: shaft inner diameter [m]
    #a: C/C pile spacing b/w two neighboring piles [m]
    L: pannel length [m]
    v: percentage of verticality [%]
    H_drilling_platform: height of drilling platform above top of piles [m]
    """
    x0 = H_drilling_platform*v/100  # deviation at top of pile when drilling platform is above, m

    x = x0 + L*v/100    # deviation at bottom of wall, m
    d_eff = D - 2*x

    return x0, x, d_eff


def plot_shaft_diaphragm_panels(di, D, B, dev0, dev, n_pieces, shaft_name='Shaft'):
    """Plot diaphragm wall shaft in 2D

    Args:
        di (float): Inner diameter of shaft [m]
        D (float): Pannel thickness [m]
        n_piecs (integer): Number of pannels
        x0 (float): Deviation at top of shaft [m]
        x (float): Deviation at base of shaft [m]
        shaftname (str, optional): Shaft name. Defaults to 'Shaft'.
    """
    #n_pieces = int(math.ceil(np.pi*(di + D/2)/B) + 1)     # number of pannels for plotting 

    angles = np.linspace(0, 2*np.pi-2*np.pi/n_pieces, n_pieces)

    r = di/2 + D
    
    # top
    directions = np.random.choice(np.array([-1, 1]), angles.size)
    r_dev0 = dev0 * directions
    x0 = (r + r_dev0) * np.cos(angles)
    y0 = (r + r_dev0) * np.sin(angles)

    # bottom
    r_dev = dev * directions
    x = (r + r_dev) * np.cos(angles)
    y = (r + r_dev) * np.sin(angles)
        
    fig, ax = plt.subplots(1, 2)
    # top of shaft
    for i in range(0, len(angles), 1):
        angle_i = (angles[i] + np.pi/n_pieces + np.pi/2)*180/np.pi
        transform_i = Affine2D().rotate_deg_around(*(x0[i]+D/2, y0[i]+B/2), angle_i) + ax[0].transData
        rect_top = Rectangle((x0[i]+D/2, y0[i]+B/2), B, D, transform=transform_i, facecolor='pink', edgecolor='black', zorder=0, alpha=0.3)
        ax[0].add_patch(rect_top)

    # bottom of shaft
    for i in range(0, len(angles), 1):
        angle_i = (angles[i] + np.pi/n_pieces + np.pi/2)*180/np.pi
        transform_i = Affine2D().rotate_deg_around(*(x[i]+D/2, y[i]+B/2), angle_i) + ax[1].transData
        rect_bottom = Rectangle((x[i]+D/2, y[i]+B/2), B, D, transform=transform_i, facecolor='pink', edgecolor='black', zorder=0, alpha=0.3)
        ax[1].add_patch(rect_bottom)

    ax[0].set_title(shaft_name + ' at top', fontsize=8)
    ax[1].set_title(shaft_name + ' at base (deviation {0:.1f} cm)'.format(dev*100), fontsize=8)
    ax[0].tick_params(axis='both', which='major', labelsize=8)
    ax[1].tick_params(axis='both', which='major', labelsize=8)
    for axi in ax:
        axi.autoscale_view()
        axi.set_aspect('equal')

    return fig


def plot_wall_diaphragm_panels(n_pieces, D, B, dev0, dev, shaft_name='Shaft'):
    """Plot diaphragm wall panels in 2D

    Args:
        D (float): Pannel thickness [m]
        n_piecs (integer): Number of pannels
        x0 (float): Deviation at top of shaft [m]
        x (float): Deviation at base of shaft [m]
        shaftname (str, optional): Shaft name. Defaults to 'Shaft'.
    """

    # top
    x0 = np.array([B/2, B + B/2])
    y0 = np.array([0.0 - dev0, 0.0 + dev0])

    # bottom
    x = np.array([B/2, B + B/2])
    y = np.array([0.0 - dev, 0.0 + dev])
        
    fig, ax = plt.subplots(1, 2)
    # top of shaft
    for i in range(0, 2):
        transform_i = Affine2D().rotate_deg_around(*(x0[i], y0[i]), 0.0) + ax[0].transData
        rect_top = Rectangle((x0[i], y0[i]-D/2), B, D, transform=transform_i, facecolor='pink', edgecolor='black', zorder=0, alpha=0.3)
        ax[0].add_patch(rect_top)

    # bottom of shaft
    for i in range(0, 2):
        transform_i = Affine2D().rotate_deg_around(*(x[i], y[i]), 0.0) + ax[1].transData
        rect_bottom = Rectangle((x[i], y[i]-D/2), B, D, transform=transform_i, facecolor='pink', edgecolor='black', zorder=0, alpha=0.3)
        ax[1].add_patch(rect_bottom)

    ax[0].set_title(shaft_name + ' at top', fontsize=8)
    ax[1].set_title(shaft_name + ' at base (deviation {0:.1f} cm)'.format(dev*100), fontsize=8)
    ax[0].tick_params(axis='both', which='major', labelsize=8)
    ax[1].tick_params(axis='both', which='major', labelsize=8)
    for axi in ax:
        axi.autoscale_view()
        axi.set_aspect('equal')

    return fig