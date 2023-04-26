import numpy as np

## Basic methods
def get_area(dia):
    """Gets are from bar
    dia: bar diameter in mm"""
    dia_cm = dia*0.1
    return 0.25*np.pi*dia_cm**2 # [cm^2]

def get_reinf_rate_cross_section_plane(dia, spacing):
    """ Gets cross sectional As [cm**2/m] for planar reinforcement
    dia: bar diameter in mm
    spacing: bar spacing cm
    """
    Ad = get_area(dia)
    As = Ad*100/spacing # cm**2/m
    return As

def get_area_moment_of_inertia_circ(D):
    """ Gets area moment of inertia for a filled circle cross-section
    D: cross-section diameter"""
    Iyy = (np.pi*D**4)/64
    return Iyy

def get_area_moment_of_inertia_rect(b, h):
    """ Gets area moment of inertia for a filled rectangular cross-section
    b: cross-section breadth
    h: cross-section height """
    Iyy = (b*h**3)/12
    return Iyy


def get_equivalent_thickness_SPW(D, A):
    """ Gets equivalent thickness for plate to model SPW in PLAXIS3D
    D: pile diameter
    A: c/c spacing between two neighboring piles"""
    h = (12*np.pi*D**4/64/(2*A))**(1/3)
    return h


def get_design_hoop_stress_from_effective_thickeness(F_hoop, d_eff, gamma_G):
    """ Gets design hoop stress from hoop force and effective thickness
    F_hoop: hoop force in kN/m
    d_eff: efective thickness in m
    gamma_G: safety factor on load"""
    sigma_cd = gamma_G*F_hoop/d_eff/1000
    return sigma_cd # MPa


def get_design_hoop_stress_for_plain_concrete(f_ck, alpha_cc, gamma_c):
    """ Gets design hoop stress for plain concrete
    f_ck: compressive strength (cylinder)
    alpha_cc: coefficient for long-term effect
    gamma_c: satefy factor on material"""
    f_cd = alpha_cc*f_ck/gamma_c
    return f_cd


def check_for_hoop_force(F_hoop, d_eff, gamma_G, f_ck, alpha_cc=0.7, gamma_c=1.5, print_results=False):
    """ Checks for hoop stress"""
    sigma_cd = get_design_hoop_stress_from_effective_thickeness(F_hoop, d_eff, gamma_G)
    f_cd = get_design_hoop_stress_for_plain_concrete(f_ck, alpha_cc, gamma_c)
    
    if print_results:
        print('N2 = {0:.2f} kN/m, d_eff = {1:.2f} cm, gamma_G = {2:.2f}, f_ck = {3:.2f} MPa, alpha_cc = {4:.2f}, gamma_c = {5:.2f}'.format(F_hoop, d_eff*100, gamma_G, f_ck, alpha_cc, gamma_c))
        if sigma_cd < f_cd:
            print('Hoop stress = {0:.2f} MPa < design hoop stress = {1:.2f} MPa: PASSED'.format(sigma_cd, f_cd))
        else:
            print('Hoop stress = {0:.2f} MPa > design hoop stress = {1:.2f} MPa: NOT PASSED'.format(sigma_cd, f_cd))

    return sigma_cd, f_cd