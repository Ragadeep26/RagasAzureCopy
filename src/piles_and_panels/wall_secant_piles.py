import numpy as np
import matplotlib.pyplot as plt
from src.piles_and_panels.shaft_secant_piles import plot_cylinder_2points, set_axis_equal_3d

def get_parameters_wall_secant_piles(D, a, L, H_drilling_platform, v=0.75):
    """ Gets parameters for secant piled wall
    D: pile diameter [m]
    a: C/C pile spacing b/w two neighboring piles [m]
    L: pile length [m]
    v: percentage of verticality [%]
    H_drilling_platform: height of drilling platform above top of piles [m]
    """
    x0 = H_drilling_platform*v/100  # deviation at top of pile when drilling platform is above, m
    t_top = D - a - 2*x0 # overcut/ interlock
    # t_top = t_top - 2*x0
    d_top = 2*np.sqrt((D/2)**2 - (a/2)**2) # overlapped thickness

    x = x0 + L*v/100 # deviation at bottom of wall, m
    t_eff = t_top - 2*x # effective/overlapped thickness at toe of wall, m
    d_eff = np.nan
    if t_eff > 0:
        d_eff = 2*np.sqrt((D/2)*t_eff - (t_eff/2)**2) # overlapped thickness, m    
    else:
        d_eff = np.nan

    return t_top, d_top, x0, x, t_eff, d_eff


def plot_wall_secant_piles_2items(a, D, dev_0=0.0, dev=0.0, wall_name='Wall'):
    x = np.array([D/2, D/2 + a])
    y = np.zeros_like(x)
        
    pile_types = ['primary', 'secondary']
    pile_colors = ['white', 'white']
    fig, ax = plt.subplots(2, 2)
    
    # worst-case deviations
    x0 = np.array([x[0] - dev_0, x[1] + dev_0]) # x top
    y0 = y
    x[0] = x[0] - dev    # x bottom
    x[1] = x[1] + dev    # x bottom

    # top of shaft
    for i in range(0,len(x),2):
        circle_p = plt.Circle((x0[i],y0[i]), D/2, facecolor=pile_colors[0], edgecolor='black', zorder=0, alpha=0.3, label=pile_types[0])
        ax[0, 0].add_patch(circle_p)       
        ax[0, 0].scatter(x0[i],y0[i])   # pile center
    for i in range(1, len(x), 2):
        circle_s = plt.Circle((x0[i],y0[i]), D/2, facecolor=pile_colors[1], edgecolor='black', zorder=0, alpha=0.3, linewidth=2.0, label=pile_types[1])
        ax[0, 0].add_patch(circle_s)
        ax[0, 0].scatter(x0[i],y0[i])   # pile center

    # bottom of shaft, deviation in horizontal direction outwards
    for i in range(0,len(x),2):
        circle_p = plt.Circle((x[i],y[i]), D/2, facecolor=pile_colors[0], edgecolor='black', zorder=0, alpha=0.3, label=pile_types[0])
        ax[1, 0].add_patch(circle_p)       
        ax[1, 0].scatter(x[i], y[i])   # pile center
        ax[1, 0].arrow(x0[i], y0[i], -dev, 0, width=0.02)
    for i in range(1, len(x), 2):
        circle_s = plt.Circle((x[i],y[i]), D/2, facecolor=pile_colors[1], edgecolor='black', zorder=0, alpha=0.3, linewidth=2.0, label=pile_types[1])
        ax[1, 0].add_patch(circle_s)
        ax[1, 0].scatter(x[i], y[i])   # pile center
        ax[1, 0].arrow(x0[i], y0[i], dev, 0, width=0.02)

    # bottom of shaft, deviation in horizontal direction inwards
    for i in range(0,len(x),2):
        circle_p = plt.Circle((x0[i] + dev,y[i]), D/2, facecolor=pile_colors[0], edgecolor='black', zorder=0, alpha=0.3, label=pile_types[0])
        ax[0, 1].add_patch(circle_p)       
        ax[0, 1].scatter(x0[i] + dev, y0[i])   # pile center
        ax[0, 1].arrow(x0[i], y0[i], dev, 0, width=0.02)
    for i in range(1, len(x), 2):
        circle_s = plt.Circle((x0[i] - dev,y[i]), D/2, facecolor=pile_colors[1], edgecolor='black', zorder=0, alpha=0.3, linewidth=2.0, label=pile_types[1])
        ax[0, 1].add_patch(circle_s)
        ax[0, 1].scatter(x0[i] - dev, y0[i])   # pile center
        ax[0, 1].arrow(x0[i], y0[i], -dev, 0, width=0.02)

    # bottom of shaft, deviation in vertical direction
    for i in range(0,len(x),2):
        circle_p = plt.Circle((x0[i],y0[i] - dev), D/2, facecolor=pile_colors[0], edgecolor='black', zorder=0, alpha=0.3, label=pile_types[0])
        ax[1, 1].add_patch(circle_p)       
        ax[1, 1].scatter(x0[i], y0[i] - dev)   # pile center
        ax[1, 1].arrow(x0[i], y0[i], 0, -dev, width=0.02)
    for i in range(1, len(x), 2):
        circle_s = plt.Circle((x0[i],y0[i] + dev), D/2, facecolor=pile_colors[1], edgecolor='black', zorder=0, alpha=0.3, linewidth=2.0, label=pile_types[1])
        ax[1, 1].add_patch(circle_s)
        ax[1, 1].scatter(x0[i], y0[i] + dev)   # pile center
        ax[1, 1].arrow(x0[i], y0[i], 0, dev, width=0.02)

    ax[0, 0].set_title('top (dev. {0:.1f} cm)'.format(dev_0*100), fontsize=8)
    ax[1, 0].set_title('base left/right outward (dev. {0:.1f} cm)'.format(dev*100), fontsize=8)
    ax[0, 1].set_title('base left/right inward (dev. {0:.1f} cm)'.format(dev*100), fontsize=8)
    ax[1, 1].set_title('base sideward (dev. {0:.1f} cm)'.format(dev*100), fontsize=8)
    for axi in ax.flatten():
        #axi.autoscale_view()
        axi.set_xlim(x0[0] - D/2 - 2*dev,x0[1] + D/2 + 2*dev)
        axi.set_ylim(y0[0] - D/2 - 2*dev,y0[1] + D/2 + 2*dev)
        axi.set_aspect('equal')
        #ax.legend()
        #handles, labels = plt.gca().get_legend_handles_labels()
        #by_label = OrderedDict(zip(labels, handles))
        #plt.legend(by_label.values(), by_label.keys())
    #plt.show()
    return fig


