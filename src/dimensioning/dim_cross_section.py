# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 09:41:35 2021

@author: nya
"""
from scipy import interpolate
from collections import OrderedDict
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from gui.gui_main_matplotlib import MyStaticMplCanvasSubplots_Dim
from gui.gui_all_dialogs_ui import Ui_Dialog
from gui.gui_widget_Dim_cross_section import Ui_Form as DimForm
from dimensioning.parameters import *
from dimensioning.pile import Pile
from dimensioning.barrette import Barrette

class Dim_cross_section(QtWidgets.QWidget):
    """ This class implements dimensioning for capping/ waler beam
    """
    def __init__(self, form, project_title, code=2, concrete_grade='', params_concrete={}, reinf_grade='', params_reinf={}, crack_width='no crack', min_reinf=False, design_situation='', params_psf={},
                cross_section_pile={}, cross_section_barrette={}, 
                internal_forces_permanent={}, internal_forces_transient={}, #internal_forces_design={}, internal_forces_characteristic={},
                #A_s=None, a_s=None, A_s1=None, A_s2=None, a_s12=None, 
                bar_diameters_vertical=[], staggered_reinf_vertical_pile=[], bar_diameters_shear=[], staggered_reinf_shear_pile=[],
                staggered_reinf_vertical_barrette_A_s_1=[], staggered_reinf_vertical_barrette_A_s_2=[], staggered_reinf_shear_barrette=[]):
        super(Dim_cross_section, self).__init__()
        self.ui = DimForm()
        self.ui.setupUi(form)
        self.ui.splitter.setSizes([600, 400]) # resize widgets' size around splitter
        self.dialog = Ui_Dialog()
        self.project_title = project_title

        # plot canvas for materials
        self.plot_layout1 = QtWidgets.QVBoxLayout(self.ui.widget)
        self.plot_canvas_mat = MyStaticMplCanvasSubplots_Dim(self.ui.widget, width=1, height=1, dpi=100, nrows=2, ncols=1)
        self.plot_layout1.addWidget(self.plot_canvas_mat)
        # plot canvas for cross-section of pile
        self.plot_layout2 = QtWidgets.QVBoxLayout(self.ui.widget_2)
        self.plot_canvas_cross_section_pile = MyStaticMplCanvasSubplots_Dim(self.ui.widget_2, width=0.5, height=0.5, dpi=100, nrows=1, ncols=1)
        self.plot_layout2.addWidget(self.plot_canvas_cross_section_pile)
        # plot canvas for cross-section of barrette
        self.plot_layout22 = QtWidgets.QVBoxLayout(self.ui.widget_5)
        self.plot_canvas_cross_section_barrette = MyStaticMplCanvasSubplots_Dim(self.ui.widget_5, width=1, height=1, dpi=100, nrows=1, ncols=1)
        self.plot_layout22.addWidget(self.plot_canvas_cross_section_barrette)

        # plot canvas for reinforcement
        self.plot_layout4 = QtWidgets.QVBoxLayout(self.ui.widget_4)
        self.plot_canvas_reinf = MyStaticMplCanvasSubplots_Dim(self.ui.widget_4, width=1, height=1, dpi=100, nrows=1, ncols=1)
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

        # pile/barrettes cross-sections
        self.pile = Pile(**cross_section_pile)
        self.pile.initialize_cross_section(self.ui.tableWidget_4, self.plot_canvas_cross_section_pile)
        self.barrette = Barrette(**cross_section_barrette)
        self.barrette.initialize_cross_section(self.ui.tableWidget_7, self.plot_canvas_cross_section_barrette)

        # internal forces
        self.internal_forces_permanent = internal_forces_permanent
        self.internal_forces_transient = internal_forces_transient
        self.internal_forces_design = {} #internal_forces_design
        self.internal_forces_characteristic = {} #internal_forces_characteristic

        self.initialize_table_concrete()  # only once
        self.initialize_table_reinforcement() # only once
        self.initialize_table_psf()   # only once

        # update code, if concrete_grade is not empty at start it will remain so
        self.update_code(self.code, self.concrete_grade=='')   
        self.update_crack_width(self.crack_width) # no crack by default

        # display results
        self.display_results_pile()
        self.display_results_barrette()

        # given reinforcement
        self.bar_diameters_vertical = bar_diameters_vertical
        self.bar_diameters_shear = bar_diameters_shear
        self.staggered_reinf_vertical_barrette_A_s_1 = staggered_reinf_vertical_barrette_A_s_1
        self.staggered_reinf_vertical_barrette_A_s_2 = staggered_reinf_vertical_barrette_A_s_2
        self.staggered_reinf_shear_barrette = staggered_reinf_shear_barrette
        self.initialize_table_reinf_vertical(self.ui.tableWidget_9)
        self.initialize_table_reinf_vertical(self.ui.tableWidget_8)
        self.initialize_table_reinf_shear(self.ui.tableWidget_10)
        if not self.staggered_reinf_vertical_barrette_A_s_1:
            self.fill_table_reinf_staggering_vertical_barrette_A_s_1(self.ui.tableWidget_9)
        if not self.staggered_reinf_vertical_barrette_A_s_2:
            self.fill_table_reinf_staggering_vertical_barrette_A_s_2(self.ui.tableWidget_8)
        if not self.staggered_reinf_shear_barrette:
            self.fill_table_reinf_staggering_shear_barrette()

        # connect signals and update basic settings once
        self.connect_signals_to_slots()

        form.exec_()


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
        push_buttons = [self.ui.pushButton, self.ui.pushButton_2]
        for push_button in push_buttons:
            push_button.setAutoDefault(False)
            push_button.setDefault(False)

        # bar diameters
        self.ui.lineEdit_3.editingFinished.connect(lambda: self.fill_table_reinf_staggering_vertical_barrette_A_s_1(self.ui.tableWidget_9))
        self.ui.lineEdit_3.editingFinished.connect(lambda: self.fill_table_reinf_staggering_vertical_barrette_A_s_2(self.ui.tableWidget_8))
        self.ui.lineEdit_4.editingFinished.connect(self.fill_table_reinf_staggering_shear_barrette)

        # internal forces
        self.ui.tableWidget_11.cellChanged.connect(lambda row, column: self.respond_to_cell_changes_in_internal_forces_pile(row, column))   # update internal forces pile
        self.ui.tableWidget_12.cellChanged.connect(lambda row, column: self.respond_to_cell_changes_in_internal_forces_barrette(row, column))   # update internal forces pile

        self.ui.tableWidget_9.cellChanged.connect(lambda row, col: self.update_table_reinf_staggering_vertical_barrette_A_s1(row, col, self.ui.tableWidget_9))
        self.ui.tableWidget_8.cellChanged.connect(lambda row, col: self.update_table_reinf_staggering_vertical_barrette_A_s2(row, col, self.ui.tableWidget_8))
        self.ui.tableWidget_10.cellChanged.connect(lambda row, col: self.update_table_reinf_staggering_shear_barrette(row, col))

        ## report generation
        self.ui.pushButton.clicked.connect(self.print_report_pile) # print report pile
        self.ui.pushButton_2.clicked.connect(self.print_report_barrette) # print report barrette

        ## load saved given reinforcement
        self.ui.tabWidget.currentChanged.connect(lambda tab_idx: self.load_saved_data(tab_idx))


    def load_saved_data(self, tab_idx):
        """ Loads saved data
        """
        if tab_idx == 1:
            #self.load_saved_data_pile()
            pass
        elif tab_idx == 2:
            self.load_saved_data_barrette()
        
        elif tab_idx == 0:
            self.ui.toolBox.setCurrentIndex(0)  # show material stress-strain curves


    def load_saved_data_barrette(self):
        """ Loads saved data pile
        """
        try:
            if self.staggered_reinf_vertical_barrette_A_s_1:
                self.fill_table_reinf_staggering_vertical_barrette_A_s_1_saved_values(self.ui.tableWidget_9)
            if self.staggered_reinf_vertical_barrette_A_s_2:
                self.fill_table_reinf_staggering_vertical_barrette_A_s_2_saved_values(self.ui.tableWidget_8)
            if self.staggered_reinf_shear_barrette:
                self.fill_table_reinf_staggering_shear_barrette_saved_values()

        except:
            pass

    def update_min_reinforcement(self, check_state):
        """ Updates minimum reinforcement parameter
        """
        if check_state is True:    # checked# checked
            self.min_reinf = True
            self.ui.checkBox.setCheckState(2)
        else:
            self.min_reinf = False
            self.ui.checkBox.setCheckState(0)

        # update results
        self.update_results_pile()
        self.update_results_barrette()


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

    
    def display_results_pile(self):
        """ Shows internal forces on table
        Assign default values if empty
        """
        if not self.internal_forces_permanent:
            self.internal_forces_permanent['N'] = -1000.0
            self.internal_forces_permanent['M'] = 2000.0
            self.internal_forces_permanent['Q'] = 1000.0
        if not self.internal_forces_transient:
            self.internal_forces_transient['N'] = 0.0
            self.internal_forces_transient['M'] = 0.0
            self.internal_forces_transient['Q'] = 0.0
        
        # get design values for internal forces
        self.get_internal_forces_design()

        # display internal forces on table
        self.ui.tableWidget_11.blockSignals(True)
        column_labels = ['Normal force N [kN]','Bending moment M [kNm]', 'Shear force Q [kN]']
        row_labels = ['Permanent force', 'Transient force', 'Design value']
        self.ui.tableWidget_11.setColumnCount(len(row_labels))
        self.ui.tableWidget_11.setRowCount(len(column_labels))
        self.ui.tableWidget_11.setHorizontalHeaderLabels(row_labels)
        self.ui.tableWidget_11.setVerticalHeaderLabels(column_labels)
        keys = ['N', 'M', 'Q']
        for i, key in enumerate(keys):
            self.ui.tableWidget_11.setItem(i, 0, QtWidgets.QTableWidgetItem(str(self.internal_forces_permanent[key])))
            self.ui.tableWidget_11.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.internal_forces_transient[key])))
            self.ui.tableWidget_11.setItem(i, 2, QtWidgets.QTableWidgetItem(str(self.internal_forces_design[key])))
            self.ui.tableWidget_11.item(i, 0).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget_11.item(i, 1).setBackground(QColor(242, 255, 116))

        # calculate the required reinforcement
        A_s, a_s = self.calculate_required_reinforcement_pile()

        # display the required reinforcement
        self.display_required_reinforcement_pile(A_s, a_s)

        # store required reinforcemetns for report
        self.A_s, self.a_s = A_s, a_s

        self.ui.tableWidget_11.blockSignals(False)


    def display_required_reinforcement_pile(self, A_s, a_s):
        """ Displays the required reinforcement for pile on table
        """
        column_labels = ['Required A_s [cm^2]', 'Required a_s [cm^2/m]']
        self.ui.tableWidget_13.setColumnCount(1)
        self.ui.tableWidget_13.setRowCount(len(column_labels))
        self.ui.tableWidget_13.setHorizontalHeaderLabels(['Value'])
        self.ui.tableWidget_13.setVerticalHeaderLabels(column_labels)
        self.ui.tableWidget_13.setItem(0, 0, QtWidgets.QTableWidgetItem('{0:.2f}'.format(A_s)))
        self.ui.tableWidget_13.setItem(1, 0, QtWidgets.QTableWidgetItem('{0:.2f}'.format(a_s)))


    def respond_to_cell_changes_in_internal_forces_pile(self, row, column):
        """ Updates internal forces for pile and display results
        """
        try:
            if row < 3:
                value = float(self.ui.tableWidget_11.item(row, column).text())
                keys = ['N', 'M', 'Q']
                if column == 0:
                    self.internal_forces_permanent[keys[row]] = value
                elif column == 1:
                    self.internal_forces_transient[keys[row]] = value

                # get and display characteristic/ design values for internal forces
                self.display_results_pile()

        except ValueError:
            self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')


    def read_internal_forces_pile(self):
        """ Reads internal forces for pile from table
        """
        keys = ['N', 'M', 'Q']
        for row_i in range(len(keys)):
            value_perm = float(self.ui.tableWidget_11.item(row_i, 0).text())
            value_tran = float(self.ui.tableWidget_11.item(row_i, 1).text())
            self.internal_forces_permanent[keys[row_i]] = value_perm
            self.internal_forces_transient[keys[row_i]] = value_tran


    def update_results_pile(self):
        """ Update results for pile
        """
        try:
            self.read_internal_forces_pile()
            self.display_results_pile()
        except:
            pass


    def display_results_barrette(self):
        """ Shows internal forces on table for rectangular cross-section
        Assign default values if empty
        """
        if not self.internal_forces_permanent:
            self.internal_forces_permanent['N'] = -1000.0
            self.internal_forces_permanent['M'] = 2000.0
            self.internal_forces_permanent['Q'] = 1000.0
        if not self.internal_forces_transient:
            self.internal_forces_transient['N'] = 0.0
            self.internal_forces_transient['M'] = 0.0
            self.internal_forces_transient['Q'] = 0.0
        
        # get design values for internal forces
        self.get_internal_forces_design()

        # display internal forces on table
        self.ui.tableWidget_12.blockSignals(True)
        column_labels = ['Normal force N [kN]','Bending moment M [kNm]', 'Shear force Q [kN]']
        row_labels = ['Permanent force', 'Transient force', 'Design value']
        self.ui.tableWidget_12.setColumnCount(len(row_labels))
        self.ui.tableWidget_12.setRowCount(len(column_labels))
        self.ui.tableWidget_12.setHorizontalHeaderLabels(row_labels)
        self.ui.tableWidget_12.setVerticalHeaderLabels(column_labels)
        keys = ['N', 'M', 'Q']
        for i, key in enumerate(keys):
            self.ui.tableWidget_12.setItem(i, 0, QtWidgets.QTableWidgetItem(str(self.internal_forces_permanent[key])))
            self.ui.tableWidget_12.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.internal_forces_transient[key])))
            self.ui.tableWidget_12.setItem(i, 2, QtWidgets.QTableWidgetItem(str(self.internal_forces_design[key])))
            self.ui.tableWidget_12.item(i, 0).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget_12.item(i, 1).setBackground(QColor(242, 255, 116))

        # calculate the required reinforcement
        A_s1, A_s2, a_s12, A_s1_sym, A_s2_sym, a_s12_sym = self.calculate_required_reinforcement_barrette()

        # display the required reinforcement
        self.display_required_reinforcement_barrette(A_s1, A_s2, a_s12, A_s1_sym, A_s2_sym, a_s12_sym )

        # store required reinforcemetns for report
        self.A_s1, self.A_s2, self.a_s12, self.A_s1_sym, self.A_s2_sym, self.a_s12_sym = A_s1, A_s2, a_s12, A_s1_sym, A_s2_sym, a_s12_sym

        self.ui.tableWidget_12.blockSignals(False)


    def display_required_reinforcement_barrette(self, A_s1, A_s2, a_s12, A_s1_sym, A_s2_sym, a_s12_sym ):
        """ Displays the required reinforcement for pile on table
        """
        column_labels = ['Required A_s1 [cm^2]','Required A_s2 [cm^2]', 'Required a_s [cm^2/m]']
        row_labels = ['Non-symmetry', 'Symmetry']
        self.ui.tableWidget_14.setColumnCount(2)
        self.ui.tableWidget_14.setRowCount(len(column_labels))
        self.ui.tableWidget_14.setHorizontalHeaderLabels(row_labels)
        self.ui.tableWidget_14.setVerticalHeaderLabels(column_labels)
        self.ui.tableWidget_14.setItem(0, 0, QtWidgets.QTableWidgetItem('{0:.2f}'.format(A_s1)))
        self.ui.tableWidget_14.setItem(1, 0, QtWidgets.QTableWidgetItem('{0:.2f}'.format(A_s2)))
        self.ui.tableWidget_14.setItem(2, 0, QtWidgets.QTableWidgetItem('{0:.2f}'.format(a_s12)))
        self.ui.tableWidget_14.setItem(0, 1, QtWidgets.QTableWidgetItem('{0:.2f}'.format(A_s1_sym)))
        self.ui.tableWidget_14.setItem(1, 1, QtWidgets.QTableWidgetItem('{0:.2f}'.format(A_s2_sym)))
        self.ui.tableWidget_14.setItem(2, 1, QtWidgets.QTableWidgetItem('{0:.2f}'.format(a_s12_sym)))


    def respond_to_cell_changes_in_internal_forces_barrette(self, row, column):
        """ Updates internal forces for barrette and display results
        """
        try:
            if row < 3:
                value = float(self.ui.tableWidget_12.item(row, column).text())
                keys = ['N', 'M', 'Q']
                if column == 0:
                    self.internal_forces_permanent[keys[row]] = value
                elif column == 1:
                    self.internal_forces_transient[keys[row]] = value

                # get and display characteristic/ design values for internal forces
                self.display_results_barrette()

        except ValueError:
            self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')


    def read_internal_forces_barrette(self):
        """ Reads internal forces for barrette from table
        """
        keys = ['N', 'M', 'Q']
        for row_i in range(len(keys)):
            value_perm = float(self.ui.tableWidget_12.item(row_i, 0).text())
            value_tran = float(self.ui.tableWidget_12.item(row_i, 1).text())
            self.internal_forces_permanent[keys[row_i]] = value_perm
            self.internal_forces_transient[keys[row_i]] = value_tran


    def update_results_barrette(self):
        """ Update results for barrette
        """
        try:
            self.read_internal_forces_barrette()
            self.display_results_barrette()
        except:
            pass


    def get_internal_forces_design(self):
        """ Gets design value of internal forces
        """
        keys = ['N', 'M', 'Q']
        gam_perm = float(self.params_psf['param_0'])
        gam_tran = float(self.params_psf['param_1'])
        for key in keys:
            self.internal_forces_design[key] = self.internal_forces_permanent[key]*gam_perm + self.internal_forces_transient[key]*gam_tran
            self.internal_forces_characteristic[key] = self.internal_forces_permanent[key] + self.internal_forces_transient[key]


    def calculate_required_reinforcement_pile(self):
        """ Calculates the required reinforcement area for pile
        """
        A_s, a_s = self.pile.calculate_required_reinforcement_cross_section(self.code, self.params_psf, self.params_concrete, self.params_reinf, self.internal_forces_characteristic, self.min_reinf)

        return A_s, a_s

    def calculate_required_reinforcement_barrette(self):
        """ Calculates the required reinforcement area for pile
        """
        A_s1, A_s2, a_s12 = self.barrette.calculate_required_reinforcement_cross_section(self.code, self.params_psf, self.params_concrete, self.params_reinf, self.internal_forces_characteristic, self.min_reinf)
        A_s1_sym, A_s2_sym, a_s12_sym = self.barrette.calculate_required_reinforcement_cross_section(self.code, self.params_psf, self.params_concrete, self.params_reinf, self.internal_forces_characteristic, self.min_reinf, sym=True)

        return abs(A_s1), abs(A_s2), abs(a_s12), abs(A_s1_sym), abs(A_s2_sym), abs(a_s12_sym)


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

        # update results
        self.update_results_pile()
        self.update_results_barrette()


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

            # update results
            self.update_results_pile()
            self.update_results_barrette()


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

                    # update results
                    self.update_results_pile()
                    self.update_results_barrette()

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

                    # update results
                    self.update_results_pile()
                    self.update_results_barrette()

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

                    # update results
                    self.update_results_pile()
                    self.update_results_barrette()

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
                        self.pile.cross_section['A'] = value/2
                    self.plot_canvas_cross_section_pile.plot_cross_section_pile(self.pile.cross_section['D'], self.pile.cross_section['H'])

                    # update result pile
                    self.update_results_pile()

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

                    # update result barrette
                    self.update_results_barrette()

                    # update reinforcement plot
                    self.plot_reinf_cross_section_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette)

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

        # update results 
        self.update_results_pile()
        self.update_results_barrette()


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

        # update results
        self.update_results_pile()
        self.update_results_barrette()


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


    def initialize_table_reinf_vertical(self, table_widget):
        """ Initializes table for vertial reinforcement
        """
        n_row = 2
        table_widget.blockSignals(True)
        table_widget.setRowCount(n_row)
        column_labels = ['n\n [-]', 'Dia.\n [mm]', 'A_s \n [cm^2]', 'Clearance\n [cm]', 'Weight [Kg/m]']
        table_widget.setColumnCount(len(column_labels))
        table_widget.setHorizontalHeaderLabels(column_labels)
        row_labels = ['Main direction', 'Orthorgonal direction']
        table_widget.setVerticalHeaderLabels(row_labels)

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
        n_row = 2
        table_widget.blockSignals(True)
        table_widget.setRowCount(n_row)
        column_labels = ['dia.\n d [mm]', 'n legs\n [-]', 'spacing\n [cm]', 'Embraces [-]', 'a_s \n [cm^2/m]', 'Weight [Kg/m]']
        table_widget.setColumnCount(len(column_labels))
        table_widget.setHorizontalHeaderLabels(column_labels)
        row_labels = ['Main direction', 'Orthorgonal direction']
        table_widget.setVerticalHeaderLabels(row_labels)

        n_column = len(column_labels)
        for row_i in range(n_row):
            for column_j in range(n_column-2):
                table_widget.setItem(row_i, column_j, QtWidgets.QTableWidgetItem(''))
                cell = table_widget.item(row_i, column_j)
                cell.setBackground(QColor(242, 255, 116))

        table_widget.blockSignals(False)


    def fill_table_reinf_staggering_vertical_barrette_A_s_1(self, table_widget):
        """ Fills table for vertical reinforcement staggering
        """
        try:
            bar_diameters = [s.strip() for s in self.ui.lineEdit_3.text().split(',')]   # text input in pannel for barrette
            self.bar_diameters_vertical = bar_diameters
            n_bars = 8

            table_widget.blockSignals(True)
            # top, n
            table_widget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(n_bars)))
            table_widget.item(0, 0).setBackground(QColor(242, 255, 116))

            # bar diameters
            for row_i in range(table_widget.rowCount()):
                combobox = QtWidgets.QComboBox()
                for dia in bar_diameters:
                    combobox.addItem(dia)
                combobox.setCurrentIndex(0)
                combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
                combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_vertical_barrette_A_s1(1,1, table_widget))
                table_widget.setCellWidget(row_i, 1, combobox)

            # calculate A_s using the initial staggered information
            try:
                dia_current = float(table_widget.cellWidget(0, 1).currentText())   #'xx'
            except ValueError:
                dia_current = float(table_widget.cellWidget(0, 1).currentText()[1:]) # 'Dxx'

            B = self.barrette.cross_section['B']
            A_s, clearance = self.barrette.calc_A_s(n_bars, dia_current, B)
            steel_weight = self.barrette.calc_weight_A_s(A_s, 1.0)  # steel weight per 1 meter
            table_widget.setItem(0, 2, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
            table_widget.setItem(0, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
            table_widget.setItem(0, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

            #### read/store and plot vertical reinf
            self.staggered_reinf_vertical_barrette_A_s_1 = self.read_reinf_vertical(table_widget)
            self.plot_reinf_cross_section_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2)

            table_widget.blockSignals(False)

        except:
            pass


    def fill_table_reinf_staggering_vertical_barrette_A_s_2(self, table_widget):
        """ Fills table for vertical reinforcement staggering
        """
        try:
            bar_diameters = [s.strip() for s in self.ui.lineEdit_3.text().split(',')]   # text input in pannel for barrette
            self.bar_diameters_vertical = bar_diameters
            n_bars = 8

            table_widget.blockSignals(True)
            # top, n
            table_widget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(n_bars)))
            table_widget.item(0, 0).setBackground(QColor(242, 255, 116))

            # bar diameters
            for row_i in range(table_widget.rowCount()):
                combobox = QtWidgets.QComboBox()
                for dia in bar_diameters:
                    combobox.addItem(dia)
                combobox.setCurrentIndex(0)
                combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")
                combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_vertical_barrette_A_s2(1,1, table_widget))
                table_widget.setCellWidget(row_i, 1, combobox)

            # calculate A_s using the initial staggered information
            try:
                dia_current = float(table_widget.cellWidget(0, 1).currentText())   #'xx'
            except ValueError:
                dia_current = float(table_widget.cellWidget(0, 1).currentText()[1:]) # 'Dxx'

            B = self.barrette.cross_section['B']
            A_s, clearance = self.barrette.calc_A_s(n_bars, dia_current, B)
            steel_weight = self.barrette.calc_weight_A_s(A_s, 1.0)  # steel weight per 1 meter
            table_widget.setItem(0, 2, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
            table_widget.setItem(0, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
            table_widget.setItem(0, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

            #### read/store and plot vertical reinf
            self.staggered_reinf_vertical_barrette_A_s_2 = self.read_reinf_vertical(table_widget, negation=True)
            self.plot_reinf_cross_section_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette)

            table_widget.blockSignals(False)

        except:
            pass


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
            combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_vertical_barrette_A_s1(1,1, table_widget))
            table_widget.setCellWidget(row_i, 1, combobox)

        for i, segment in enumerate(self.staggered_reinf_vertical_barrette_A_s_1):
            table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(segment['n'])))
            table_widget.item(i, 0).setBackground(QColor(242, 255, 116))

            # set combobox for index of bar diameter
            combobox_i = table_widget.cellWidget(i, 1)
            self.set_combobox_item(combobox_i, segment['dia'])

            try:
                dia_current = float(segment['dia'])
            except ValueError:
                dia_current = float(segment['dia'][1:])

            B = self.barrette.cross_section['B']
            A_s, clearance = self.barrette.calc_A_s(segment['n'], dia_current, B)
            steel_weight = self.barrette.calc_weight_A_s(A_s, 1.0)
            table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
            # correct clearance for additional reinforcement
            if row_i == 1:
                D = self.barrette.cross_section['D']
                H1 = self.barrette.cross_section['H1']*0.001
                H2 = self.barrette.cross_section['H2']*0.001
                h = D - H1 - H2 - dia_current*0.001   # for the correction of clearance in meter
                _, clearance = self.barrette.calc_A_s(segment['n'], segment['dia'], h)
            table_widget.setItem(i, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
            table_widget.setItem(i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

        # plot
        self.plot_reinf_cross_section_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette)

        table_widget.blockSignals(False)


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
            combobox.currentIndexChanged.connect(lambda: self.update_table_reinf_staggering_vertical_barrette_A_s2(1,1, table_widget))
            table_widget.setCellWidget(row_i, 1, combobox)

        for i, segment in enumerate(self.staggered_reinf_vertical_barrette_A_s_2):
            table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(segment['n'])))
            table_widget.item(i, 0).setBackground(QColor(242, 255, 116))

            # set combobox for index of bar diameter
            combobox_i = table_widget.cellWidget(i, 1)
            self.set_combobox_item(combobox_i, segment['dia'])

            try:
                dia_current = float(segment['dia'])
            except ValueError:
                dia_current = float(segment['dia'][1:])

            B = self.barrette.cross_section['B']
            A_s, clearance = self.barrette.calc_A_s(segment['n'], dia_current, B)
            steel_weight = self.barrette.calc_weight_A_s(A_s, 1.0)
            table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
            # correct clearance for additional reinforcement
            if row_i == 1:
                D = self.barrette.cross_section['D']
                H1 = self.barrette.cross_section['H1']*0.001
                H2 = self.barrette.cross_section['H2']*0.001
                h = D - H1 - H2 - dia_current*0.001   # for the correction of clearance in meter
                _, clearance = self.barrette.calc_A_s(segment['n'], segment['dia'], h)
            table_widget.setItem(i, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
            table_widget.setItem(i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

        # plot
        self.plot_reinf_cross_section_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette)

        table_widget.blockSignals(False)


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
            self.ui.tableWidget_10.setCellWidget(row_i, 0, combobox)

        for i, segment in enumerate(self.staggered_reinf_shear_barrette):
            self.ui.tableWidget_10.setItem(i, 1, QtWidgets.QTableWidgetItem(str(segment['n_legs'])))
            self.ui.tableWidget_10.setItem(i, 2, QtWidgets.QTableWidgetItem(str(segment['spacing'])))
            self.ui.tableWidget_10.setItem(i, 3, QtWidgets.QTableWidgetItem(segment['embrace']))
            self.ui.tableWidget_10.item(i, 1).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget_10.item(i, 2).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget_10.item(i, 3).setBackground(QColor(242, 255, 116))

            # set combobox for index of bar diameter
            combobox_i = self.ui.tableWidget_10.cellWidget(i, 0)
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
            steel_weight = self.barrette.calc_weight_a_s(a_s, 1.0, D, B, H1, H2, segment['n_legs']) # steel weight per 1 meter
            self.ui.tableWidget_10.setItem(i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(a_s)))
            self.ui.tableWidget_10.setItem(i, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

        # plot
        self.plot_reinf_cross_section_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette)

        self.ui.tableWidget_10.blockSignals(False)



    def update_table_reinf_staggering_vertical_barrette_A_s1(self, row, column, table_widget):
        """ Updates with user staggered vertical reinforcement
        """
        try:
            # calculate and fill As and clearance to table if input values are available
            for row_i in range(table_widget.rowCount()):
                text_n = table_widget.item(row_i, 0).text()
                text_dia = table_widget.cellWidget(row_i, 1).currentText()
                try:
                    if (text_n != ''):
                        B = self.barrette.cross_section['B']
                        A_s, clearance = self.barrette.calc_A_s(float(text_n), text_dia, B)
                        segment_top  = 0.0
                        segment_bottom = -1.0
                        steel_weight = self.barrette.calc_weight_A_s(A_s, segment_top - segment_bottom) # steel weight per 1 meter
                        table_widget.blockSignals(True)
                        table_widget.setItem(row_i, 2, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
                        # correct clearance for additional reinforcement
                        if row_i == 1:
                            D = self.barrette.cross_section['D']
                            H1 = self.barrette.cross_section['H1']*0.001
                            H2 = self.barrette.cross_section['H2']*0.001
                            dia = float(text_dia[1:]) if 'D' in text_dia else float(text_dia)
                            h = D - H1 - H2 - dia*0.001   # for the correction of clearance in meter
                            _, clearance = self.barrette.calc_A_s(float(text_n)+2, text_dia, h)
                        table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
                        table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                        table_widget.blockSignals(False)
                    else:
                        # clear cells
                        table_widget.blockSignals(True)
                        table_widget.setItem(row_i, 2, QtWidgets.QTableWidgetItem(''))
                        table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem(''))
                        table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                        table_widget.blockSignals(False)

                except (ValueError, ZeroDivisionError) as e:
                    self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')
                    # clear cells
                    table_widget.blockSignals(True)
                    table_widget.setItem(row_i, 2, QtWidgets.QTableWidgetItem(''))
                    table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem(''))
                    table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                    table_widget.blockSignals(False)
                    return

            ## read/store and plot vertical reinf
            self.staggered_reinf_vertical_barrette_A_s_1 = self.read_reinf_vertical(self.ui.tableWidget_9)
            self.plot_reinf_cross_section_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette)

        except ValueError:
            self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')


    def update_table_reinf_staggering_vertical_barrette_A_s2(self, row, column, table_widget):
        """ Updates with user staggered vertical reinforcement
        """
        try:
            # calculate and fill As and clearance to table if input values are available
            for row_i in range(table_widget.rowCount()):
                text_n = table_widget.item(row_i, 0).text()
                text_dia = table_widget.cellWidget(row_i, 1).currentText()
                try:
                    if (text_n != ''):
                        B = self.barrette.cross_section['B']
                        A_s, clearance = self.barrette.calc_A_s(float(text_n), text_dia, B)
                        segment_top  = 0.0
                        segment_bottom = -1.0
                        steel_weight = self.barrette.calc_weight_A_s(A_s, segment_top - segment_bottom) # steel weight per 1 meter
                        table_widget.blockSignals(True)
                        table_widget.setItem(row_i, 2, QtWidgets.QTableWidgetItem('{:.2f}'.format(A_s)))
                        # correct clearance for additional reinforcement
                        if row_i == 1:
                            D = self.barrette.cross_section['D']
                            H1 = self.barrette.cross_section['H1']*0.001
                            H2 = self.barrette.cross_section['H2']*0.001
                            dia = float(text_dia[1:]) if 'D' in text_dia else float(text_dia)
                            h = D - H1 - H2 - dia*0.001   # for the correction of clearance in meter
                            _, clearance = self.barrette.calc_A_s(float(text_n)+2, text_dia, h)
                        table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(clearance)))
                        table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))
                        table_widget.blockSignals(False)
                    else:
                        # clear cells
                        table_widget.blockSignals(True)
                        table_widget.setItem(row_i, 2, QtWidgets.QTableWidgetItem(''))
                        table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem(''))
                        table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                        table_widget.blockSignals(False)

                except (ValueError, ZeroDivisionError) as e:
                    self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')
                    # clear cells
                    table_widget.blockSignals(True)
                    table_widget.setItem(row_i, 2, QtWidgets.QTableWidgetItem(''))
                    table_widget.setItem(row_i, 3, QtWidgets.QTableWidgetItem(''))
                    table_widget.setItem(row_i, 4, QtWidgets.QTableWidgetItem(''))
                    table_widget.blockSignals(False)
                    return

            ## read/store and plot vertical reinf
            self.staggered_reinf_vertical_barrette_A_s_2 = self.read_reinf_vertical(self.ui.tableWidget_8, negation=True)
            self.plot_reinf_cross_section_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette)

        except ValueError:
            self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')


    def fill_table_reinf_staggering_shear_barrette(self):
        """ Fills table for vertical reinforcement staggering
        """
        try:
            bar_diameters = [s.strip() for s in self.ui.lineEdit_4.text().split(',')]   # text input in pannel for barrette
            self.bar_diameters_shear = bar_diameters
            n_legs = 4
            spacing = 25.0
            # intial embrace for main vertical bars
            if not self.staggered_reinf_shear_barrette:
                embrace = '1 ' + str(int(self.staggered_reinf_vertical_barrette_A_s_1[0]['n']))
            else:
                embrace = self.staggered_reinf_shear_barrette[0]['embrace']

            self.ui.tableWidget_10.blockSignals(True)
            # top, n_legs
            self.ui.tableWidget_10.setItem(0, 1, QtWidgets.QTableWidgetItem(str(n_legs)))
            self.ui.tableWidget_10.setItem(0, 2, QtWidgets.QTableWidgetItem(str(spacing)))
            self.ui.tableWidget_10.setItem(0, 3, QtWidgets.QTableWidgetItem(embrace))
            self.ui.tableWidget_10.item(0, 1).setBackground(QColor(242, 255, 116))
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
                self.ui.tableWidget_10.setCellWidget(row_i, 0, combobox)

            # calculate a_s using the initial staggered information
            try:
                dia_current = float(self.ui.tableWidget_10.cellWidget(0, 0).currentText())   #'xx'
            except ValueError:
                dia_current = float(self.ui.tableWidget_10.cellWidget(0, 0).currentText()[1:]) # 'Dxx'
            D = self.barrette.cross_section['D']
            B = self.barrette.cross_section['B']
            H1 = self.barrette.cross_section['H1']
            H2 = self.barrette.cross_section['H2']
            a_s = self.barrette.calc_a_s(n_legs, dia_current, spacing)
            steel_weight = self.barrette.calc_weight_a_s(a_s, 1.0, D, B, H1, H2, n_legs)    # steel weight per 1 meter
            self.ui.tableWidget_10.setItem(0, 4, QtWidgets.QTableWidgetItem('{:.2f}'.format(a_s)))
            self.ui.tableWidget_10.setItem(0, 5, QtWidgets.QTableWidgetItem('{:.2f}'.format(steel_weight)))

            ## read/store and plot vertical reinf
            self.staggered_reinf_shear_barrette = self.read_reinf_shear(self.ui.tableWidget_10)
            self.plot_reinf_cross_section_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette)

            self.ui.tableWidget_10.blockSignals(False)

        except:
            pass


    def update_table_reinf_staggering_shear_barrette(self, row, column):
        """ Updates with user staggered shear reinforcement
        """
        #print('update tale reinf staggering shear')
        try:
            # calculate and fill As and clearance to table if input values are available
            for row_i in range(self.ui.tableWidget_10.rowCount()):
                text_n_legs = self.ui.tableWidget_10.item(row_i, 1).text()
                text_spacing = self.ui.tableWidget_10.item(row_i, 2).text()
                text_dia = self.ui.tableWidget_10.cellWidget(row_i, 0).currentText()
                try:
                    if (text_n_legs != '') and (text_spacing != ''):
                        D = self.barrette.cross_section['D']
                        B = self.barrette.cross_section['B']
                        H1 = self.barrette.cross_section['H1']
                        H2 = self.barrette.cross_section['H2']
                        a_s = self.barrette.calc_a_s(float(text_n_legs), text_dia, float(text_spacing))
                        steel_weight = self.barrette.calc_weight_a_s(a_s, 1.0, D, B, H1, H2, float(text_n_legs))    # steel weigth per 1 meter
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
            self.plot_reinf_cross_section_barrette(self.staggered_reinf_vertical_barrette_A_s_1, self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette)

        except ValueError:
            self.dialog.show_message_box('Error', 'Please check if the value you entered is correct!')


    def read_reinf_vertical(self, table_widget, negation=False):
        """ Reads staggered vertical reinforcement and store it
        """
        staggered_reinf_vertical_all = []   # include additional reinforcement in the other direction

        for row_i in range(table_widget.rowCount()):
            staggered_reinf_vertical = {}

            text_n = table_widget.item(row_i, 0).text()
            if text_n != '':
                text_dia = table_widget.cellWidget(row_i, 1).currentText()
                item_weight = table_widget.item(row_i, 4)
                item_A_s = table_widget.item(row_i, 2)
                item_clearance = table_widget.item(row_i, 3)
                if item_A_s is not None:
                    staggered_reinf_vertical['top'] = 0.0
                    staggered_reinf_vertical['bottom'] = -1.0
                    staggered_reinf_vertical['n'] = float(text_n)
                    staggered_reinf_vertical['dia'] = text_dia
                    staggered_reinf_vertical['clearance'] = float(item_clearance.text())
                    if negation:
                        staggered_reinf_vertical['A_s'] = -float(item_A_s.text())
                    else:
                        staggered_reinf_vertical['A_s'] = float(item_A_s.text())
                    staggered_reinf_vertical['weight'] = float(item_weight.text())
                    staggered_reinf_vertical_all.append(staggered_reinf_vertical)
            
        return staggered_reinf_vertical_all


    def read_reinf_shear(self, table_widget):
        """ Reads staggered shear reinforcement and store it
        """
        staggered_reinf_shear_all = []   # include additional reinforcement in the other direction

        for row_i in range(table_widget.rowCount()):
            staggered_reinf_shear = {}

            text_n_legs = table_widget.item(row_i, 1).text()
            text_spacing = table_widget.item(row_i, 2).text()
            text_embrace = table_widget.item(row_i, 3).text()
            text_dia = table_widget.cellWidget(row_i, 0).currentText()
            item_weight = table_widget.item(row_i, 5)
            item_a_s = table_widget.item(row_i, 4)
            if (item_a_s is not None) and (item_a_s.text() != ''):
                staggered_reinf_shear['top'] = 0.0
                staggered_reinf_shear['bottom'] = -1.0
                staggered_reinf_shear['n_legs'] = float(text_n_legs)
                staggered_reinf_shear['spacing'] = float(text_spacing)
                staggered_reinf_shear['embrace'] = text_embrace
                staggered_reinf_shear['dia'] = text_dia
                staggered_reinf_shear['a_s'] = float(item_a_s.text())
                staggered_reinf_shear['weight'] = float(item_weight.text())
                staggered_reinf_shear_all.append(staggered_reinf_shear)

        return staggered_reinf_shear_all


    def plot_reinf_cross_section_barrette(self, reinf_vertical_As1, reinf_vertical_As2, reinf_shear=None):
        """ Plots the required vertical reinforcement and the reinforcement given by user
        """
        self.ui.toolBox.setCurrentIndex(1)

        # clear axis
        self.plot_canvas_reinf.axes.cla()

        if reinf_vertical_As1 and reinf_vertical_As2:
            self.plot_canvas_reinf.plot_reinf_cross_section_barrette(self.barrette.cross_section, reinf_vertical_As1, reinf_vertical_As2, reinf_shear)


    def print_report_pile(self):
        """ Generates PDF report
        """
        self.dialog.show_message_box('Error', 'No implementation yet, please make a request if you need this feature.')


    def print_report_barrette(self):
        """ Generates PDF report
        """
        try:
            r = self.barrette.print_report_cross_section(self.project_title, self.code, self.concrete_grade, self.concrete_param_names_per_code, self.params_concrete, self.reinf_grade, self.reinf_param_names, self.params_reinf, self.stress_strain,
                         self.design_situation, self.psf_param_names_per_code, self.params_psf, self.internal_forces_permanent, self.internal_forces_transient, self.internal_forces_design, self.staggered_reinf_vertical_barrette_A_s_1,  self.staggered_reinf_vertical_barrette_A_s_2, self.staggered_reinf_shear_barrette, self.A_s1_sym, self.A_s2_sym, self.a_s12_sym)

            if r != int(0):
                self.dialog.show_message_box('Error', 'Before printing the report, please close the file {}'.format(r))

        except Exception as e:
            write_traceback_to_file(sys.modules['moniman_paths']['MONIMAN_OUTPUTS'], e)
            self.dialog.show_message_box('Error', 'Please view ERROR_LOG.txt in {} for further information'.format(os.path.join(sys.modules['moniman_paths']['MONIMAN_OUTPUTS'])))
        