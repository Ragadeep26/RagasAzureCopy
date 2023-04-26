import pickle
from PIL import Image
from src.co2_calculator.projects.project import Project
#from src.co2_calculator.projects.graphs import (create_tCO2eq_piechart, create_tCO2eq_piechart_matplotlib, create_tCO2eq_barchart_all_projects_categories, 
#                                                create_tCO2eq_barchart_all_projects_categories_2, 
#                                                create_tCO2eq_barchart_all_projects_matplotlib, create_tCO2eq_barchart_all_categories_matplotlib)
from src.co2_calculator.projects.graphs import (create_tCO2eq_piechart_matplotlib, create_tCO2eq_barchart_all_categories_matplotlib)
from src.co2_calculator.structures.wall_pile import PileWall
from src.co2_calculator.structures.wall_diaphragm import DiaphragmWall
from src.co2_calculator.structures.wall_MIP import MIPWall
from src.co2_calculator.structures.wall_MIP_steelprofile import MIPSteelProfileWall
from src.co2_calculator.structures.anchor import Anchor
from matplotlib.backends.backend_pdf import PdfPages
from src.report.report_matplotlib import Report

password = 'bara-3854'
password_user = ''
parameters_init = {'projects': [], 'project_id': ''}

def main_CO2_calculator(st, parameters=None):
    """ This is a CO2 calculator
    """
    if parameters is None:
        parameters = parameters_init
        #print('\n\n\n Restart...........')
        #print(parameters['projects'])

    password_user = ''

    logo_bauer = Image.open('./common/BAUER_ohneSchriftzug_Logo_png.png')
    col1, col2 = st.columns((0.8, 9.2))
    col1.image(logo_bauer)
    col2.title('CO2 Evaluator')
    col2.markdown('### Approximate calculation of CO2_eq footprint according to EFFC/ DFI Carbon Calculator')
    col2.markdown('### Life cycle modules: A1 to A5')

    # password field
    placeholder = st.empty()
    with placeholder.container():
        #st.write('This program is password protected. Please enter your password to continue!')
        st.write('This program is password protected. Please enter your password to continue!')
        st.write('Please contact our BT-Secretary for getting the password! :arrow_right: petra.ziegltrum@bauer.de')
        password_user = st.text_input('Password', value="", key="password_CO2", type="password", on_change=check_password(st))

    if password_user == password:
        placeholder.empty() # empty prompt for entering password if successfully entered
        continue_program(st, parameters)

def check_password(st):
    """ Checks if the entered password is correct"""
    session_state = dict(st.session_state)
    if 'password_CO2' in session_state:
        if session_state['password_CO2'] != password:
            #st.write('Your entered password is not correct!')
            st.write('Your entered password is not correct!')


