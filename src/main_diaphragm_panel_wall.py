import numpy as np
from src.piles_and_panels.shaft_diaphragm_panels import (get_parameters_shaft_diaphragm_panels, plot_wall_diaphragm_panels)
from src.common import get_area_moment_of_inertia_rect
from src.file_utilitites import load_parameters_from_json_file, st_json_download_button

# Initial parameters
parameters_init = {"project_name_dw": "Sample project", "project_revision_dw": "First issue, rev0", "wall_name_dw": "Wall 1", "D_dw": 1.2,

            "B_dw": 2.8, "L_dw": 35.0, "v_dw": 0.5, "H_drilling_platform_dw": 0.0, "E_dw": 30.0e6}

def main_diaphragm_panel_wall(st, parameters=None):
    """Main form for diagragm panel wall

    Args:
        st (streamlit): A streamlit object
    """
    st.title('Geometric check for diaphragm panel wall')

    st.header('Load saved session state (optional)')
    uploaded_file_session_state = st.file_uploader('Select session state file to load', type='json', key='fileuploader_dw')
    parameters_user_dw = None
    if uploaded_file_session_state is not None:
        try:
            parameters_user_dw = load_parameters_from_json_file(uploaded_file_session_state)
            st.success('File successfully loaded')
            if parameters_user_dw['selected_form'] != 'Diaphragm panel wall':
                st.write("Wrong JSON data file. Please load data for the selected form 'Diaphragm panel wall'!!")
                st.stop()
        except Exception as e:
            st.error(e)
            st.write("Wrong JSON data file. Please load data for the selected form 'Micropile buckling'!!")
            st.stop()

    if parameters_user_dw is None:
        parameters = parameters_init
    else:
        parameters = parameters_user_dw

    st.header('Project information')
    col1, col2 = st.columns(2)
    project_name = col1.text_input('Project', value=parameters['project_name_dw'], key='project_name_dw')
    col2.text_input('Revision', value=parameters['project_revision_dw'], key='project_revision_dw')


    st.header('Input parameters')
    col1, col2, col3 = st.columns(3)
    wall_name = col1.text_input('Wall identification', value=parameters['wall_name_dw'], key='wall_name_dw')
    #di = col1.number_input('Shaft inner diameter [m]', value=parameters['di_dws'], format='%.2f', min_value=1.0, max_value=100.0, step=1.0, key='di_dws')
    D = col2.number_input('Pannel thickness [m]', value=parameters['D_dw'], format='%.2f', min_value=0.3, max_value=5.0, step=0.1, key='D_dw')
    B = col3.number_input('Pannel length (for plotting) [m]', value=parameters['B_dw'], format='%.2f', min_value=0.3, max_value=15.0, step=0.1, key='B_dw')
    #n_pieces = int(col3.number_input('Numer of pannels [-]', value=int(parameters['n_pieces_dws']), format='%i', min_value=4, max_value=1000, step=1, key='n_pieces_dws'))
    L = col1.number_input('Length of wall [m]', value=parameters['L_dw'], step=1.0,min_value=1.0, max_value=150.0, key='L_dw')
    v = col2.number_input('Drilling verticality [%]', value=parameters['v_dw'], step=0.1, min_value=0.05, max_value=2.0, key='v_dw')
    col1, col2, _ = st.columns(3)
    H_drilling_platform = col1.number_input('Height of drilling platform above top of panels [m]', value=parameters['H_drilling_platform_dw'], step=1.0, min_value=0.0, max_value=20.0, key='H_drilling_platform_dw')
    col2.write('The initial deviation by free drilling x0 = {:.2f} cm'.format(H_drilling_platform*v))
    col3.write('Rotational inaccuracy is currently not considered.')

    x0, x, d_eff = get_parameters_shaft_diaphragm_panels(D, L, H_drilling_platform, v)

    st.header('Output parameters for {}'.format(wall_name))
    col1, col2, _ = st.columns(3)
    col1.write('Deviation at bottom of shaft dx = {:.2f} cm'.format(x*100))
    col1.write('Effective pannel thickness at bottom of shaft d_eff = {:.2f} cm'.format(d_eff*100))
    if d_eff <= 0:
        col2.warning('PANELS DO NOT TOUCH IN BASE OF WALL!!')

    else:
        with st.expander('Axial and flexural rigidity considering effective thickness at top and bottom of shaft'):
            E = st.number_input("Concrete Young's modulus E [KPa]", value=parameters['E_dw'], format='%.0f', min_value=25.0e6, max_value=35.0e6, step=1.0E6, key='E_dw')
            display_wall_stiffnesses(D, d_eff, E, st)

    st.header('Visualization for {}'.format(wall_name))
    st.write('Panels view at base of the shaft are plotted for random movement in out-of-plane direction for each of the panels, given a deviation dx = {:.2f} cm.'.format(x*100))
    fig1 = plot_wall_diaphragm_panels(2, D, B, x0, x, wall_name)
    st.pyplot(fig1)

    # Download session state JSON file
    session_state = dict(st.session_state)  # LazySessionState to dict
    session_state.pop('fileuploader_dw')   # do not save state for file uploader
    download_filename = 'piles_and_pannels' + '_Dwall' + '.JSON'
    href = st_json_download_button(session_state, download_filename)
    st.markdown(href, unsafe_allow_html=True)


def display_wall_stiffnesses(d_top, d_eff, E, st):
    """ Displays wall stiffness
    """
    I = get_area_moment_of_inertia_rect(1.0, d_top)
    EI = E*I        # [kNm**2/m]
    EA = E*d_top    # [kN/m]
    st.write('EI at top = {0:.2f} [kNm$^2$/m], EA at top = {1:.2f} [kN/m]'.format(EI, EA))
    I = get_area_moment_of_inertia_rect(1.0, d_eff)
    EI = E*I        # [kNm**2/m]
    EA = E*d_eff    # [kN/m]
    st.write('EI at bottom = {0:.2f} [kNm$^2$/m], EA at bottom = {1:.2f} [kN/m]'.format(EI, EA))