def plot_wall_secant_piles(n_pieces, a, D, dev_0=0.0, dev=0.0, wall_name='Wall'):
    x = np.linspace(0.0, (n_pieces-1)*a, n_pieces)
    y = np.zeros_like(x)
        
    pile_types = ['primary', 'secondary']
    #pile_colors = ['blue', 'red']
    pile_colors = ['white', 'white']
    fig, ax = plt.subplots(2, 1)
    
    # deviations
    #angles_deviation = 2*np.pi*np.random.rand(angles.size) # random angle of deviation for each of the piles
    angles_deviation = 2*np.pi*np.random.uniform(0, 1, x.size) # random angle of deviation for each of the piles
    x0 = x + dev_0*np.cos(angles_deviation) # x top
    y0 = y + dev_0*np.sin(angles_deviation) # y top
    x = x + dev*np.cos(angles_deviation)    # x bottom
    y = y + dev*np.sin(angles_deviation)    # y bottom

    # top of shaft
    for i in range(0,len(x),2):
        circle_p = plt.Circle((x0[i],y0[i]), D/2, facecolor=pile_colors[0], edgecolor='black', zorder=0, alpha=0.3, label=pile_types[0])
        ax[0].add_patch(circle_p)       
    for i in range(1, len(x), 2):
        circle_s = plt.Circle((x0[i],y0[i]), D/2, facecolor=pile_colors[1], edgecolor='black', zorder=0, alpha=0.3, linewidth=2.0, label=pile_types[1])
        ax[0].add_patch(circle_s)
    
    # bottom of shaft
    for i in range(0,len(x),2):
        circle_p = plt.Circle((x[i],y[i]), D/2, facecolor=pile_colors[0], edgecolor='black', zorder=0, alpha=0.3, label=pile_types[0])
        ax[1].add_patch(circle_p)       
    for i in range(1, len(x), 2):
        circle_s = plt.Circle((x[i],y[i]), D/2, facecolor=pile_colors[1], edgecolor='black', zorder=0, alpha=0.3, linewidth=2.0, label=pile_types[1])
        ax[1].add_patch(circle_s)

    ax[0].set_title(wall_name + ' at top')
    ax[1].set_title(wall_name + ' at base (deviation {0:.1f} cm)'.format(dev*100))
    for axi in ax:
        axi.autoscale_view()
        axi.set_aspect('equal')
        #ax.legend()
        #handles, labels = plt.gca().get_legend_handles_labels()
        #by_label = OrderedDict(zip(labels, handles))
        #plt.legend(by_label.values(), by_label.keys())
    #plt.show()
    return fig