def continue_program(st, parameters):
    """ Runs the main program"""

    col1, col2 = st.columns((0.5, 0.5))
    col1.subheader('Load projects data (optional)')
    uploaded_file = col1.file_uploader('Select session state file to load (.pickle)', type='pickle', key='fileuploader_CO22_calculator')  # pickle file must have the suffix .pickle
    with col1.form('my form', clear_on_submit=True):
        submitted = st.form_submit_button('Transfer loaded data file!')
        if submitted and uploaded_file is not None:
            loaded_data = pickle.loads(uploaded_file.read())
            parameters['projects'] = loaded_data['projects']            # assign projects data at loading
            parameters['project_id'] = loaded_data['project_id']      # assign projects data at loading

    col2.subheader('Clear data')
    button_clear_projects =  col2.button('Clear all data', key='clear_all_data')
    project_names_current = [project.project_variant for project in parameters['projects']]
    if button_clear_projects:
        remove_projects(project_names_current, parameters)
        parameters['project_id'] = ''

    st.header('Project options')

    # projects
    parameters['project_id'] = st.text_input('Project identification', value=parameters['project_id'])

    st.write('Two or more construction variants can be entered for comparison of emission information')
    col1, col2 = st.columns(2)
    # construction variants
    project_name = col1.text_input('Construction variant', key='construction_variant')
    button_add_project =  col2.button('Add construction variant', key='add_project')
    project_names_current = [project.project_variant for project in parameters['projects']]
    if button_add_project:
        if project_name:
            if is_unique_names(project_names_current+[project_name]):
                project = Project(project_name, structures=[])  # structures=[] must be explicitly given, else the same structure object is assigned to all created project instances
                parameters['projects'].append(project)
            else:   # project names must be unique
                st.warning('Construction variant names must be unique!')
        else:
            st.warning('Construction variant cannot be empty!')

    # project(s) removal
    col1, col2 = st.columns(2)
    project_names_current = [project.project_variant for project in parameters['projects']]
    projects_to_remove = col1.multiselect('Select construction variant(s) to remove', project_names_current)
    button_remove_project =  col2.button('Remove construction variant', key='remove_project')
    if button_remove_project:
        remove_projects(projects_to_remove, parameters)

    # structure(s) adding to a selected project
    col1, col2, col3 = st.columns(3)
    project_names_current = [project.project_variant for project in parameters['projects']]
    foundation_structures = ('Anchor', 'MIP wall', 'MIP wall with steel profiles', 'Pile/ Pile wall', 'Diaphragm wall')
    project_names_to_be_assigned = col1.multiselect('Select a construction variant to assign structure(s) to', project_names_current)
    structures_to_assign = col2.multiselect('Select structure(s) to assign', foundation_structures)
    button_add_structures_to_projects =  col3.button('Add structures {0} to construction variant {1}'.format(structures_to_assign, project_names_to_be_assigned), key='add_structure')
    if button_add_structures_to_projects:
        # first, remove all structures from the selected variant
        remove_structures_from_projects(project_names_to_be_assigned, parameters['projects'])
        # then, assign all selected structures to the selected variant
        add_structures_to_projects(structures_to_assign, project_names_to_be_assigned, parameters['projects'])

    # foundation structures for each project
    if parameters['projects']:
        project_names = [project.project_variant for project in parameters['projects']] + ['Summary']
        tabs = st.tabs(project_names)
        # foundation structures for each of the projects
        for i, tab in enumerate(tabs[:-1]):
            with tab:
                #tab.write('all projects: {}'.format(parameters['projects']))
                #tab.write('this project: {}'.format(parameters['projects'][i]))
                #tab.write("this project's structures: {}".format(parameters['projects'][i].structures))

                for structure in parameters['projects'][i].structures:

                    if isinstance(structure, Anchor):
                        tab.header('Details for anchors')
                        cols = tab.columns(3)
                        structure.anchor_lfm = cols[0].number_input('Anchor length [m]', value=structure.anchor_lfm, step=100.0, key='length_lfm_anchor'+str(i))
                        structure.weight_anchorhead = cols[1].number_input('Steel weight of anchor head [ton]', value=structure.weight_anchorhead, step=1.0, help='According to input field in EFFC Carbon Calculator', key='weight_anchorhead_anchor'+str(i))
                        structure.weight_anchorstrands = cols[2].number_input('Steel weight of anchor strands [ton]', value=structure.weight_anchorstrands, step=1.0, help='According to input field in EFFC Carbon Calculator', key='weight_anchorstrands_anchor'+str(i))
                        structure.productivity = cols[0].number_input('Production rate (productivity) [m/working day]', value=structure.productivity, step=10.0, help='Basic value (without obstruction): 100 m/working day', key='productivity_anchor'+str(i))
                        structure.cement = cols[1].number_input('Cement consumption [kg/m]', value=structure.cement, step=1.0, help='Basic value ~ 25 kg/m CEM I 42,5 R', key='cement_anchor'+str(i))
                        structure.diesel = cols[2].number_input('Diesel consumption [liter/working day]', value=structure.diesel, step=10.0, help='According to input field in EFFC Carbon Calculator', key='diesel_anchor'+str(i))
                        structure.electricity = cols[0].number_input('Electricity consumption [kWh/h]', value=structure.electricity, step=1.0, help='Basic value 16 kWh/h', key='electricity_anchor'+str(i))
                        structure.distance_mob_demob = cols[1].number_input('Mob./ demob. distance [km]', value=structure.distance_mob_demob, step=10.0, help='One-way distance of transport for heavy machines', key='distance_mob_demob_anchor'+str(i))
                        #updated_attributes = {'anchor_lfm': anchor_lfm, 'weight_anchorhead': weight_anchorhead, 'weight_anchorstrands':weight_anchorstrands, 'productivity': productivity, 'cement': cement, 
                        #                    'diesel': diesel, 'electricity':electricity, 'distance_mob_demob': distance_mob_demob}
                        # calc tCO2_eq
                        #sum_tco2_eq = structure.calc_co2eq(**updated_attributes)    # explicit updates of structure's attributes: tried solving delayed assignment when clicking on +/- of number input -> not successful
                        sum_tco2_eq = structure.calc_co2eq()
                        tab.markdown("### Total $tCO2eq$ for anchors: {0:.1f}".format(sum_tco2_eq))
                        col1, col2, col3 = tab.columns([4, 4, 2])
                        col1.write('Material production [tCO2_eq]: {0:.1f}'.format(structure.out_material_production))
                        col1.write('Material transport [tCO2_eq]: {0:.1f}'.format(structure.out_material_transport))
                        col1.write('Disposal transport [tCO2_eq]: {0:.1f}'.format(structure.out_disposal_transport))
                        col1.write('Equipment [tCO2_eq]: {0:.1f}'.format(structure.out_equipment))
                        col1.write('Energy/ electricity/ hour [tCO2_eq]: {0:.1f}'.format(structure.out_energy_electricity_hour))
                        col1.write('Mobilization/ demobilization [tCO2_eq]: {0:.1f}'.format(structure.out_mob_demob))
                        col1.write('Persons transport [tCO2_eq]: {0:.1f}'.format(structure.out_persons_transport))
                        #tab.write(df)
                        axis = create_tCO2eq_piechart_matplotlib(structure)
                        col2.pyplot(axis.figure, use_container_width=False)


                    if isinstance(structure, PileWall):
                        tab.header('Details for piles/ pile wall')
                        cols = tab.columns(3)
                        structure.borelength_lfm = cols[0].number_input('Pile bore length [lm]', value=structure.borelength_lfm, step=100.0, key='borelength_lfm_pile'+str(i))
                        structure.productivity = cols[1].number_input('Production rate (productivity) [m/working day]', value=structure.productivity, step=10.0, help='Basic value (without obstruction) for DKS system: 200 m/working day', key='productivity_pile'+str(i))
                        structure.length_drilling_template = cols[2].number_input('Length of the drilling template [m]', value=structure.length_drilling_template, step=100.0, help='Basic value: concrete grade C20/25 for the drilling template', key='length_drilling_template'+str(i))
                        cols_concrete = tab.columns(6)
                        help_volume_concrete = """According to input field in EFFC Carbon Calculator
                                                Basic value for concrete raw material supply in concrete production: 7% from tCO2 concrete production.
                                                Concrete supplier distance: 20 km (not variable)."""
                        structure.volume_concrete['C16/20'] = cols_concrete[0].number_input('Concrete volume C16/20 [m^3]', value=structure.volume_concrete['C16/20'], step=100.0, help=help_volume_concrete, key='volume_concrete_C16/20_pile'+str(i))
                        structure.volume_concrete['C20/25'] = cols_concrete[1].number_input('Concrete volume C20/25 [m^3]', value=structure.volume_concrete['C20/25'], step=100.0, help=help_volume_concrete, key='volume_concrete_C20/25_pile'+str(i))
                        structure.volume_concrete['C25/30'] = cols_concrete[2].number_input('Concrete volume C25/30 [m^3]', value=structure.volume_concrete['C25/30'], step=100.0, help=help_volume_concrete, key='volume_concrete_C25/30_pile'+str(i))
                        structure.volume_concrete['C30/37'] = cols_concrete[3].number_input('Concrete volume C30/37 [m^3]', value=structure.volume_concrete['C30/37'], step=100.0, help=help_volume_concrete, key='volume_concrete_C30/37_pile'+str(i))
                        structure.volume_concrete['C35/45'] = cols_concrete[4].number_input('Concrete volume C35/45 [m^3]', value=structure.volume_concrete['C35/45'], step=100.0, help=help_volume_concrete, key='volume_concrete_C35/45_pile'+str(i))
                        structure.volume_concrete['C40/50'] = cols_concrete[5].number_input('Concrete volume C40/50 [m^3]', value=structure.volume_concrete['C40/50'], step=100.0, help=help_volume_concrete, key='volume_concrete_C40/50_pile'+str(i))
                        cols = tab.columns(3)
                        structure.weight_steel_reinf = cols[0].number_input('Weight of reinforcement steel [ton]', value=structure.weight_reinf_steel, step=10.0, help='According to input field in EFFC Carbon Calculator. Steel supplier distance: 300 km (not variable)', key='weight_reinf_steel_pile'+str(i))
                        structure.weight_soil_disposal = cols[1].number_input('Weight of soil disposal [ton]', value=structure.weight_soil_disposal, step=10.0, help='According to input field in EFFC Carbon Calculator. Distance to waste disposal: 20 km (not variable)', key='weight_soil_disposal_pile'+str(i))
                        structure.diesel = cols[2].number_input('Diesel consumption [liter/working day]', value=structure.diesel, step=10.0, help='Basic value 650 liter/working day. Distance to diesel supplier: 10 km (not variable)', key='diesel_pile'+str(i))
                        structure.electricity = cols[0].number_input('Electricity consumption [kWh/h]', value=structure.electricity, step=1.0, help='Basic value 50 kWh/h', key='electricity_pile'+str(i))
                        structure.distance_mob_demob = cols[1].number_input('Mob./ demob. distance [km]', value=structure.distance_mob_demob, step=10.0, help='One-way distance of transport for heavy machines', key='distance_mob_demob_pile'+str(i))
                        # calc tCO2_eq
                        sum_tco2_eq = structure.calc_co2eq()
                        #container = tab.container()
                        #col1, col2 = container.columns([3, 7])
                        tab.markdown('### Results $tCO2eq$ for piles/ pile wall: {0:.1f}'.format(sum_tco2_eq))
                        col1, col2, col3 = tab.columns([4, 4, 2])
                        col1.write('Material production [tCO2_eq]: {0:.1f}'.format(structure.out_material_production))
                        col1.write('Material transport [tCO2_eq]: {0:.1f}'.format(structure.out_material_transport))
                        col1.write('Disposal transport [tCO2_eq]: {0:.1f}'.format(structure.out_disposal_transport))
                        col1.write('Equipment [tCO2_eq]: {0:.1f}'.format(structure.out_equipment))
                        col1.write('Energy/ electricity/ hour [tCO2_eq]: {0:.1f}'.format(structure.out_energy_electricity_hour))
                        col1.write('Mobilization/ demobilization [tCO2_eq]: {0:.1f}'.format(structure.out_mob_demob))
                        col1.write('Persons transport [tCO2_eq]: {0:.1f}'.format(structure.out_persons_transport))
                        axis = create_tCO2eq_piechart_matplotlib(structure)
                        col2.pyplot(axis.figure, use_container_width=False)

                    elif isinstance(structure, DiaphragmWall):
                        tab.header('Details for diaphragm wall')
                        cols = tab.columns(4)
                        structure.wall_area = cols[0].number_input('Wall area [m^2]', value=structure.wall_area, step=100.0, key='wall_area_dwall'+str(i))
                        structure.wall_thickness = cols[1].number_input('Wall thickness [m]', value=structure.wall_thickness, step=0.1, key='wall_thickness_dwall'+str(i))
                        structure.productivity = cols[2].number_input('Production rate (productivity) [m^2/working day]', value=structure.productivity, step=10.0, help='Basic value (without obstruction): 200 m^2/working day', key='productivity_dwall'+str(i))
                        structure.guidewall_length = cols[3].number_input('Guidewall length [m]', value=structure.guidewall_length, step=10.0, help='Basic value: conrete grade C20/25 for the guide wall', key='guidewall_length_dwall'+str(i))
                        cols_concrete = tab.columns(6)
                        help_volume_concrete = """According to input field in EFFC Carbon Calculator
                                                Basic value for concrete raw material supply in concrete production: 7% from tCO2 concrete production.
                                                Concrete supplier distance: 20 km (not variable)."""
                        structure.volume_concrete['C16/20'] = cols_concrete[0].number_input('Concrete volume C16/20 [m^3]', value=structure.volume_concrete['C16/20'], step=100.0, help=help_volume_concrete, key='volume_concrete_C16/20_dwall'+str(i))
                        structure.volume_concrete['C20/25'] = cols_concrete[1].number_input('Concrete volume C20/25 [m^3]', value=structure.volume_concrete['C20/25'], step=100.0, help=help_volume_concrete, key='volume_concrete_C20/25_dwall'+str(i))
                        structure.volume_concrete['C25/30'] = cols_concrete[2].number_input('Concrete volume C25/30 [m^3]', value=structure.volume_concrete['C25/30'], step=100.0, help=help_volume_concrete, key='volume_concrete_C25/30_dwall'+str(i))
                        structure.volume_concrete['C30/37'] = cols_concrete[3].number_input('Concrete volume C30/37 [m^3]', value=structure.volume_concrete['C30/37'], step=100.0, help=help_volume_concrete, key='volume_concrete_C30/37_dwall'+str(i))
                        structure.volume_concrete['C35/45'] = cols_concrete[4].number_input('Concrete volume C35/45 [m^3]', value=structure.volume_concrete['C35/45'], step=100.0, help=help_volume_concrete, key='volume_concrete_C35/45_dwall'+str(i))
                        structure.volume_concrete['C40/50'] = cols_concrete[5].number_input('Concrete volume C40/50 [m^3]', value=structure.volume_concrete['C40/50'], step=100.0, help=help_volume_concrete, key='volume_concrete_C40/50_dwall'+str(i))
                        cols = tab.columns(3)
                        structure.weight_reinf_steel = cols[0].number_input('Weight of reinforcement steel [ton]', value=structure.weight_reinf_steel, step=10.0, help='According to input field in EFFC Carbon Calculator. Steel supplier distance: 300 km (not variable)', key='weight_reinf_steel_dwall'+str(i))
                        structure.betonite = cols[1].number_input('Betonite [kg/m^3]', value=structure.betonite, step=10.0, help='Basic setting: additional comsumption 35% (not variable). Distance to betonite supplier: 20 km (not variable)', key='betonite_dwall'+str(i))
                        structure.weight_soil_disposal = cols[2].number_input('Weight of soil disposal [ton]', value=structure.weight_soil_disposal, step=10.0, help='According to input field in EFFC Carbon Calculator. Distance to waste disposal: 20 km (not variable)', key='weight_soil_disposal_dwall'+str(i))
                        structure.diesel = cols[0].number_input('Diesel consumption [liter/working day]', value=structure.diesel, step=10.0, help='Basic value 500 liter/working day. Distance to diesel supplier: 20 km (not variable)', key='diesel_dwall'+str(i))
                        structure.electricity = cols[1].number_input('Electricity consumption [kWh/h]', value=structure.electricity, step=1.0, help='Basic value 100 kWh/h', key='electricity_dwall'+str(i))
                        structure.distance_mob_demob = cols[2].number_input('Mob./ demob. distance [km]', value=structure.distance_mob_demob, step=10.0, help='One-way distance of transport for heavy machines', key='distance_mob_demob_dwall'+str(i))
                        # calc tCO2_eq
                        sum_tco2_eq = structure.calc_co2eq()
                        tab.markdown('### Results $tCO2eq$ for diaphragm wall: {0:.1f}'.format(sum_tco2_eq))
                        col1, col2, col3 = tab.columns([4, 4, 2])
                        col1.write('Material production [tCO2_eq]: {0:.1f}'.format(structure.out_material_production))
                        col1.write('Material transport [tCO2_eq]: {0:.1f}'.format(structure.out_material_transport))
                        col1.write('Disposal transport [tCO2_eq]: {0:.1f}'.format(structure.out_disposal_transport))
                        col1.write('Equipment [tCO2_eq]: {0:.1f}'.format(structure.out_equipment))
                        col1.write('Energy/ electricity/ hour [tCO2_eq]: {0:.1f}'.format(structure.out_energy_electricity_hour))
                        col1.write('Mobilization/ demobilization [tCO2_eq]: {0:.1f}'.format(structure.out_mob_demob))
                        col1.write('Persons transport [tCO2_eq]: {0:.1f}'.format(structure.out_persons_transport))
                        axis = create_tCO2eq_piechart_matplotlib(structure)
                        col2.pyplot(axis.figure, use_container_width=False)

                    elif isinstance(structure, MIPWall):
                        tab.header('Details for MIP as cut-off wall')
                        cols = tab.columns(3)
                        structure.wall_area = cols[0].number_input('Wall area [m^2]', value=structure.wall_area, step=100.0, help='Area of the constructed wall', key='wall_area_MIPwall'+str(i))
                        structure.wall_thickness = cols[1].number_input('Wall thickness [m]', value=structure.wall_thickness, step=0.1, key='wall_thickness_MIPwall'+str(i))
                        structure.productivity = cols[2].number_input('Production rate (productivity) [m^2/working day]', value=structure.productivity, step=10.0, help='Basic value (without obstruction): 250 m^2/working day', key='productivity_MIPwall'+str(i))
                        structure.cement = cols[0].number_input('Cement consumption [kg/m^3]', value=structure.cement, step=1.0, help='Basic setting: CEM III/B (not variable). Distance to concrete supplier: 20 km (not variable)', key='cement_MIPwall'+str(i))
                        structure.betonite = cols[1].number_input('Betonite consumption [kg/m^3]', value=structure.betonite, step=1.0, help='Distance of betonite dilivery: 20 Km (not variable)', key='betonite_MIPwall'+str(i))
                        #structure.support_fluid = cols[1].number_input('Betonite [kg/m^3]', value=structure.support_fluid, step=10.0, help='Distance to betonite supplier: 20 km (not variable)', key='support_fluid_MIPwall'+str(i))
                        structure.diesel = cols[2].number_input('Diesel consumption [liter/working day]', value=structure.diesel, step=10.0, help='Basic value 750 liter/working day and 850 liter/working day respectively for ... Distance to diesel supplier: 10 km (not variable)', key='diesel_MIPwall'+str(i))
                        structure.electricity = cols[0].number_input('Electricity consumption [kWh/h]', value=structure.electricity, step=1.0, help='Basic value 80 kWh/h', key='electricity_MIPwall'+str(i))
                        structure.distance_mob_demob = cols[1].number_input('Mob./ demob. distance [km]', value=structure.distance_mob_demob, step=10.0, help='One-way distance of transport for heavy machines', key='distance_mob_demob_MIPwall'+str(i))
                        structure.excess = cols[2].number_input('Excess bore [%]', value=structure.excess, step=5.0, help="Basic value: 25% for gravelly soil, 35% for sandy soil, 45% for cohesive soil. Distance to waste disposal: 20 km (not variable)", key='excess_MIPwall'+str(i))
                        # calc tCO2_eq
                        sum_tco2_eq = structure.calc_co2eq()
                        tab.markdown('### Results $tCO2eq$ for MIP wall as cut-off wall: {0:.1f}'.format(sum_tco2_eq))
                        col1, col2, col3 = tab.columns([4, 4, 2])
                        col1.write('Material production [tCO2_eq]: {0:.1f}'.format(structure.out_material_production))
                        col1.write('Material transport [tCO2_eq]: {0:.1f}'.format(structure.out_material_transport))
                        col1.write('Disposal transport [tCO2_eq]: {0:.1f}'.format(structure.out_disposal_transport))
                        col1.write('Equipment [tCO2_eq]: {0:.1f}'.format(structure.out_equipment))
                        col1.write('Energy/ electricity/ hour [tCO2_eq]: {0:.1f}'.format(structure.out_energy_electricity_hour))
                        col1.write('Mobilization/ demobilization [tCO2_eq]: {0:.1f}'.format(structure.out_mob_demob))
                        col1.write('Persons transport [tCO2_eq]: {0:.1f}'.format(structure.out_persons_transport))
                        axis = create_tCO2eq_piechart_matplotlib(structure)
                        col2.pyplot(axis.figure, use_container_width=False)

                    elif isinstance(structure, MIPSteelProfileWall):
                        tab.header('Details for MIP wall with steel profiles')
                        cols = tab.columns(3)
                        structure.wall_area = cols[0].number_input('Wall area [m^2]', value=structure.wall_area, step=100.0, help='Area of the constructed wall', key='wall_area_MIPSteelwall'+str(i))
                        structure.wall_thickness = cols[1].number_input('Wall thickness [m]', value=structure.wall_thickness, step=0.1, key='wall_thickness_MIPSteelwall'+str(i))
                        structure.productivity = cols[2].number_input('Production rate (productivity) [m^2/working day]', value=structure.productivity, step=10.0, help='Basic value (without obstruction): 170 m^2/working day', key='productivity_MIPSteelwall'+str(i))
                        structure.cement = cols[0].number_input('Cement consumption [kg/m^3]', value=structure.cement, step=1.0, help='Basic setting: CEM III/B (not variable). Distance to concrete supplier: 20 km (not variable)', key='cement_MIPSteelwall'+str(i))
                        structure.betonite = cols[1].number_input('Betonite consumption [kg/m^3]', value=structure.betonite, step=1.0, help='Distance of betonite dilivery: 20 Km (not variable)', key='betonite_MIPSteelwall'+str(i))
                        structure.weight_steelprofile = cols[2].number_input('Weight of steel beams [ton]', value=structure.weight_steelprofile, step=1.0, help='According to input field in EFFC Carbon Calculator. Distance to steel supplier: 300 km (not variable)', key='weight_steelprofile_MIPSteelwall'+str(i))
                        #structure.support_fluid = cols[0].number_input('Betonite [kg/m^3]', value=structure.support_fluid, step=10.0, help='Distance to betonite supplier: 20 km (not variable)', key='support_fluid_MISteelPwall'+str(i))
                        structure.diesel = cols[0].number_input('Diesel consumption [liter/working day]', value=structure.diesel, step=10.0, help='Basic value 750 liter/working day and 850 liter/working day respectively for ... Distance to diesel supplier: 10 km (not variable)', key='diesel_MIPSteelwall'+str(i))
                        structure.electricity = cols[1].number_input('Electricity consumption [kWh/h]', value=structure.electricity, step=1.0, help='Basic value 80 kWh/h', key='electricity_MIPSteelwall'+str(i))
                        structure.distance_mob_demob = cols[2].number_input('Mob./ demob. distance [km]', value=structure.distance_mob_demob, step=10.0, help='One-way distance of transport for heavy machines', key='distance_mob_demob_MIPSteelwall'+str(i))
                        structure.excess = cols[0].number_input('Excess bore [%]', value=structure.excess, step=5.0, help="Basic value: 25% for gravelly soil, 35% for sandy soil, 45% for cohesive soil. Distance to waste disposal: 20 km (not variable)", key='excess_MIPSteelwall'+str(i))
                        # calc tCO2_eq
                        sum_tco2_eq = structure.calc_co2eq()
                        tab.markdown('### Results $tCO2eq$ for MIP wall with steel profiles: {0:.1f}'.format(sum_tco2_eq))
                        col1, col2, col3 = tab.columns([4, 4, 2])
                        col1.write('Material production [tCO2_eq]: {0:.1f}'.format(structure.out_material_production))
                        col1.write('Material transport [tCO2_eq]: {0:.1f}'.format(structure.out_material_transport))
                        col1.write('Disposal transport [tCO2_eq]: {0:.1f}'.format(structure.out_disposal_transport))
                        col1.write('Equipment [tCO2_eq]: {0:.1f}'.format(structure.out_equipment))
                        col1.write('Energy/ electricity/ hour [tCO2_eq]: {0:.1f}'.format(structure.out_energy_electricity_hour))
                        col1.write('Mobilization/ demobilization [tCO2_eq]: {0:.1f}'.format(structure.out_mob_demob))
                        col1.write('Persons transport [tCO2_eq]: {0:.1f}'.format(structure.out_persons_transport))
                        axis = create_tCO2eq_piechart_matplotlib(structure)
                        col2.pyplot(axis.figure, use_container_width=False)

        with tabs[-1]: # All projects
            #st.header('$tCO2eq$ summary')
            #st.markdown('### $tCO2eq$ total')
            #c = create_tCO2eq_barchart_all_projects(parameters['projects'])
            #st.altair_chart(c, use_container_width=False)

            if len(parameters['projects']) > 1:
                st.header('Overview of all construction variants')
            else:
                st.header("Overview of the construction variant")

            cols = st.columns(len(parameters['projects']))
            for i, project in enumerate(parameters['projects']):
                cols[i].markdown('### ' + project.project_variant)
                for structure in project.structures:
                    structure_tco2_eq = structure.calc_co2eq()
                    if isinstance(structure, Anchor):
                        cols[i].write('Ground anchors $tCO2eq$: {0:.1f}'.format(structure_tco2_eq))
                    if isinstance(structure, PileWall):
                        cols[i].write('Piles/ pile wall $tCO2eq$: {0:.1f}'.format(structure_tco2_eq))
                    elif isinstance(structure, DiaphragmWall):
                        cols[i].write('Diaphragm wall $tCO2eq$: {0:.1f}'.format(structure_tco2_eq))
                    elif isinstance(structure, MIPWall):
                        cols[i].write('MIP as cut-off wall $tCO2eq$: {0:.1f}'.format(structure_tco2_eq))
                    elif isinstance(structure, MIPSteelProfileWall):
                        cols[i].write('MIP wall with steel profiles $tCO2eq$: {0:.1f}'.format(structure_tco2_eq))


            if len(parameters['projects']) > 1:
                st.header('$tCO2eq$ breakdown for all construction variants')
            else:
                st.header("$tCO2eq$ breakdown")
            #st.markdown('### $tCO2eq$ summary')
            categrogy = {'MP': 'Material production', 'MT':'Material transport', 'DT': 'Disposal transport', 'EQ': 'Equipment', 'EE': 'Energy/ electricity/ hour', 
                        'MD': 'Mobilization/ demobilization', 'PT': 'Persons transport'}
            cols = st.columns(4)
            for i, (key, value) in enumerate(categrogy.items()):
                cols[i%4].write('{0}: {1}'.format(key, value))
            #c = create_tCO2eq_barchart_all_projects_categories(parameters['projects'])
            #c = create_tCO2eq_barchart_all_projects_categories_2(parameters['projects'])
            #st.altair_chart(c, use_container_width=False)

            try:
                #col1, col2 = st.columns(2)
                #_, axis_projs, df_prjs = create_tCO2eq_barchart_all_projects_matplotlib(parameters['projects'])
                _, axis_cats, df_cats = create_tCO2eq_barchart_all_categories_matplotlib(parameters['projects'])
                #col1.pyplot(axis_projs.figure, use_container_width=False)
                st.pyplot(axis_cats.figure, use_container_width=False)

            except: # exception when a project has no structures assigned to it
                pass


            #st.bar_chart(df)
            


    # Download project data to pickle file
    if parameters['projects']:
        st.subheader('Save session state')
        #download_filename = 'CO2_Calculator_' + '_'.join(project_names_current) + '.pickle'    # pickle file
        download_filename = 'CO2_Calculator' + '_' + parameters['project_id'] + '.pickle'    # pickle file
        data_to_dump = pickle.dumps(parameters)
        st.download_button("Save calculations to file", data=data_to_dump, file_name=download_filename)
    
    # PDF report
    #checkbox = st.checkbox('Download report in PDF', value=False)
    should_print_report_botton =  st.button('Create report in PDF', key='create_pdf_report')
    if should_print_report_botton and parameters['projects']:
        pdf_fn = 'Report_CO2_Evaluator' + parameters['project_id'] + '.pdf'
        pp = PdfPages(pdf_fn)
        #report_page1 = Report()
        report_page2 = Report()
        #report_page1.add_project_info_CO2(form_title='CO2 Evaluator according to EFFC', project_title=parameters['project_id'])
        report_page2.add_project_info_CO2(form_title='CO2 Evaluator according to EFFC/ DFI Carbon Calculator\nLife cycles modules: A1 to A5', project_title=parameters['project_id'])
        #y = report_page1.add_overview_info_CO2(parameters['projects'])
        y = report_page2.add_overview_info_CO2(parameters['projects'])
        try:
            #report_page1.add_summary_graph_CO2_projects(y, parameters['projects'], df_prjs)
            report_page2.add_summary_graph_CO2_categories(y, parameters['projects'], df_cats)
        except: # exception when a project has no structures assigned to it
            pass
        # report pages for input and intermediate results
        pages = []
        for project in parameters['projects']:
            for structure in project.structures:
                page_project = Report()
                page_project.add_project_info_CO2(form_title='CO2 Evaluator according to EFFC/ DFI Carbon Calculator\nLife cycles modules: A1 to A5', project_title=parameters['project_id'])
                page_project.add_project_structures_input_and_results(project, structure)
                pages.append(page_project)

        # stack plots to a single pdf file
        #report_page1.fig.savefig(pp, format='pdf', bbox_inches='tight')
        report_page2.fig.savefig(pp, format='pdf', bbox_inches='tight')
        for page_project in pages:
            page_project.fig.savefig(pp, format='pdf', bbox_inches='tight')
        pp.close()

        with open(pdf_fn, 'rb') as h_pdf:
            st.download_button(
                label="PDF file",
                data=h_pdf,
                file_name=pdf_fn,
                mime="application/pdf",
            )


