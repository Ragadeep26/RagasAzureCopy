import numpy as np
from src.piles_and_panels.wall_secant_piles import (get_parameters_wall_secant_piles, plot_wall_secant_piles,
                                   plot_wall_secant_piles_3d, plot_wall_secant_piles_2items,
                                   plot_wall_secant_piles_3d_2items)
from src.common import get_area_moment_of_inertia_rect
from src.file_utilitites import load_parameters_from_json_file, st_json_download_button

# Initial parameters
parameters_init = {"project_name_spw": "Sample project", "project_revision_spw": "First issue, rev0", "wall_name_spw": "Wall 1", "D_spw": 1.2,
            "n_pieces_spw": 10, "a_spw": 0.75, "L_spw": 25.0, "v_spw": 0.75, "H_drilling_platform_spw": 0.0, "E_spw": 30.0e6, "plotting_option_spw":'Two piles apart'}

def main_secant_piled_wall(st):
    """ Main program for secant piled wall
    """
    st.title('Geometric check for secant piled wall')

    st.header('Load saved session state (optional)')
    uploaded_file_session_state = st.file_uploader('Select session state file to load', type='json', key='fileuploader_spw')
    parameters_user_spw = None
    if uploaded_file_session_state is not None:
        try:
            parameters_user_spw = load_parameters_from_json_file(uploaded_file_session_state)
            st.success('File successfully loaded')
            if parameters_user_spw['selected_form'] != 'Secant piled wall':
                st.write("Wrong JSON data file. Please load data for the selected form 'Secant piled wall'!!")
                st.stop()
        except Exception as e:
            st.error(e)
            st.write("Wrong JSON data file. Please load data for the selected form 'Micropile buckling'!!")
            st.stop()

    if parameters_user_spw is None:
        parameters = parameters_init
    else:
        parameters = parameters_user_spw

    st.header('Project information')
    col1, col2 = st.columns(2)
    project_name = col1.text_input('Project', value=parameters['project_name_spw'], key='project_name_spw')
    col2.text_input('Revision', value=parameters['project_revision_spw'], key='project_revision_spw')

    st.header('Input parameters')
    col1, col2, col3 = st.columns(3)
    wall_name = col1.text_input('Wall identification', value=parameters['wall_name_spw'], key='wall_name_spw')
    D = col2.number_input('Pile diameter [m]', value=parameters['D_spw'], format='%.2f', min_value=0.3, max_value=5.0, step=0.1, key='D_spw')
    a = col3.number_input('C/C pile spacing b/w two neighboring piles [m]', value=parameters['a_spw'], format='%.2f', min_value=0.0, max_value=5.0, step=0.1, key='a_spw')
    L = col1.number_input('Length of shaft [m]', value=parameters['L_spw'], step=1.0, min_value=1.0, max_value=150.0, key='L_spw')
    v = col2.number_input('Drilling verticality [%]', value=parameters['v_spw'], step=0.1, min_value=0.00, max_value=2.0, key='v_spw')
    col1, col2, _ = st.columns(3)
    H_drilling_platform = col1.number_input('Height of drilling platform above top of piles [m]', value=parameters['H_drilling_platform_spw'], step=1.0, min_value=0.0, max_value=20.0, key='H_drilling_platform_spw')
    col2.write('The initial deviation by free drilling x0 = {:.2f} cm'.format(H_drilling_platform*v))
    t_top, d_top, x0, x, t_eff, d_eff = get_parameters_wall_secant_piles(D, a, L, H_drilling_platform, v)

    st.header('Output parameters for {}'.format(wall_name))
    col1, col2, col3 = st.columns(3)
    #col1.write('C/c spacing at top of wall a = {:.2f} m'.format(a))
    col1.write('Overcut at top of wall t = {:.2f} cm'.format(t_top*100))
    col1.write('Effective thickness at top of wall d = {:.2f} cm'.format(d_top*100))
    col1.write('Deviation at bottom of wall dx = {:.2f} cm'.format(x*100))

    if t_eff > 0:
        d_eff = 2*np.sqrt((D/2)*t_eff - (t_eff/2)**2) # overlapped thickness, m    
        col2.write('Overcut at bottom of wall t_eff = {:.2f} cm'.format(t_eff*100))
        col2.write('Effective thickness at bottom of wall d_eff = {:.2f} cm'.format(d_eff*100))

        # Write overlapped area
        #A_triangular_wedge = (D/2 - t_top/2)*d_top/2
        A_triangular_wedge = (a/2) * (d_top/2)
        theta = 2*np.arcsin((d_top/2)/(D/2))    # radian
        A_theta = theta/2 * (D/2)**2
        #col3.write(theta*180/np.pi)
        #col3.write(A_theta)
        #col3.write(A_triangular_wedge)
        A_intersect = 2*(A_theta - A_triangular_wedge)
        col3.write('Intersected area b/t two neighboring piles: {:.2f} cm$^2$'.format(A_intersect*10000))
        with st.expander('Axial and flexural rigidity considering effective thickness at top and bottom of shaft'):
            E = st.number_input("Concrete Young's modulus E [KPa]", value=parameters['E_spw'], format='%.0f', min_value=25.0e6, max_value=35.0e6, step=1.0E6, key='E_spw')
            display_wall_stiffnesses(d_top, d_eff, E, st)
    else:
        d_eff = np.nan
        col2.warning('PILES DO NOT TOUCH IN BASE OF WALL!!')


    st.header('Visualization for {}'.format(wall_name))
    col1, col2 = st.columns(2)
    plotting_options = ['Two piles apart', 'Random deviations']
    plotting_option = col1.selectbox('Type of visualization', plotting_options, index=plotting_options.index(parameters['plotting_option_spw']), key='plotting_option_spw')
    if plotting_option == 'Two piles apart':
        st.write('Piles view at base of the shaft are plotted for 3 orientations (in-plane inward, in-plane outward, out-of-plane opposite directions), given a deviation dx = {:.2f} cm.'.format(x*100))
        fig1 = plot_wall_secant_piles_2items(a, D, x0, x, wall_name)
        st.pyplot(fig1)
        fig2 = plot_wall_secant_piles_3d_2items(2, a, D, L, x0, x, wall_name)
        st.pyplot(fig2)
    else:
        st.write('Piles view at base of the shaft are plotted for random orientations for each of the piles, given a deviation dx = {:.2f} cm.'.format(x*100))
        n_pieces = int(col2.number_input('Number of piles to plot', value=int(parameters['n_pieces_spw']), format='%i', min_value=2, max_value=100, step=1, key='n_pieces_spw'))
        fig1 = plot_wall_secant_piles(n_pieces, a, D, x0, x, wall_name)
        st.pyplot(fig1)
        fig2 = plot_wall_secant_piles_3d(n_pieces, a, D, L, x0, x, wall_name)
        st.pyplot(fig2)

    # Download session state JSON file
    session_state = dict(st.session_state)  # LazySessionState to dict
    session_state.pop('fileuploader_spw')   # do not save state for file uploader
    download_filename = 'piles_and_pannels' + '_secant_piles_wall' + '.JSON'
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