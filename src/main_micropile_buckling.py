import os
from matplotlib.pyplot import plot
from src.pile_buckling.micropile_buckling import (get_cross_section_parameters_circular, get_w_f_elastoplastic_eq1, get_p_f_elastoplastic_eq2, 
                                    get_p_f_elastoplastic_eq3, get_p_f_elastoplastic_eq4, get_p_f_elastoplastic_user, get_Ncr_by_iteration, get_Nb_Rd_EC3,
                                    display_micropile_buckling_resistance, plot_cross_section, get_slenderness_lambda,
                                    get_cross_section_parameters_tube)
from src.file_utilitites import load_parameters_from_json_file, st_json_download_button

# Initial parameters
parameters_init = {'d': 50.0, 'D': 270.0, 'E': 200000.0, 'fy': 500.0, 'Ec': 15000.0, 'fc': 20.0, 'c_u': 25.0, 'contact_surface': 'Ideally rough', 'L': 5.0, 'k_imp': 1.0/200, 'buckling_curve': 'c', 'gamma_M': 1.1}

def main_micropile_buckling(st, parameters=None):
    st.title('Micro-pile buckling check')

    st.subheader('Load saved session state (optional)')
    uploaded_file_session_state = st.file_uploader('Select session state file to load', type='json', key='fileuploader_micropile_buckling')
    parameters_user = None
    if uploaded_file_session_state is not None:
        try:
            parameters_user = load_parameters_from_json_file(uploaded_file_session_state)
            st.success('File successfully loaded')
            if parameters_user['selected_form'] != 'Micropile buckling':
                st.write("Wrong JSON data file. Please load data for the selected form 'Micropile buckling'!!")
                st.stop()
        except Exception as e:
            st.error(e)
            st.write("Wrong JSON data file. Please load data for the selected form 'Micropile buckling'!!")
            st.stop()

    if parameters_user is None:
        parameters = parameters_init
    else:
        parameters = parameters_user

    # Cross-sectional parameters
    st.subheader('Cross-sectional parameters')
    col1, col2, col3 = st.columns((2, 2, 1))
    d = col1.number_input('Steel bar diameter d [mm]', value=parameters['d'], format='%.2f', min_value=1.0, max_value=100.0, step=1.0, key='d')
    D = col2.number_input('Pile shaft diameter D [mm]', value=parameters['D'], format='%.2f', min_value=50.0, max_value=400.0, step=10.0, key='D') 
    E = col1.number_input("Young's modulus of steel bar E [kN/m^2]", value=parameters['E'], format='%.2f', min_value=50000.0, max_value=300000.0, step=10000.0, key='E')
    fy =col2.number_input('Characteristic yield stress of steel bar fy [MN/m^2]', value=parameters['fy'], format='%.2f', min_value=300.0, max_value=800.0, step=100.0, key='fy')
    A, I, EI, fyA = get_cross_section_parameters_circular(d, E, fy)
    col1.write('Steel bar: Area A = {0:.2f} [mm$^2$]; Second moment of inertia I = {1:.2f} [cm$^4$]'.format(A, I))
    col2.write('Steel bar: Regidity EI = {0:.2f} [kNm$^2$]; Characteristic plastic capacity normal force fyA = {1:.2f} [kN]'.format(EI, fyA))

    #col1, col2, col3 = st.columns((2, 2, 1))
    Ec = col1.number_input("Young's modulus of grout [kN/m^2]", value=parameters['Ec'], min_value=5000.0, max_value=50000.0, step=1000.0, key='Ec')
    fc = col2.number_input('Characteristic yield stress of grout [MN/m^2]', value=parameters['fc'], min_value=5.0, max_value=100.0, step=10.0, key='fc')
    A_c, I_c, EI_c, fyA_c = get_cross_section_parameters_tube(D, D/2-d/2, Ec, fc)
    col1.write('Outer grout: Area A_c = {0:.2f} [mm$^2$]; Second moment of inertia I_c = {1:.2f} [cm$^4$]'.format(A_c, I_c))
    col2.write('Outer grout: Regidity EI_c = {0:.2f} [kNm$^2$]; Characteristic plastic capacity normal force fyA_c = {1:.2f} [kN]'.format(EI_c, fyA_c))

    # Plot cross-section
    fig = plot_cross_section(D, d)
    col3.pyplot(fig)

    # Selection for p-y cur2e
    #st.subheader('Maximal mobilized lateral displacement and stress (soil-pile interaction)')
    st.subheader('Soil-pile interaction and buckling parameters')
    col1, col2, col3 = st.columns((1, 1, 1))
    c_u = col1.number_input('Undrained shear strength [kN/m^2]', value=parameters['c_u'], format='%.2f', min_value=1.0, max_value=150.0, step=5.0, key='c_u', help='Soil displacement at failure $w_f/D = 0.2/(c_u^{0.4})$')
    w_f = get_w_f_elastoplastic_eq1(D, c_u)
    contact_surface_options = ('Ideally smooth', 'Ideally rough', 'Pile not completely encircled by soil', 'User defined')
    help_p_f_c_u = """Soil bearing pressure at failure $p_f = (6 + \pi)*c_u$ (ideally smooth), $p_f = (4\sqrt{2} + 2\pi)*c_u$ (ideally rough),
                    $p_f = (2 + 2\pi)*c_u$ (Pile not completely encircled by soil)"""
    eq_p_f = col2.selectbox('Pile contact surface (with soil)', contact_surface_options, index=contact_surface_options.index(parameters['contact_surface']), key='contact_surface', help=help_p_f_c_u)
    a = 10.5 # default value for a
    if eq_p_f == 'Ideally smooth':
        p_f = get_p_f_elastoplastic_eq2(c_u)
        p_f_eq = get_p_f_elastoplastic_eq2
    elif eq_p_f == 'Ideally rough':
        p_f = get_p_f_elastoplastic_eq3(c_u)
        p_f_eq = get_p_f_elastoplastic_eq3
    elif eq_p_f == 'Pile not completely encircled by soil':
        p_f = get_p_f_elastoplastic_eq4(c_u)
        p_f_eq = get_p_f_elastoplastic_eq4
    else: # user defined
        a = float(col3.text_input('User-defined constant a, for p_f = a*c_u', a))
        p_f = get_p_f_elastoplastic_user(c_u, a)
        p_f_eq = get_p_f_elastoplastic_user

    col1.write('Soil displacement at failure w_f = {0:.2f} [mm]'.format(w_f))
    col2.write('Soil stress at failure p_f = {0:.2f} [kN/m$^2$]\n\n'.format(p_f))


    # Micropile length and buckling parameters
    #st.subheader('Micropile length and buckling parameters')
    L = col1.number_input('Pile length [m]', value=parameters['L'], format='%.2f', min_value=1.0, max_value=100.0, step=1.0, key='L')
    k_imp = col2.number_input('Imperfection parameter kappa [m]', value=parameters['k_imp'], format='%.4f', min_value=1.0/900, max_value=1.0/50, step=1.0/1000, key='k_imp')       # [1/m]
    buckling_curve_options = ('a0', 'a', 'b', 'c', 'd')
    buckling_curve = col1.selectbox("Buckling curve (Table 6.2 and Figure 6.4, EC3: curve 'c' for a filled circle cross-section)", buckling_curve_options, index=buckling_curve_options.index(parameters['buckling_curve']), key='buckling_curve') 
    gamma_M = col2.number_input('gamma_M1 (EC3, gamma_M1 = 1.1 for buckling)', value=parameters['gamma_M'], format='%.2f', min_value=1.0, max_value=3.0, step=0.1, key='gamma_M')

    # Buckling resistance check for the given c_u value
    #st.subheader('Design resistance against buckling')
    Lcr, Ncr = get_Ncr_by_iteration(w_f*0.001, EI+EI_c, p_f, D*0.001, k_imp, L)
    Nb_Rd, lambda_, chi = get_Nb_Rd_EC3(fyA+fyA_c, Ncr, buckling_curve, gamma_M)
    col1.write('Design resistance against buckling with slenderness $\lambda = {:.2f}$'.format(lambda_))
    col1.write('EC3 reduction factor $\chi = {:.2f}$'.format(chi))
    col2.write('Ideal buckling length Lcr = {0:.2f} [m] and force Ncr = {1:.2f} [kN]'.format(Lcr, Ncr))
    col2.write('EC3 design buckling resistance Nb_Rd = {0:.2f} [kN]'.format(Nb_Rd))

    # Data generation and plotting
    fig = display_micropile_buckling_resistance(D, EI+EI_c, fyA+fyA_c, k_imp, L, p_f_eq, a, c_u, Nb_Rd, buckling_curve, gamma_M)
    col3.pyplot(fig)

    # Download session state JSON file
    session_state = dict(st.session_state)  # LazySessionState to dict
    session_state.pop('fileuploader_micropile_buckling')   # do not save state for file uploader
    download_filename = 'piles_and_pannels' + '_micropile_buckling' + '.JSON'
    href = st_json_download_button(session_state, download_filename)
    st.markdown(href, unsafe_allow_html=True)


    st.subheader('Reference')
    #st.markdown('Vogt, N., & Vogt, S. (2013). Biegeknickwiderstand von Mikropfählen gemäß den Eurocodes. Bautechnik, 90(9), 550-558.')
    # linking referenced document
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #st.write(dir_path)
    #pdf_path = os.path.join(dir_path, 'pile_buckling', 'refs', 'Vogt_und_Vogt_2013_Biegeknickwiderstand.pdf')
    #st.write(pdf_path)
    #st.markdown("Vogt, N., & Vogt, S. (2013). Biegeknickwiderstand von Mikropfählen gemäß den Eurocodes. Bautechnik, 90(9), 550-558. [Link]({})".format(pdf_path_manual), unsafe_allow_html=True)
    #st.markdown("""<embed src="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf" width="400" height="400">""", unsafe_allow_html=True)
    #st.write("Something[link](https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf)")
    pdf_hyperlink_sharepoint = 'https://bauergroup-my.sharepoint.com/personal/luan_nguyen_bauer_de/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fluan%5Fnguyen%5Fbauer%5Fde%2FDocuments%2FMysite%20Documents%2FF%C3%BCr%20jeden%20freigegeben%2FStreamlit%5Fdocs%2FVogt%5Fund%5FVogt%5F2013%5FBiegeknickwiderstand%2Epdf&parent=%2Fpersonal%2Fluan%5Fnguyen%5Fbauer%5Fde%2FDocuments%2FMysite%20Documents%2FF%C3%BCr%20jeden%20freigegeben%2FStreamlit%5Fdocs'
    st.write("Vogt, N., & Vogt, S. (2013). Biegeknickwiderstand von Mikropfählen gemäß den Eurocodes. Bautechnik, 90(9), 550-558. [Open document]({})".format(pdf_hyperlink_sharepoint))