def add_structures_to_projects(structures_to_assign, project_names_to_be_assigned, projects):
    """ Adds selected structure(s) to selected project(s)
    """
    for project in projects:
        if project.project_variant in project_names_to_be_assigned:
            for structure in structures_to_assign:
                if structure == 'Anchor':
                    project.add_structure(Anchor())
                elif structure == 'MIP wall':
                    project.add_structure(MIPWall())
                elif structure == 'MIP wall with steel profiles':
                    project.add_structure(MIPSteelProfileWall())
                elif structure == 'Pile/ Pile wall':
                    project.add_structure(PileWall())
                elif structure == 'Diaphragm wall':
                    project.add_structure(DiaphragmWall())


def remove_structures_from_projects(project_names_to_be_assigned, projects):
    """ Removes all structures from the selected project(s)
    """
    for project in projects:
        if project.project_variant in project_names_to_be_assigned:
            while project.structures:   # remove structure until structures list is empty
                project.structures.pop()


def remove_projects(projects_to_remove, parameters):
    """ Removes one or more selected projects
    """
    for project_to_remove in projects_to_remove:
        for i, project in enumerate(parameters['projects']):
            if project.project_variant == project_to_remove:
                parameters['projects'].pop(i)

    #print(parameters['projects'])


def is_unique_names(names):
    """ Check if names are unique
    """
    if len(names) > len(set(names)):
        return False
    else:
        return True


#def assign_structure_attributes(structure, **kwargs):
#    """ Assign structure attributes
#    """
#    structure.__dict__.update(kwargs)