def plot_wall_secant_piles_3d(n_pieces, a, D, L, dev0=0.0, dev=0.0, wall_name='Wall'):
    """ Plots shaft in 3D with random drilling deviation
    dev0: maxinum deviation at top of pile [m]
    dev: maxinum deviation at base of pile [m]"""
    x = np.linspace(0.0, (n_pieces-1)*a, n_pieces)
    y = np.zeros_like(x)
    
    # deviations
    #angles_deviation = 2*np.pi*np.random.rand(angles.size) # random angle of deviation for each of the piles
    angles_deviation = 2*np.pi*np.random.uniform(0, 1, x.size) # random angle of deviation for each of the piles
    x_dev0 = x + dev0*np.cos(angles_deviation) # x top
    y_dev0 = y + dev0*np.sin(angles_deviation) # y top
    x_dev = x + dev*np.cos(angles_deviation)    # x bottom
    y_dev = y + dev*np.sin(angles_deviation)    # y bottom
    
    fig = plt.figure()
    #ax = fig.gca(projection='3d')
    ax = fig.add_subplot(projection='3d')
    if n_pieces < 3:
        ax.view_init(azim=90.0, elev=0.0)
    
    for i in range(0,len(x),2):
        point0 = np.array([x_dev[i], y_dev[i], 0])          # bottom
        point1 = np.array([x_dev0[i], y_dev0[i], L])        # top
        plot_cylinder_2points(ax, point0, point1, D/2)
        
    for i in range(1, len(x), 2):
        point0 = np.array([x_dev[i], y_dev[i], 0])  # bottom
        point1 = np.array([x_dev0[i], y_dev0[i], L])          # top
        plot_cylinder_2points(ax, point0, point1, D/2, color='orange')
        
    ax.set_title(wall_name + ' 3D', fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=8)
    #ax.set_aspect('equal')
    set_axis_equal_3d(ax)
    #plt.show()
    return fig


def plot_wall_secant_piles_3d_2items(n_pieces, a, D, L, dev0=0.0, dev=0.0, wall_name='Wall'):
    """ Plots shaft in 3D with random drilling deviation
    dev0: maxinum deviation at top of pile [m]
    dev: maxinum deviation at base of pile [m]"""
    x = np.array([D/2, D/2 + a])
    y = np.zeros_like(x)

    # worst-case deviations
    x0 = np.array([x[0] + dev0, x[1] - dev0]) # x top
    y0 = y                                      # y top
    x[0] = x[0] - dev    # x bottom
    x[1] = x[1] + dev    # x bottom

    fig = plt.figure()
    #ax = fig.gca(projection='3d')
    ax = fig.add_subplot(projection='3d')
    if n_pieces < 3:
        ax.view_init(azim=90.0, elev=0.0)
    
    for i in range(0,len(x),2):
        point0 = np.array([x[i], y[i], 0])          # bottom
        point1 = np.array([x0[i], y0[i], L])        # top
        plot_cylinder_2points(ax, point0, point1, D/2)
        
    for i in range(1, len(x), 2):
        point0 = np.array([x[i], y[i], 0])  # bottom
        point1 = np.array([x0[i], y0[i], L])          # top
        plot_cylinder_2points(ax, point0, point1, D/2, color='orange')
        
    ax.set_title(wall_name + ' 3D', fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=8)
    #ax.set_aspect('equal')
    set_axis_equal_3d(ax)
    #plt.show()
    return fig