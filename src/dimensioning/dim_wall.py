# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:13:32 2020

@author: nya
"""
import os
import sys
import win32com.client
import numpy as np
from scipy import interpolate
from collections import OrderedDict
import time
from tools.file_tools import write_traceback_to_file, get_file_reg_expr, combine_Ux_NMQ_files
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
#sys.path.insert(0, os.path.abspath(r'D:\Data\3Packages\Moniman'))   # for testing
from gui.gui_widget_Dim_wall import Ui_Form as DimForm
from gui.gui_all_dialogs_ui import Ui_Dialog
from gui.gui_main_matplotlib import MyStaticMplCanvasSubplots_Dim
from dimensioning.parameters import *
from dimensioning.pile import Pile
from dimensioning.barrette import Barrette

class Dim_wall(QtWidgets.QWidget):
    """ This class implements dimensioning tool in Plaxman
    """
    def __init__(self, form, project_title, cross_section_pile, cross_section_barrette, code=2, concrete_grade='', params_concrete={}, reinf_grade='', params_reinf={}, crack_width='no crack', min_reinf=False, design_situation='', params_psf={},
                percentage_N=100.0, wall_outputs_phases=[], A_s=None, a_s=None, A_s1=None, A_s2=None, a_s12=None, 
                bar_diameters_vertical=[], staggered_reinf_vertical_pile=[], bar_diameters_shear=[], staggered_reinf_shear_pile=[],
                staggered_reinf_vertical_barrette_A_s_1=[], staggered_reinf_vertical_barrette_A_s_2=[], staggered_reinf_shear_barrette=[]):
        """ Initializes Dim
        """
        super(Dim_wall, self).__init__()
        self.ui = DimForm()
        self.ui.setupUi(form)
        #print(self.ui.splitter.sizes())
        #self.ui.splitter.setSizes([500, 500]) # resize widgets' size around splitter
        #print(self.ui.splitter.sizes())
        self.dialog = Ui_Dialog()
        self.project_title = project_title

        # plot canvas for materials
        self.plot_layout1 = QtWidgets.QVBoxLayout(self.ui.widget)
        self.plot_canvas_mat = MyStaticMplCanvasSubplots_Dim(self.ui.widget, width=1, height=1, dpi=100, nrows=2, ncols=1)
        self.plot_layout1.addWidget(self.plot_canvas_mat)
        # plot canvas for cross-section of pile
        self.plot_layout2 = QtWidgets.QVBoxLayout(self.ui.widget_2)
        self.plot_canvas_cross_section_pile = MyStaticMplCanvasSubplots_Dim(self.ui.widget_2, width=1, height=1, dpi=100, nrows=1, ncols=1)
        self.plot_layout2.addWidget(self.plot_canvas_cross_section_pile)
        # plot canvas for cross-section of barrette
        self.plot_layout22 = QtWidgets.QVBoxLayout(self.ui.widget_5)
        self.plot_canvas_cross_section_barrette = MyStaticMplCanvasSubplots_Dim(self.ui.widget_5, width=1, height=1, dpi=100, nrows=1, ncols=1)
        self.plot_layout22.addWidget(self.plot_canvas_cross_section_barrette)
        # plot canvas for wall outputs (internal forces)
        self.plot_layout3 = QtWidgets.QVBoxLayout(self.ui.widget_3)
        self.plot_canvas_wall_output = MyStaticMplCanvasSubplots_Dim(self.ui.widget_3, width=1, height=1, dpi=100, nrows=1, ncols=3)
        self.plot_layout3.addWidget(self.plot_canvas_wall_output)
        # plot canvas for reinforcement staggering
        self.plot_layout4 = QtWidgets.QVBoxLayout(self.ui.widget_4)
        self.plot_canvas_reinf = MyStaticMplCanvasSubplots_Dim(self.ui.widget_4, width=1, height=1, dpi=100, nrows=1, ncols=2)
        self.plot_layout4.addWidget(self.plot_canvas_reinf)

        # concrete
        self.code = code # Eurocode 2 by default
        self.ui.comboBox.setCurrentIndex(self.code)
        self.concrete_grade = concrete_grade # concrete grade will be updated later
        self.concrete_param_names_per_code = (PARAM_NAMES_CODE_0, PARAM_NAMES_CODE_1, PARAM_NAMES_CODE_2, PARAM_NAMES_CODE_3)
        self.concrete_grade_per_code = (CONCRETE_GRADE_CODE_0, CONCRETE_GRADE_CODE_1, CONCRETE_GRADE_CODE_2, CONCRETE_GRADE_CODE_3)
        self.concrete_alpha_per_code = (CONCRETE_ALPHA_CODE_0, CONCRETE_ALPHA_CODE_1, CONCRETE_ALPHA_CODE_2, CONCRETE_ALPHA_CODE_3)
        self.concrete_epsilon_c2_per_code = (CONCRETE_EPSILON_C2_CODE_0, CONCRETE_EPSILON_C2_CODE_1, CONCRETE_EPSILON_C2_CODE_2, CONCRETE_EPSILON_C2_CODE_3)
        self.concrete_epsilon_c2u_per_code = (CONCRETE_EPSILON_C2U_CODE_0, CONCRETE_EPSILON_C2U_CODE_1, CONCRETE_EPSILON_C2U_CODE_2, CONCRETE_EPSILON_C2U_CODE_3)
        self.concrete_exp_per_code = (CONCRETE_EXP_CODE_0, CONCRETE_EXP_CODE_1, CONCRETE_EXP_CODE_2, CONCRETE_EXP_CODE_3)
        self.concrete_delta_alpha_pl_per_code = (CONCRETE_DELTA_ALPHA_PL_CODE_0, CONCRETE_DELTA_ALPHA_PL_CODE_1, CONCRETE_DELTA_ALPHA_PL_CODE_2, CONCRETE_DELTA_ALPHA_PL_CODE_3)
        self.concrete_unreinforced_per_code = (CONCRETE_UNREINFORCED_CODE_0, CONCRETE_UNREINFORCED_CODE_1, CONCRETE_UNREINFORCED_CODE_2, CONCRETE_UNREINFORCED_CODE_3)
        self.concrete_Ecm_per_code = (CONCRETE_E_CM_CODE_0, CONCRETE_E_CM_CODE_1, CONCRETE_E_CM_CODE_2, CONCRETE_E_CM_CODE_3)
        self.params_concrete = params_concrete

        # reinforcement
        self.reinf_grade = reinf_grade # steel grad will be udpated later
        self.reinf_grade_per_code = (REINF_CODE_0, REINF_CODE_1, REINF_CODE_2, REINF_CODE_3)
        self.reinf_f_tk_per_code = (REINF_F_TK_CODE_0, REINF_F_TK_CODE_1, REINF_F_TK_CODE_2, REINF_F_TK_CODE_3)
        self.reinf_E_per_code = (REINF_E_CODE_0, REINF_E_CODE_1, REINF_E_CODE_2, REINF_E_CODE_3)
        self.reinf_epsilon_su_per_code = (REINF_EPSILON_CU_CODE_0, REINF_EPSILON_CU_CODE_1, REINF_EPSILON_CU_CODE_2, REINF_EPSILON_CU_CODE_3)
        self.stress_strain = {}
        self.params_reinf = params_reinf

        # crack
        self.sigma_ds_per_code = (SIGMA_DS_CODE_0, SIGMA_DS_CODE_1, SIGMA_DS_CODE_2, SIGMA_DS_CODE_3)
        self.crack_width = crack_width   # no crack by default
        self.min_reinf = min_reinf  # no minimum reinforcement by default
        self.update_min_reinforcement(self.min_reinf)   # check/ uncheck check box for min_reinf

        # partial safety factors
        self.psf_load_case_per_code = (PSF_LOAD_CASES_CODE_0, PSF_LOAD_CASES_CODE_1, PSF_LOAD_CASES_CODE_2, PSF_LOAD_CASES_CODE_3)
        self.psf_param_names_per_code = (PSF_NAMES_CODE_0, PSF_NAMES_CODE_1, PSF_NAMES_CODE_2, PSF_NAMES_CODE_3)
        self.psf_gammaG_per_code = (PSF_GAMMA_G_CODE_0, PSF_GAMMA_G_CODE_1, PSF_GAMMA_G_CODE_2, PSF_GAMMA_G_CODE_3)
        self.psf_gammaQ_per_code = (PSF_GAMMA_Q_CODE_0, PSF_GAMMA_Q_CODE_1, PSF_GAMMA_Q_CODE_2, PSF_GAMMA_Q_CODE_3)
        self.psf_gammaC_per_code = (PSF_GAMMA_C_CODE_0, PSF_GAMMA_C_CODE_1, PSF_GAMMA_C_CODE_2, PSF_GAMMA_C_CODE_3)
        self.psf_gammaS_per_code = (PSF_GAMMA_S_CODE_0, PSF_GAMMA_S_CODE_1, PSF_GAMMA_S_CODE_2, PSF_GAMMA_S_CODE_3)
        self.design_situation = design_situation
        self.params_psf = params_psf

        # percentage of axial normal force used N
        self.percentage_N = percentage_N
        self.initialize_percentage_N()

        ## pile/barrettes cross-sections
        self.pile = Pile(**cross_section_pile)
        self.pile.initialize_cross_section(self.ui.tableWidget_4, self.plot_canvas_cross_section_pile)
        self.barrette = Barrette(**cross_section_barrette)
        self.barrette.initialize_cross_section(self.ui.tableWidget_7, self.plot_canvas_cross_section_barrette)

        self.wall_outputs_phases = wall_outputs_phases # internal forces used for dimensioning
        self.staggered_reinf_vertical_pile = staggered_reinf_vertical_pile # staggered vertical reinforcement for pile
        self.staggered_reinf_shear_pile = staggered_reinf_shear_pile # staggered vertical reinforcement for pile
        self.staggered_reinf_vertical_barrette_A_s_1 = staggered_reinf_vertical_barrette_A_s_1 # staggered vertical reinforcement As1 for barrette
        self.staggered_reinf_vertical_barrette_A_s_2 = staggered_reinf_vertical_barrette_A_s_2 # staggered vertical reinforcement As2 for barrette
        self.staggered_reinf_shear_barrette = staggered_reinf_shear_barrette # staggered vertical reinforcement for barrette

        self.initialize_table_concrete()  # only once

        self.initialize_table_reinforcement() # only once

        self.initialize_table_psf()   # only once
        # initialize reinf tables
        self.initialize_table_reinf_vertical(self.ui.tableWidget_5) # Pile vertical
        self.initialize_table_reinf_vertical(self.ui.tableWidget_8) # Barrette vertical
        self.initialize_table_reinf_vertical(self.ui.tableWidget_9) # Barrette vertical
        self.initialize_table_reinf_shear(self.ui.tableWidget_6)    # Pile shear
        self.initialize_table_reinf_shear(self.ui.tableWidget_10)   # Barrette shear

        # required reinforcement for pile
        self.A_s = A_s
        self.a_s = a_s
        # required reinforcement for barrette
        self.A_s1 = A_s1
        self.A_s2 = A_s2
        self.a_s12 = a_s12

        # staggered data
        self.bar_diameters_vertical = bar_diameters_vertical
        self.bar_diameters_shear = bar_diameters_shear

        # update code, if concrete_grade is not empty at start it will remain so
        self.update_code(self.code, self.concrete_grade=='')   
        self.update_crack_width(self.crack_width) # no crack by default

        # connect signals and update basic settings once
        self.connect_signals_to_slots()

        form.exec_()
        
    
    def initialize_percentage_N(self):
        """ Displays percentage of normal force used for calculation reinforcement
        """
        self.ui.lineEdit_5.setText(str(self.percentage_N))
        self.ui.lineEdit_6.setText(str(self.percentage_N))
        self.ui.lineEdit_5.setStyleSheet("background-color: rgb(242, 255, 116);\n")
        self.ui.lineEdit_6.setStyleSheet("background-color: rgb(242, 255, 116);\n")

        
    def initialize_table_concrete(self):
        """ Initializes table for concrete
        This function is called once when the object is constructed.
        """
        # fill the table headers
        self.ui.tableWidget.setRowCount(2)
        column_labels = self.concrete_param_names_per_code[self.code]
        self.ui.tableWidget.blockSignals(True)
        self.ui.tableWidget.setColumnCount(len(column_labels))
        self.ui.tableWidget.setHorizontalHeaderLabels(column_labels)
        # set color for custom cells
        for i in range(self.ui.tableWidget.columnCount()):
            self.ui.tableWidget.setItem(1, i, QtWidgets.QTableWidgetItem(''))
            custom_cell = self.ui.tableWidget.item(1, i)
            custom_cell.setBackground(QColor(242, 255, 116))
        self.ui.tableWidget.blockSignals(False)


    def initialize_table_reinforcement(self):
        """ Initializes table for reinforcement
        This function is called once when the object is constructed.
        """
        self.reinf_param_names = ['yield stress \n f_yk [MPa]', 'tens. strength \n f_tk [MPa]', 'Elastic modulus \n E [MPa]', 'max. strain \n \N{GREEK SMALL LETTER EPSILON}_s,u [\N{PER MILLE SIGN}]', 'with crack \n max. \N{GREEK SMALL LETTER SIGMA}_s [MPa]', 'with crack \n reinf. bar \n max. ds [mm]', 'with crack \n bar spacing \n max. s [mm]']
        # fill the table headers for steel only once
        self.ui.tableWidget_2.setRowCount(2)
        column_labels = self.reinf_param_names
        self.ui.tableWidget_2.setColumnCount(len(column_labels))
        self.ui.tableWidget_2.setHorizontalHeaderLabels(column_labels)
        # set color for custom cells
        for i in range(self.ui.tableWidget_2.columnCount()):
            self.ui.tableWidget_2.setItem(0, i, QtWidgets.QTableWidgetItem(''))
            self.ui.tableWidget_2.setItem(1, i, QtWidgets.QTableWidgetItem(''))
            custom_cell = self.ui.tableWidget_2.item(1, i)
            custom_cell.setBackground(QColor(242, 255, 116))


    def initialize_table_psf(self):
        """ Initializes table for PSF
        This function is called once when the object is constructed.
        """
        # fill the table headers
        self.ui.tableWidget_3.setRowCount(2)
        #column_labels = OrderedDict(sorted(self.psf_load_case_per_code[self.code].items())).values()
        column_labels = self.psf_param_names_per_code[self.code]
        self.ui.tableWidget_3.blockSignals(True)
        self.ui.tableWidget_3.setColumnCount(len(column_labels))
        self.ui.tableWidget_3.setHorizontalHeaderLabels(column_labels)
        # set color for custom cells
        for i in range(self.ui.tableWidget_3.columnCount()):
            self.ui.tableWidget_3.setItem(1, i, QtWidgets.QTableWidgetItem(''))
            custom_cell = self.ui.tableWidget_3.item(1, i)
            custom_cell.setBackground(QColor(242, 255, 116))
        self.ui.tableWidget_3.blockSignals(False)


    def initialize_table_reinf_vertical(self, table_widget):
        """ Initializes table for vertial reinforcement
        """
        n_row = 10
        table_widget.blockSignals(True)
        table_widget.setRowCount(n_row)
        column_labels = ['Level\n [m]', 'n\n [-]', 'Dia.\n [mm]', 'A_s \n [cm^2]', 'Clearance\n [cm]', 'Weight [Kg]']
        table_widget.setColumnCount(len(column_labels))
        table_widget.setHorizontalHeaderLabels(column_labels)

        n_column = len(column_labels)
        for row_i in range(n_row):
            for column_j in range(n_column-3):
                table_widget.setItem(row_i, column_j, QtWidgets.QTableWidgetItem(''))
                cell = table_widget.item(row_i, column_j)
                cell.setBackground(QColor(242, 255, 116))

        table_widget.blockSignals(False)


    def initialize_table_reinf_shear(self, table_widget):
        """ Initializes table for shear reinforcement
        """
        n_row = 10
        table_widget.blockSignals(True)
        table_widget.setRowCount(n_row)
        column_labels = ['Level\n [m]',  'dia.\n d [mm]', 'n legs\n [-]', 'spacing\n [cm]', 'a_s \n [cm^2/m]', 'Weight [Kg]']
        table_widget.setColumnCount(len(column_labels))
        table_widget.setHorizontalHeaderLabels(column_labels)

        n_column = len(column_labels)
        for row_i in range(n_row):
            for column_j in range(n_column-2):
                table_widget.setItem(row_i, column_j, QtWidgets.QTableWidgetItem(''))
                cell = table_widget.item(row_i, column_j)
                cell.setBackground(QColor(242, 255, 116))

        table_widget.blockSignals(False)


    def connect_signals_to_slots(self):
        """ Connects all signals to slots
        """
        self.ui.comboBox.currentIndexChanged.connect(self.update_code)  # code
        self.ui.comboBox_2.currentTextChanged.connect(self.update_concrete_grade)
        self.ui.comboBox_3.currentTextChanged.connect(self.update_reinf_grade)
        self.ui.comboBox_5.currentTextChanged.connect(self.update_crack_width)
        self.ui.tableWidget.cellChanged.connect(lambda row, column: self.update_with_custom_value_concrete(row, column))
        self.ui.tableWidget_2.cellChanged.connect(lambda row, column: self.update_with_custom_value_reinforcement(row, column))
        self.ui.checkBox.stateChanged.connect(lambda state_int: self.update_min_reinforcement(state_int==2))
        self.ui.comboBox_4.currentTextChanged.connect(self.update_design_situation)
        self.ui.tableWidget_3.cellChanged.connect(lambda row, column: self.update_with_custom_value_psf(row, column))
        self.ui.tableWidget_4.cellChanged.connect(lambda row, column: self.update_with_custom_cross_section_pile(row, column))       # update cross-section pile
        self.ui.tableWidget_7.cellChanged.connect(lambda row, column: self.update_with_custom_cross_section_barrette(row, column))   # update cross-section barrette
        push_buttons = [self.ui.pushButton, self.ui.pushButton_2, self.ui.pushButton_3, self.ui.pushButton_4, self.ui.pushButton_5, self.ui.pushButton_6, 
                        self.ui.pushButton_9, self.ui.pushButton_10, self.ui.pushButton_11, self.ui.pushButton_12]
        for push_button in push_buttons:
            push_button.setAutoDefault(False)
            push_button.setDefault(False)
        # percentage of N
        self.ui.lineEdit_5.editingFinished.connect(lambda : self.set_percentage_N(self.ui.lineEdit_5.text()))
        self.ui.lineEdit_6.editingFinished.connect(lambda : self.set_percentage_N(self.ui.lineEdit_6.text()))

        self.ui.pushButton.clicked.connect(self.load_wall_internal_forces_pile)      # load wall outputs for pile
        self.ui.pushButton_11.clicked.connect(self.load_wall_internal_forces_pile_from_Plaxis2D_report_generator)      # load wall outputs form Plaxis2D report generator for pile
        self.ui.pushButton_4.clicked.connect(self.load_wall_internal_forces_barrette)    # load wall outputs for barrette
        self.ui.pushButton_12.clicked.connect(self.load_wall_internal_forces_barrette_from_Plaxis2D_report_generator)      # load wall outputs form Plaxis2D report generator for barrette
        self.ui.pushButton_2.clicked.connect(self.calculate_required_reinforcement_pile) # pile
        self.ui.pushButton_5.clicked.connect(self.calculate_required_reinforcement_barrette) # barrette
        self.ui.lineEdit.editingFinished.connect(lambda: self.fill_table_reinf_staggering_vertical_pile(fill_anyway=True))
        self.ui.lineEdit_2.editingFinished.connect(lambda: self.fill_table_reinf_staggering_shear_pile(fill_anyway=True))
        self.ui.lineEdit_3.editingFinished.connect(lambda: self.fill_table_reinf_staggering_vertical_barrette_A_s_1(self.ui.tableWidget_9, fill_anyway=True))
        self.ui.lineEdit_3.editingFinished.connect(lambda: self.fill_table_reinf_staggering_vertical_barrette_A_s_2(self.ui.tableWidget_8, fill_anyway=True))
        self.ui.lineEdit_4.editingFinished.connect(lambda: self.fill_table_reinf_staggering_shear_barrette(fill_anyway=True))
        # vertical reinf table for staggering
        self.ui.tableWidget_5.cellChanged.connect(lambda row, col: self.update_table_reinf_staggering_vertical_pile(row, col))
        self.ui.tableWidget_6.cellChanged.connect(lambda row, col: self.update_table_reinf_staggering_shear_pile(row, col))
        self.ui.tableWidget_8.cellChanged.connect(lambda row, col: self.update_table_reinf_staggering_vertical_barrette_A_s2(row, col, self.ui.tableWidget_8))
        self.ui.tableWidget_9.cellChanged.connect(lambda row, col: self.update_table_reinf_staggering_vertical_barrette_A_s1(row, col, self.ui.tableWidget_9))
        self.ui.tableWidget_10.cellChanged.connect(lambda row, col: self.update_table_reinf_staggering_shear_barrette(row, col))
        # change plot styles between 'All selected phases' and 'Envelop'
        self.ui.comboBox_6.currentTextChanged.connect(lambda current_text: self.update_plot_reinf_vertical(current_text=='Envelope'))
        self.ui.comboBox_6.currentTextChanged.connect(lambda current_text: self.update_plot_reinf_shear(current_text=='Envelope'))
        # report generation
        self.ui.pushButton_3.clicked.connect(self.generate_report_pile) # print report pile
        self.ui.pushButton_6.clicked.connect(self.generate_report_barrette) # print report pile
        # write file
        self.ui.pushButton_7.clicked.connect(self.write_file_reinf_results_pile)   # write file pile
        self.ui.pushButton_8.clicked.connect(self.write_file_reinf_results_barrette)   # write file barrette
        # send email
        self.ui.pushButton_9.clicked.connect(self.send_email_data_pile)   # send email file pile
        self.ui.pushButton_10.clicked.connect(self.send_email_data_barrette)   # send email file barrette

        # load saved data when
        self.ui.tabWidget.currentChanged.connect(lambda tab_idx: self.load_saved_data(tab_idx))


    def set_percentage_N(self, text):
        """ Sets value for the percentage of normal force used
        """
        try:
            value = float(text)
            self.percentage_N = value
            print('{0:.2f} % of the normal force is used in the calculation'.format(value))

        except:
            pass

    def load_saved_data(self, tab_idx):
        """ Loads saved data
        """
        if tab_idx == 1:
            self.load_saved_data_pile()
        elif tab_idx == 2:
            self.load_saved_data_barrette()


    def load_saved_data_pile(self):
        """ Loads saved data pile
        """
        try:
            if self.wall_outputs_phases:
                self.plot_wall_internal_forces_pile()
            if self.A_s is not None:
                self.display_required_reinforcement_pile()
            if self.bar_diameters_vertical:
                bar_diameters = ', '.join(self.bar_diameters_vertical)
                self.ui.lineEdit.setText(bar_diameters)
            if self.staggered_reinf_vertical_pile:
                self.fill_table_reinf_staggering_vertical_pile_saved_values()
            if self.bar_diameters_shear:
                bar_diameters = ', '.join(self.bar_diameters_shear)
                self.ui.lineEdit_2.setText(bar_diameters)
            if self.staggered_reinf_shear_pile:
                self.fill_table_reinf_staggering_shear_pile_saved_values()
        except:
            pass


    def load_saved_data_barrette(self):
        """ Loads saved data pile
        """
        try:
            if self.wall_outputs_phases:
                self.plot_wall_internal_forces_barrette()
            if self.A_s1 is not None:
                self.display_required_reinforcement_barrette()
            if self.bar_diameters_vertical:
                bar_diameters = ', '.join(self.bar_diameters_vertical)
                self.ui.lineEdit_3.setText(bar_diameters)
            if self.staggered_reinf_vertical_barrette_A_s_1:
                self.fill_table_reinf_staggering_vertical_barrette_A_s_1_saved_values(self.ui.tableWidget_9)
            if self.staggered_reinf_vertical_barrette_A_s_2:
                self.fill_table_reinf_staggering_vertical_barrette_A_s_2_saved_values(self.ui.tableWidget_8)
            if self.bar_diameters_shear:
                bar_diameters = ', '.join(self.bar_diameters_shear)
                self.ui.lineEdit_4.setText(bar_diameters)
            if self.staggered_reinf_shear_barrette:
                self.fill_table_reinf_staggering_shear_barrette_saved_values()
        except:
            pass


    def update_min_reinforcement(self, check_state):
        """ Updates minimum reinforcement parameter
        """
        if check_state is True:
            self.min_reinf = True
            self.ui.checkBox_4.setCheckState(2)
        else:
            self.min_reinf = False
            self.ui.checkBox_4.setCheckState(0)


    def update_code(self, ind, should_initialize_concrete_grade=True):
        """ Updates code and values in concrete table
        ind: integer number for code
        """
        self.code = ind

        # fill available concrete grades for the selected code
        self.ui.comboBox_2.blockSignals(True) # change in concrete grade will not emit signals
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.insertItems(0, OrderedDict(sorted(self.concrete_grade_per_code[self.code].items())).keys())
        self.ui.comboBox_2.blockSignals(False)
        # fill available reinforcement grades for the selected code
        self.ui.comboBox_3.blockSignals(True) # change in reinf grade will not emit signals
        self.ui.comboBox_3.clear()
        self.ui.comboBox_3.insertItems(0, OrderedDict(sorted(self.reinf_grade_per_code[self.code].items())).keys())
        self.ui.comboBox_3.blockSignals(False)
        # fill available load cases for the selected code
        self.ui.comboBox_4.blockSignals(True) # change in load case will not emit signals
        self.ui.comboBox_4.clear()
        #self.ui.comboBox_4.insertItems(0, OrderedDict(sorted(self.psf_load_case_per_code[self.code].items())).keys())
        self.ui.comboBox_4.insertItems(0, self.psf_load_case_per_code[self.code])
        self.ui.comboBox_4.blockSignals(False)

        # fill in table headers for concrete & psf
        self.update_parameter_names_concrete()
        self.update_parameter_names_psf()

        # fill in table values for concrete
        if should_initialize_concrete_grade:
            self.concrete_grade = self.ui.comboBox_2.currentText()
            self.fill_table_concrete()
        else: # show saved concrete_grade on combobox
            self.set_combobox_item(self.ui.comboBox_2, self.concrete_grade)
            self.fill_table_concrete_saved_values()

        # fill in table values for reinforcement
        if should_initialize_concrete_grade:
            self.reinf_grade = self.ui.comboBox_3.currentText()
            self.fill_table_reinforcement()
        else:   # show saved reinf_grade on combobox
            self.set_combobox_item(self.ui.comboBox_3, self.reinf_grade)
            self.fill_table_reinforcement_saved_values()

        # fill in table values for psf
        if should_initialize_concrete_grade:
            self.design_situation = self.ui.comboBox_4.currentText()
            self.fill_table_psf()
        else:
            self.set_combobox_item(self.ui.comboBox_4, self.design_situation)
            self.fill_table_psf_saved_values()
        
        # fill crack width
        self.set_combobox_item(self.ui.comboBox_5, self.crack_width)

        # read and store parameter values
        self.read_parameters_concrete()
        self.read_parameters_reinforcement()
        self.read_parameters_psf()

        # get stress-strain curve and plot it
        self.get_stress_strain_concrete()
        self.get_stress_strain_reinforcement()


    def set_combobox_item(self, combobox, item_text):
        """ Sets current index of combobox
        """
        for idx in range(combobox.count()):
                if combobox.itemText(idx) == item_text:
                    combobox.setCurrentIndex(idx)


    def update_parameter_names_concrete(self):
        """ Updates table headers per code
        """
        # fill the table headers
        column_labels = self.concrete_param_names_per_code[self.code]
        self.ui.tableWidget.blockSignals(True)
        self.ui.tableWidget.setHorizontalHeaderLabels(column_labels)
        self.ui.tableWidget.blockSignals(False)


    def update_parameter_names_psf(self):
        """ Updates table headers per code
        """
        # fill the table headers
        column_labels = self.psf_param_names_per_code[self.code]
        self.ui.tableWidget_3.blockSignals(True)
        self.ui.tableWidget_3.setHorizontalHeaderLabels(column_labels)
        self.ui.tableWidget_3.blockSignals(False)


    def update_concrete_grade(self, concrete_grade):
        """ Updates concrete grade
        concrete_grade: text for concrete grade
        """
        if concrete_grade != '':
            # fill in table values
            self.concrete_grade = concrete_grade
            self.fill_table_concrete()

            # read and store parameter values
            self.read_parameters_concrete()

            # get stress-strain curve and plot it
            self.get_stress_strain_concrete()


    def fill_table_concrete(self):
        """ Fills concrete parameters in table
        The coded values are overloaded by custom values if any
        """
        self.ui.tableWidget.blockSignals(True)
        # fill in default values defined in the code
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(self.concrete_grade_per_code[self.code][self.concrete_grade])))
        self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.concrete_alpha_per_code[self.code][self.concrete_grade])))
        self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(self.concrete_epsilon_c2_per_code[self.code][self.concrete_grade])))
        self.ui.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(str(self.concrete_epsilon_c2u_per_code[self.code][self.concrete_grade])))
        self.ui.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(str(self.concrete_exp_per_code[self.code][self.concrete_grade])))
        self.ui.tableWidget.setItem(0, 5, QtWidgets.QTableWidgetItem(str(self.concrete_delta_alpha_pl_per_code[self.code][self.concrete_grade])))
        self.ui.tableWidget.setItem(0, 6, QtWidgets.QTableWidgetItem(str(self.concrete_unreinforced_per_code[self.code][self.concrete_grade])))
        self.ui.tableWidget.setItem(0, 7, QtWidgets.QTableWidgetItem(str(self.concrete_Ecm_per_code[self.code][self.concrete_grade])))

        # check and fill in custom values if any
        for i in range(self.ui.tableWidget.columnCount()):
            custom_cell = self.ui.tableWidget.item(1, i)
            if custom_cell.text() != '': # no empty
                self.ui.tableWidget.setItem(0, i, QtWidgets.QTableWidgetItem(custom_cell.text()))

        self.ui.tableWidget.blockSignals(False)


    def fill_table_concrete_saved_values(self):
        """ Fills saved concrete parameters in table
        The coded values are overloaded by custom values if any
        """
        self.ui.tableWidget.blockSignals(True)
        # fill in saved values in the code
        for i in range(self.ui.tableWidget.columnCount()):
            value = self.params_concrete['param_' + str(i)]
            self.ui.tableWidget.setItem(0, i, QtWidgets.QTableWidgetItem(str(value)))
        self.ui.tableWidget.blockSignals(False)


    def fill_table_reinforcement(self):
        """ Fills reinforcement parameters in table
        The coded values are overloaded by custom values if any
        """
        self.ui.tableWidget_2.blockSignals(True)
        self.ui.tableWidget_2.setItem(0, 0, QtWidgets.QTableWidgetItem(str(self.reinf_grade_per_code[self.code][self.reinf_grade])))
        self.ui.tableWidget_2.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.reinf_f_tk_per_code[self.code][self.reinf_grade])))
        self.ui.tableWidget_2.setItem(0, 2, QtWidgets.QTableWidgetItem(str(self.reinf_E_per_code[self.code][self.reinf_grade])))
        self.ui.tableWidget_2.setItem(0, 3, QtWidgets.QTableWidgetItem(str(self.reinf_epsilon_su_per_code[self.code][self.reinf_grade])))
        # check and fill in custom values if any
        for i in range(self.ui.tableWidget_2.columnCount()):
            custom_cell = self.ui.tableWidget_2.item(1, i)
            if custom_cell.text() != '': # no empty
                self.ui.tableWidget_2.setItem(0, i, QtWidgets.QTableWidgetItem(custom_cell.text()))

        self.ui.tableWidget_2.blockSignals(False)


    def fill_table_reinforcement_saved_values(self):
        """ Fills saved reinforcement parameters in table
        The coded values are overloaded by custom values if any
        """
        self.ui.tableWidget_2.blockSignals(True)
        # fill in saved values in the code
        for i in range(self.ui.tableWidget_2.columnCount()):
            value = self.params_reinf['param_' + str(i)]
            self.ui.tableWidget_2.setItem(0, i, QtWidgets.QTableWidgetItem(str(value)))
        self.ui.tableWidget_2.blockSignals(False)


    def fill_table_psf(self):
        """ Fills psf parameters in table
        The coded values are overloaded by custom values if any
        """
        self.ui.tableWidget_3.blockSignals(True)
        self.ui.tableWidget_3.setItem(0, 0, QtWidgets.QTableWidgetItem(str(self.psf_gammaG_per_code[self.code][self.design_situation])))
        self.ui.tableWidget_3.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.psf_gammaQ_per_code[self.code][self.design_situation])))
        self.ui.tableWidget_3.setItem(0, 2, QtWidgets.QTableWidgetItem(str(self.psf_gammaC_per_code[self.code][self.design_situation])))
        self.ui.tableWidget_3.setItem(0, 3, QtWidgets.QTableWidgetItem(str(self.psf_gammaS_per_code[self.code][self.design_situation])))
        # check and fill in custom values if any
        for i in range(self.ui.tableWidget_3.columnCount()):
            custom_cell = self.ui.tableWidget_3.item(1, i)
            if custom_cell.text() != '': # no empty
                self.ui.tableWidget_3.setItem(0, i, QtWidgets.QTableWidgetItem(custom_cell.text()))

        self.ui.tableWidget_3.blockSignals(False)


    def fill_table_psf_saved_values(self):
        """ Fills psf parameters in table
        The coded values are overloaded by custom values if any
        """
        self.ui.tableWidget_3.blockSignals(True)
        # fill in saved values in the code
        for i in range(self.ui.tableWidget_3.columnCount()):
            value = self.params_psf['param_' + str(i)]
            self.ui.tableWidget_3.setItem(0, i, QtWidgets.QTableWidgetItem(str(value)))
        self.ui.tableWidget_3.blockSignals(False)
    

    def update_with_custom_value_concrete(self, row, column):
        """ Updates a custom value for concrete parameter
        column: integer for column number of concrete table
        """
        if int(row) == 1:
            text = self.ui.tableWidget.item(row, column).text()
            if text != '':
                try:
                    value = float(text)
                    #print('value: ', value)
                    self.ui.tableWidget.setItem(0, column, QtWidgets.QTableWidgetItem(str(value)))
                    # read and store parameter values
                    self.read_parameters_concrete()
                    # get stress-strain curve and plot it
                    self.get_stress_strain_concrete()

                except ValueError:
                    self.dialog.show_message_box('Error', 'Please check if the value you entered are correct!')

            else: # text is empty, set back coded values
                self.update_concrete_grade(self.concrete_grade)


    def update_with_custom_value_reinforcement(self, row, column):
        """ Updates a custom value for reinf parameter
        column: integer for column number of reinf table
        """
        if int(row) == 1:
            text = self.ui.tableWidget_2.item(row, column).text()
            if text != '':
                try:
                    value = float(text)
                    #print('value: ', value)
                    self.ui.tableWidget_2.setItem(0, column, QtWidgets.QTableWidgetItem(str(value)))
                    # read and store parameter values
                    self.read_parameters_reinforcement()
                    # get stress-strain curve and plot it
                    self.update_crack_width(self.crack_width)
                    self.get_stress_strain_reinforcement()

                except ValueError:
                    self.dialog.show_message_box('Error', 'Please check if the value you entered are correct!')

            else: # text is empty, set back coded values
                self.update_reinf_grade(self.reinf_grade)


    def update_with_custom_value_psf(self, row, column):
        """ Updates a custom value for psf parameter
        column: integer for column number of reinf table
        """
        if int(row) == 1:
            text = self.ui.tableWidget_3.item(row, column).text()
            if text != '':
                try:
                    value = float(text)
                    #print('value: ', value)
                    self.ui.tableWidget_3.setItem(0, column, QtWidgets.QTableWidgetItem(str(value)))
                    # read and store parameter values
                    self.read_parameters_psf()

                except ValueError:
                    self.dialog.show_message_box('Error', 'Please check if the value you entered are correct!')

            else: # text is empty, set back coded values
                self.update_design_situation(self.design_situation)


    def update_with_custom_cross_section_pile(self, row, column):
        """ Updates a custom value for pile cross-section
        column: integer for column number of reinf table
        """
        #print('update_cross_section is called')
        if int(row) == 0:
            text = self.ui.tableWidget_4.item(row, column).text()
            if text != '':
                try:
                    value = float(text)
                    #print('value: ', value)
                    # read and store parameter values
                    if column == 0:
                        self.pile.cross_section['D'] = value
                    elif column == 1:
                        self.pile.cross_section['H'] = value
                    elif column == 2:
                        self.pile.cross_section['S'] = value/2
                    self.plot_canvas_cross_section_pile.plot_cross_section_pile(self.pile.cross_section['D'], self.pile.cross_section['H'])

                    # replot internal forces
                    self.plot_wall_internal_forces_pile()

                    ## (re)calcualte the required reinforcement if wall outputs have been loaded
                    #if self.wall_outputs_phases:
                    #    self.calculate_required_reinforcement_pile()

                except ValueError:
                    self.dialog.show_message_box('Error', 'Please check if the value you entered are correct!')

            else: # text is empty, set back default values
                self.pile.initialize_cross_section(self.ui.tableWidget_4, self.plot_canvas_cross_section_pile)


    def update_with_custom_cross_section_barrette(self, row, column):
        """ Updates a custom value for pile cross-section
        column: integer for column number of reinf table
        """
        #print('update_cross_section is called')
        if int(row) == 0:
            text = self.ui.tableWidget_7.item(row, column).text()
            if text != '':
                try:
                    value = float(text)
                    #print('value: ', value)
                    # read and store parameter values
                    if column == 0:
                        self.barrette.cross_section['D'] = value
                    elif column == 1:
                        self.barrette.cross_section['BT'] = value
                    elif column == 2:
                        self.barrette.cross_section['B'] = value
                    elif column == 3:
                        self.barrette.cross_section['H1'] = value
                    elif column == 4:
                        self.barrette.cross_section['H2'] = value
                    D = self.barrette.cross_section['D']
                    BT = self.barrette.cross_section['BT']
                    B = self.barrette.cross_section['B']
                    H1 = self.barrette.cross_section['H1']
                    H2 = self.barrette.cross_section['H2']
                    self.plot_canvas_cross_section_barrette.plot_cross_section_barrette(D, BT, B, H1, H2)

                    # replot internal forces
                    self.plot_wall_internal_forces_barrette()

                    ## (re)calcualte the required reinforcement if wall outputs have been loaded
                    #if self.wall_outputs_phases:
                    #    self.calculate_required_reinforcement_barrette()

                except ValueError:
                    self.dialog.show_message_box('Error', 'Please check if the value you entered are correct!')

            else: # text is empty, set back default values
                self.barrette.initialize_cross_section(self.ui.tableWidget_7, self.plot_canvas_cross_section_barrette)

    def update_design_situation(self, design_situation):
        """ Updates design situation
        """
        # fill in table values
        self.design_situation = design_situation
        self.fill_table_psf()

        # read and store parameter values
        self.read_parameters_psf()


    def update_reinf_grade(self, reinf_grade):
        """ Updates reinf grade
        reinf_grade: text for reinforcement grade
        """
        # fill in table values
        self.reinf_grade = reinf_grade
        self.fill_table_reinforcement()

        # read and store parameter values
        self.read_parameters_reinforcement()

        # get stress-strain curve and plot it
        self.get_stress_strain_reinforcement(crack_width=None)


    def update_crack_width(self, crack_width):
        """ Updates max. sigma_s depending on crack width
        crack_width: text for the crack width
        """
        self.crack_width = crack_width
        self.ui.tableWidget_2.blockSignals(True)
        if crack_width != 'no crack':
            if self.ui.tableWidget_2.item(0, 5).text() == '':
                self.ui.tableWidget_2.setItem(0, 5, QtWidgets.QTableWidgetItem(str(28.0)))
            if self.ui.tableWidget_2.item(0, 6).text() == '':
                self.ui.tableWidget_2.setItem(0, 6, QtWidgets.QTableWidgetItem(str(200.0)))

            # calculate maximum sigma_s by interpolating prescribed data
            ds = float(self.ui.tableWidget_2.item(0, 5).text())
            s = float(self.ui.tableWidget_2.item(0, 6).text())
            sigma_ds_interp = self.sigma_ds_per_code[self.code]['sigma']
            ds_interp = self.sigma_ds_per_code[self.code][crack_width]
            sigma1_interp = interpolate.interp1d(ds_interp, sigma_ds_interp)
            sigma1 = sigma1_interp(ds)
            sigma_s_interp = SIGMA_S['sigma']
            s_interp = SIGMA_S[crack_width]
            sigma2_interp = interpolate.interp1d(s_interp, sigma_s_interp)
            sigma2 = sigma2_interp(s)
            sigma = max(sigma1, sigma2)

            self.ui.tableWidget_2.setItem(0, 4, QtWidgets.QTableWidgetItem(str(sigma)))

        else:   # no crack
            if self.ui.tableWidget_2.columnCount() > 4:
                self.ui.tableWidget_2.setItem(0, 4, QtWidgets.QTableWidgetItem(str(0.0)))
                self.ui.tableWidget_2.setItem(0, 5, QtWidgets.QTableWidgetItem(str('')))
                self.ui.tableWidget_2.setItem(0, 6, QtWidgets.QTableWidgetItem(str('')))

        # store values
        self.read_parameters_reinforcement()

        self.ui.tableWidget_2.blockSignals(False)


    def read_parameters_concrete(self):
        """ Reads and stores parameter values from concrete table
        """
        params_concrete = OrderedDict()
        for i in range(self.ui.tableWidget.columnCount()):
            params_concrete['param_' + str(i)] = self.ui.tableWidget.item(0, i).text()
        
        self.params_concrete = params_concrete
        #print(params_concrete)


    def read_parameters_reinforcement(self):
        """ Reads and stores parameter values from reinforcement table
        """
        params_reinf = OrderedDict()
        for i in range(self.ui.tableWidget_2.columnCount()):
            if self.ui.tableWidget_2.item(0, i): # is not None
                params_reinf['param_' + str(i)] = self.ui.tableWidget_2.item(0, i).text()
        
        self.params_reinf = params_reinf
        #print(params_reinf)


    def read_parameters_psf(self):
        """ Reads and stores parameter values from psf table
        """
        params_psf = OrderedDict()
        for i in range(self.ui.tableWidget_3.columnCount()):
            if self.ui.tableWidget_3.item(0, i): # is not None
                params_psf['param_' + str(i)] = self.ui.tableWidget_3.item(0, i).text()
        
        self.params_psf = params_psf
        #print(params_psf)


    def get_stress_strain_concrete(self):
        """ Calculates and plots stress-strain curve for concrete
        """
        #Ecm = float(self.params_concrete['param_7'])
        epsilon_c2 = float(self.params_concrete['param_2'])
        epsilon_c2u = float(self.params_concrete['param_3'])
        f_ck = float(self.params_concrete['param_0'])
        alpha = float(self.params_concrete['param_1'])
        exp = float(self.params_concrete['param_4'])

        Ecm_i = 0.0
        Ecm_range = [Ecm_i]
        #while Ecm_i < epsilon_c2u:
        while Ecm_i < 2.0:
            Ecm_i += epsilon_c2/25
            Ecm_range.append(Ecm_i)
        Ecm_range.append(epsilon_c2u) # the last strain point

        f_ck_max = f_ck*alpha
        f_ck_i = f_ck_max
        f_ck_range = [f_ck_i]
        for Ecm_i in reversed(Ecm_range[:-1]):
            f_ck_i = f_ck_max * (1.0 - ((epsilon_c2 - Ecm_i)/epsilon_c2)**exp)
            f_ck_range.append(f_ck_i)
        
        f_ck_range.reverse() # reverse order
        #print(Ecm_range)
        #print(f_ck_range)
        self.plot_canvas_mat.plot_stress_strain_material(Ecm_range, f_ck_range, index=0)
        self.stress_strain['Ecm_range'] = Ecm_range
        self.stress_strain['f_ck_range'] = f_ck_range


    def get_stress_strain_reinforcement(self, crack_width=None):
        """ Calculates and plots stress-strain curve for reinforcement
        """
        epsilon_su = float(self.params_reinf['param_3'])
        f_tk = float(self.params_reinf['param_1'])
        f_yk = float(self.params_reinf['param_0'])
        E = float(self.params_reinf['param_2'])

        f_yk_range = [0, f_yk, f_tk]
        epsilon_range = [0, f_yk/E*1000, epsilon_su]
        self.plot_canvas_mat.plot_stress_strain_material(epsilon_range, f_yk_range, index=1)
        self.stress_strain['epsilon_range'] = epsilon_range
        self.stress_strain['f_yk_range'] = f_yk_range



    def load_wall_internal_forces_pile_from_Plaxis2D_report_generator(self):
        """ Loads internal forces of wall from Plaxis2D report generator
        """
        try:
            MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
        except KeyError: # no project folder exists
            MONIMAN_OUTPUTS = '.'

        try:
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            data_dir = QtWidgets.QFileDialog.getExistingDirectory(QtWidgets.QFileDialog(), 'Select the folder Report from Plaxis2D report generator', MONIMAN_OUTPUTS)

            # search for Plaxis2D report generated files and convert to the format that Moniman uses: ux, N, M, Q
            data_files_ux = get_file_reg_expr(os.path.join(data_dir,'*Table of total displacements.txt'))
            data_files_NMQ = get_file_reg_expr(os.path.join(data_dir,'*Table of plate force envelopes.txt'))
            x_coord_wall = float(self.ui.lineEdit_7.text())
            data_files = combine_Ux_NMQ_files(data_files_ux, data_files_NMQ, x_coord_wall)    # combine ux with NMQ and save to disc

            # use data_dir for printing out the report
            sys.modules['moniman_paths']['MONIMAN_OUTPUTS'] = data_dir

            # clear all data
            self.wall_outputs_phases.clear()
            # read data in for each of the selected phases
            for data_file in data_files:
                data = np.loadtxt(data_file.replace('/','\\'), skiprows=1)
                # sort after y-axis
                columnIndex = 0 # y
                data = data[data[:, columnIndex].argsort()]

                # store internal forces
                wall_outputs = {} # wall outputs of the concerned phase
                wall_outputs['y'] = data[:, 0]
                wall_outputs['Ux'] = data[:, 1]
                data[:, 2][np.where(data[:, 2] < 0.0)] = data[:, 2][np.where(data[:, 2] < 0.0)]*self.percentage_N/100
                wall_outputs['N'] = data[:, 2]
                wall_outputs['M'] = data[:, 3]
                wall_outputs['Q'] = data[:, 4]
                self.wall_outputs_phases.append(wall_outputs)

            # plot internal forces
            self.plot_wall_internal_forces_pile()

        except:
            self.dialog.show_message_box('Error', 'Please check the Report folder or the given x-coordinate of wall!')


    def load_wall_internal_forces_pile(self):
        """ Loads internal forces of wall
        """
        try:
            MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
        except KeyError: # no project folder exists
            MONIMAN_OUTPUTS = '.'

        try:
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            data_files, _ = QtWidgets.QFileDialog.getOpenFileNames(QtWidgets.QFileDialog(), 'Select data for one or more calculation phases', MONIMAN_OUTPUTS)

            # clear all data
            self.wall_outputs_phases.clear()
            # read data in for each of the selected phases
            for data_file in data_files:
                data = np.loadtxt(data_file.replace('/','\\'), skiprows=1)
                # sort after y-axis
                columnIndex = 0 # y
                data = data[data[:, columnIndex].argsort()]

                # store internal forces
                wall_outputs = {} # wall outputs of the concerned phase
                wall_outputs['y'] = data[:, 0]
                wall_outputs['Ux'] = data[:, 1]
                data[:, 2][np.where(data[:, 2] < 0.0)] = data[:, 2][np.where(data[:, 2] < 0.0)]*self.percentage_N/100
                wall_outputs['N'] = data[:, 2]
                wall_outputs['M'] = data[:, 3]
                wall_outputs['Q'] = data[:, 4]
                self.wall_outputs_phases.append(wall_outputs)

            # plot internal forces
            self.plot_wall_internal_forces_pile()

        except:
            self.dialog.show_message_box('Error', 'Please select the correct data file(s)!')


    def plot_wall_internal_forces_pile(self):
        """ Plots wall internal forces
        """
        A = self.pile.cross_section['S']*2    # pile spacing
        self.ui.toolBox.setCurrentIndex(1)
        self.plot_canvas_wall_output.axes[0].cla()
        self.plot_canvas_wall_output.axes[1].cla()
        self.plot_canvas_wall_output.axes[2].cla()
        for wall_outputs in self.wall_outputs_phases:
            self.plot_canvas_wall_output.plot_wall_output(wall_outputs['y'], wall_outputs['N'], A, index=0, clear=False)
            self.plot_canvas_wall_output.plot_wall_output(wall_outputs['y'], wall_outputs['M'], A, index=1, clear=False)
            #self.plot_canvas_wall_output.plot_wall_output(wall_outputs['y'], wall_outputs['M'], A, index=1, clear=False, staggered_reinf=self.staggered_reinf_vertical_pile)
            self.plot_canvas_wall_output.plot_wall_output(wall_outputs['y'], wall_outputs['Q'], A, index=2, clear=False)
            #self.plot_canvas_wall_output.plot_wall_output(wall_outputs['y'], wall_outputs['Q'], A, index=2, clear=False, staggered_reinf=self.staggered_reinf_shear_pile)


    def load_wall_internal_forces_barrette_from_Plaxis2D_report_generator(self):
        """ Loads internal forces of wall from Plaxis2D report generator
        """
        try:
            MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
        except KeyError: # no project folder exists
            MONIMAN_OUTPUTS = '.'

        try:
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            data_dir = QtWidgets.QFileDialog.getExistingDirectory(QtWidgets.QFileDialog(), 'Select the folder Report from Plaxis2D report generator', MONIMAN_OUTPUTS)

            # search for Plaxis2D report generated files and convert to the format that Moniman uses: ux, N, M, Q
            data_files_ux = get_file_reg_expr(os.path.join(data_dir,'*Table of total displacements.txt'))
            data_files_NMQ = get_file_reg_expr(os.path.join(data_dir,'*Table of plate force envelopes.txt'))
            x_coord_wall = float(self.ui.lineEdit_8.text())
            data_files = combine_Ux_NMQ_files(data_files_ux, data_files_NMQ, x_coord_wall)    # combine ux with NMQ and save to disc

            # use data_dir for printing out the report
            sys.modules['moniman_paths']['MONIMAN_OUTPUTS'] = data_dir

            # clear all data
            self.wall_outputs_phases.clear()
            # read data in for each of the selected phases
            for data_file in data_files:
                data = np.loadtxt(data_file.replace('/','\\'), skiprows=1)
                # sort after y-axis
                columnIndex = 0 # y
                data = data[data[:, columnIndex].argsort()]

                # store internal forces
                wall_outputs = {} # wall outputs of the concerned phase
                wall_outputs['y'] = data[:, 0]
                wall_outputs['Ux'] = data[:, 1]
                data[:, 2][np.where(data[:, 2] < 0.0)] = data[:, 2][np.where(data[:, 2] < 0.0)]*self.percentage_N/100
                wall_outputs['N'] = data[:, 2]
                wall_outputs['M'] = data[:, 3]
                wall_outputs['Q'] = data[:, 4]
                self.wall_outputs_phases.append(wall_outputs)

            # plot internal forces
            self.plot_wall_internal_forces_barrette()

        except:
            self.dialog.show_message_box('Error', 'Please check the Report folder or the given x-coordinate of wall!')


    def load_wall_internal_forces_barrette(self):
        """ Loads internal forces of wall
        """
        try:
            MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
        except KeyError: # no project folder exists
            MONIMAN_OUTPUTS = '.'

        try:
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            data_files, _ = QtWidgets.QFileDialog.getOpenFileNames(QtWidgets.QFileDialog(), 'Select data for one or more calculation phases', MONIMAN_OUTPUTS)

            # clear all data
            self.wall_outputs_phases.clear()
            # read data in for each of the selected phases
            for data_file in data_files:
                data = np.loadtxt(data_file.replace('/','\\'), skiprows=1)
                # sort after y-axis
                columnIndex = 0 # y
                data = data[data[:, columnIndex].argsort()]

                # store internal forces
                wall_outputs = {} # wall outputs of the concerned phase
                wall_outputs['y'] = data[:, 0]
                wall_outputs['Ux'] = data[:, 1]
                data[:, 2][np.where(data[:, 2] < 0.0)] = data[:, 2][np.where(data[:, 2] < 0.0)]*self.percentage_N/100
                wall_outputs['N'] = data[:, 2]
                wall_outputs['M'] = data[:, 3]
                wall_outputs['Q'] = data[:, 4]
                self.wall_outputs_phases.append(wall_outputs)

            # plot internal forces
            self.plot_wall_internal_forces_barrette()

        except:
            self.dialog.show_message_box('Error', 'Please select the correct data file(s)!')


    def plot_wall_internal_forces_barrette(self):
        """ Plots wall internal forces
        """
        BT = self.barrette.cross_section['BT']    # barrette length in meter
        self.ui.toolBox.setCurrentIndex(1)
        self.plot_canvas_wall_output.axes[0].cla()
        self.plot_canvas_wall_output.axes[1].cla()
        self.plot_canvas_wall_output.axes[2].cla()
        for wall_outputs in self.wall_outputs_phases:
            self.plot_canvas_wall_output.plot_wall_output(wall_outputs['y'], wall_outputs['N'], BT, index=0, clear=False)
            self.plot_canvas_wall_output.plot_wall_output(wall_outputs['y'], wall_outputs['M'], BT, index=1, clear=False)
            self.plot_canvas_wall_output.plot_wall_output(wall_outputs['y'], wall_outputs['Q'], BT, index=2, clear=False)


    def calculate_required_reinforcement_pile(self):
        """ Calculates the required reinforcement area for pile
        """
        if not self.wall_outputs_phases:
            self.dialog.show_message_box('Error', 'Please load wall internal forces first!')
        else:
            # clear required reinforcement for barrette
            self.A_s1 = None
            self.A_s2 = None
            self.a_s12 = None
            # calculate
            method = self.ui.comboBox_7.currentText()
            start_time = time.time()
            A_s_all, a_s_all = self.pile.calculate_required_reinforcement(self.code, self.params_psf, self.params_concrete, self.params_reinf, self.wall_outputs_phases, self.min_reinf, method)
            elapsed_time = time.time() - start_time
            self.A_s = A_s_all
            self.a_s = a_s_all

            # display the required reinforcement areas
            self.display_required_reinforcement_pile()

            # fill in reinf tables with basic values
            self.fill_table_reinf_staggering_vertical_pile()
            self.fill_table_reinf_staggering_shear_pile()

            self.dialog.show_message_box('Infomation', 'Reinforcement calculation is finished. Calculation time is {0:.2f} minutes'.format(elapsed_time/60))


    def display_required_reinforcement_pile(self):
        """ Displays the required reinforcement area for pile
        """
        self.ui.toolBox.setCurrentIndex(2)
        y_all = self.wall_outputs_phases[0]['y']
        self.plot_canvas_reinf.axes[0].cla()
        self.plot_canvas_reinf.axes[1].cla()

        n_phases = len(self.wall_outputs_phases)
        for j in range(n_phases):
            self.plot_canvas_reinf.plot_reinf(y_all, np.array(self.A_s[:, j]), index=0, clear=False)
            self.plot_canvas_reinf.plot_reinf(y_all, np.array(self.a_s[:, j]), index=1, clear=False)
 


    def calculate_required_reinforcement_barrette(self):
        """ Calculates the required reinforcement area for barrette
        """
        if not self.wall_outputs_phases:
            self.dialog.show_message_box('Error', 'Please load wall internal forces first!')
        else:
            # clear required reinforcement for pile
            self.A_s = None
            self.a_s = None
            # calculate
            method = self.ui.comboBox_8.currentText()   # calculation method
            sym = self.ui.checkBox_3.checkState() == 2  # symmetric vertical reinforcement or not
            start_time = time.time()
            A_s1_all, A_s2_all, a_s_all = self.barrette.calculate_required_reinforcement(self.code, self.params_psf, self.params_concrete, self.params_reinf, self.wall_outputs_phases, self.min_reinf, sym, method)
            elapsed_time = time.time() - start_time
            self.A_s1 = A_s1_all
            self.A_s2 = A_s2_all
            self.a_s12 = a_s_all

            # displays the required reinforcement areas
            self.display_required_reinforcement_barrette()

            ## fill in reinf tables with basic values
            self.fill_table_reinf_staggering_vertical_barrette_A_s_2(self.ui.tableWidget_8)
            self.fill_table_reinf_staggering_vertical_barrette_A_s_1(self.ui.tableWidget_9)
            self.fill_table_reinf_staggering_shear_barrette()

            self.dialog.show_message_box('Infomation', 'Reinforcement calculation is finished. Calculation time is {0:.2f} minutes'.format(elapsed_time/60))


    def display_required_reinforcement_barrette(self):
        """ Displays the required reinforcement area for barrette
        """
        self.ui.toolBox.setCurrentIndex(2)
        y_all = self.wall_outputs_phases[0]['y']
        self.plot_canvas_reinf.axes[0].cla()
        self.plot_canvas_reinf.axes[1].cla()

        n_phases = len(self.wall_outputs_phases)
        for j in range(n_phases):
            self.plot_canvas_reinf.plot_reinf(y_all, np.array(self.A_s1[:, j]), index=0, clear=False)
            self.plot_canvas_reinf.plot_reinf(y_all, np.array(self.A_s2[:, j]), index=0, clear=False)
            self.plot_canvas_reinf.plot_reinf(y_all, np.array(self.a_s12[:, j]), index=1, clear=False)


    def write_file_reinf_results_pile(self):
        """ Writes reinforcement requirement and the results of reinforcement staggering to file
        """
        MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
        if self.A_s is not None:
            y = self.wall_outputs_phases[0]['y']
            A_s_envelop = np.amax(np.abs(self.A_s), axis=1) # enveloped A_s
            a_s_envelop = np.amax(np.abs(self.a_s), axis=1) # enveloped a_s
            #data = np.c_[y, self.A_s[:], self.a_s]
            data = np.c_[y, A_s_envelop, a_s_envelop]
            staggered_A_s = np.zeros(y.size)
            staggered_string = np.empty(y.size, dtype=object)
            staggered_a_s = np.zeros(y.size)
            staggered_string_s = np.empty(y.size, dtype=object)
            for i in range(y.size):
                staggered_A_s[i], staggered_string[i] = self.get_vertical_reinf_staggering_at_level(self.staggered_reinf_vertical_pile, y[i])
                staggered_a_s[i], staggered_string_s[i] = self.get_shear_reinf_staggering_at_level(self.staggered_reinf_shear_pile, y[i])
            data = np.c_[data, staggered_string, staggered_A_s, staggered_string_s, staggered_a_s]

            dest = os.path.join(MONIMAN_OUTPUTS, 'REINF_DATA_PILE.txt')
            header_items = ['y', 'A_s_req.', 'a_s_req.', 'n, dia', 'A_s', 'dia@spacing, n_legs', 'a_s']
            header = ''.join([s.rjust(20) for s in header_items])
            np.savetxt(dest, data, fmt='%20s', delimiter='\t', header=header, comments='')
            self.ui.label_9.setText('Data path: ' + dest)
        

    def write_file_reinf_results_barrette(self):
        """ Writes reinforcement requirement and the results of reinforcement staggering to file
        """
        MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
        if self.A_s1 is not None:
            y = self.wall_outputs_phases[0]['y']
            A_s1_envelop = np.amax(np.abs(self.A_s1), axis=1) # enveloped A_s1
            A_s2_envelop = np.amax(np.abs(self.A_s2), axis=1) # enveloped A_s2
            a_s12_envelop = np.amax(np.abs(self.a_s12), axis=1) # enveloped a_s12
            #data = np.c_[y, self.A_s1[:], self.A_s2, self.a_s12[:]]
            data = np.c_[y, A_s1_envelop, A_s2_envelop, a_s12_envelop]
            staggered_A_s1 = np.zeros(y.size)
            staggered_A_s2 = np.zeros(y.size)
            staggered_string_A_s1 = np.empty(y.size, dtype=object)
            staggered_string_A_s2 = np.empty(y.size, dtype=object)
            staggered_a_s12 = np.zeros(y.size)
            staggered_string_s12 = np.empty(y.size, dtype=object)
            for i in range(y.size):
                staggered_A_s1[i], staggered_string_A_s1[i] = self.get_vertical_reinf_staggering_at_level(self.staggered_reinf_vertical_barrette_A_s_1, y[i])
                staggered_A_s2[i], staggered_string_A_s2[i] = self.get_vertical_reinf_staggering_at_level(self.staggered_reinf_vertical_barrette_A_s_2, y[i])
                staggered_a_s12[i], staggered_string_s12[i] = self.get_shear_reinf_staggering_at_level(self.staggered_reinf_shear_barrette, y[i])
            data = np.c_[data, staggered_string_A_s1, staggered_A_s1, staggered_string_A_s2, staggered_A_s2, staggered_string_s12, staggered_a_s12]

            dest = os.path.join(MONIMAN_OUTPUTS, 'REINF_DATA_BARRETTE.txt')
            header_items = ['y', 'A_s1_req.', 'A_s2_req.', 'a_s_req.', 'n, dia', 'A_s1', 'n, dia', 'A_s2', 'dia@spacing, n_legs', 'a_s']
            header = ''.join([s.rjust(20) for s in header_items])
            np.savetxt(dest, data, fmt='%20s', delimiter='\t', header=header, comments='')
            self.ui.label_9.setText('Data path: ' + dest)
        


    def get_vertical_reinf_staggering_at_level(self, staggered_reinf_vertical, level):
        """ Gets a string of staggerd reinforcement information
        vertical reinf: n, dia
        shear reinf: dia@spacing, n_legs
        """
        for segment in staggered_reinf_vertical:
            if (level <= segment['top']) and (level >= segment['bottom']):
                staggered_string = str(segment['n']) + ', ' + segment['dia']
                staggered_A_s = segment['A_s']
                return staggered_A_s, staggered_string


    def get_shear_reinf_staggering_at_level(self, staggered_reinf_shear, level):
        """ Gets a string of staggerd reinforcement information
        vertical reinf: n, dia
        shear reinf: dia@spacing, n_legs
        """
        for segment in staggered_reinf_shear:
            if (level <= segment['top']) and (level >= segment['bottom']):
                staggered_string = segment['dia'] + '@' + str(segment['spacing']) + ', ' + str(segment['n_legs'])
                staggered_a_s = segment['a_s']
                return staggered_a_s, staggered_string


    def fill_table_reinf_staggering_vertical_barrette_A_s_2(self, table_widget, fill_anyway=False):
        """ Fills table for vertical reinforcement staggering
        """
        if (table_widget.item(0, 0).text() == '') or fill_anyway:
            try:
                wall_top = np.max(self.wall_outputs_phases[0]['y'])
                wall_toe = np.min(self.wall_outputs_phases[0]['y'])
                bar_diameters = [s.strip() for s in self.ui.lineEdit_3.text().split(',')]   # text input in pannel for barrette
                self.bar_diameters_vertical = bar_diameters
                n_bars = 10

                table_widget.blockSignals(True)
                # top, n
                table_widget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(wall_top)))
                table_widget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(n_bars)))
                table_widget.item(0, 0).setBackground(QColor(242, 255, 116))
                table_widget.item(0, 1).setBackground(QColor(242, 255, 116))

                # bar diameters
                for row_i in range(table_widget.rowCount()):
                    combobox = QtWidgets.QComboBox()
                    for dia in bar_diameters:
                        combobox.addItem(dia)
                    combobox.setCurrentIndex(0)
                    combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
                    combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_vertical_barrette_A_s2(1,1, table_widget))
                    table_widget.setCellWidget(row_i, 2, combobox)
                    #table_widget.item(row_i, 2).setBackground(QColor(242, 255, 116))

                # calculate A_s using the initial staggered information
                try:
                    dia_current = float(table_widget.cellWidget(0, 2).currentText())   #'xx'
                except ValueError:
                    dia_current = float(table_widget.cellWidget(0, 2).currentText()[1:]) # 'Dxx'

                B = self.barrette.cross_section['B']
                A_s, clearance = self.barrette.calc_A_s(n_bars, dia_current, B)
                steel_weight = self.barrette.calc_weight_A_s(A_s, wall_top - wall_toe)
                table_widget.setItem(0, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
                table_widget.setItem(0, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
                table_widget.setItem(0, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                # fill wall's toe if the cell is empty
                if table_widget.item(1, 0).text() == '':
                    table_widget.setItem(1, 0, QtWidgets.QTableWidgetItem(str(wall_toe)))
                    table_widget.item(1, 0).setBackground(QColor(242, 255, 116))

                ### read/store and plot vertical reinf
                self.staggered_reinf_vertical_barrette_A_s_2 = self.read_reinf_vertical(table_widget, negation=True)
                self.plot_reinf_vertical_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.A_s1, self.A_s2)

                table_widget.blockSignals(False)

            except:
                pass

        else:
            ### read/store and plot vertical reinf
            self.staggered_reinf_vertical_barrette_A_s_2 = self.read_reinf_vertical(table_widget, negation=True)
            self.plot_reinf_vertical_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.A_s1, self.A_s2)


    def fill_table_reinf_staggering_vertical_barrette_A_s_2_saved_values(self, table_widget):
        """ Fills table for vertical reinforcement staggering with saved values
        """
        bar_diameters = self.bar_diameters_vertical

        table_widget.blockSignals(True)
        # bar diameters
        for row_i in range(table_widget.rowCount()):
            combobox = QtWidgets.QComboBox()
            for dia in bar_diameters:
                combobox.addItem(dia)
            combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
            table_widget.setCellWidget(row_i, 2, combobox)
            combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_vertical_barrette_A_s2(1,1, table_widget))

        for i, segment in enumerate(self.staggered_reinf_vertical_barrette_A_s_2):
            table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(segment['top'])))
            table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(segment['n'])))
            table_widget.item(i, 0).setBackground(QColor(242, 255, 116))
            table_widget.item(i, 1).setBackground(QColor(242, 255, 116))

            # set combobox for index of bar diameter
            combobox_i = table_widget.cellWidget(i, 2)
            self.set_combobox_item(combobox_i, segment['dia'])

            try:
                dia_current = float(segment['dia'])
            except ValueError:
                dia_current = float(segment['dia'][1:])

            B = self.barrette.cross_section['B']
            A_s, clearance = self.barrette.calc_A_s(segment['n'], dia_current, B)
            steel_weight = self.barrette.calc_weight_A_s(A_s, segment['top'] - segment['bottom'])
            table_widget.setItem(i, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
            table_widget.setItem(i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
            table_widget.setItem(i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

        # wall toe
        wall_toe = np.min(self.wall_outputs_phases[0]['y'])
        table_widget.setItem(i+1, 0, QtWidgets.QTableWidgetItem(str(wall_toe)))
        table_widget.item(i+1, 0).setBackground(QColor(242, 255, 116))

        # plot
        self.plot_reinf_vertical_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.A_s1, self.A_s2)

        table_widget.blockSignals(False)



    def fill_table_reinf_staggering_vertical_barrette_A_s_1(self, table_widget, fill_anyway=False):
        """ Fills table for vertical reinforcement staggering
        """
        if (table_widget.item(0, 0).text() == '') or fill_anyway:
            try:
                wall_top = np.max(self.wall_outputs_phases[0]['y'])
                wall_toe = np.min(self.wall_outputs_phases[0]['y'])
                bar_diameters = [s.strip() for s in self.ui.lineEdit_3.text().split(',')]   # text input in pannel for barrette
                self.bar_diameters_vertical = bar_diameters
                n_bars = 10

                table_widget.blockSignals(True)
                # top, n
                table_widget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(wall_top)))
                table_widget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(n_bars)))
                table_widget.item(0, 0).setBackground(QColor(242, 255, 116))
                table_widget.item(0, 1).setBackground(QColor(242, 255, 116))

                # bar diameters
                for row_i in range(table_widget.rowCount()):
                    combobox = QtWidgets.QComboBox()
                    for dia in bar_diameters:
                        combobox.addItem(dia)
                    combobox.setCurrentIndex(0)
                    combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
                    combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_vertical_barrette_A_s1(1,1, table_widget))
                    table_widget.setCellWidget(row_i, 2, combobox)
                    #table_widget.item(row_i, 2).setBackground(QColor(242, 255, 116))

                # calculate A_s using the initial staggered information
                try:
                    dia_current = float(table_widget.cellWidget(0, 2).currentText())   #'xx'
                except ValueError:
                    dia_current = float(table_widget.cellWidget(0, 2).currentText()[1:]) # 'Dxx'

                B = self.barrette.cross_section['B']
                A_s, clearance = self.barrette.calc_A_s(n_bars, dia_current, B)
                steel_weight = self.barrette.calc_weight_A_s(A_s, wall_top - wall_toe)
                table_widget.setItem(0, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
                table_widget.setItem(0, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
                table_widget.setItem(0, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                # fill wall's toe if the cell is empty
                if table_widget.item(1, 0).text() == '':
                    table_widget.setItem(1, 0, QtWidgets.QTableWidgetItem(str(wall_toe)))
                    table_widget.item(1, 0).setBackground(QColor(242, 255, 116))

                ### read/store and plot vertical reinf
                self.staggered_reinf_vertical_barrette_A_s_1 = self.read_reinf_vertical(table_widget)
                self.plot_reinf_vertical_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.A_s1, self.A_s2)

                table_widget.blockSignals(False)

            except:
                pass
        
        else:
            ### read/store and plot vertical reinf
            self.staggered_reinf_vertical_barrette_A_s_1 = self.read_reinf_vertical(table_widget)
            self.plot_reinf_vertical_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.A_s1, self.A_s2)


    def fill_table_reinf_staggering_vertical_barrette_A_s_1_saved_values(self, table_widget):
        """ Fills table for vertical reinforcement staggering with saved values
        """
        bar_diameters = self.bar_diameters_vertical

        table_widget.blockSignals(True)
        # bar diameters
        for row_i in range(table_widget.rowCount()):
            combobox = QtWidgets.QComboBox()
            for dia in bar_diameters:
                combobox.addItem(dia)
            combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
            table_widget.setCellWidget(row_i, 2, combobox)
            combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_vertical_barrette_A_s1(1,1, table_widget))

        for i, segment in enumerate(self.staggered_reinf_vertical_barrette_A_s_1):
            table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(segment['top'])))
            table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(segment['n'])))
            table_widget.item(i, 0).setBackground(QColor(242, 255, 116))
            table_widget.item(i, 1).setBackground(QColor(242, 255, 116))

            # set combobox for index of bar diameter
            combobox_i = table_widget.cellWidget(i, 2)
            self.set_combobox_item(combobox_i, segment['dia'])

            try:
                dia_current = float(segment['dia'])
            except ValueError:
                dia_current = float(segment['dia'][1:])

            B = self.barrette.cross_section['B']
            A_s, clearance = self.barrette.calc_A_s(segment['n'], dia_current, B)
            steel_weight = self.barrette.calc_weight_A_s(A_s, segment['top'] - segment['bottom'])
            table_widget.setItem(i, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
            table_widget.setItem(i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
            table_widget.setItem(i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

        # wall toe
        wall_toe = np.min(self.wall_outputs_phases[0]['y'])
        table_widget.setItem(i+1, 0, QtWidgets.QTableWidgetItem(str(wall_toe)))
        table_widget.item(i+1, 0).setBackground(QColor(242, 255, 116))

        # plot
        self.plot_reinf_vertical_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.A_s1, self.A_s2)

        table_widget.blockSignals(False)


    def fill_table_reinf_staggering_vertical_pile(self, fill_anyway=False):
        """ Fills table for vertical reinforcement staggering
        """
        if (self.ui.tableWidget_5.item(0, 0).text() == '') or fill_anyway:
            try:
                wall_top = np.max(self.wall_outputs_phases[0]['y'])
                wall_toe = np.min(self.wall_outputs_phases[0]['y'])
                bar_diameters = [s.strip() for s in self.ui.lineEdit.text().split(',')]
                self.bar_diameters_vertical = bar_diameters
                n_bars = 10

                self.ui.tableWidget_5.blockSignals(True)
                # top, n
                self.ui.tableWidget_5.setItem(0, 0, QtWidgets.QTableWidgetItem(str(wall_top)))
                self.ui.tableWidget_5.setItem(0, 1, QtWidgets.QTableWidgetItem(str(n_bars)))
                self.ui.tableWidget_5.item(0, 0).setBackground(QColor(242, 255, 116))
                self.ui.tableWidget_5.item(0, 1).setBackground(QColor(242, 255, 116))

                # bar diameters
                for row_i in range(self.ui.tableWidget_5.rowCount()):
                    combobox = QtWidgets.QComboBox()
                    for dia in bar_diameters:
                        combobox.addItem(dia)
                    combobox.setCurrentIndex(0)
                    combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
                    combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_vertical_pile(1,1))
                    self.ui.tableWidget_5.setCellWidget(row_i, 2, combobox)
                    #self.ui.tableWidget_5.item(row_i, 2).setBackground(QColor(242, 255, 116))

                # calculate A_s using the initial staggered information
                try:
                    dia_current = float(self.ui.tableWidget_5.cellWidget(0, 2).currentText())   #'xx'
                except ValueError:
                    dia_current = float(self.ui.tableWidget_5.cellWidget(0, 2).currentText()[1:]) # 'Dxx'

                D = self.pile.cross_section['D']
                H = self.pile.cross_section['H']
                A_s, clearance = self.pile.calc_A_s(n_bars, dia_current, D, H)
                steel_weight = self.pile.calc_weight_A_s(A_s, wall_top - wall_toe)
                self.ui.tableWidget_5.setItem(0, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
                self.ui.tableWidget_5.setItem(0, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
                self.ui.tableWidget_5.setItem(0, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                # fill wall's toe if the cell is empty
                if self.ui.tableWidget_5.item(1, 0).text() == '':
                    self.ui.tableWidget_5.setItem(1, 0, QtWidgets.QTableWidgetItem(str(wall_toe)))
                    self.ui.tableWidget_5.item(1, 0).setBackground(QColor(242, 255, 116))

                ## read/store and plot vertical reinf
                self.staggered_reinf_vertical_pile = self.read_reinf_vertical(self.ui.tableWidget_5)
                self.plot_reinf_vertical_pile(self.staggered_reinf_vertical_pile, self.A_s)

                self.ui.tableWidget_5.blockSignals(False)

            except:
                pass
        else:
            ## read/store and plot vertical reinf
            self.staggered_reinf_vertical_pile = self.read_reinf_vertical(self.ui.tableWidget_5)
            self.plot_reinf_vertical_pile(self.staggered_reinf_vertical_pile, self.A_s)



    def fill_table_reinf_staggering_vertical_pile_saved_values(self):
        """ Fills table for vertical reinforcement staggering with saved values
        """
        bar_diameters = self.bar_diameters_vertical

        self.ui.tableWidget_5.blockSignals(True)
        # bar diameters
        for row_i in range(self.ui.tableWidget_5.rowCount()):
            combobox = QtWidgets.QComboBox()
            for dia in bar_diameters:
                combobox.addItem(dia)
            combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
            combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_vertical_pile(1,1))
            self.ui.tableWidget_5.setCellWidget(row_i, 2, combobox)

        for i, segment in enumerate(self.staggered_reinf_vertical_pile):
            self.ui.tableWidget_5.setItem(i, 0, QtWidgets.QTableWidgetItem(str(segment['top'])))
            self.ui.tableWidget_5.setItem(i, 1, QtWidgets.QTableWidgetItem(str(segment['n'])))
            self.ui.tableWidget_5.item(i, 0).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget_5.item(i, 1).setBackground(QColor(242, 255, 116))

            # set combobox for index of bar diameter
            combobox_i = self.ui.tableWidget_5.cellWidget(i, 2)
            self.set_combobox_item(combobox_i, segment['dia'])

    	    # show reinforcement requirement for segment
            try:
                dia_current = float(segment['dia'])
            except ValueError:
                dia_current = float(segment['dia'][1:])
            D = self.pile.cross_section['D']
            H = self.pile.cross_section['H']
            A_s, clearance = self.pile.calc_A_s(segment['n'], dia_current, D, H)
            steel_weight = self.pile.calc_weight_A_s(A_s, segment['top'] - segment['bottom'])
            self.ui.tableWidget_5.setItem(i, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
            self.ui.tableWidget_5.setItem(i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
            self.ui.tableWidget_5.setItem(i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

        # wall toe
        wall_toe = np.min(self.wall_outputs_phases[0]['y'])
        self.ui.tableWidget_5.setItem(i+1, 0, QtWidgets.QTableWidgetItem(str(wall_toe)))
        self.ui.tableWidget_5.item(i+1, 0).setBackground(QColor(242, 255, 116))

        # plot
        self.plot_reinf_vertical_pile(self.staggered_reinf_vertical_pile, self.A_s)

        self.ui.tableWidget_5.blockSignals(False)




    def fill_table_reinf_staggering_shear_barrette(self, fill_anyway=False):
        """ Fills table for vertical reinforcement staggering
        """
        if (self.ui.tableWidget_10.item(0, 0).text() == '') or fill_anyway:
            try:
                wall_top = np.max(self.wall_outputs_phases[0]['y'])
                wall_toe = np.min(self.wall_outputs_phases[0]['y'])
                bar_diameters = [s.strip() for s in self.ui.lineEdit_4.text().split(',')]   # text input in pannel for barrette
                self.bar_diameters_shear = bar_diameters
                n_legs = 2
                spacing = 25.0

                self.ui.tableWidget_10.blockSignals(True)
                # top, n_legs
                self.ui.tableWidget_10.setItem(0, 0, QtWidgets.QTableWidgetItem(str(wall_top)))
                self.ui.tableWidget_10.setItem(0, 2, QtWidgets.QTableWidgetItem(str(n_legs)))
                self.ui.tableWidget_10.setItem(0, 3, QtWidgets.QTableWidgetItem(str(spacing)))
                self.ui.tableWidget_10.item(0, 0).setBackground(QColor(242, 255, 116))
                self.ui.tableWidget_10.item(0, 2).setBackground(QColor(242, 255, 116))
                self.ui.tableWidget_10.item(0, 3).setBackground(QColor(242, 255, 116))

                # bar diameters
                for row_i in range(self.ui.tableWidget_10.rowCount()):
                    combobox = QtWidgets.QComboBox()
                    for dia in bar_diameters:
                        combobox.addItem(dia)
                    combobox.setCurrentIndex(0)
                    combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
                    combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_shear_barrette(1,1))
                    self.ui.tableWidget_10.setCellWidget(row_i, 1, combobox)
                    #self.ui.tableWidget_10.item(row_i, 1).setBackground(QColor(242, 255, 116))

                # calculate a_s using the initial staggered information
                try:
                    dia_current = float(self.ui.tableWidget_10.cellWidget(0, 1).currentText())   #'xx'
                except ValueError:
                    dia_current = float(self.ui.tableWidget_10.cellWidget(0, 1).currentText()[1:]) # 'Dxx'
                D = self.barrette.cross_section['D']
                B = self.barrette.cross_section['B']
                H1 = self.barrette.cross_section['H1']
                H2 = self.barrette.cross_section['H2']
                a_s = self.barrette.calc_a_s(n_legs, dia_current, spacing)
                steel_weight = self.barrette.calc_weight_a_s(a_s, wall_top - wall_toe, D, B, H1, H2, n_legs)
                self.ui.tableWidget_10.setItem(0, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(a_s)))
                self.ui.tableWidget_10.setItem(0, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                # fill wall's toe if the cell is empty
                if self.ui.tableWidget_10.item(1, 0).text() == '':
                    self.ui.tableWidget_10.setItem(1, 0, QtWidgets.QTableWidgetItem(str(wall_toe)))
                    self.ui.tableWidget_10.item(1, 0).setBackground(QColor(242, 255, 116))

                ## read/store and plot vertical reinf
                self.staggered_reinf_shear_barrette = self.read_reinf_shear(self.ui.tableWidget_10)
                self.plot_reinf_shear(self.staggered_reinf_shear_barrette, self.a_s12)

                self.ui.tableWidget_10.blockSignals(False)

            except:
                pass

        else:
            ## read/store and plot vertical reinf
            self.staggered_reinf_shear_barrette = self.read_reinf_shear(self.ui.tableWidget_10)
            self.plot_reinf_shear(self.staggered_reinf_shear_barrette, self.a_s12)


    def fill_table_reinf_staggering_shear_barrette_saved_values(self):
        """ Fills table for vertical reinforcement staggering from saved values
        """
        bar_diameters = self.bar_diameters_shear
        self.ui.tableWidget_10.blockSignals(True)
        # bar diameters
        for row_i in range(self.ui.tableWidget_10.rowCount()):
            combobox = QtWidgets.QComboBox()
            for dia in bar_diameters:
                combobox.addItem(dia)
            combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
            combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_shear_barrette(1,1))
            self.ui.tableWidget_10.setCellWidget(row_i, 1, combobox)

        for i, segment in enumerate(self.staggered_reinf_shear_barrette):
            self.ui.tableWidget_10.setItem(i, 0, QtWidgets.QTableWidgetItem(str(segment['top'])))
            self.ui.tableWidget_10.setItem(i, 2, QtWidgets.QTableWidgetItem(str(segment['n_legs'])))
            self.ui.tableWidget_10.setItem(i, 3, QtWidgets.QTableWidgetItem(str(segment['spacing'])))
            self.ui.tableWidget_10.item(i, 0).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget_10.item(i, 2).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget_10.item(i, 3).setBackground(QColor(242, 255, 116))

            # set combobox for index of bar diameter
            combobox_i = self.ui.tableWidget_10.cellWidget(i, 1)
            self.set_combobox_item(combobox_i, segment['dia'])

            try:
                dia_current = float(segment['dia'])
            except ValueError:
                dia_current = float(segment['dia'][1:])
            D = self.barrette.cross_section['D']
            B = self.barrette.cross_section['B']
            H1 = self.barrette.cross_section['H1']
            H2 = self.barrette.cross_section['H2']
            a_s = self.barrette.calc_a_s(segment['n_legs'], dia_current, segment['spacing'])
            steel_weight = self.barrette.calc_weight_a_s(a_s, segment['top'] - segment['bottom'], D, B, H1, H2, segment['n_legs'])
            self.ui.tableWidget_10.setItem(i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(a_s)))
            self.ui.tableWidget_10.setItem(i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

        # wall toe
        wall_toe = np.min(self.wall_outputs_phases[0]['y'])
        self.ui.tableWidget_10.setItem(i+1, 0, QtWidgets.QTableWidgetItem(str(wall_toe)))
        self.ui.tableWidget_10.item(i+1, 0).setBackground(QColor(242, 255, 116))

        # plot
        self.plot_reinf_shear(self.staggered_reinf_shear_barrette, self.a_s12)

        self.ui.tableWidget_10.blockSignals(False)


    def fill_table_reinf_staggering_shear_pile(self, fill_anyway=False):
        """ Fills table for vertical reinforcement staggering
        """
        if (self.ui.tableWidget_6.item(0, 0).text() == '') or fill_anyway:
            try:
                wall_top = np.max(self.wall_outputs_phases[0]['y'])
                wall_toe = np.min(self.wall_outputs_phases[0]['y'])
                bar_diameters = [s.strip() for s in self.ui.lineEdit_2.text().split(',')]
                self.bar_diameters_shear = bar_diameters
                n_legs = 2
                spacing = 25.0

                self.ui.tableWidget_6.blockSignals(True)
                # top, n_legs
                self.ui.tableWidget_6.setItem(0, 0, QtWidgets.QTableWidgetItem(str(wall_top)))
                self.ui.tableWidget_6.setItem(0, 2, QtWidgets.QTableWidgetItem(str(n_legs)))
                self.ui.tableWidget_6.setItem(0, 3, QtWidgets.QTableWidgetItem(str(spacing)))
                self.ui.tableWidget_6.item(0, 0).setBackground(QColor(242, 255, 116))
                self.ui.tableWidget_6.item(0, 2).setBackground(QColor(242, 255, 116))
                self.ui.tableWidget_6.item(0, 3).setBackground(QColor(242, 255, 116))

                # bar diameters
                for row_i in range(self.ui.tableWidget_6.rowCount()):
                    combobox = QtWidgets.QComboBox()
                    for dia in bar_diameters:
                        combobox.addItem(dia)
                    combobox.setCurrentIndex(0)
                    combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
                    combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_shear_pile(1,1))
                    self.ui.tableWidget_6.setCellWidget(row_i, 1, combobox)
                    #self.ui.tableWidget_6.item(row_i, 1).setBackground(QColor(242, 255, 116))

                # calculate a_s using the initial staggered information
                try:
                    dia_current = float(self.ui.tableWidget_6.cellWidget(0, 1).currentText())   #'xx'
                except ValueError:
                    dia_current = float(self.ui.tableWidget_6.cellWidget(0, 1).currentText()[1:]) # 'Dxx'
                D = self.pile.cross_section['D']
                H = self.pile.cross_section['H']
                a_s = self.pile.calc_a_s(n_legs, dia_current, spacing, D, H)
                steel_weight = self.pile.calc_weight_a_s(a_s, wall_top - wall_toe, D, H)
                self.ui.tableWidget_6.setItem(0, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(a_s)))
                self.ui.tableWidget_6.setItem(0, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                # fill wall's toe if the cell is empty
                if self.ui.tableWidget_6.item(1, 0).text() == '':
                    self.ui.tableWidget_6.setItem(1, 0, QtWidgets.QTableWidgetItem(str(wall_toe)))
                    self.ui.tableWidget_6.item(1, 0).setBackground(QColor(242, 255, 116))

                ## read/store and plot vertical reinf
                self.staggered_reinf_shear_pile = self.read_reinf_shear(self.ui.tableWidget_6)
                self.plot_reinf_shear(self.staggered_reinf_shear_pile, self.a_s)

                self.ui.tableWidget_6.blockSignals(False)

            except:
                pass

        else:
            ## read/store and plot vertical reinf
            self.staggered_reinf_shear_pile = self.read_reinf_shear(self.ui.tableWidget_6)
            self.plot_reinf_shear(self.staggered_reinf_shear_pile, self.a_s)


    def fill_table_reinf_staggering_shear_pile_saved_values(self):
        """ Fills table for vertical reinforcement staggering with saved values
        """
        bar_diameters = self.bar_diameters_shear
        self.ui.tableWidget_6.blockSignals(True)
        # bar diameters
        for row_i in range(self.ui.tableWidget_6.rowCount()):
            combobox = QtWidgets.QComboBox()
            for dia in bar_diameters:
                combobox.addItem(dia)
            combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
            combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_shear_pile(1,1))
            self.ui.tableWidget_6.setCellWidget(row_i, 1, combobox)

        for i, segment in enumerate(self.staggered_reinf_shear_pile):
            self.ui.tableWidget_6.setItem(i, 0, QtWidgets.QTableWidgetItem(str(segment['top'])))
            self.ui.tableWidget_6.setItem(i, 2, QtWidgets.QTableWidgetItem(str(segment['n_legs'])))
            self.ui.tableWidget_6.setItem(i, 3, QtWidgets.QTableWidgetItem(str(segment['spacing'])))
            self.ui.tableWidget_6.item(i, 0).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget_6.item(i, 2).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget_6.item(i, 3).setBackground(QColor(242, 255, 116))

            # set combobox for index of bar diameter
            combobox_i = self.ui.tableWidget_6.cellWidget(i, 1)
            self.set_combobox_item(combobox_i, segment['dia'])

            try:
                dia_current = float(segment['dia'])
            except ValueError:
                dia_current = float(segment['dia'][1:])
            D = self.pile.cross_section['D']
            H = self.pile.cross_section['H']
            a_s = self.pile.calc_a_s(segment['n_legs'], dia_current, segment['spacing'], D, H)
            steel_weight = self.pile.calc_weight_a_s(a_s, segment['top'] - segment['bottom'], D, H)
            self.ui.tableWidget_6.setItem(i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(a_s)))
            self.ui.tableWidget_6.setItem(i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

        # wall toe
        wall_toe = np.min(self.wall_outputs_phases[0]['y'])
        self.ui.tableWidget_6.setItem(i+1, 0, QtWidgets.QTableWidgetItem(str(wall_toe)))
        self.ui.tableWidget_6.item(i+1, 0).setBackground(QColor(242, 255, 116))

        # plot
        self.plot_reinf_shear(self.staggered_reinf_shear_pile, self.a_s)

        self.ui.tableWidget_6.blockSignals(False)


    def update_table_reinf_staggering_vertical_pile(self, row, column):
        """ Updates with user staggered vertical reinforcement
        """
        try:
            # calculate and fill As and clearance to table if input values are available
            for row_i in range(self.ui.tableWidget_5.rowCount()-1):
                text_level_current = self.ui.tableWidget_5.item(row_i, 0).text()
                text_level_next = self.ui.tableWidget_5.item(row_i+1, 0).text()
                text_n = self.ui.tableWidget_5.item(row_i, 1).text()
                text_dia = self.ui.tableWidget_5.cellWidget(row_i, 2).currentText()
                try:
                    if (text_level_current != '') and (text_n != ''):
                        D = self.pile.cross_section['D']
                        H = self.pile.cross_section['H']
                        A_s, clearance = self.pile.calc_A_s(float(text_n), text_dia, D, H)
                        segment_top  = float(text_level_current)
                        segment_bottom = 0.0 if text_level_next=='' else float(text_level_next)
                        steel_weight = self.pile.calc_weight_A_s(A_s, segment_top - segment_bottom)
                        self.ui.tableWidget_5.blockSignals(True)
                        self.ui.tableWidget_5.setItem(row_i, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
                        self.ui.tableWidget_5.setItem(row_i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
                        self.ui.tableWidget_5.setItem(row_i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                        self.ui.tableWidget_5.blockSignals(False)
                    else:
                        # clear cells
                        self.ui.tableWidget_5.blockSignals(True)
                        self.ui.tableWidget_5.setItem(row_i, 3, QtWidgets.QTableWidgetItem(''))
                        self.ui.tableWidget_5.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                        self.ui.tableWidget_5.setItem(row_i, 5, QtWidgets.QTableWidgetItem(''))
                        self.ui.tableWidget_5.blockSignals(False)

                except (ValueError, ZeroDivisionError) as e:
                    self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')
                    # clear cells
                    self.ui.tableWidget_5.blockSignals(True)
                    self.ui.tableWidget_5.setItem(row_i, 3, QtWidgets.QTableWidgetItem(''))
                    self.ui.tableWidget_5.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                    self.ui.tableWidget_5.setItem(row_i, 5, QtWidgets.QTableWidgetItem(''))
                    self.ui.tableWidget_5.blockSignals(False)
                    return

            ## read/store and plot vertical reinf
            self.staggered_reinf_vertical_pile = self.read_reinf_vertical(self.ui.tableWidget_5)
            self.plot_reinf_vertical_pile(self.staggered_reinf_vertical_pile, self.A_s)
            #self.plot_wall_internal_forces_pile()

        except ValueError:
            self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')


    def update_table_reinf_staggering_vertical_barrette_A_s1(self, row, column, table_widget):
        """ Updates with user staggered vertical reinforcement
        """
        try:
            # calculate and fill As and clearance to table if input values are available
            for row_i in range(table_widget.rowCount()-1):
                text_level_current = table_widget.item(row_i, 0).text()
                text_level_next = table_widget.item(row_i+1, 0).text()
                text_n = table_widget.item(row_i, 1).text()
                text_dia = table_widget.cellWidget(row_i, 2).currentText()
                try:
                    if (text_level_current != '') and (text_n != ''):
                        B = self.barrette.cross_section['B']
                        A_s, clearance = self.barrette.calc_A_s(float(text_n), text_dia, B)
                        segment_top  = float(text_level_current)
                        segment_bottom = 0.0 if text_level_next=='' else float(text_level_next)
                        steel_weight = self.barrette.calc_weight_A_s(A_s, segment_top - segment_bottom)
                        table_widget.blockSignals(True)
                        table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
                        table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
                        table_widget.setItem(row_i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                        table_widget.blockSignals(False)
                    else:
                        # clear cells
                        table_widget.blockSignals(True)
                        table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem(''))
                        table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                        table_widget.setItem(row_i, 5, QtWidgets.QTableWidgetItem(''))
                        table_widget.blockSignals(False)

                except (ValueError, ZeroDivisionError) as e:
                    self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')
                    # clear cells
                    table_widget.blockSignals(True)
                    table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem(''))
                    table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                    table_widget.setItem(row_i, 5, QtWidgets.QTableWidgetItem(''))
                    table_widget.blockSignals(False)
                    return

            ## read/store and plot vertical reinf
            self.staggered_reinf_vertical_barrette_A_s_1 = self.read_reinf_vertical(self.ui.tableWidget_9)
            #self.staggered_reinf_vertical_barrette_A_s_2 = self.read_reinf_vertical(self.ui.tableWidget_8, negation=True)
            self.plot_reinf_vertical_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.A_s1, self.A_s2)

        except ValueError:
            self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')


    def update_table_reinf_staggering_vertical_barrette_A_s2(self, row, column, table_widget):
        """ Updates with user staggered vertical reinforcement
        """
        try:
            # calculate and fill As and clearance to table if input values are available
            for row_i in range(table_widget.rowCount()-1):
                text_level_current = table_widget.item(row_i, 0).text()
                text_level_next = table_widget.item(row_i+1, 0).text()
                text_n = table_widget.item(row_i, 1).text()
                text_dia = table_widget.cellWidget(row_i, 2).currentText()
                try:
                    if (text_level_current != '') and (text_n != ''):
                        B = self.barrette.cross_section['B']
                        A_s, clearance = self.barrette.calc_A_s(float(text_n), text_dia, B)
                        segment_top  = float(text_level_current)
                        segment_bottom = 0.0 if text_level_next=='' else float(text_level_next)
                        steel_weight = self.barrette.calc_weight_A_s(A_s, segment_top - segment_bottom)
                        table_widget.blockSignals(True)
                        table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
                        table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
                        table_widget.setItem(row_i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                        table_widget.blockSignals(False)
                    else:
                        # clear cells
                        table_widget.blockSignals(True)
                        table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem(''))
                        table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                        table_widget.setItem(row_i, 5, QtWidgets.QTableWidgetItem(''))
                        table_widget.blockSignals(False)

                except (ValueError, ZeroDivisionError) as e:
                    self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')
                    # clear cells
                    table_widget.blockSignals(True)
                    table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem(''))
                    table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                    table_widget.setItem(row_i, 5, QtWidgets.QTableWidgetItem(''))
                    table_widget.blockSignals(False)
                    return

            ## read/store and plot vertical reinf
            #self.staggered_reinf_vertical_barrette_A_s_1 = self.read_reinf_vertical(self.ui.tableWidget_9)
            self.staggered_reinf_vertical_barrette_A_s_2 = self.read_reinf_vertical(self.ui.tableWidget_8, negation=True)
            self.plot_reinf_vertical_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.A_s1, self.A_s2)

        except ValueError:
            self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')


    def update_table_reinf_staggering_shear_pile(self, row, column):
        """ Updates with user staggered shear reinforcement
        """
        #print('update tale reinf staggering shear')
        try:
            # calculate and fill As and clearance to table if input values are available
            for row_i in range(self.ui.tableWidget_6.rowCount()-1):
                text_level_current = self.ui.tableWidget_6.item(row_i, 0).text()
                text_level_next = self.ui.tableWidget_6.item(row_i+1, 0).text()
                text_n_legs = self.ui.tableWidget_6.item(row_i, 2).text()
                text_spacing = self.ui.tableWidget_6.item(row_i, 3).text()
                text_dia = self.ui.tableWidget_6.cellWidget(row_i, 1).currentText()
                try:
                    if (text_level_current != '') and (text_n_legs != '') and (text_spacing != ''):
                        D = self.pile.cross_section['D']
                        H = self.pile.cross_section['H']
                        a_s = self.pile.calc_a_s(float(text_n_legs), text_dia, float(text_spacing), D, H)
                        segment_top  = float(text_level_current)
                        segment_bottom = 0.0 if text_level_next=='' else float(text_level_next)
                        steel_weight = self.pile.calc_weight_a_s(a_s, segment_top - segment_bottom, D, H)
                        self.ui.tableWidget_6.blockSignals(True)
                        self.ui.tableWidget_6.setItem(row_i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(a_s)))
                        self.ui.tableWidget_6.setItem(row_i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                        self.ui.tableWidget_6.blockSignals(False)
                    else:
                        # clear cells
                        self.ui.tableWidget_6.blockSignals(True)
                        self.ui.tableWidget_6.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                        self.ui.tableWidget_6.setItem(row_i, 5, QtWidgets.QTableWidgetItem(''))
                        self.ui.tableWidget_6.blockSignals(False)

                except (ValueError, ZeroDivisionError) as e:
                    # clear cells
                    self.ui.tableWidget_6.blockSignals(True)
                    self.ui.tableWidget_6.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                    self.ui.tableWidget_6.setItem(row_i, 5, QtWidgets.QTableWidgetItem(''))
                    self.ui.tableWidget_6.blockSignals(False)
                    return

            ## read/store and plot vertical reinf
            self.staggered_reinf_shear_pile = self.read_reinf_shear(self.ui.tableWidget_6)
            self.plot_reinf_shear(self.staggered_reinf_shear_pile, self.a_s)
            #self.plot_wall_internal_forces_pile()

        except ValueError:
            self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')


    def update_table_reinf_staggering_shear_barrette(self, row, column):
        """ Updates with user staggered shear reinforcement
        """
        #print('update tale reinf staggering shear')
        try:
            # calculate and fill As and clearance to table if input values are available
            for row_i in range(self.ui.tableWidget_10.rowCount()-1):
                text_level_current = self.ui.tableWidget_10.item(row_i, 0).text()
                text_level_next = self.ui.tableWidget_10.item(row_i+1, 0).text()
                text_n_legs = self.ui.tableWidget_10.item(row_i, 2).text()
                text_spacing = self.ui.tableWidget_10.item(row_i, 3).text()
                text_dia = self.ui.tableWidget_10.cellWidget(row_i, 1).currentText()
                try:
                    if (text_level_current != '') and (text_n_legs != '') and (text_spacing != ''):
                        D = self.barrette.cross_section['D']
                        B = self.barrette.cross_section['B']
                        H1 = self.barrette.cross_section['H1']
                        H2 = self.barrette.cross_section['H2']
                        a_s = self.barrette.calc_a_s(float(text_n_legs), text_dia, float(text_spacing))
                        segment_top  = float(text_level_current)
                        segment_bottom = 0.0 if text_level_next=='' else float(text_level_next)
                        steel_weight = self.barrette.calc_weight_a_s(a_s, segment_top - segment_bottom, D, B, H1, H2, float(text_n_legs))
                        self.ui.tableWidget_10.blockSignals(True)
                        self.ui.tableWidget_10.setItem(row_i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(a_s)))
                        self.ui.tableWidget_10.setItem(row_i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                        self.ui.tableWidget_10.blockSignals(False)
                    else:
                        # clear cells
                        self.ui.tableWidget_10.blockSignals(True)
                        self.ui.tableWidget_10.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                        self.ui.tableWidget_10.setItem(row_i, 5, QtWidgets.QTableWidgetItem(''))
                        self.ui.tableWidget_10.blockSignals(False)

                except (ValueError, ZeroDivisionError) as e:
                    # clear cells
                    self.ui.tableWidget_10.blockSignals(True)
                    self.ui.tableWidget_10.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                    self.ui.tableWidget_10.setItem(row_i, 5, QtWidgets.QTableWidgetItem(''))
                    self.ui.tableWidget_10.blockSignals(False)
                    return

            ## read/store and plot vertical reinf
            self.staggered_reinf_shear_barrette = self.read_reinf_shear(self.ui.tableWidget_10)
            self.plot_reinf_shear(self.staggered_reinf_shear_barrette, self.a_s12)

        except ValueError:
            self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')


    def read_reinf_vertical(self, table_widget, negation=False):
        """ Reads staggered vertical reinforcement and store it
        """
        #self.staggered_reinf_vertical_pile.clear()
        staggered_reinf_vertical_all_segments = []

        for row_i in range(table_widget.rowCount()-1):
            staggered_reinf_vertical = {}

            text_level_current = table_widget.item(row_i, 0).text()
            text_level_next = table_widget.item(row_i+1, 0).text()
            text_n = table_widget.item(row_i, 1).text()
            text_dia = table_widget.cellWidget(row_i, 2).currentText()
            item_weight = table_widget.item(row_i, 5)
            item_A_s = table_widget.item(row_i, 3)
            item_clearance = table_widget.item(row_i, 4)
            if (item_A_s is not None) and (text_level_next != ''):
                staggered_reinf_vertical['top'] = float(text_level_current)
                staggered_reinf_vertical['bottom'] = float(text_level_next)
                staggered_reinf_vertical['n'] = float(text_n)
                staggered_reinf_vertical['dia'] = text_dia
                if negation:
                    staggered_reinf_vertical['A_s'] = -float(item_A_s.text())
                else:
                    staggered_reinf_vertical['A_s'] = float(item_A_s.text())
                staggered_reinf_vertical['clearance'] = float(item_clearance.text())
                staggered_reinf_vertical['weight'] = float(item_weight.text())
                #self.staggered_reinf_vertical_pile.append(staggered_reinf_vertical)
                staggered_reinf_vertical_all_segments.append(staggered_reinf_vertical)
            
                ## store max. bending moment in the segment
                #M_max = self.get_M_or_Q_max_wall_segment(staggered_reinf_vertical, quantity='M')
                #staggered_reinf_vertical['M_max'] = M_max

        
        return staggered_reinf_vertical_all_segments


    def get_M_or_Q_max_wall_segment(self, staggered_reinf, quantity='M'):
        M_max = 0.0
        for wall_outputs in self.wall_outputs_phases:
            index_top = np.where(wall_outputs['y'] <= staggered_reinf['top'])[0][-1]
            index_bottom = np.where(wall_outputs['y'] >= staggered_reinf['bottom'])[0][0]
            M_segment = wall_outputs[quantity][index_bottom:index_top]
            M_segment_max_pos = np.max(M_segment)
            M_segment_max_neg = np.min(M_segment)
            if abs(M_segment_max_pos) > abs(M_segment_max_neg): # positive M_max
                M_max = max(M_max, M_segment_max_pos)
            else: # negative M
                M_max = min(M_max, M_segment_max_neg)

        return M_max


    def read_reinf_shear(self, table_widget):
        """ Reads staggered shear reinforcement and store it
        """
        #self.staggered_reinf_shear_pile.clear()
        staggered_reinf_shear_all_segments = []

        for row_i in range(table_widget.rowCount()-1):
            staggered_reinf_shear = {}

            text_level_current = table_widget.item(row_i, 0).text()
            text_level_next = table_widget.item(row_i+1, 0).text()
            text_n_legs = table_widget.item(row_i, 2).text()
            text_spacing = table_widget.item(row_i, 3).text()
            text_dia = table_widget.cellWidget(row_i, 1).currentText()
            item_weight = table_widget.item(row_i, 5)
            item_a_s = table_widget.item(row_i, 4)
            if (item_a_s is not None) and (text_level_next != ''):
                staggered_reinf_shear['top'] = float(text_level_current)
                staggered_reinf_shear['bottom'] = float(text_level_next)
                staggered_reinf_shear['n_legs'] = float(text_n_legs)
                staggered_reinf_shear['spacing'] = float(text_spacing)
                staggered_reinf_shear['dia'] = text_dia
                staggered_reinf_shear['a_s'] = float(item_a_s.text())
                staggered_reinf_shear['weight'] = float(item_weight.text())
                #self.staggered_reinf_shear_pile.append(staggered_reinf_shear)
                staggered_reinf_shear_all_segments.append(staggered_reinf_shear)

                ## store max. shear force in the segment
                #Q_max = self.get_M_or_Q_max_wall_segment(staggered_reinf_shear, quantity='Q')
                #staggered_reinf_shear['Q_max'] = Q_max
            
        return staggered_reinf_shear_all_segments
    

    def update_plot_reinf_vertical(self, should_plot_envelop):
        """ Updates plot of vertical reinforcement exclusively for pile or barrette
        The required reinforcement for pile or barrette is exclusively available
        """
        if (self.A_s is not None): # pile
            self.plot_reinf_vertical_pile(self.staggered_reinf_vertical_pile, self.A_s, should_plot_envelop)

        elif (self.A_s1 is not None) and (self.A_s2 is not None): #barrette
            self.plot_reinf_vertical_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.A_s1, self.A_s2, should_plot_envelop)


    def update_plot_reinf_shear(self, should_plot_envelop):
        """ Updates plot of shear reinforcement exclusively for pile or barrette
        The required reinforcement for pile or barrette is exclusively available
        """
        if (self.a_s is not None): # pile
            self.plot_reinf_shear(self.staggered_reinf_shear_pile, self.a_s, should_plot_envelop)

        elif (self.a_s12 is not None): #barrette
            self.plot_reinf_shear(self.staggered_reinf_shear_barrette, self.a_s12, should_plot_envelop)


    def plot_reinf_vertical_barrette(self, staggered_reinf_vertical_As1, staggered_reinf_vertical_As2, A_s1, A_s2, should_plot_envelop=False):
        """ Plots the required vertical reinforcement and the user input staggered reinforcement
        """
        # replot the required vertical reinforcement
        self.plot_canvas_reinf.axes[0].cla()
        #should_plot_envelop = self.ui.comboBox_6.currentText() == 'Envelope'
        if A_s1 is not None:
            self.plot_canvas_reinf.plot_reinf(self.wall_outputs_phases[0]['y'], A_s1, should_plot_envelop, index=0)
        if A_s2 is not None:
            self.plot_canvas_reinf.plot_reinf(self.wall_outputs_phases[0]['y'], A_s2, should_plot_envelop, negative=True, index=0, clear=False)
        
        for i, reinf_vertical in enumerate(staggered_reinf_vertical_As1):
            y_top = reinf_vertical['top']
            y_bottom = reinf_vertical['bottom']
            A_s1 = reinf_vertical['A_s']

            if i>0:
                A_s1_upper = staggered_reinf_vertical_As1[i-1]['A_s']
            else:
                A_s1_upper = 0

            annotation = str(int(reinf_vertical['n'])) + 'X' + reinf_vertical['dia'] + 'mm'
            self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, A_s1, index=0, value_upper=A_s1_upper, annotation=annotation)

            if i == 0: # first (top) segment
                self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, A_s1, index=0, segment='first')

            if i==(len(staggered_reinf_vertical_As1) - 1): # last (bottom) segment
                self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, A_s1, index=0, segment='last')

        for i, reinf_vertical in enumerate(staggered_reinf_vertical_As2):
            y_top = reinf_vertical['top']
            y_bottom = reinf_vertical['bottom']
            A_s2 = reinf_vertical['A_s']

            if i>0:
                A_s2_upper = staggered_reinf_vertical_As2[i-1]['A_s']
            else:
                A_s2_upper = 0

            annotation = str(int(reinf_vertical['n'])) + 'X' + reinf_vertical['dia'] + 'mm'
            self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, A_s2, index=0, value_upper=A_s2_upper, annotation=annotation)

            if i == 0: # first (top) segment
                self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, A_s2, index=0, segment='first')

            if i==(len(staggered_reinf_vertical_As2) - 1): # last (bottom) segment
                self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, A_s2, index=0, segment='last')


    def plot_reinf_vertical_pile(self, staggered_reinf_vertical, A_s, should_plot_envelop=False):
        """ Plots the required vertical reinforcement and the user input staggered reinforcement
        """
        # replot the required vertical reinforcement
        self.plot_canvas_reinf.axes[0].cla()
        #should_plot_envelop = self.ui.comboBox_6.currentText() == 'Envelope'
        if A_s is not None:
            self.plot_canvas_reinf.plot_reinf(self.wall_outputs_phases[0]['y'], A_s, should_plot_envelop, index=0)
        
        for i, reinf_vertical in enumerate(staggered_reinf_vertical):
            y_top = reinf_vertical['top']
            y_bottom = reinf_vertical['bottom']
            A_s = reinf_vertical['A_s']

            if i>0:
                A_s_upper = staggered_reinf_vertical[i-1]['A_s']
            else:
                A_s_upper = 0

            annotation = str(int(reinf_vertical['n'])) + 'X' + reinf_vertical['dia'] + 'mm'
            self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, A_s, index=0, value_upper=A_s_upper, annotation=annotation)

            if i == 0: # first (top) segment
                self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, A_s, index=0, segment='first')

            if i==(len(staggered_reinf_vertical) - 1): # last (bottom) segment
                self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, A_s, index=0, segment='last')


    def plot_reinf_shear(self, staggered_reinf_shear, a_s, should_plot_envelop=False):
        """ Plots the required shear reinforcement and the user input staggered reinforcement
        """
        # replot the required shear reinforcement
        self.plot_canvas_reinf.axes[1].cla()
        #should_plot_envelop = self.ui.comboBox_6.currentText() == 'Envelope'
        if a_s is not None:
            self.plot_canvas_reinf.plot_reinf(self.wall_outputs_phases[0]['y'], a_s, should_plot_envelop, index=1)
        
        for i, reinf_shear in enumerate(staggered_reinf_shear):
            y_top = reinf_shear['top']
            y_bottom = reinf_shear['bottom']
            a_s = reinf_shear['a_s']

            if i>0:
                a_s_upper = staggered_reinf_shear[i-1]['a_s']
            else:
                a_s_upper = 0

            annotation = reinf_shear['dia'] + 'mm@' + str(int(reinf_shear['spacing'])) + 'cm, ' + str(reinf_shear['n_legs']) + ' legs'
            self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, a_s, index=1, value_upper=a_s_upper, annotation=annotation)

            if i == 0: # first (top) segment
                self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, a_s, index=1, segment='first')

            if i==(len(staggered_reinf_shear) - 1): # last (bottom) segment
                self.plot_canvas_reinf.plot_reinf_staggering(y_top, y_bottom, a_s, index=1, segment='last')


    def generate_report_pile(self):
        """ Generates PDF report
        """
        try:
            isSeparateGraphs = self.ui.checkBox.checkState() == 2
            if not isSeparateGraphs:
                r = self.pile.print_report(self.project_title, self.code, self.concrete_grade, self.concrete_param_names_per_code, self.params_concrete, self.reinf_grade, self.reinf_param_names, self.params_reinf, self.stress_strain,
                         self.design_situation, self.psf_param_names_per_code, self.params_psf, self.wall_outputs_phases, self.percentage_N, self.staggered_reinf_vertical_pile, self.staggered_reinf_shear_pile, self.A_s, self.a_s)
            else:
                r = self.pile.print_report_separate_graphs(self.project_title, self.code, self.concrete_grade, self.concrete_param_names_per_code, self.params_concrete, self.reinf_grade, self.reinf_param_names, self.params_reinf, self.stress_strain,
                         self.design_situation, self.psf_param_names_per_code, self.params_psf, self.wall_outputs_phases, self.percentage_N, self.staggered_reinf_vertical_pile, self.staggered_reinf_shear_pile, self.A_s, self.a_s)

            if r != int(0):
                self.dialog.show_message_box('Error', 'Before printing the report, please close the file {}'.format(r))

        except Exception as e:
            write_traceback_to_file(sys.modules['moniman_paths']['MONIMAN_OUTPUTS'], e)
            self.dialog.show_message_box('Error', 'Please view ERROR_LOG.txt in {} for further information'.format(os.path.join(sys.modules['moniman_paths']['MONIMAN_OUTPUTS'])))


    def generate_report_barrette(self):
        """ Generates PDF report
        """
        try:
            isSeparateGraphs = self.ui.checkBox_2.checkState() == 2
            if not isSeparateGraphs:
                r = self.barrette.print_report(self.project_title, self.code, self.concrete_grade, self.concrete_param_names_per_code, self.params_concrete, self.reinf_grade, self.reinf_param_names, self.params_reinf, self.stress_strain,
                         self.design_situation, self.psf_param_names_per_code, self.params_psf, self.wall_outputs_phases, self.percentage_N, self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette, self.A_s1, self.A_s2, self.a_s12)
            else:
                r = self.barrette.print_report_separate_graphs(self.project_title, self.code, self.concrete_grade, self.concrete_param_names_per_code, self.params_concrete, self.reinf_grade, self.reinf_param_names, self.params_reinf, self.stress_strain,
                         self.design_situation, self.psf_param_names_per_code, self.params_psf, self.wall_outputs_phases, self.percentage_N, self.staggered_reinf_vertical_barrette_A_s_1,  self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette, self.A_s1, self.A_s2, self.a_s12)

            if r != int(0):
                self.dialog.show_message_box('Error', 'Before printing the report, please close the file {}'.format(r))

        except Exception as e:
            write_traceback_to_file(sys.modules['moniman_paths']['MONIMAN_OUTPUTS'], e)
            self.dialog.show_message_box('Error', 'Please view ERROR_LOG.txt in {} for further information'.format(os.path.join(sys.modules['moniman_paths']['MONIMAN_OUTPUTS'])))


    def send_email_data_pile(self):
        """ Sends email with attached data
        """
        try:
            MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
            attched_file = os.path.join(MONIMAN_OUTPUTS, 'REINF_DATA_PILE.txt')
            subject = 'REINF_DATA_PILE'
            D = self.pile.cross_section['D']
            A = self.pile.cross_section['A']
            H = self.pile.cross_section['H']
            body = 'Pile diameter {0}mm, spacing b/t secondary piles {1}m, concrete cover {2}mm'.format(D, A, H)

            email_recipient = 'ragadeep.bojja@bauer.de'
            email_cc = 'luan.nguyen@bauer.de'
            profilename = 'Outlook2010'

            if os.path.isfile(attched_file):
                self.send_email_via_com(body, subject, email_recipient, profilename, email_cc, attched_file)
                self.dialog.show_message_box('Information', 'Your staggering result has been sent to {}.'.format(email_recipient))
            else:
                self.dialog.show_message_box('Warning', 'Please write your staggering result to file first!'.format(email_recipient))

        except Exception as e:
            write_traceback_to_file(sys.modules['moniman_paths']['MONIMAN_OUTPUTS'], e)
            self.dialog.show_message_box('Error', 'Please view ERROR_LOG.txt in {} for further information!'.format(os.path.join(sys.modules['moniman_paths']['MONIMAN_OUTPUTS'])))


    def send_email_data_barrette(self):
        """ Sends email with attached data
        """
        try:
            MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
            attched_file = os.path.join(MONIMAN_OUTPUTS, 'REINF_DATA_BARRETTE.txt')
            subject = 'REINF_DATA_BARRETTE'
            D = self.barrette.cross_section['D']
            BT = self.barrette.cross_section['BT']
            B = self.barrette.cross_section['B']
            H1 = self.barrette.cross_section['H1']
            H2 = self.barrette.cross_section['H2']
            body = 'Barrette thickness {0}m, width {1}m, cage width {2}m, concrete covers H1 {3}mm, H2 {4}mm'.format(D, BT, B, H1, H2)

            email_recipient = 'ragadeep.bojja@bauer.de'
            #email_recipient = 'luan.nguyen@bauer.de'
            email_cc = 'luan.nguyen@bauer.de'
            profilename = 'Outlook2010'

            if os.path.isfile(attched_file):
                self.send_email_via_com(body, subject, email_recipient, profilename, email_cc, attched_file)
                self.dialog.show_message_box('Information', 'Your staggering result has been sent to {}.'.format(email_recipient))
            else:
                self.dialog.show_message_box('Warning', 'Please write your staggering result to file first!'.format(email_recipient))

        except Exception as e:
            write_traceback_to_file(sys.modules['moniman_paths']['MONIMAN_OUTPUTS'], e)
            self.dialog.show_message_box('Error', 'Please view ERROR_LOG.txt in {} for further information!'.format(os.path.join(sys.modules['moniman_paths']['MONIMAN_OUTPUTS'])))


    def send_email_via_com(self, text, subject, recipient, profilename ,msgcc,attachment):
        """ Sends email with attached data
        """
        olMailItem = 0x0
        obj = win32com.client.Dispatch("Outlook.Application")
        Msg = obj.CreateItem(olMailItem)

    
        Msg.To = recipient

        Msg.CC = msgcc
        #Msg.BCC = "address"

        Msg.Subject = subject
        Msg.Body = text

        #attachment1 = "Path to attachment no. 1"
        #attachment2 = "Path to attachment no. 2"
  
        Msg.Attachments.Add(attachment)

        Msg.Send()


if __name__ == '__main__':
    """ Testing
    """

    app = QtWidgets.QApplication(sys.argv)        
    form = QtWidgets.QDialog()
    project_title = 'Sample'
    Dim(form, D=0.9, S=0.67, project_title=project_title)
    #form.show()
    sys.exit(app.exec_()) 