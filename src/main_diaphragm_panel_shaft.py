import numpy as np
import math
from src.piles_and_panels.shaft_diaphragm_panels import (get_parameters_shaft_diaphragm_panels, plot_shaft_diaphragm_panels)
from src.common import get_area_moment_of_inertia_rect, check_for_hoop_force
from src.file_utilitites import load_parameters_from_json_file, st_json_download_button

# Initial parameters
parameters_init = {"project_name_dws": "Sample project", "project_revision_dws": "First issue, rev0", "shaft_name_dws": "Shaft 1", "di_dws": 18.0, "D_dws": 0.8,
            "B_dws": 2.8, "L_dws": 30.0, "v_dws": 0.4, "H_drilling_platform_dws": 0.0, "E_dws": 30e6, "n_pieces_user": 22,
            "F_hoop_at_base_dws": 1200.0, "gamma_G_dws": 1.35, "f_ck_dws": 10.0, "alpha_cc_dws": 0.7, "gamma_c_dws": 1.5, 
            "check_hoop_stress_base_dws": False, "check_hoop_stress_more_dws": False, "F_hoop_dws": 1100.0, "L_hoop_dws": 10.0}

def main_diaphragm_panel_shaft(st, parameters=None):
    """Main form for diagragm panel shaft

    Args:
        st (streamlit): A streamlit object
    """
    st.title('Geometric and plain concrete resistance check for diaphragm panel shaft')

    st.header('Load saved session state (optional)')
    uploaded_file_session_state = st.file_uploader('Select session state file to load', type='json', key='fileuploader_dws')
    parameters_user_dws = None
    if uploaded_file_session_state is not None:
        try:
            parameters_user_dws = load_parameters_from_json_file(uploaded_file_session_state)
            st.success('File successfully loaded')
            if parameters_user_dws['selected_form'] != 'Diaphragm panel shaft':
                st.write("Wrong JSON data file. Please load data for the selected form 'Diaphragm panel shaft'!!")
                st.stop()
        except Exception as e:
            st.error(e)
            st.write("Wrong JSON data file. Please load data for the selected form 'Micropile buckling'!!")
            st.stop()

    if parameters_user_dws is None:
        parameters = parameters_init
    else:
        parameters = parameters_user_dws

    st.header('Project information')
    col1, col2 = st.columns(2)
    project_name = col1.text_input('Project', value=parameters['project_name_dws'], key='project_name_dws')
    col2.text_input('Revision', value=parameters['project_revision_dws'], key='project_revision_dws')


    st.header('Input parameters')
    col1, col2, col3 = st.columns(3)
    shaft_name = col1.text_input('Shaft identification', value=parameters['shaft_name_dws'], key='shaft_name_dws')
    di = col1.number_input('Shaft inner diameter [m]', value=parameters['di_dws'], format='%.2f', min_value=1.0, max_value=100.0, step=1.0, key='di_dws')
    D = col2.number_input('Pannel thickness [m]', value=parameters['D_dws'], format='%.2f', min_value=0.3, max_value=5.0, step=0.1, key='D_dws')
    B = col3.number_input('Pannel length (for plotting) [m]', value=parameters['B_dws'], format='%.2f', min_value=0.3, max_value=15.0, step=0.1, key='B_dws')
    #n_pieces = int(col3.number_input('Numer of pannels [-]', value=int(parameters['n_pieces_dws']), format='%i', min_value=4, max_value=1000, step=1, key='n_pieces_dws'))
    L = col2.number_input('Length of shaft [m]', value=parameters['L_dws'], step=1.0,min_value=1.0, max_value=150.0, key='L_dws')
    v = col3.number_input('Drilling verticality [%]', value=parameters['v_dws'], step=0.1, min_value=0.05, max_value=2.0, key='v_dws')
    col1, col2, col3 = st.columns(3)
    H_drilling_platform = col1.number_input('Height of drilling platform above top of panels [m]', value=parameters['H_drilling_platform_dws'], step=1.0, min_value=0.0, max_value=20.0, key='H_drilling_platform_dws')
    col2.write('The initial deviation by free drilling x0 = {:.2f} cm'.format(H_drilling_platform*v))
    col3.write('Rotational inaccuracy is currently not considered.')

    x0, x, d_eff = get_parameters_shaft_diaphragm_panels(D, L, H_drilling_platform, v)
    n_pieces = int(math.ceil(np.pi*(di + D/2)/B) + 1)     # number of pannels for plotting 
    n_pieces_user = n_pieces
    col1.write('Estimation of the needed number of panels {}'.format(n_pieces))
    #n_pieces_user = col2.number_input("Number of actual used panels", value=n_pieces, key='n_pieces_user')
    n_pieces_user = col2.number_input("Number of actual used panels", value=parameters['n_pieces_user'], key='n_pieces_user')

    st.header('Output parameters for {}'.format(shaft_name))
    col1, col2, _ = st.columns(3)
    col1.write('Deviation at bottom of shaft dx = {:.2f} cm'.format(x*100))
    col1.write('Effective pannel thickness at bottom of shaft d_eff = {:.2f} cm'.format(d_eff*100))
    if d_eff <= 0:
        col2.warning('PANELS DO NOT TOUCH IN BASE OF SHAFT!!')
    else:
        # Write concrete volume
        V_c_total = n_pieces_user * L * D * B
        col2.write('Total concrete volume to be casted: {:.2f} m$^3$'.format(V_c_total))

        with st.expander('Axial and flexural rigidity considering effective thickness at top and bottom of shaft'):
            E = st.number_input("Concrete Young's modulus E [KPa]", value=parameters['E_dws'], format='%.0f', min_value=25.0e6, max_value=35.0e6, step=1.0E6, key='E_dws')
            display_shaft_stiffnesses(D, d_eff, E, st)


    st.header('Visualization for {}'.format(shaft_name))
    st.write('Panels view at base of the shaft are plotted for random movement in radial direction (inward, outward) for each of the panels, given a deviation dx = {:.2f} cm.'.format(x*100))
    fig1 = plot_shaft_diaphragm_panels(di, D, B, x0, x, n_pieces_user, shaft_name)
    st.pyplot(fig1)


    check_hoop_stress_base = st.checkbox('Check for hoop stress at base of the shaft', value=parameters['check_hoop_stress_base_dws'], key='check_hoop_stress_base_dws')
    if check_hoop_stress_base:
        st.header('Check for hoop stress at base of shaft')
        col1, col2, col3 = st.columns(3)
        F_hoop_at_base = col1.number_input('Hoop force [kN/m]', value=parameters['F_hoop_at_base_dws'], min_value=10.0, max_value=100000.0, step=100.0, key='F_hoop_at_base_dws')
        gamma_G = col2.number_input('gamma_G [-]', value=parameters['gamma_G_dws'], min_value=1.0, max_value=2.0, step=0.05, key='gamma_G_dws')
        f_ck = col3.number_input('f_ck [MPa]', value=parameters['f_ck_dws'], min_value=5.0, max_value=80.0, step=5.0, key='f_ck_dws')
        alpha_cc = col1.number_input('alpha_cc [-]', value=0.7, min_value=0.0, max_value=1.0, step=0.1, key='alpha_cc_dws')
        gamma_c = col2.number_input('gamma_c [-]', value=1.5, min_value=0.0, max_value=2.0, step=0.1, key='gamma_c_dws')
        sigma_cd, f_cd = check_for_hoop_force(F_hoop_at_base, d_eff, gamma_G, f_ck, alpha_cc, gamma_c)
        if sigma_cd < f_cd:
            st.success('Hoop stress = {0:.2f} MPa < design hoop stress = {1:.2f} MPa: PASSED'.format(sigma_cd, f_cd))
        else:
            st.error('Hoop stress = {0:.2f} MPa > design hoop stress = {1:.2f} MPa: NOT PASSED'.format(sigma_cd, f_cd))

        check_hoop_stress_more = st.checkbox('Check for hoop stress at any shaft depth', value=parameters['check_hoop_stress_more_dws'], key='check_hoop_stress_more_dws')
        if check_hoop_stress_more:
            st.header('Check for hoop stress at any shaft depth')
            col1, col2 = st.columns(2)
            F_hoop = col1.number_input('Hoop force [kN/m]', value=parameters['F_hoop_dws'], min_value=10.0, max_value=100000.0, step=100.0, key='F_hoop_dws')
            L_hoop_dws = col2.number_input('Depth from top of shaft [m]', value=parameters['L_hoop_dws'], min_value=1.0, max_value=150.0, step=1.0, key='L_hoop_dws')
            x0, x, d_eff = get_parameters_shaft_diaphragm_panels(D, L_hoop_dws, H_drilling_platform, v)
            sigma_cd, f_cd = check_for_hoop_force(F_hoop, d_eff, gamma_G, f_ck, alpha_cc, gamma_c)
            if sigma_cd < f_cd:
                st.success('Hoop stress = {0:.2f} MPa < design hoop stress = {1:.2f} MPa: PASSED'.format(sigma_cd, f_cd))
            else:
                st.error('Hoop stress = {0:.2f} MPa > design hoop stress = {1:.2f} MPa: NOT PASSED'.format(sigma_cd, f_cd))

    # Download session state JSON file
    session_state = dict(st.session_state)  # LazySessionState to dict
    session_state.pop('fileuploader_dws')   # do not save state for file uploader
    download_filename = 'piles_and_pannels' + '_shaft_Dwall_panels' + '.JSON'
    href = st_json_download_button(session_state, download_filename)
    st.markdown(href, unsafe_allow_html=True)


def display_shaft_stiffnesses(d_top, d_eff, E, st):
    """ Displays shaft stiffness
    """
    I = get_area_moment_of_inertia_rect(1.0, d_top)
    EI = E*I        # [kNm**2/m]
    EA = E*d_top    # [kN/m]
    st.write('EI at top = {0:.2f} [kNm$^2$/m], EA at top = {1:.2f} [kN/m]'.format(EI, EA))
    I = get_area_moment_of_inertia_rect(1.0, d_eff)
    EI = E*I        # [kNm**2/m]
    EA = E*d_eff    # [kN/m]
    st.write('EI at bottom = {0:.2f} [kNm$^2$/m], EA at bottom = {1:.2f} [kN/m]'.format(EI, EA))