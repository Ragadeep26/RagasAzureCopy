#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.patches import PathPatch, Rectangle, Circle, Arrow
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import pandas as pd
from datetime import date
from src.co2_calculator.structures.anchor import Anchor
from src.co2_calculator.structures.wall_pile import PileWall
from src.co2_calculator.structures.wall_diaphragm import DiaphragmWall
from src.co2_calculator.structures.wall_MIP import MIPWall
from src.co2_calculator.structures.wall_MIP_EPD import MIPWall_EPD
from src.co2_calculator.structures.wall_MIP_steelprofile import MIPSteelProfileWall
from src.co2_calculator.structures.wall_MIP_steelprofile_EPD import MIPSteelProfileWall_EPD

class Report(FigureCanvas):
    """ This class uses matplotlib for creating A4 pdf report
    """
    cm = 1/2.54

    def __init__(self, parent=None, dpi=100):
        self.fig = Figure(figsize=(21*Report.cm, 29.7*Report.cm), facecolor='w', dpi=dpi)
        #self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)

        # add frame
        self.add_frame()

        #self.draw()
        #self.show()
    
    def add_frame(self):
        """ Add the outer frame
        """
        # BAUER logo
        #bauer_logo = mpimg.imread('.\common\BAUER_ohneSchriftzug_Logo_png.png')    # local
        bauer_logo = mpimg.imread('./common/BAUER_ohneSchriftzug_Logo_png.png')     # on server
        imagebox = OffsetImage(bauer_logo, zoom=0.135)
        anno_box = AnnotationBbox(imagebox, (18.15*Report.cm, 26.15*Report.cm), frameon=False)
        self.axes.add_artist(anno_box)

        # Frame layout - rect(lower left point coordinates, width, height, rotation angle)
        rect = Rectangle((2.85*Report.cm, 2.7*Report.cm), 16.45*Report.cm, 24.7*Report.cm, linewidth=0.5, edgecolor='k', facecolor='none')
        self.axes.add_patch(rect)

        heights = [24.95, 24.90]
        # drawing the lines that make up the horizontal lines
        for height in heights:
            self.axes.plot([2.85*Report.cm, 19.3*Report.cm], [height*Report.cm, height*Report.cm], linewidth=0.5, color='k')

        self.axes.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

        # footnote
        self.axes.text(3*Report.cm, 2.3*Report.cm, 'BAUER Spezialtiefbau GmbH - 86529 Schrobenhausen', fontsize=7)


    def add_project_info_CO2(self, form_title, project_title=''):
        """ Adds project information for pile wall
        """
        self.axes.text(3*Report.cm, 26.8*Report.cm, form_title, fontsize=9, fontweight='bold', va='center')
        if project_title:
            self.axes.text(3*Report.cm, 26.0*Report.cm, 'Project: {} '.format(project_title), fontsize=9, fontweight='bold', va='center')
            self.axes.text(3*Report.cm, 25.4*Report.cm, 'Date: {} '.format(date.today().strftime("%b-%d-%Y")), fontsize=9, fontweight='bold', va='center')


    def add_overview_info_CO2(self, projects):
        """ Adds project overview
        """
        x0 = 3*Report.cm
        y0 = 24*Report.cm
        if len(projects) > 1:
            self.axes.text(x0, y0, 'Overview of all construction variants', fontsize=8, fontweight='bold')
        else:
            self.axes.text(x0, y0, "Overview of the construction variant", fontsize=8, fontweight='bold')

        x = [3*Report.cm, 11*Report.cm]
        y = list([y0, y0])
        for i, project in enumerate(projects):
            #y = [y[0] - 0.6*Report.cm, y[1] - 0.6*Report.cm]
            y[i%2] -= 0.6*Report.cm
            self.axes.text(x[i%2]+0.5*Report.cm, y[i%2], '{}'.format(project.project_variant), fontsize=9)
            for structure in project.structures:
                structure_tco2_eq = structure.calc_co2eq()
                #y -= 0.6*Report.cm
                y[i%2] -= 0.6*Report.cm
                if isinstance(structure, Anchor):
                    self.axes.text(x[i%2]+1.0*Report.cm, y[i%2], 'Ground anchors $tCO2eq$: {0:.1f}'.format(structure_tco2_eq), fontsize=8)
                elif isinstance(structure, PileWall):
                    self.axes.text(x[i%2]+1.0*Report.cm, y[i%2], 'Piles/ pile wall $tCO2eq$: {0:.1f}'.format(structure_tco2_eq), fontsize=8)
                elif isinstance(structure, DiaphragmWall):
                    self.axes.text(x[i%2]+1.0*Report.cm, y[i%2], 'Diaphragm wall $tCO2eq$: {0:.1f}'.format(structure_tco2_eq), fontsize=8)
                elif isinstance(structure, MIPWall):
                    self.axes.text(x[i%2]+1.0*Report.cm, y[i%2], 'MIP as cut-off wall $tCO2eq$: {0:.1f}'.format(structure_tco2_eq), fontsize=8)
                elif isinstance(structure, MIPWall_EPD):
                    self.axes.text(x[i%2]+1.0*Report.cm, y[i%2], 'MIP as cut-off wall according to EPD $tCO2eq$: {0:.1f}'.format(structure_tco2_eq), fontsize=8)
                elif isinstance(structure, MIPSteelProfileWall):
                    self.axes.text(x[i%2]+1.0*Report.cm, y[i%2], 'MIP wall with steel profiles $tCO2eq$: {0:.1f}'.format(structure_tco2_eq), fontsize=8)
                elif isinstance(structure, MIPSteelProfileWall_EPD):
                    self.axes.text(x[i%2]+1.0*Report.cm, y[i%2], 'MIP wall with steel profiles according to EPD $tCO2eq$: {0:.1f}'.format(structure_tco2_eq), fontsize=8)

        return min(y) - 0.6*Report.cm


    def add_summary_graph_CO2_projects(self, y_start, projects, df):
        """ Adds a summary graphs
        """
        x1 = 3*Report.cm
        y = y_start - 0.6*Report.cm

        if len(projects) > 1:
            self.axes.text(x1, y, '$tCO2eq$ breakdown for all construction variants', fontsize=8, fontweight='bold')
        else:
            self.axes.text(x1, y, "$tCO2eq$ breakdown", fontsize=8, fontweight='bold')

        categrogy = {'MP': 'Material production', 'MT':'Material transport', 'DT': 'Disposal transport', 'EQ': 'Equipment', 'EE': 'Energy/ electricity/ hour', 
                    'MD': 'Mobilization/ demobilization', 'PT': 'Persons transport'}

        y -= 0.6*Report.cm
        x = [3*Report.cm, 7*Report.cm, 12*Report.cm, 16*Report.cm]
        for i, (key, value) in enumerate(categrogy.items()):
            #cols[i%4].write('{0}: {1}'.format(key, value))
            y1 =  y - (i//4)*0.6*Report.cm
            self.axes.text(x[i%4], y1, '{0}: {1}'.format(key, value), fontsize=7)

        ax = self.axes.figure.add_axes([0.32, 0.2, 0.5, 0.35])
        df.plot.barh(x='Project', stacked=False, colormap='cool', ax=ax)
        ax.set_xlabel('tCO2_eq')
        #ax.set_aspect('equal')
        #ax.set_axis_off()
        ax.plot()
        self.draw()


    def add_summary_graph_CO2_categories(self, y_start, projects, df):
        """ Adds a summary graphs after categories
        """
        x1 = 3*Report.cm
        y = y_start - 0.6*Report.cm

        if len(projects) > 1:
            self.axes.text(x1, y, '$tCO2eq$ breakdown for all construction variants', fontsize=8, fontweight='bold')
        else:
            self.axes.text(x1, y, "$tCO2eq$ breakdown", fontsize=8, fontweight='bold')

        categrogy = {'MP': 'Material production', 'MT':'Material transport', 'DT': 'Disposal transport', 'EQ': 'Equipment', 'EE': 'Energy/ electricity/ hour', 
                    'MD': 'Mobilization/ demobilization', 'PT': 'Persons transport'}

        y -= 0.6*Report.cm
        x = [3*Report.cm, 7*Report.cm, 12*Report.cm, 16*Report.cm]
        for i, (key, value) in enumerate(categrogy.items()):
            #cols[i%4].write('{0}: {1}'.format(key, value))
            y1 =  y - (i//4)*0.6*Report.cm
            self.axes.text(x[i%4], y1, '{0}: {1}'.format(key, value), fontsize=7)

        ax = self.axes.figure.add_axes([0.25, 0.2, 0.60, 0.35])
        #df.plot.barh(x='Category', stacked=False, colormap='summer', ax=ax)
        #ax.set_xlabel('tCO2_eq')
        #ax.set_aspect('equal')
        #ax.set_axis_off()
        # colors
        colors_scale = np.linspace(0.4, 0.8, len(projects)) # higher number is darker
        variants_tCO2eq_sum_total = [df[proj.project_variant][0] for proj in projects]
        variants_tCO2eq_sum_total_index = sorted(range(len(variants_tCO2eq_sum_total)), key=lambda k:variants_tCO2eq_sum_total[k])
        #colors_scale_sorted # a variant with bigger tCO2_eq is darker
        colors_scale_sorted = [0]*len(projects)
        for i, index in enumerate(variants_tCO2eq_sum_total_index):
            colors_scale_sorted[index] = colors_scale[i]
        colors = plt.cm.GnBu(colors_scale_sorted)

        # some divisions for good spacing
        categrogy = ['Total', 'MP', 'MT', 'DT', 'EQ', 'EE', 'MD', 'PT']
        width = 7
        x = np.linspace(0, width, len(categrogy))
        group_width = 0.6
        bar_width = group_width/len(projects)
        x = x - group_width/2 - bar_width/2
        for i, proj in enumerate(projects):
                ax.bar(x, list(df[proj.project_variant]), width=bar_width, color=colors[i], label=proj.project_variant)
                x = x + bar_width + bar_width/5

        ax.set_xticks(x - group_width/2 - bar_width/2)
        ax.set_xticklabels(categrogy)
        ax.legend(fontsize=8)
        ax.set_ylabel('tCO2_eq')

        # For each bar in the chart, add a text label.
        for bar in ax.patches:
            # The text annotation for each bar should be its height.
            bar_value = bar.get_height()
            # Format the text with commas to separate thousands. You can do
            # any type of formatting here though.
            #text = f'{bar_value:,}'
            text = '{:.0f}'.format(bar_value)
            # This will give the middle of each bar on the x-axis.
            text_x = bar.get_x() + bar.get_width() / 2
            # get_y() is where the bar starts so we add the height to it.
            text_y = bar.get_y() + bar_value
            # If we want the text to be the same color as the bar, we can
            # get the color like so:
            bar_color = bar.get_facecolor()
            # If you want a consistent color, you can just set it as a constant, e.g. #222222
            ax.text(text_x, text_y, text, ha='center', va='bottom', color='black', size=7)

        ax.plot()
        self.draw()


    def add_summary_graph_CO2_EPD(self, y_start, projects, df):
        """ Adds a summary graphs 
        """
        x1 = 3*Report.cm
        y = y_start - 0.6*Report.cm

        categrogy = ['Total']
        df = pd.DataFrame({
                            'Category': categrogy,
                            })
        for project in projects:
            sum_project = 0.0
            for structure in project.structures:
                sum_structure = structure.calc_co2eq()
                sum_project += sum_structure

            data_project = [sum_project]  # only total CO2 for each of the projects is stored for plotting

            df[project.project_variant] = data_project

        ax = self.axes.figure.add_axes([0.25, 0.2, 0.60, 0.35])

        # colors
        colors_scale = np.linspace(0.4, 0.8, len(projects)) # higher number is darker
        variants_tCO2eq_sum_total = [df[proj.project_variant][0] for proj in projects]
        variants_tCO2eq_sum_total_index = sorted(range(len(variants_tCO2eq_sum_total)), key=lambda k:variants_tCO2eq_sum_total[k])
        #colors_scale_sorted # a variant with bigger tCO2_eq is darker
        colors_scale_sorted = [0]*len(projects)
        for i, index in enumerate(variants_tCO2eq_sum_total_index):
            colors_scale_sorted[index] = colors_scale[i]
        colors = plt.cm.GnBu(colors_scale_sorted)

        # some divisions for good spacing
        width = 1
        x = np.linspace(0, width, len(categrogy))
        group_width = 0.1
        bar_width = group_width/len(projects)
        x = x - group_width/2 - bar_width/2
        for i, proj in enumerate(projects):
            ax.bar(x, df[proj.project_variant], width=bar_width, color=colors[i], label=proj.project_variant)
            x = x + bar_width + bar_width*3

        ax.set_xticks(x - group_width/2 - bar_width/2)
        ax.set_xticklabels(categrogy)
        ax.legend(fontsize=8)
        ax.set_ylabel('tCO2_eq')

        # For each bar in the chart, add a text label.
        for bar in ax.patches:
            # The text annotation for each bar should be its height.
            bar_value = bar.get_height()
            # Format the text with commas to separate thousands. You can do
            # any type of formatting here though.
            #text = f'{bar_value:,}'
            text = '{:.0f}'.format(bar_value)
            # This will give the middle of each bar on the x-axis.
            text_x = bar.get_x() + bar.get_width() / 2
            # get_y() is where the bar starts so we add the height to it.
            text_y = bar.get_y() + bar_value
            # If we want the text to be the same color as the bar, we can
            # get the color like so:
            bar_color = bar.get_facecolor()
            # If you want a consistent color, you can just set it as a constant, e.g. #222222
            ax.text(text_x, text_y, text, ha='center', va='bottom', color='black', size=7)

        ax.plot()
        self.draw()


    def add_project_structures_input_and_results(self, project, structure):
        """ Adds input and tCO2_eq for project's structures
        """
        x1, x2 = 3*Report.cm, 10.5*Report.cm
        y = 24*Report.cm
        self.axes.text(x1, y, '{}'.format(project.project_variant), fontsize=9, fontweight='bold')
        if isinstance(structure, Anchor):
            self.axes.text(x1, y-0.6*Report.cm, 'Details for anchors', fontsize=9, fontweight='bold')
            self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, 'Anchor length [m]: {0:.1f}'.format(structure.anchor_lfm), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-2*0.6*Report.cm, 'Steel weight of anchor head [ton]: {0:.1f}'.format(structure.weight_anchorhead), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, 'Steel weight of anchor strands [m]: {0:.1f}'.format(structure.weight_anchorstrands), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-3*0.6*Report.cm, 'Production rate [m/working day]: {0:.1f} [m]'.format(structure.productivity), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-4*0.6*Report.cm, 'Cement consumption [kg/m]: {0:.1f}'.format(structure.cement), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-4*0.6*Report.cm, 'Diesel consumption [liter/working day]: {0:.1f} [m]'.format(structure.diesel), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-5*0.6*Report.cm, 'Electricity consumption [kWh/h]: {0:.1f}'.format(structure.electricity), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-5*0.6*Report.cm, 'Mob./ demob. distance [km]: {0:.1f} [m]'.format(structure.distance_mob_demob), fontsize=8)
            # intermediate results
            self.add_intermediate_results_CO2(structure, y-6*0.6*Report.cm)

        elif isinstance(structure, PileWall):
            self.axes.text(x1, y-0.6*Report.cm, 'Details for piles/ pile wall', fontsize=9, fontweight='bold')
            self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, 'Pile bore length [lm]: {0:.1f}'.format(structure.borelength_lfm), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-2*0.6*Report.cm, 'Production rate [m/working day]'.format(structure.productivity), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, 'Length of drilling template [m]: {0:.1f}'.format(structure.length_drilling_template), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-3*0.6*Report.cm, 'Production rate [m/working day]'.format(structure.productivity), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-4*0.6*Report.cm, 'Concrete volume [m$^3$] C16/20: {0:.1f}; C20/25: {1:.2f}; C25/30: {2:.2f}'.format(structure.volume_concrete['C16/20'], structure.volume_concrete['C20/25'], structure.volume_concrete['C25/30']), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-5*0.6*Report.cm, 'Concrete volume [m$^3$] C30/37: {0:.1f}; C35/45: {1:.2f}; C40/50: {2:.2f}'.format(structure.volume_concrete['C30/37'], structure.volume_concrete['C35/45'], structure.volume_concrete['C40/50']), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-6*0.6*Report.cm, 'Weight of reinforcement steel [ton]: {0:.1f}'.format(structure.weight_reinf_steel), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-6*0.6*Report.cm, 'Weight of soil disposal [ton]: {0:.1f}'.format(structure.weight_soil_disposal), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-7*0.6*Report.cm, 'Diesel consumption [liter/working day]: {0:.1f}'.format(structure.diesel), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-7*0.6*Report.cm, 'Electricity consumption [kWh/h]: {0:.1f}'.format(structure.electricity), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-8*0.6*Report.cm, 'Mob./ demob. distance [km]: {0:.1f}'.format(structure.distance_mob_demob), fontsize=8)
            # intermediate results
            self.add_intermediate_results_CO2(structure, y-9*0.6*Report.cm)

        elif isinstance(structure, DiaphragmWall):
            self.axes.text(x1, y-0.6*Report.cm, 'Details for diaphragm wall', fontsize=9, fontweight='bold')
            self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, 'Wall area [m$^2$]: {0:.1f}'.format(structure.wall_area), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-2*0.6*Report.cm, 'Wall thickness [m]: {0:.1f}'.format(structure.wall_thickness), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, 'Production rate [m$^2$/working day]: {0:.1f}'.format(structure.productivity), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-3*0.6*Report.cm, 'Guidewall length [m]: {0:.1f}'.format(structure.guidewall_length), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-4*0.6*Report.cm, 'Concrete volume [m$^3$] C16/20: {0:.1f}; C20/25: {1:.2f}; C25/30: {2:.2f}'.format(structure.volume_concrete['C16/20'], structure.volume_concrete['C20/25'], structure.volume_concrete['C25/30']), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-5*0.6*Report.cm, 'Concrete volume [m$^3$] C30/37: {0:.1f}; C35/45: {1:.2f}; C40/50: {2:.2f}'.format(structure.volume_concrete['C30/37'], structure.volume_concrete['C35/45'], structure.volume_concrete['C40/50']), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-6*0.6*Report.cm, 'Weight of reinforcement steel [ton]: {0:.1f}'.format(structure.weight_reinf_steel), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-6*0.6*Report.cm, 'Betonite [kg/m$^3$]: {0:.1f}'.format(structure.betonite), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-7*0.6*Report.cm, 'Weight of soil disposal [ton]: {0:.1f}'.format(structure.weight_soil_disposal), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-7*0.6*Report.cm, 'Diesel consumption [liter/working day]: {0:.1f}'.format(structure.diesel), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-8*0.6*Report.cm, 'Electricity consumption [kWh/h]: {0:.1f}'.format(structure.electricity), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-8*0.6*Report.cm, 'Mob./ demob. distance [km]: {0:.1f}'.format(structure.distance_mob_demob), fontsize=8)
            # intermediate results
            self.add_intermediate_results_CO2(structure, y-9*0.6*Report.cm)
            
        elif isinstance(structure, MIPWall):
            self.axes.text(x1, y-0.6*Report.cm, 'Details for MIP as cut-off wall', fontsize=9, fontweight='bold')
            self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, 'Wall area [m$^2$]: {0:.1f}'.format(structure.wall_area), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-2*0.6*Report.cm, 'Wall thickness [m]: {0:.1f}'.format(structure.wall_thickness), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, 'Production rate [m$^2$/working day]: {0:.1f}'.format(structure.productivity), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-3*0.6*Report.cm, 'Cement consumption [kg/m]: {0:.1f}'.format(structure.cement), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-4*0.6*Report.cm, 'Betonite consumption [kg/m$^3$]: {0:.1f}'.format(structure.betonite), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-4*0.6*Report.cm, 'Diesel consumption [liter/working day]: {0:.1f}'.format(structure.diesel), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-5*0.6*Report.cm, 'Electricity consumption [kWh/h]: {0:.1f}'.format(structure.electricity), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-5*0.6*Report.cm, 'Mob./ demob. distance [km]: {0:.1f}'.format(structure.distance_mob_demob), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-6*0.6*Report.cm, 'Excess bore [%]: {0:.1f}'.format(structure.excess), fontsize=8)
            # intermediate results
            self.add_intermediate_results_CO2(structure, y-7*0.6*Report.cm)

        elif isinstance(structure, MIPWall_EPD):
            self.axes.text(x1, y-0.6*Report.cm, 'Details for MIP as cut-off wall according to EPD', fontsize=9, fontweight='bold')
            self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, 'Wall area [m$^2$]: {0:.1f}'.format(structure.wall_area), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-2*0.6*Report.cm, 'Wall thickness [m]: {0:.1f}'.format(structure.wall_thickness), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, 'BAUER MIP class [-]: {}'.format(structure.classification), fontsize=8)
            # intermediate results
            self.axes.text(x1, y-4*0.6*Report.cm, 'Results tCO2_eq ', fontsize=8, fontweight='bold')
            self.axes.text(x1, y-5*0.6*Report.cm, 'Total [tCO2_eq]: {0:.1f}'.format(structure.calc_co2eq()), fontsize=8)

        elif isinstance(structure, MIPSteelProfileWall):
            self.axes.text(x1, y-0.6*Report.cm, 'Details for MIP wall with steel profiles', fontsize=9, fontweight='bold')
            self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, 'Wall area [m$^2$]: {0:.1f}'.format(structure.wall_area), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-2*0.6*Report.cm, 'Wall thickness [m]: {0:.1f}'.format(structure.wall_thickness), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, 'Production rate [m$^2$/working day]: {0:.1f}'.format(structure.productivity), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-3*0.6*Report.cm, 'Cement consumption [kg/m]: {0:.1f}'.format(structure.cement), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-4*0.6*Report.cm, 'Betonite consumption [kg/m$^3$]: {0:.1f}'.format(structure.betonite), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-4*0.6*Report.cm, 'Weight of steel beams [ton]: {0:.1f}'.format(structure.weight_steelprofile), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-5*0.6*Report.cm, 'Diesel consumption [liter/working day]: {0:.1f}'.format(structure.diesel), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-5*0.6*Report.cm, 'Electricity consumption [kWh/h]: {0:.1f}'.format(structure.electricity), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-6*0.6*Report.cm, 'Mob./ demob. distance [km]: {0:.1f}'.format(structure.distance_mob_demob), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-6*0.6*Report.cm, 'Excess bore [%]: {0:.1f}'.format(structure.excess), fontsize=8)
            # intermediate results
            self.add_intermediate_results_CO2(structure, y-7*0.6*Report.cm)

        elif isinstance(structure, MIPSteelProfileWall_EPD):
            self.axes.text(x1, y-0.6*Report.cm, 'Details for MIP wall with steel profiles according to EPD', fontsize=9, fontweight='bold')
            self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, 'Wall area [m$^2$]: {0:.1f}'.format(structure.wall_area), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-2*0.6*Report.cm, 'Wall thickness [m]: {0:.1f}'.format(structure.wall_thickness), fontsize=8)
            self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, 'BAUER MIP class [-]: {}'.format(structure.classification), fontsize=8)
            self.axes.text(x2+0.5*Report.cm, y-3*0.6*Report.cm, 'Weight of steel beams [ton]: {0:.1f}'.format(structure.weight_steelprofile), fontsize=8)
            # intermediate results
            self.axes.text(x1, y-4*0.6*Report.cm, 'Results tCO2_eq ', fontsize=8, fontweight='bold')
            self.axes.text(x1, y-5*0.6*Report.cm, 'Total [tCO2_eq]: {0:.1f}'.format(structure.calc_co2eq()), fontsize=8)


    def add_intermediate_results_CO2(self, structure, y_start):
        """ Adds tCO2 results for structure
        """
        x1, x2 = 3*Report.cm, 11*Report.cm
        y = y_start - 0.6*Report.cm
        self.axes.text(x1, y, 'Results tCO2_eq ', fontsize=8, fontweight='bold')
        self.axes.text(x1+0.5*Report.cm, y-0.6*Report.cm, 'Material production [tCO2_eq]: {0:.1f}'.format(structure.out_material_production), fontsize=8)
        self.axes.text(x2+0.5*Report.cm, y-0.6*Report.cm, 'Material transport [tCO2_eq]: {0:.1f}'.format(structure.out_material_transport), fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, 'Disposal transport [tCO2_eq]: {0:.1f}'.format(structure.out_disposal_transport), fontsize=8)
        self.axes.text(x2+0.5*Report.cm, y-2*0.6*Report.cm, 'Equipment [tCO2_eq]: {0:.1f}'.format(structure.out_equipment), fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, 'Energy/ electricity/ hour [tCO2_eq]: {0:.1f}'.format(structure.out_energy_electricity_hour), fontsize=8)
        self.axes.text(x2+0.5*Report.cm, y-3*0.6*Report.cm, 'Mobilization/ demobilization [tCO2_eq]: {0:.1f}'.format(structure.out_mob_demob), fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-4*0.6*Report.cm, 'Persons transport [tCO2_eq]: {0:.1f}'.format(structure.out_persons_transport), fontsize=8)
        
        # plot a pie
        df = pd.DataFrame({
                        'Category': ['Material production', 'Material transport', 'Disposal transport', 'Equipment', 'Energy/ electricity/ hour', 'Mobilization/ demobilization', 'Persons transport'],
                        'tCO2_eq': [structure.out_material_production, structure.out_material_transport, structure.out_disposal_transport, structure.out_equipment, structure.out_energy_electricity_hour, structure.out_mob_demob, structure.out_persons_transport]
                        },
                        index = ['Material production', 'Material transport', 'Disposal transport', 'Equipment', 'Energy/ electricity/ hour', 'Mobilization/ demobilization', 'Persons transport'])

        ax = self.axes.figure.add_axes([0.18, 0.2, 0.3, 0.3])
        #df.plot.pie(y='tCO2_eq', stacked=False, colormap='cool', ax=ax, legend=False, autopct="%.1f%%")
        wedges, _ = ax.pie(list(df['tCO2_eq']))
        categories = list(df['Category'])
        categories_with_percentage = [item + ': {:.1f}%'.format(100*tCO2eq/df['tCO2_eq'].sum()) for item, tCO2eq in zip(categories, list(df['tCO2_eq']))]
        ax.legend(wedges, categories_with_percentage,
              title="Category",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

        #ax.set_aspect('equal')
        #ax.set_axis_off()
        ax.plot()
        self.draw()
    

    def add_project_info_MIP_E_Modul(self, form_title, project_title=''):
        """ Adds project information for pile wall
        """
        self.axes.text(3*Report.cm, 27*Report.cm, form_title, fontsize=9, fontweight='bold', va='center')
        if project_title:
            self.axes.text(3*Report.cm, 26.4*Report.cm, '{} '.format(project_title), fontsize=9, fontweight='bold', va='center')
            self.axes.text(3*Report.cm, 25.8*Report.cm, 'Datum: {} '.format(date.today().strftime("%b-%d-%Y")), fontsize=9, fontweight='bold', va='center')


    def add_basis_info_MIP_E_Modul(self):
        """ Adds basis information
        """
        x1 = 3*Report.cm
        y = 24*Report.cm
        self.axes.text(x1, y, 'Basis, Normen und Probekörper', fontsize=8, fontweight='bold')
        self.axes.text(x1+0.5*Report.cm, y-0.6*Report.cm, '- Interne BAUER-Datenbank/ Versuchsergebnisse', fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, '- DIN 4093:2015; vereinfachter Nachweis', fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, '- DIN EN 12390-13', fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-4*0.6*Report.cm, '- Probekörperabmessungen: h/d = 2/1', fontsize=8)

        y = 20*Report.cm
        self.axes.text(x1, y, 'Anwendungsbereich', fontsize=8, fontweight='bold')
        self.axes.text(x1+0.5*Report.cm, y-0.6*Report.cm, '- Druckfestigkeiten fm,k: 2,0 MPa bis 9,0 MPa', fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, "- Ton- und Schluffanteile: 10% bis 60% (Anteil im Boden < 0,063 mm)", fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, "- Bei Ton- und Schluffanteilen > 60% ist mit höherer Ungenauigkeit zu rechnen", fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-4*0.6*Report.cm, "- Bei Ton- und Schluffanteilen < 10% wird 10% angesetzt", fontsize=8)


    def add_input_and_result_MIP_E_Modul(self, fmk, fines_content, fm_mittel, E_modul):
        """ Adds input and the calculation result
        """
        x1 = 3*Report.cm
        y = 16*Report.cm
        self.axes.text(x1, y, 'Eingaben', fontsize=8, fontweight='bold')
        self.axes.text(x1+0.5*Report.cm, y-0.6*Report.cm, 'MIP fm,k = {0:.1f} [N/mm$^2$]'.format(fmk), fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-2*0.6*Report.cm, 'MIP fm,mittel ist {0:.1f} [N/mm$^2$]'.format(fm_mittel), fontsize=8)
        self.axes.text(x1+0.5*Report.cm, y-3*0.6*Report.cm, 'Ton- und Schluffanteil {0:.1f} [%]'.format(fines_content), fontsize=8)

        y = 12*Report.cm
        self.axes.text(x1, y, 'E-Modul', fontsize=8, fontweight='bold')
        self.axes.text(x1+0.5*Report.cm, y-0.6*Report.cm, 'E-Modul ist {0:.0f} [N/mm$^2$]'.format(E_modul), fontsize=8)


    def add_additional_message_MIP_E_Modul(self, message):
        """ Adds additional messge
        """
        self.axes.text(3.5*Report.cm, 10.8*Report.cm, '{}'.format(message), fontsize=8)
        