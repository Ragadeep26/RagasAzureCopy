# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:41:55 2020

@author: nya
"""
import copy
import numpy as np

PARAM_NAMES_CODE_0 = ['cube strength \n \N{GREEK SMALL LETTER BETA}_WN [MPa]', 'reduct. factor \n \N{GREEK SMALL LETTER ALPHA} [1]', 'stress-strain \n \N{GREEK SMALL LETTER EPSILON}_c2 [\N{PER MILLE SIGN}]', 'stress-strain \n \N{GREEK SMALL LETTER EPSILON}_c2u [\N{PER MILLE SIGN}]', 
                        'stress-strain \n exp. [1]', 'comp. loaded \n safety \n \N{GREEK CAPITAL LETTER DELTA}\N{GREEK SMALL LETTER GAMMA}_pl [1]', 'comp. loaded \n strain limits \n \N{GREEK SMALL LETTER EPSILON}_s  \N{GREEK SMALL LETTER EPSILON}_s [\N{PER MILLE SIGN}]', 'E_cm [MPa]']
PARAM_NAMES_CODE_1 = ['cylinder str. \n f_ck [MPa]', 'reduct. factor \n \N{GREEK SMALL LETTER ALPHA} [1]', 'stress-strain \n \N{GREEK SMALL LETTER EPSILON}_c2 [\N{PER MILLE SIGN}]', 'stress-strain \n \N{GREEK SMALL LETTER EPSILON}_c2u [\N{PER MILLE SIGN}]', 
                        'stress-strain \n exp. [1]', 'unreinf. \n safety \n \N{GREEK CAPITAL LETTER DELTA}\N{GREEK SMALL LETTER GAMMA}_pl [1]', 'unreinf. \n min. reinf. \n N_Ed, min [1]', 'E_cm [MPa]']
PARAM_NAMES_CODE_2 = ['cylinder str. \n f_ck [MPa]', 'reduct. factor \n \N{GREEK SMALL LETTER ALPHA} [1]', 'stress-strain \n \N{GREEK SMALL LETTER EPSILON}_c2 [\N{PER MILLE SIGN}]', 'stress-strain \n \N{GREEK SMALL LETTER EPSILON}_c2u [\N{PER MILLE SIGN}]', 
                        'stress-strain \n exp. [1]', 'unreinf. \n safety \n \N{GREEK CAPITAL LETTER DELTA}\N{GREEK SMALL LETTER ALPHA}_pl [1]', 'unreinf. \n min. reinf. \n N_Ed  A_s [%]', 'E_cm [MPa]']
PARAM_NAMES_CODE_3 = ['cylinder str. \n f_ck [MPa]', 'reduct. factor \n \N{GREEK SMALL LETTER ALPHA} [1]', 'stress-strain \n \N{GREEK SMALL LETTER EPSILON}_c2 [\N{PER MILLE SIGN}]', 'stress-strain \n \N{GREEK SMALL LETTER EPSILON}_c2u [\N{PER MILLE SIGN}]', 
                        'stress-strain \n exp. [1]', 'unreinf. \n safety \n \N{GREEK CAPITAL LETTER DELTA}\N{GREEK SMALL LETTER ALPHA}_pl [1]', 'unreinf. \n min. reinf. \n N_Ed, min [1]', 'E_cm [MPa]']
# concrete grade
CONCRETE_GRADE_CODE_0 = {'B 15': 15.0, 'B 25': 25.0, 'B 35': 35.0, 'B 45': 45.0, 'B 55': 55.0} # DIN 1045:1988
CONCRETE_GRADE_CODE_1 = {'C 12/15': 12.0, 'C 16/20': 15.0, 'C 20/25': 20.0, 'C 25/30': 25.0, 'C 30/37': 30.0, 'C 33/40': 33.0, 'C 35/45': 35.0, 'C 40/50': 40.0, 'C 45/55': 45.0, 'C 50/60': 50.0} # DIN 1045:2008
CONCRETE_GRADE_CODE_2 = {'C 12/15': 12.0, 'C 16/20': 15.0, 'C 20/25': 20.0, 'C 25/30': 25.0, 'C 30/37': 30.0, 'C 33/40': 33.0, 'C 35/45': 35.0, 'C 40/50': 40.0, 'C 45/55': 45.0, 'C 50/60': 50.0} # EN 1992-1-1:2004 (Eurocode 2)
CONCRETE_GRADE_CODE_3 = {'C 12/15': 12.0, 'C 16/20': 15.0, 'C 20/25': 20.0, 'C 25/30': 25.0, 'C 30/37': 30.0, 'C 33/40': 33.0, 'C 35/45': 35.0, 'C 40/50': 40.0, 'C 45/55': 45.0, 'C 50/60': 50.0} # DIN EN 1992-1-1:2004 + AC:2010 + NA:2011

# concrete alpha
CONCRETE_ALPHA_CODE_0 = {'B 15': 0.7, 'B 25': 0.7, 'B 35': 0.65714286, 'B 45': 0.6, 'B 55': 0.54545455} # DIN 1045:1988
CONCRETE_ALPHA_CODE_1 = {'C 12/15': 0.85, 'C 16/20': 0.85, 'C 20/25': 0.85, 'C 25/30': 0.85, 'C 30/37': 0.85, 'C 33/40': 0.85, 'C 35/45': 0.85, 'C 40/50': 0.85, 'C 45/55': 0.85, 'C 50/60': 0.85} # DIN 1045:2008
CONCRETE_ALPHA_CODE_2 = {'C 12/15': 0.90909091, 'C 16/20': 0.90909091, 'C 20/25': 0.90909091, 'C 25/30': 0.90909091, 'C 30/37': 0.90909091, 'C 33/40': 0.90909091, 'C 35/45': 0.90909091, 'C 40/50': 0.90909091, 'C 45/55': 0.90909091, 'C 50/60': 0.90909091} # EN 1992-1-1:2004 (Eurocode 2)
CONCRETE_ALPHA_CODE_3 = {'C 12/15': 0.85, 'C 16/20': 0.85, 'C 20/25': 0.85, 'C 25/30': 0.85, 'C 30/37': 0.85, 'C 33/40': 0.85, 'C 35/45': 0.85, 'C 40/50': 0.85, 'C 45/55': 0.85, 'C 50/60': 0.85} # DIN EN 1992-1-1:2004 + AC:2010 + NA:2011

# concrete epsilon_c2
CONCRETE_EPSILON_C2_CODE_0 = CONCRETE_GRADE_CODE_0.fromkeys(CONCRETE_GRADE_CODE_0, 2.0)
CONCRETE_EPSILON_C2_CODE_1 = CONCRETE_GRADE_CODE_1.fromkeys(CONCRETE_GRADE_CODE_1, 2.0)
CONCRETE_EPSILON_C2_CODE_2 = CONCRETE_GRADE_CODE_2.fromkeys(CONCRETE_GRADE_CODE_2, 2.0)
CONCRETE_EPSILON_C2_CODE_3 = CONCRETE_GRADE_CODE_3.fromkeys(CONCRETE_GRADE_CODE_3, 2.0)

# concrete epsilon_c2u
CONCRETE_EPSILON_C2U_CODE_0 = CONCRETE_GRADE_CODE_0.fromkeys(CONCRETE_GRADE_CODE_0, 3.5)
CONCRETE_EPSILON_C2U_CODE_1 = CONCRETE_GRADE_CODE_1.fromkeys(CONCRETE_GRADE_CODE_1, 3.5)
CONCRETE_EPSILON_C2U_CODE_2 = CONCRETE_GRADE_CODE_2.fromkeys(CONCRETE_GRADE_CODE_2, 3.5)
CONCRETE_EPSILON_C2U_CODE_3 = CONCRETE_GRADE_CODE_3.fromkeys(CONCRETE_GRADE_CODE_3, 3.5)

# concrete exp
CONCRETE_EXP_CODE_0 = CONCRETE_GRADE_CODE_0.fromkeys(CONCRETE_GRADE_CODE_0, 2.0)
CONCRETE_EXP_CODE_1 = CONCRETE_GRADE_CODE_1.fromkeys(CONCRETE_GRADE_CODE_1, 2.0)
CONCRETE_EXP_CODE_2 = CONCRETE_GRADE_CODE_2.fromkeys(CONCRETE_GRADE_CODE_2, 2.0)
CONCRETE_EXP_CODE_3 = CONCRETE_GRADE_CODE_3.fromkeys(CONCRETE_GRADE_CODE_3, 2.0)

# concrete delta_alpha_pl
CONCRETE_DELTA_ALPHA_PL_CODE_0 = CONCRETE_GRADE_CODE_0.fromkeys(CONCRETE_GRADE_CODE_0, 0.35)
CONCRETE_DELTA_ALPHA_PL_CODE_1 = CONCRETE_GRADE_CODE_1.fromkeys(CONCRETE_GRADE_CODE_1, 0.3)
CONCRETE_DELTA_ALPHA_PL_CODE_2 = CONCRETE_GRADE_CODE_2.fromkeys(CONCRETE_GRADE_CODE_2, 0.18)
CONCRETE_DELTA_ALPHA_PL_CODE_3 = CONCRETE_GRADE_CODE_3.fromkeys(CONCRETE_GRADE_CODE_3, 0.15)

# concrete unreinforced
CONCRETE_UNREINFORCED_CODE_0 = CONCRETE_GRADE_CODE_0.fromkeys(CONCRETE_GRADE_CODE_0, '3.0 0.0')
CONCRETE_UNREINFORCED_CODE_1 = CONCRETE_GRADE_CODE_1.fromkeys(CONCRETE_GRADE_CODE_1, 0.15)
CONCRETE_UNREINFORCED_CODE_2 = CONCRETE_GRADE_CODE_2.fromkeys(CONCRETE_GRADE_CODE_2, '0.1 0.2')
CONCRETE_UNREINFORCED_CODE_3 = CONCRETE_GRADE_CODE_3.fromkeys(CONCRETE_GRADE_CODE_3, 0.15)

# concrete E_cm
CONCRETE_E_CM_CODE_0 = CONCRETE_GRADE_CODE_0.fromkeys(CONCRETE_GRADE_CODE_0, 30000.0)
CONCRETE_E_CM_CODE_1 = {'C 12/15': 21800.0, 'C 16/20': 23400.0, 'C 20/25': 24900.0, 'C 25/30': 26700.0, 'C 30/37': 28300.0, 'C 33/40': 29100.0, 'C 35/45': 29900.0, 'C 40/50': 31400.0, 'C 45/55': 32800.0, 'C 50/60': 34300.0} # DIN 1045:2008
CONCRETE_E_CM_CODE_2 = {'C 12/15': 27000.0, 'C 16/20': 29000.0, 'C 20/25': 30000.0, 'C 25/30': 31000.0, 'C 30/37': 33000.0, 'C 33/40': 33000.0, 'C 35/45': 34000.0, 'C 40/50': 35000.0, 'C 45/55': 36000.0, 'C 50/60': 37000.0} # EN 1992-1-1:2004 (Eurocode 2)
CONCRETE_E_CM_CODE_3 = copy.deepcopy(CONCRETE_E_CM_CODE_2)

# reinforcement grade
REINF_CODE_0 = {'BSt 420': 420.0, 'BSt 500': 500.0}
REINF_CODE_1 = {'BSt 500A': 500.0, 'BSt 500B': 500.0}
REINF_CODE_2 = {'B500A': 500.0, 'B500B': 500.0}
REINF_CODE_3 = {'B500A': 500.0, 'B500B': 500.0}

# reinforcement f_tk
REINF_F_TK_CODE_0 = {'BSt 420': 420.0, 'BSt 500': 500.0}
REINF_F_TK_CODE_1 = {'BSt 500A': 525.0, 'BSt 500B': 540.0}
REINF_F_TK_CODE_2 = {'B500A': 525.0, 'B500B': 525.0}
REINF_F_TK_CODE_3 = {'B500A': 525.0, 'B500B': 525.0}

# reinforcement E
REINF_E_CODE_0 = {'BSt 420': 210000.0, 'BSt 500': 210000.0}
REINF_E_CODE_1 = {'BSt 500A': 200000.0, 'BSt 500B': 200000.0}
REINF_E_CODE_2 = {'B500A': 200000.0, 'B500B': 200000.0}
REINF_E_CODE_3 = {'B500A': 200000.0, 'B500B': 200000.0}

# reinforcement epsilon_cu
REINF_EPSILON_CU_CODE_0 = {'BSt 420': 5.0, 'BSt 500': 5.0}
REINF_EPSILON_CU_CODE_1 = {'BSt 500A': 25.0, 'BSt 500B': 50.0}
REINF_EPSILON_CU_CODE_2 = {'B500A': 25.0, 'B500B': 25.0}
REINF_EPSILON_CU_CODE_3 = {'B500A': 25.0, 'B500B': 25.0}

# crack width sigma_s - ds relation
SIGMA_S1_CODE_0OR1 = np.array([160, 200, 240, 280, 320, 360, 400, 450])
DS040_CODE_0OR1 = np.array([56, 36, 25, 18, 14, 11, 9, 7])
DS030_CODE_0OR1 = np.array([42, 27, 19, 14, 11, 8, 7, 5])
DS020_CODE_0OR1 = np.array([28, 18, 13, 9, 7, 6, 5, 4])
SIGMA_DS_CODE_0 = {'sigma': SIGMA_S1_CODE_0OR1, '0.4 mm': DS040_CODE_0OR1, '0.3 mm': DS030_CODE_0OR1, '0.2 mm': DS020_CODE_0OR1}
SIGMA_DS_CODE_1 = {'sigma': SIGMA_S1_CODE_0OR1, '0.4 mm': DS040_CODE_0OR1, '0.3 mm': DS030_CODE_0OR1, '0.2 mm': DS020_CODE_0OR1}
SIGMA_S1_CODE_2 = np.array([160, 200, 240, 280, 320, 360, 400, 450])
DS040_CODE_2 = np.array([40, 32, 20, 16, 12, 10, 8, 6])
DS030_CODE_2 = np.array([32, 25, 16, 12, 10, 8, 6, 5])
DS020_CODE_2 = np.array([25, 16, 12, 8, 6, 5, 4, 2])
SIGMA_DS_CODE_2 = {'sigma': SIGMA_S1_CODE_2, '0.4 mm': DS040_CODE_2, '0.3 mm': DS030_CODE_2, '0.2 mm': DS020_CODE_2}
SIGMA_S1_CODE_3 = np.array([160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 400, 450])
DS040_CODE_3 = np.array([54, 43, 35, 29, 24, 21, 18, 15, 14, 12, 11, 9, 7])
DS030_CODE_3 = np.array([41, 32, 26, 22, 18, 15, 13, 12, 10, 9, 8, 7, 5])
#DS020_CODE_3 = np.array([27, 21, 17, 14, 12, 10, 9, 8, 7, 6, 5, 4, 3])
DS020_CODE_3 = np.array([28, 21, 17, 14, 12, 10, 9, 8, 7, 6, 5, 4, 3])  # to cover the limit, by default ds = 28 mm
SIGMA_DS_CODE_3 = {'sigma': SIGMA_S1_CODE_3, '0.4 mm': DS040_CODE_3, '0.3 mm': DS030_CODE_3, '0.2 mm': DS020_CODE_3}
# crack width sigma_s - s relation
SIGMA_S2 = np.array([160, 200, 240, 280, 320, 360])
S040 = np.array([350, 300, 250, 200, 150, 100])
S030 = np.array([300, 250, 200, 150, 100, 50])
S020 = np.array([200, 150, 100, 50, 20, 10])
SIGMA_S = {'sigma': SIGMA_S2, '0.4 mm': S040, '0.3 mm': S030, '0.2 mm': S020}

# PSF for load cases
#PSF_LOAD_CASES_CODE_0 = {'LF 1: Persistent': '\N{GREEK SMALL LETTER GAMMA} [1]', 'LF 2. Transient': '\N{GREEK SMALL LETTER GAMMA} [1]', 'LF 3: Accidential': '\N{GREEK SMALL LETTER GAMMA} [1]', 'LF 3: Seismic': '\N{GREEK SMALL LETTER GAMMA} [1]'}
#PSF_LOAD_CASES_CODE_1 = {'LF 1: Persistent': 'permanent', 'LF 2: Transient': 'transient', 'LF 3: Accidential': '\N{GREEK SMALL LETTER GAMMA}_c [1]', 'LF 3: Seismic': '\N{GREEK SMALL LETTER GAMMA}_s [1]'}
#PSF_LOAD_CASES_CODE_2 = {'BS-P: Persistent': 'permanent', 'BS-T: Transient': 'transient', 'BS-A: Accidential': '\N{GREEK SMALL LETTER GAMMA}_c [1]', 'BS-E: Seismic': '\N{GREEK SMALL LETTER GAMMA}_s [1]'}
#PSF_LOAD_CASES_CODE_3 = {'BS-P: Persistent': 'permanent', 'BS-T: Transient': 'transient', 'BS-A: Accidential': '\N{GREEK SMALL LETTER GAMMA}_c [1]', 'BS-E: Seismic': '\N{GREEK SMALL LETTER GAMMA}_s [1]'}
PSF_LOAD_CASES_CODE_0 = ['LF 1: Persistent', 'LF 2: Transient', 'LF 3: Accidential', 'LF 3: Seismic']
PSF_LOAD_CASES_CODE_1 = ['LF 1: Persistent', 'LF 2: Transient', 'LF 3: Accidential', 'LF 3: Seismic']
PSF_LOAD_CASES_CODE_2 = ['BS-P: Persistent', 'BS-T: Transient', 'BS-A: Accidential', 'BS-E: Seismic']
PSF_LOAD_CASES_CODE_3 = ['BS-P: Persistent', 'BS-T: Transient', 'BS-A: Accidential', 'BS-E: Seismic']
PSF_NAMES_CODE_0 = ['', '', '\N{GREEK SMALL LETTER GAMMA} [1]', '']
PSF_NAMES_CODE_1 = ['permanent', 'transient', '\N{GREEK SMALL LETTER GAMMA}_c [1]', '\N{GREEK SMALL LETTER GAMMA}_s [1]']
PSF_NAMES_CODE_2 = ['permanent', 'transient', '\N{GREEK SMALL LETTER GAMMA}_c [1]', '\N{GREEK SMALL LETTER GAMMA}_s [1]']
PSF_NAMES_CODE_3 = ['permanent', 'transient', '\N{GREEK SMALL LETTER GAMMA}_c [1]', '\N{GREEK SMALL LETTER GAMMA}_s [1]']
# PSF gamma_G
PSF_GAMMA_G_CODE_0 = {'LF 1: Persistent': 1.0,  'LF 2: Transient': 1.0, 'LF 3: Accidential': 1.0, 'LF 3: Seismic': 1.0}
PSF_GAMMA_G_CODE_1 = {'LF 1: Persistent': 1.35, 'LF 2: Transient': 1.2, 'LF 3: Accidential': 1.1, 'LF 3: Seismic': 1.0}
PSF_GAMMA_G_CODE_2 = {'BS-P: Persistent': 1.35, 'BS-T: Transient': 1.2, 'BS-A: Accidential': 1.1, 'BS-E: Seismic': 1.0}
PSF_GAMMA_G_CODE_3 = {'BS-P: Persistent': 1.35, 'BS-T: Transient': 1.2, 'BS-A: Accidential': 1.1, 'BS-E: Seismic': 1.0}
# PSF gamma_Q
PSF_GAMMA_Q_CODE_0 = {'LF 1: Persistent': 1.0, 'LF 2: Transient': 1.0, 'LF 3: Accidential': 1.0, 'LF 3: Seismic': 1.0}
PSF_GAMMA_Q_CODE_1 = {'LF 1: Persistent': 1.5, 'LF 2: Transient': 1.3, 'LF 3: Accidential': 1.1, 'LF 3: Seismic': 1.1}
PSF_GAMMA_Q_CODE_2 = {'BS-P: Persistent': 1.5, 'BS-T: Transient': 1.3, 'BS-A: Accidential': 1.1, 'BS-E: Seismic': 1.0}
PSF_GAMMA_Q_CODE_3 = {'BS-P: Persistent': 1.5, 'BS-T: Transient': 1.3, 'BS-A: Accidential': 1.1, 'BS-E: Seismic': 1.0}
# PSF gamma_c
PSF_GAMMA_C_CODE_0 = {'LF 1: Persistent': 1.75,'LF 2: Transient': 1.75,'LF 3: Accidential': 1.3, 'LF 3: Seismic': 1.3}
PSF_GAMMA_C_CODE_1 = {'LF 1: Persistent': 1.5, 'LF 2: Transient': 1.5, 'LF 3: Accidential': 1.3, 'LF 3: Seismic': 1.3}
PSF_GAMMA_C_CODE_2 = {'BS-P: Persistent': 1.5, 'BS-T: Transient': 1.5, 'BS-A: Accidential': 1.2, 'BS-E: Seismic': 1.2}
PSF_GAMMA_C_CODE_3 = {'BS-P: Persistent': 1.5, 'BS-T: Transient': 1.5, 'BS-A: Accidential': 1.3, 'BS-E: Seismic': 1.3}
# PSF gamma_s
PSF_GAMMA_S_CODE_0 = {'LF 1: Persistent': 1.75, 'LF 2: Transient': 1.75, 'LF 3: Accidential': 1.3, 'LF 3: Seismic': 1.3}
PSF_GAMMA_S_CODE_1 = {'LF 1: Persistent': 1.15, 'LF 2: Transient': 1.15, 'LF 3: Accidential': 1.0, 'LF 3: Seismic': 1.0}
PSF_GAMMA_S_CODE_2 = {'BS-P: Persistent': 1.15, 'BS-T: Transient': 1.15, 'BS-A: Accidential': 1.0, 'BS-E: Seismic': 1.0}
PSF_GAMMA_S_CODE_3 = {'BS-P: Persistent': 1.15, 'BS-T: Transient': 1.15, 'BS-A: Accidential': 1.0, 'BS-E: Seismic': 1.0}
