# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 22:10:47 2020

@author: nya
"""
import multiprocessing
import sys
import os
import numpy as np
from collections import OrderedDict
import subprocess
from multiprocessing import Pool
#import xlwings as xw
#from report.report_with_matplotlib import Report
from matplotlib.backends.backend_pdf import PdfPages
from src.dimensioning.py_StB.StB_K_As_and_a_s import StB_K_MN, StB_K_Q

ACROBAT = r'C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat'

class Pile():
    def __init__(self, D=1.2, S=0.5, H=100.0):
        cross_section = OrderedDict()
        cross_section['D'] = D    # pile diameter in m
        cross_section['H'] = H    # concrete cover in mm
        cross_section['S'] = S    # spacing between secondary piles in m
        self.cross_section = cross_section
        
    
    def calculate_required_reinforcement(self, code, params_psf, params_concrete, params_reinf, wall_outputs_phases, min_reinf, method='py_StB'):
        """ Calculates the required reinforcement area
        """
        ## load 0_stb methods if method is 0_stb
        #if method == '0_stb':
        #    MONIMAN = sys.modules['moniman_paths']['MONIMAN']
        #    wb = xw.Book(os.path.join(MONIMAN, r'dimensioning\0_stb.xlsm'))
        #    xw.Visible = False
        #    StB_K_MN_0_stb = wb.macro('StB_K_MN')
        #    StB_K_Q_0_stb = wb.macro('StB_K_Q')

        # params_psf
        gam_perm = float(params_psf['param_0'])
        #gam_tran = float(self.params_psf['param_1'])
        gam_c = float(params_psf['param_2'])
        gam_s = float(params_psf['param_3'])
    
        # params cross-section
        D = self.cross_section['D']*1000 # mm
        H = self.cross_section['H']
        A = self.cross_section['S']*2

        # params concrete
        f_ck = float(params_concrete['param_0'])
        alpha = float(params_concrete['param_1'])
        eps_c2 = float(params_concrete['param_2'])/1000
        eps_c2u = float(params_concrete['param_3'])/1000
        exp = float(params_concrete['param_4'])
        delta_S = float(params_concrete['param_5'])
        delta_K = params_concrete['param_6']
        delta_K = delta_K + ' 0.0' if (len(delta_K.split())==1) else delta_K # append ' 0.0' if it is single

        # params reinf
        f_yk = float(params_reinf['param_0'])
        f_tk = float(params_reinf['param_1'])
        Es = float(params_reinf['param_2'])
        eps_su = float(params_reinf['param_3'])/1000
        RissP1 = float(params_reinf['param_4'])
        minBew = 1 if min_reinf else 0
        n_phases = len(wall_outputs_phases)
        n_data = wall_outputs_phases[0]['y'].size
        A_s_all = np.zeros((n_data, n_phases))
        a_s_all = np.zeros((n_data, n_phases))
        if method == 'py_StB':
            for j, wall_outputs in enumerate(wall_outputs_phases):
                N = wall_outputs['N']*A
                M = wall_outputs['M']*A
                Q = wall_outputs['Q']*A
                ## multiprocessing
                #dim_args = ([code, gam_c, gam_s, gam_perm, Mi, Ni, Qi, D, H, f_ck, alpha, eps_c2, eps_c2u, exp, delta_S, delta_K, f_yk, f_tk, Es, eps_su, RissP1, minBew] for Mi, Ni, Qi in zip(M,N,Q))
                #with Pool(multiprocessing.cpu_count() - 1) as pool:
                #    results = pool.starmap(self.evaluate_py_StB, dim_args)
                #    results_array = np.array(results)
                #A_s_all[:, j] = results_array[:, 0]
                #a_s_all[:, j] = results_array[:, 1]

                # serial
                for i in range(n_data):
                    A_s_i, a_s_i = self.evaluate_py_StB(code, gam_c, gam_s, gam_perm, M[i], N[i], Q[i], D, H, f_ck, alpha, eps_c2, eps_c2u, exp, delta_S, delta_K, f_yk, f_tk, Es, eps_su, RissP1, minBew)
                    A_s_all[i, j] = A_s_i
                    a_s_all[i, j] = a_s_i

        else: # 0_stb
            for j, wall_outputs in enumerate(wall_outputs_phases):
                N = wall_outputs['N']*A
                M = wall_outputs['M']*A
                Q = wall_outputs['Q']*A
                # serial
                for i in range(n_data):
                    A_s_i = StB_K_MN_0_stb(code, gam_c, gam_s, gam_perm*M[i], gam_perm*N[i], M[i], N[i], D, H, 0.0, f_ck, alpha, eps_c2, eps_c2u, exp, delta_S, delta_K, f_yk, f_tk, Es, eps_su, RissP1, minBew, 17)
                    a_s_i = StB_K_Q_0_stb(code, gam_c, gam_s, gam_perm*M[i], gam_perm*N[i], gam_perm*Q[i], D, H, float(A_s_i), f_ck, alpha, eps_c2, eps_c2u, exp, delta_S, delta_K, f_yk, f_tk, Es, eps_su, 0.0, 0.0, 0.0, 19)

                    A_s_all[i, j] = float(A_s_i)
                    a_s_all[i, j] = max(float(a_s_i), 0.0)
        
        return A_s_all, a_s_all


    def calculate_required_reinforcement_cross_section(self, code, params_psf, params_concrete, params_reinf, wall_outputs, min_reinf):
        """ Calculates the required reinforcement area, method is py_StB by default
        Cross section internal forces are characteristic.
        """
        # params_psf
        gam_perm = float(params_psf['param_0'])
        #gam_tran = float(self.params_psf['param_1'])
        gam_c = float(params_psf['param_2'])
        gam_s = float(params_psf['param_3'])
    
        # params cross-section
        D = self.cross_section['D']*1000 # mm
        H = self.cross_section['H']
        #A = self.cross_section['S']*2

        # params concrete
        f_ck = float(params_concrete['param_0'])
        alpha = float(params_concrete['param_1'])
        eps_c2 = float(params_concrete['param_2'])/1000
        eps_c2u = float(params_concrete['param_3'])/1000
        exp = float(params_concrete['param_4'])
        delta_S = float(params_concrete['param_5'])
        delta_K = params_concrete['param_6']
        delta_K = delta_K + ' 0.0' if (len(delta_K.split())==1) else delta_K # append ' 0.0' if it is single

        # params reinf
        f_yk = float(params_reinf['param_0'])
        f_tk = float(params_reinf['param_1'])
        Es = float(params_reinf['param_2'])
        eps_su = float(params_reinf['param_3'])/1000
        RissP1 = float(params_reinf['param_4'])
        minBew = 1 if min_reinf else 0
        
        N = wall_outputs['N']
        M = wall_outputs['M']
        Q = wall_outputs['Q']

        dim_args = (code, gam_c, gam_s, gam_perm, M, N, Q, D, H, f_ck, alpha, eps_c2, eps_c2u, exp, delta_S, delta_K, f_yk, f_tk, Es, eps_su, RissP1, minBew)
        A_s, a_s = self.evaluate_py_StB(*dim_args)

        return A_s, a_s


    def evaluate_py_StB(self, code, gam_c, gam_s, gam_perm, Mi, Ni, Qi, D, H, f_ck, alpha, eps_c2, eps_c2u, exp, delta_S, delta_K, f_yk, f_tk, Es, eps_su, RissP1, minBew):
        """ Gets required reinforcement 
        This function will be called in pool by multiprocessing
        """
        A_s_i = StB_K_MN(code, gam_c, gam_s, gam_perm*Mi, gam_perm*Ni, Mi, Ni, D, H, 0.0, f_ck, alpha, eps_c2, eps_c2u, exp, delta_S, delta_K, f_yk, f_tk, Es, eps_su, RissP1, minBew, 17)
        a_s_i = StB_K_Q(code, gam_c, gam_s, gam_perm*Mi, gam_perm*Ni, gam_perm*Qi, D, H, float(A_s_i), f_ck, alpha, eps_c2, eps_c2u, exp, delta_S, delta_K, f_yk, f_tk, Es, eps_su, 0.0, 0.0, 0.0, 19)
        return float(A_s_i), max(float(a_s_i), 0.0)
        

    def calc_A_s(self, n, dia_string, D, H):
        """ Calculates A_s
        n: number of vertical bars
        dia_string: string for diameter of bars in mm. This can be 'xx' or 'Dxx'
        D: pile diameter in mm
        H: separation to edge in mm
        """
        D_reinf = D*1000 - 2*H  # mm
        try: # single bars
            dia = float(dia_string)   #'xx'
            A_s = (n*1/4*np.pi*dia**2) * 1e-2 # cm^2
            clearance = (np.pi*D_reinf/n - dia) * 1e-1 #cm
        except ValueError: # double bars
            dia = float(dia_string[1:])   #'Dxx'
            A_s = 2*(n*1/4*np.pi*dia**2) * 1e-2 # cm^2
            clearance = (np.pi*D_reinf/n - 2*dia) * 1e-1 #cm

        return (A_s, clearance)
        

    def calc_a_s(self, n_legs, dia_string, spacing, D, H):
        """ Calculates a_s
        n: number of vertical bars
        dia_string: string for diameter of bars in mm. This can be 'xx' or 'Dxx'
        D: pile diameter in mm
        H: separation to edge in mm
        """
        #D_reinf = D*1000 - 2*H # mm
        try: # single bars
            dia = float(dia_string)   #'xx'
            area = (1/4*np.pi*dia**2) * 1e-2 # cm^2
            a_s = area * n_legs * 100.0/spacing #cm^2/m
        except ValueError: # double bars
            dia = float(dia_string[1:])   #'Dxx'
            area = (1/4*np.pi*dia**2) * 1e-2 # cm^2
            a_s = area * n_legs * 100.0/spacing #cm^2/m

        return a_s


    def calc_weight_A_s(self, A_s, length, rho=7850):
        """ Calculates steel weight for a longitudinal segment
        rho: 7800 Kg/m^3
        A_s: cm^2
        length: m
        """
        return abs(A_s*1e-4 * length * rho) # Kg


    def calc_weight_a_s(self, a_s, length, D, H, rho=7850):
        """ Calculates steel weight for a shear segment
        rho: 7800 Kg/m^3
        """
        D_reinf = (D*1000 - 2*(H - 10))*0.001   # m
        perimeter = np.pi*D_reinf
        #volume = perimeter*length
        #weight = volume * a_s*1e-4 * rho
        weight = length * a_s*1e-4 * rho * perimeter #  *1/2?
        return abs(weight)   # Kg


    def get_weight_ratio(self, staggered_reinf_vertical_wall, staggered_reinf_shear_wall, wall_outputs_phases):
        """ Gets weight per meter long of pile
        """
        weight = 0.0
        weight_ratio = 0.0
        if wall_outputs_phases:
            wall_top = wall_outputs_phases[0]['y'][0]
            wall_toe = wall_outputs_phases[0]['y'][-1]
            for reinf_vertical in staggered_reinf_vertical_wall:
                weight += reinf_vertical['weight']
            for reinf_shear in staggered_reinf_shear_wall:
                weight += reinf_shear['weight']
            weight_ratio = weight/(wall_top - wall_toe)
        
        return abs(weight_ratio)
    
    
    def print_report(self, project_title, code, concrete_grade, concrete_param_names_per_code, params_concrete, reinf_grade, reinf_param_names, params_reinf, stress_strain, 
                     design_situation, psf_param_names_per_code, params_psf, wall_outputs_phases, percentage_N, staggered_reinf_vertical_wall, staggered_reinf_shear_wall, A_s, a_s):
        """ Prints out the report
        """
        try:
            MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
        except KeyError: # no project folder exists
            MONIMAN_OUTPUTS = '.'

        #project_title = 'Sample project'
        weight_ratio = self.get_weight_ratio(staggered_reinf_vertical_wall, staggered_reinf_shear_wall, wall_outputs_phases)
        # page 1
        report_page1 = Report()
        report_page1.add_project_info_pile(project_title, self.cross_section, weight_ratio)
        report_page1.add_table_cross_section_pile(self.cross_section)
        report_page1.add_table_conrete(concrete_grade, concrete_param_names_per_code[code], params_concrete)
        report_page1.add_table_reinf(reinf_grade, reinf_param_names, params_reinf)
        report_page1.add_table_psf(design_situation, psf_param_names_per_code[code], params_psf)
        report_page1.plot_stress_strain_curves(stress_strain)
        # page 2
        report_page2 = Report()
        report_page2.add_project_info_pile(project_title, self.cross_section, weight_ratio)
        A = self.cross_section['S']*2    # pile spacing
        if wall_outputs_phases:    # internal forces have been loaded
            report_page2.plot_wall_outputs(wall_outputs_phases, A, percentage_N)
        # page 3
        report_page3 = Report()
        report_page3.add_project_info_pile(project_title, self.cross_section, weight_ratio)
        if wall_outputs_phases:    # internal forces have been loaded
            report_page3.plot_staggered_reinf_vertical(staggered_reinf_vertical_wall, wall_outputs_phases[0]['y'], A_s)
            report_page3.plot_staggered_reinf_shear(staggered_reinf_shear_wall, wall_outputs_phases[0]['y'], a_s)
        # page 4
        report_page4 = Report()
        report_page4.add_project_info_pile(project_title, self.cross_section, weight_ratio)
        y = report_page4.add_table_staggered_reinf_vertical(staggered_reinf_vertical_wall)
        y = report_page4.add_table_staggered_reinf_shear(staggered_reinf_shear_wall, y)
        #print(y)

        # dim all pages
        try:    
            filename = os.path.join(MONIMAN_OUTPUTS, project_title + '.pdf')
            pp = PdfPages(filename)
            report_page1.fig.savefig(pp, format='pdf')
            report_page2.fig.savefig(pp, format='pdf')
            report_page3.fig.savefig(pp, format='pdf')
            report_page4.fig.savefig(pp, format='pdf')
            pp.close()
            # view report in Acrobat Reader
            cmd = [os.path.join(ACROBAT, r'Acrobat.exe')]
            cmd.append(filename)
            subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)
            
            return int(0)

        except PermissionError:
            return filename
        
        
    def print_report_separate_graphs(self, project_title, code, concrete_grade, concrete_param_names_per_code, params_concrete, reinf_grade, reinf_param_names, params_reinf, stress_strain, 
                     design_situation, psf_param_names_per_code, params_psf, wall_outputs_phases, percentage_N, staggered_reinf_vertical_wall, staggered_reinf_shear_wall, A_s, a_s):
        """ Prints out the report
        """
        try:
            MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
        except KeyError: # no project folder exists
            MONIMAN_OUTPUTS = '.'

        #project_title = 'Sample project'
        weight_ratio = self.get_weight_ratio(staggered_reinf_vertical_wall, staggered_reinf_shear_wall, wall_outputs_phases)
        # page 1
        report_page1 = Report()
        report_page1.add_project_info_pile(project_title, self.cross_section, weight_ratio)
        report_page1.add_table_cross_section_pile(self.cross_section)
        report_page1.add_table_conrete(concrete_grade, concrete_param_names_per_code[code], params_concrete)
        report_page1.add_table_reinf(reinf_grade, reinf_param_names, params_reinf)
        report_page1.add_table_psf(design_situation, psf_param_names_per_code[code], params_psf)
        report_page1.plot_stress_strain_curves(stress_strain)
        # page 2, 3, 4
        report_page234 = []
        for page_number in range(3):
            report_page = Report()
            report_page.add_project_info_pile(project_title, self.cross_section, weight_ratio)
            A = self.cross_section['S']*2    # pile spacing
            if wall_outputs_phases:    # internal forces have been loaded
                if page_number == 0:
                    report_page.plot_wall_outputs_separate_N(wall_outputs_phases, A, percentage_N)
                elif page_number == 1:
                    report_page.plot_wall_outputs_separate_M(wall_outputs_phases, A, staggered_reinf_vertical_wall)
                elif page_number == 2:
                    report_page.plot_wall_outputs_separate_Q(wall_outputs_phases, A, staggered_reinf_shear_wall)    
                report_page234.append(report_page)
        # page 5, 6
        report_page56 = []
        for page_number in range(2):
            report_page = Report()
            report_page.add_project_info_pile(project_title, self.cross_section, weight_ratio)
            if wall_outputs_phases:    # internal forces have been loaded
                if page_number == 0:
                    report_page.plot_staggered_reinf_vertical(staggered_reinf_vertical_wall, wall_outputs_phases[0]['y'], A_s, separate=True)
                elif page_number == 1:
                    report_page.plot_staggered_reinf_shear(staggered_reinf_shear_wall, wall_outputs_phases[0]['y'], a_s, separate=True)
                report_page56.append(report_page)
        # page 7
        report_page7 = Report()
        report_page7.add_project_info_pile(project_title, self.cross_section, weight_ratio)
        y = report_page7.add_table_staggered_reinf_vertical(staggered_reinf_vertical_wall)
        y = report_page7.add_table_staggered_reinf_shear(staggered_reinf_shear_wall, y)
        #print(y)

        # dim all pages
        try:    
            filename = os.path.join(MONIMAN_OUTPUTS, project_title + '.pdf')
            pp = PdfPages(filename)
            report_page1.fig.savefig(pp, format='pdf')
            for report_page in report_page234:
                report_page.fig.savefig(pp, format='pdf')
            for report_page in report_page56:
                report_page.fig.savefig(pp, format='pdf')
            report_page7.fig.savefig(pp, format='pdf')
            pp.close()
            # view report in Acrobat Reader
            cmd = [os.path.join(ACROBAT, r'Acrobat.exe')]
            cmd.append(filename)
            subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)
            
            return int(0)

        except PermissionError:
            return filename
        