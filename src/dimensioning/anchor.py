# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 08:58:38 2021

@author: nya
"""


# Basic methods for dimensioning of anchor strand
def get_f_t_01_k(R_p01, area, n_strand):
    """ Gets characteristic tension force for n_strand strands at 0.1% strain
    """
    f_t_01_k = n_strand * area * R_p01
    return f_t_01_k/1000 # [kN]

def get_R_t_d(R_p01, area, n_strand, gamma_M=1.15):
    """ Gets load capacity (design resistance) for n_strand strands
    """
    f_t_01_k = get_f_t_01_k(R_p01, area, n_strand)
    R_t_d = f_t_01_k / gamma_M
    return R_t_d # [kN]

def get_F_p(R_p01, R_m, area, n_strand, R_t_d, gamma_a=1.1):
    """ Gets anchor test load
    R_m: tensile strength
    """
    f_t_01_k = get_f_t_01_k(R_p01, area, n_strand)
    F_p1 = 0.95 * f_t_01_k
    F_p2 = 0.8 * n_strand * area * R_m / 1000 # [kN]
    F_p3 = R_t_d * gamma_a
    
    return min(F_p1, F_p2, F_p3)

def get_F_p_wallman(F_d, gamma_a=1.1):
    """ Gets anchor test load after Wallman
    """
    return F_d*gamma_a
    