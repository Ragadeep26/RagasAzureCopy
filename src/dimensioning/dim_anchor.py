# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 16:34:14 2021

@author: nya
"""

import sys
import os
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtGui import QBrush, QColor, QFont
#from PyQt5.QtCore import pyqtSlot
from gui.gui_widget_Dim_anchor import Ui_Form as DimForm
from gui.gui_all_dialogs_ui import Ui_Dialog
from dimensioning.anchor import get_f_t_01_k, get_R_t_d, get_F_p, get_F_p_wallman
from report.report_with_matplotlib import Report
from matplotlib.backends.backend_pdf import PdfPages

ACROBAT = r'C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat'

# parameters for strands
PARAM_STRAND_GRADE_1570_1770 = {'R_p0.01%': 1350.0, 'R_p0.1%': 1500.0, 'R_p0.2%':1570.0, 'R_m': 1770, 'E_p': 195000.0} # units: limit strengths [N/mm**2], E modulus [N/mm**2]
PARAM_STRAND_GRADE_1660_1860 = {'R_p0.01%': 1400.0, 'R_p0.1%': 1600.0, 'R_p0.2%':1660.0, 'R_m': 1860, 'E_p': 195000.0} # unit: limit strengths [N/mm**2]
PARAM_STRAND_DIA_060INC = {'Perimeter': 15.3, 'Area': 140.0, 'Weight': 1093.0} # units [mm], [mm**2], [g/m]
PARAM_STRAND_DIA_062INC = {'Perimeter': 15.7, 'Area': 150.0, 'Weight': 1172.0} # units [mm], [mm**2], [g/m]

# parameter for PSFs
PARAM_PSF_E = {'gamma_G': 1.35, 'gamma_M': 1.15, 'gamma_a': 1.1} # safety factors for final construction stage on load, material, and grout body
PARAM_PSF_V = {'gamma_G': 1.2, 'gamma_M': 1.15, 'gamma_a': 1.1} # safety factors for transient construction stage on load, material, and grout body

              
class Dim_anchor(QtWidgets.QWidget):
    """ This class implements dimensioning tool for anchors
    """
    def __init__(self, form, project_title, Anchors):
        super(Dim_anchor, self).__init__()
        self.ui = DimForm()
        self.ui.setupUi(form)
        self.dialog = Ui_Dialog()
        self.project_title = project_title

        self.Anchors = Anchors
        
        self.initialize_params()
        self.initialize_psfs()

        # check strand utilization
        self.check_strand_utilization()

        # display results on table
        self.display_anchors_on_table()
        
        
        # connect signals and update basic settings once
        self.connect_signals_to_slots()
        
        form.exec_()
        

    def connect_signals_to_slots(self):
        """ Connects all signals to slots
        """
        self.ui.tableWidget.cellChanged.connect(lambda row, column: self.respond_to_change_in_value_psf(row, column))
        self.ui.tableWidget_2.cellChanged.connect(lambda row, column: self.respond_to_change_in_value_strand(row, column))
        self.ui.pushButton.clicked.connect(self.print_report) # print report 
        
    def initialize_params(self):
        """ Initialize parameters for strand grades and strand diameters
        """
        self.param_strand_grades = {'1570/1770': PARAM_STRAND_GRADE_1570_1770, '1660/1860': PARAM_STRAND_GRADE_1660_1860}
        self.param_strand_dias = {"0.6''": PARAM_STRAND_DIA_060INC, "0.62''": PARAM_STRAND_DIA_062INC}
        

    def initialize_psfs(self):
        """ Initializes partial safety factors
        """
        self.param_psfs = {'Situation E': PARAM_PSF_E, 'Situation V':PARAM_PSF_V}
        self.display_psfs_on_table(self.param_psfs)

    

    
    def display_psfs_on_table(self, param_psfs):
        """ Displays safety factors on table
        """
        self.ui.tableWidget.blockSignals(True)

        column_labels = ['Situation E', 'Situation V']
        row_labels = ['Safety on load gamma_G', 'Safety on strand gamma_M', 'Safety on grout body gamma_a']
        self.ui.tableWidget.setRowCount(3)
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setHorizontalHeaderLabels(column_labels)
        self.ui.tableWidget.setVerticalHeaderLabels(row_labels)

        for i_col, case in enumerate(column_labels):
            item_gamma_G = QtWidgets.QTableWidgetItem(str(param_psfs[case]['gamma_G']))
            item_gamma_M = QtWidgets.QTableWidgetItem(str(param_psfs[case]['gamma_M']))
            item_gamma_a = QtWidgets.QTableWidgetItem(str(param_psfs[case]['gamma_a']))
            self.ui.tableWidget.setItem(0, i_col, item_gamma_G)
            self.ui.tableWidget.item(0, i_col).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget.setItem(1, i_col, item_gamma_M)
            self.ui.tableWidget.item(1, i_col).setBackground(QColor(242, 255, 116))
            self.ui.tableWidget.setItem(2, i_col, item_gamma_a)
            self.ui.tableWidget.item(2, i_col).setBackground(QColor(242, 255, 116))
    
        self.ui.tableWidget.blockSignals(False)


    def check_strand_utilization(self):
        """ Calculate strand capacity and utilization
        """
        for anchor in self.Anchors:
            F_k = anchor['F_anchor']            # characteristic anchor force (from PLAXIS2D)
            gamma_G = self.param_psfs[anchor['design situation']]['gamma_G']
            F_d = F_k * gamma_G       # design anchor force
            anchor['F_d'] = F_d
            gamma_M = self.param_psfs[anchor['design situation']]['gamma_M']
            gamma_a = self.param_psfs[anchor['design situation']]['gamma_a']
            f_t_01_k = get_f_t_01_k(self.param_strand_grades[anchor['strand grade']]['R_p0.1%'], self.param_strand_dias[anchor['strand diameter']]['Area'], anchor['strand number'])
            R_t_d = get_R_t_d(self.param_strand_grades[anchor['strand grade']]['R_p0.1%'], self.param_strand_dias[anchor['strand diameter']]['Area'], anchor['strand number'], gamma_M)
            F_p_permissible = get_F_p(self.param_strand_grades[anchor['strand grade']]['R_p0.1%'], self.param_strand_grades[anchor['strand grade']]['R_m'], self.param_strand_dias[anchor['strand diameter']]['Area'], anchor['strand number'], R_t_d, gamma_a)
            F_p = get_F_p_wallman(F_d, gamma_a)
            anchor['f_t_01_k'] = f_t_01_k
            anchor['R_t_d'] = R_t_d
            anchor['F_p'] = F_p
            anchor['F_p permissible'] = F_p_permissible
            anchor['F_d/R_t_d'] = F_d/R_t_d
            anchor['F_p/F_p permissible'] = F_p/F_p_permissible


    def display_anchors_on_table(self):
        """ Displays anchors on table
        """
        self.ui.tableWidget_2.blockSignals(True)
        self.ui.tableWidget_2.setColumnCount(len(self.Anchors))
        column_labels = ['Anchor ' + str(i+1) for i in range(len(self.Anchors))]
        row_keys = ['strand grade', 'position', 'angle', 'Lspacing', 'strand number', 'strand diameter', 'F_anchor', 'design situation', 'F_d', 'R_t_d', 'F_p', 'F_p permissible', 'F_d/R_t_d', 'F_p/F_p permissible']
        row_units = ['[-]', '[mNN]', '[deg]', '[m]', '[-]', "['']", '[kN]', '[-]', '[kN]', '[kN]', '[kN]', '[kN]', '[-]', '[-]']
        row_labels = [key for key in row_keys]
        # capitalize row headers
        for i in range(10):
            row_labels[i] = row_labels[i].capitalize()
        # add prefix to row headers
        prefixes = ['']*len(row_labels)
        prefixes[8] = 'Design load '
        prefixes[9] = 'Design resistance '
        prefixes[10] = 'Test force '
        prefixes[11] = 'Test force '
        prefixes[12] = 'Utilization '
        prefixes[13] = 'Utilization '
        for i in range(len(row_labels)):
            row_labels[i] = prefixes[i] + row_labels[i]

        # add units
        row_labels = [key + ' ' + unit for key, unit in zip(row_labels, row_units)]

        self.ui.tableWidget_2.setRowCount(len(row_labels))
        self.ui.tableWidget_2.setHorizontalHeaderLabels(column_labels)
        self.ui.tableWidget_2.setVerticalHeaderLabels(row_labels)

        for i_col, anchor in enumerate(self.Anchors):
            for i_row, key in enumerate(row_keys):
                #if anchor['F_anchor'] is None: # no anchor force(s) registered
                #    anchor['F_anchor'] = 0.0
                #    self.ui.tableWidget_2.setItem(i_row, i_col, QtWidgets.QTableWidgetItem(str(anchor[key])))
                #    self.ui.tableWidget_2.item(i_row, i_col).setBackground(QColor(242, 255, 116))

                # format float number to display
                if isinstance(anchor[key], float):
                    text = '{0:.2f}'.format(anchor[key])
                else:
                    text = str(anchor[key])

                if key == 'position':
                    self.ui.tableWidget_2.setItem(i_row, i_col, QtWidgets.QTableWidgetItem('{0:.2f}'.format(anchor[key][1])))

                elif key == 'strand grade':  # combobox item
                    combobox = self.display_steel_grade_in_combobox(text)
                    combobox.setProperty('column', i_col)  # set property for later access
                    combobox.activated[str].connect(self.respond_to_change_in_strand_grade)
                    self.ui.tableWidget_2.setCellWidget(i_row, i_col, combobox)
                
                elif key == 'strand diameter':  # combobox item
                    combobox = self.display_strand_dia_in_combobox(text)
                    combobox.setProperty('column', i_col)  # set property for later access
                    combobox.activated[str].connect(self.respond_to_change_in_dia)
                    self.ui.tableWidget_2.setCellWidget(i_row, i_col, combobox)

                elif key == 'design situation':  # combobox item
                    combobox = self.display_design_situation_in_combobox(text)
                    combobox.setProperty('column', i_col)  # set property for later access
                    combobox.activated[str].connect(self.respond_to_change_in_design_situation)
                    self.ui.tableWidget_2.setCellWidget(i_row, i_col, combobox)

                elif key in ['strand number', 'strand diameter', 'F_anchor']: # user can adjust these parameters
                    self.ui.tableWidget_2.setItem(i_row, i_col, QtWidgets.QTableWidgetItem(text))
                    self.ui.tableWidget_2.item(i_row, i_col).setBackground(QColor(242, 255, 116))
                
                elif key in ['R_t_d', 'F_p', 'F_d/R_t_d', 'F_p/F_p permissible']: # set front bold
                    self.ui.tableWidget_2.setItem(i_row, i_col, QtWidgets.QTableWidgetItem(text))
                    self.ui.tableWidget_2.item(i_row, i_col).setFont(QFont('Anton', 10, QFont.Bold))

                    # set color
                    if key in ['F_d/R_t_d', 'F_p/F_p permissible']:
                        if anchor[key] < 1.0:
                            self.ui.tableWidget_2.item(i_row, i_col).setForeground(QBrush(QColor(0, 0, 255)))
                        else:
                            self.ui.tableWidget_2.item(i_row, i_col).setForeground(QBrush(QColor(255, 0, 0)))

                else:
                    self.ui.tableWidget_2.setItem(i_row, i_col, QtWidgets.QTableWidgetItem(text))


        self.ui.tableWidget_2.blockSignals(False)
    

    def display_steel_grade_in_combobox(self, steel_grade):
        """ Displays strand steel grade in combobox
        """
        combobox = QtWidgets.QComboBox()
        combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")

        steel_grades = ['1570/1770', '1660/1860']
        for grade in steel_grades:
            combobox.addItem(grade)

        # show current item
        for idx in range(combobox.count()):
            if combobox.itemText(idx) == steel_grade:
                combobox.setCurrentIndex(idx)
        
        return combobox


    def display_strand_dia_in_combobox(self, strand_dia):
        """ Displays strand diameter in combobox
        """
        combobox = QtWidgets.QComboBox()
        combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")

        strand_dias = ["0.6''", "0.62''"]
        for dia in strand_dias:
            combobox.addItem(dia)

        # show current item
        for idx in range(combobox.count()):
            if combobox.itemText(idx) == strand_dia:
                combobox.setCurrentIndex(idx)
        
        return combobox


    def display_design_situation_in_combobox(self, design_situation):
        """ Displays design situation in combobox
        """
        combobox = QtWidgets.QComboBox()
        combobox.setStyleSheet("background-color: rgb(242, 255, 116);\n")

        situations = ['Situation E', 'Situation V']
        for situation in situations:
            combobox.addItem(situation)

        # show current item
        for idx in range(combobox.count()):
            if combobox.itemText(idx) == design_situation:
                combobox.setCurrentIndex(idx)
        
        return combobox


    #@pyqtSlot()
    def respond_to_change_in_dia(self, text):
        """ Responds to change in strand diameter
        """
        combobox = self.ui.tableWidget_2.sender()
        i_anchor = combobox.property('column')
        self.Anchors[i_anchor]['strand diameter'] = text
        # recalculate
        self.check_strand_utilization()
        # show on table
        self.display_anchors_on_table()


    #@pyqtSlot()
    def respond_to_change_in_strand_grade(self, text):
        """ Responds to change in strand grade
        """
        combobox = self.ui.tableWidget_2.sender()
        i_anchor = combobox.property('column')
        self.Anchors[i_anchor]['strand grade'] = text
        # recalculate
        self.check_strand_utilization()
        # show on table
        self.display_anchors_on_table()


    #@pyqtSlot()
    def respond_to_change_in_design_situation(self, text):
        """ Responds to change in design situation
        """
        combobox = self.ui.tableWidget_2.sender()
        i_anchor = combobox.property('column')
        self.Anchors[i_anchor]['design situation'] = text
        # recalculate
        self.check_strand_utilization()
        # show on table
        self.display_anchors_on_table()
    

    #@pyqtSlot()
    def respond_to_change_in_value_strand(self, row, column):
        """ Responds to change in strand
        """
        if column < len(self.Anchors):
            try:
                if row == 4:    # strand number
                    text = self.ui.tableWidget_2.item(row, column).text()
                    self.Anchors[column]['strand number'] = int(text)

                elif row == 6:    # F_anchor
                    text = self.ui.tableWidget_2.item(row, column).text()
                    self.Anchors[column]['F_anchor'] = float(text)

                # recalculate
                self.check_strand_utilization()
                # show on table
                self.display_anchors_on_table()

            except:
                pass


    #@pyqtSlot()
    def respond_to_change_in_value_psf(self, row, column):
        """ Responds to change in safety factors
        """
        try:
            text = self.ui.tableWidget.item(row, column).text()

            design_situation = self.ui.tableWidget.horizontalHeaderItem(column).text()
            if row == 0:
                self.param_psfs[design_situation]['gamma_G'] = float(text)
            elif row == 1:
                self.param_psfs[design_situation]['gamma_M'] = float(text)
            elif row == 2:
                self.param_psfs[design_situation]['gamma_a'] = float(text)

            # recalculate
            self.check_strand_utilization()
            # show on table
            self.display_anchors_on_table()

        except:
            pass
    

    def print_report(self):
        """ Prints report for anchor dimensions
        """
        try:
            MONIMAN_OUTPUTS = sys.modules['moniman_paths']['MONIMAN_OUTPUTS']
        except KeyError: # no project folder exists
            MONIMAN_OUTPUTS = '.'

        report_pages = []   # max. 5 anchors are shown in each page
        for anchors_group in range(len(self.Anchors)//5 + 1):
            report_page = Report()
            report_page.add_project_info_anchor(self.project_title)
            report_page.add_table_psf_anchor(self.param_psfs)
            index_start = 5*anchors_group
            index_end = 5*anchors_group + 5
            index_end = index_end if (index_end <= len(self.Anchors)) else len(self.Anchors)
            if len(self.Anchors) == 1:    # only 1 anchor
                report_page.add_table_anchors([self.Anchors[0]], 0)
            else:
                report_page.add_table_anchors(self.Anchors[index_start: index_end], index_start)
            report_pages.append(report_page)

        try:    
            filename = os.path.join(MONIMAN_OUTPUTS, 'Design of Anchors' + self.project_title + '.pdf')
            pp = PdfPages(filename)
            for report_page in report_pages:
                report_page.fig.savefig(pp, format='pdf')

            pp.close()
            # view report in Acrobat Reader
            cmd = [os.path.join(ACROBAT, r'Acrobat.exe')]
            cmd.append(filename)
            subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)
            
            return int(0)

        except PermissionError:
            return filename