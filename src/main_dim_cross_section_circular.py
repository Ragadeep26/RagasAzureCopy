#from ssl import SSLSession
#from turtle import update
from scipy import interpolate
from src.dimensioning.parameters import *
#from src.dimensioning.barrette import Barrette
from src.dimensioning.pile import Pile
from src.file_utilitites import load_parameters_from_json_file, st_json_download_button

parameters_init = {'project_title': 'Sample project', 'project_revision': 'r00', 'code': 'EN 1992-1-1:2004 (Eurocode 2)', 'concrete_grade': 'C 25/30', 'params_concrete': {}, 'params_reinf': {}, 'min_reinf': False, 'params_psf': {},
                    'internal_forces_permanent': {}, 'internal_forces_transient': {}}

def main_dim_cross_section(st, parameters=None):
    """ Main program for dimensiong of cross section
    """
    st.title('Reinforcement calculation for circular cross-section')
    #st.header('Under testing for saving and loading..')

    st.subheader('Load saved session state (optional)')
    uploaded_file_session_state = st.file_uploader('Select session state file to load', type='json', key='fileuploader')
    parameters_user = None
    if uploaded_file_session_state is not None:
        try:
            parameters_user = load_parameters_from_json_file(uploaded_file_session_state)
            st.success('File successfully loaded')
            if parameters_user['selected_form'] != 'Concrete reinforcement circ. section':
                st.write("Wrong JSON data file. Please load data for the selected form 'Concrete reinforcement circ. section'!!")
                st.stop()
        except Exception as e:
            st.error(e)
            st.write("Wrong JSON data file. Please load data for the selected form 'Micropile buckling'!!")
            st.stop()

    if parameters_user is None:
        parameters = parameters_init
    else:
        parameters = parameters_user

    st.subheader('Project information')
    col1, col2 = st.columns(2)
    project_name = col1.text_input('Project', value=parameters['project_title'], key='project_title')
    col2.text_input('Revision', value=parameters['project_revision'], key='project_revision')

    # concrete
    params_concrete = parameters['params_concrete']
    code_names = ['DIN 1045:1998', 'DIN 1045:2008', 'EN 1992-1-1:2004 (Eurocode 2)', 'EN 1992-1-1:2004 + AX:2010 + NA:2011']
    st.subheader('Code, concrete and steel')
    #code_str = st.selectbox('Code', code_names, index=code_names.index(parameters['code']), key='code', on_change=update_code, args=(st, parameters)) # code name
    code_str = st.selectbox('Code', code_names, index=code_names.index(parameters['code']), key='code') # code name
    code = code_names.index(code_str)                       # integer index for code

    concrete_param_names_per_code = (PARAM_NAMES_CODE_0, PARAM_NAMES_CODE_1, PARAM_NAMES_CODE_2, PARAM_NAMES_CODE_3)
    concrete_grade_per_code = (CONCRETE_GRADE_CODE_0, CONCRETE_GRADE_CODE_1, CONCRETE_GRADE_CODE_2, CONCRETE_GRADE_CODE_3)
    concrete_alpha_per_code = (CONCRETE_ALPHA_CODE_0, CONCRETE_ALPHA_CODE_1, CONCRETE_ALPHA_CODE_2, CONCRETE_ALPHA_CODE_3)
    concrete_epsilon_c2_per_code = (CONCRETE_EPSILON_C2_CODE_0, CONCRETE_EPSILON_C2_CODE_1, CONCRETE_EPSILON_C2_CODE_2, CONCRETE_EPSILON_C2_CODE_3)
    concrete_epsilon_c2u_per_code = (CONCRETE_EPSILON_C2U_CODE_0, CONCRETE_EPSILON_C2U_CODE_1, CONCRETE_EPSILON_C2U_CODE_2, CONCRETE_EPSILON_C2U_CODE_3)
    concrete_exp_per_code = (CONCRETE_EXP_CODE_0, CONCRETE_EXP_CODE_1, CONCRETE_EXP_CODE_2, CONCRETE_EXP_CODE_3)
    concrete_delta_alpha_pl_per_code = (CONCRETE_DELTA_ALPHA_PL_CODE_0, CONCRETE_DELTA_ALPHA_PL_CODE_1, CONCRETE_DELTA_ALPHA_PL_CODE_2, CONCRETE_DELTA_ALPHA_PL_CODE_3)
    concrete_unreinforced_per_code = (CONCRETE_UNREINFORCED_CODE_0, CONCRETE_UNREINFORCED_CODE_1, CONCRETE_UNREINFORCED_CODE_2, CONCRETE_UNREINFORCED_CODE_3)
    concrete_Ecm_per_code = (CONCRETE_E_CM_CODE_0, CONCRETE_E_CM_CODE_1, CONCRETE_E_CM_CODE_2, CONCRETE_E_CM_CODE_3)
    #concrete_grade = st.selectbox('Concrete grade', list(concrete_grade_per_code[code].keys()), key='concrete_grade', on_change=update_params_concrete, args=(st, params_concrete))   # string for concrete grade
    concrete_grade = st.selectbox('Concrete grade', list(concrete_grade_per_code[code].keys()), key='concrete_grade')   # string for concrete grade
    #concrete_grade = st.selectbox('Concrete grade', list(concrete_grade_per_code[code].keys()), index=list(concrete_grade_per_code[code].keys()).index(parameters['concrete_grade']), key='concrete_grade')   # string for concrete grade
    cols = st.columns(8)
    params_concrete = parameters['params_concrete']
    params_concrete['param_0'] = cols[0].text_input(concrete_param_names_per_code[code][0], concrete_grade_per_code[code][concrete_grade], key='concrete_param_0')
    params_concrete['param_1'] = cols[1].text_input(concrete_param_names_per_code[code][1], concrete_alpha_per_code[code][concrete_grade], key='concrete_param_1')
    params_concrete['param_2'] = cols[2].text_input(concrete_param_names_per_code[code][2], concrete_epsilon_c2_per_code[code][concrete_grade], key='concrete_param_2')
    params_concrete['param_3'] = cols[3].text_input(concrete_param_names_per_code[code][3], concrete_epsilon_c2u_per_code[code][concrete_grade], key='concrete_param_3')
    params_concrete['param_4'] = cols[4].text_input(concrete_param_names_per_code[code][4], concrete_exp_per_code[code][concrete_grade], key='concrete_param_4')
    params_concrete['param_5'] = cols[5].text_input(concrete_param_names_per_code[code][5], concrete_delta_alpha_pl_per_code[code][concrete_grade], key='concrete_param_5')
    params_concrete['param_6'] = cols[6].text_input(concrete_param_names_per_code[code][6], concrete_unreinforced_per_code[code][concrete_grade], key='concrete_param_6')
    params_concrete['param_7'] = cols[7].text_input(concrete_param_names_per_code[code][7], concrete_Ecm_per_code[code][concrete_grade], key='concrete_param_7') # param not used in calculation

    # reinforcement
    #reinf_grade = reinf_grade # steel grad will be udpated later
    reinf_grade_per_code = (REINF_CODE_0, REINF_CODE_1, REINF_CODE_2, REINF_CODE_3)
    reinf_f_tk_per_code = (REINF_F_TK_CODE_0, REINF_F_TK_CODE_1, REINF_F_TK_CODE_2, REINF_F_TK_CODE_3)
    reinf_E_per_code = (REINF_E_CODE_0, REINF_E_CODE_1, REINF_E_CODE_2, REINF_E_CODE_3)
    reinf_epsilon_su_per_code = (REINF_EPSILON_CU_CODE_0, REINF_EPSILON_CU_CODE_1, REINF_EPSILON_CU_CODE_2, REINF_EPSILON_CU_CODE_3)
    #stress_strain = {}
    #params_reinf = params_reinf
    reinf_grade = st.selectbox('Reinforcement grade', list(reinf_grade_per_code[code].keys()), key='reinf_grade')   # string for concrete grade
    reinf_param_names = ['yield stress \n f_yk [MPa]', 'tens. strength \n f_tk [MPa]', 'elastic modulus \n E [MPa]', 'max. strain \n \N{GREEK SMALL LETTER EPSILON}_s,u [\N{PER MILLE SIGN}]', 'with crack \n max. \N{GREEK SMALL LETTER SIGMA}_s [MPa]', 'with crack \n reinf. bar \n max. ds [mm]', 'with crack \n bar spacing \n max. s [mm]']
    cols = st.columns(4)
    params_reinf = parameters['params_reinf']
    params_reinf['param_0'] = cols[0].text_input(reinf_param_names[0], reinf_grade_per_code[code][reinf_grade], key='reinf_param_0')
    params_reinf['param_1'] = cols[1].text_input(reinf_param_names[1], reinf_f_tk_per_code[code][reinf_grade], key='reinf_param_1')
    params_reinf['param_2'] = cols[2].text_input(reinf_param_names[2], reinf_E_per_code[code][reinf_grade], key='reinf_param_2')
    params_reinf['param_3'] = cols[3].text_input(reinf_param_names[3], reinf_epsilon_su_per_code[code][reinf_grade], key='reinf_param_3')

    # crack control
    crack_options = ['no crack', '0.4 mm', '0.3 mm', '0.2 mm']
    sigma_ds_per_code = (SIGMA_DS_CODE_0, SIGMA_DS_CODE_1, SIGMA_DS_CODE_2, SIGMA_DS_CODE_3)
    cols = st.columns(5)
    crack_width = cols[0].selectbox('Crack width', crack_options, key='crack_width')
    if crack_width == 'no crack':
        sigma = cols[1].text_input(reinf_param_names[4], 0.0) 
    else:
        sigma_ds_interp = sigma_ds_per_code[code]['sigma'] 
        ds_interp = sigma_ds_per_code[code][crack_width]
        ds = cols[2].number_input(reinf_param_names[5], value=28.0) 
        s = cols[3].number_input(reinf_param_names[6], value=200.0)
        sigma1_interp = interpolate.interp1d(ds_interp, sigma_ds_interp)
        sigma1 = sigma1_interp(ds)
        sigma_s_interp = SIGMA_S['sigma']
        s_interp = SIGMA_S[crack_width]
        sigma2_interp = interpolate.interp1d(s_interp, sigma_s_interp)
        sigma2 = sigma2_interp(s)
        sigma = max(sigma1, sigma2)
        cols[1].number_input(reinf_param_names[4], value=float(sigma)) ##### STOPPED HERE

    params_reinf['param_4'] = sigma

    min_reinf = cols[4].checkbox('Minimum reinforcement?', value=parameters['min_reinf'], key='min_reinf')  # no minimum reinforcement by default
    # partial safety factors
    psf_load_case_per_code = (PSF_LOAD_CASES_CODE_0, PSF_LOAD_CASES_CODE_1, PSF_LOAD_CASES_CODE_2, PSF_LOAD_CASES_CODE_3)
    psf_param_names_per_code = (PSF_NAMES_CODE_0, PSF_NAMES_CODE_1, PSF_NAMES_CODE_2, PSF_NAMES_CODE_3)
    psf_gammaG_per_code = (PSF_GAMMA_G_CODE_0, PSF_GAMMA_G_CODE_1, PSF_GAMMA_G_CODE_2, PSF_GAMMA_G_CODE_3)
    psf_gammaQ_per_code = (PSF_GAMMA_Q_CODE_0, PSF_GAMMA_Q_CODE_1, PSF_GAMMA_Q_CODE_2, PSF_GAMMA_Q_CODE_3)
    psf_gammaC_per_code = (PSF_GAMMA_C_CODE_0, PSF_GAMMA_C_CODE_1, PSF_GAMMA_C_CODE_2, PSF_GAMMA_C_CODE_3)
    psf_gammaS_per_code = (PSF_GAMMA_S_CODE_0, PSF_GAMMA_S_CODE_1, PSF_GAMMA_S_CODE_2, PSF_GAMMA_S_CODE_3)

    st.subheader('Design situation')
    design_situations = psf_load_case_per_code[code]
    cols = st.columns(5)
    design_situation = cols[0].selectbox('Design situation', design_situations, key='design_situation')
    gamma_G = cols[1].number_input(psf_param_names_per_code[code][0], psf_gammaG_per_code[code][design_situation], step=0.05, key='psf_param_0')
    gamma_Q = cols[2].number_input(psf_param_names_per_code[code][1], psf_gammaQ_per_code[code][design_situation], step=0.05, key='psf_param_1')
    gamma_C = cols[3].number_input(psf_param_names_per_code[code][2], psf_gammaC_per_code[code][design_situation], step=0.05, key='psf_param_2')
    gamma_S = cols[4].number_input(psf_param_names_per_code[code][3], psf_gammaS_per_code[code][design_situation], step=0.05, key='psf_param_3')
    params_psf = parameters['params_psf']
    params_psf['param_0'] = gamma_G
    params_psf['param_1'] = gamma_Q
    params_psf['param_2'] = gamma_C
    params_psf['param_3'] = gamma_S

    st.subheader('Cross-section')
    cross_section_pile = {'D': 1.2, 'H': 100.0, 'S': 1.0}
    cross_section_keys = ['diameter D [m]', 'sep. to edge H [mm]', 'spacing b/w reinforced piles [m]']
    cols = st.columns(3)
    cross_section_pile['D'] = cols[0].number_input(cross_section_keys[0], cross_section_pile['D'], step=0.1)
    cross_section_pile['H'] = cols[1].number_input(cross_section_keys[1], cross_section_pile['H'], step=100.0)
    cross_section_pile['S'] = cols[2].number_input(cross_section_keys[2], cross_section_pile['S'], step=0.1)
    ## Plot cross-section here

    st.subheader('Section forces')
    st.write('Compressive normal force is negative!')
    force_keys_perm= ['perm. normal N_k [kN]', 'perm. bending M_k [kNm]', 'perm. shear Q_k [m]']
    force_keys_trans= ['trans. normal N_k [kN]', 'trans. bending M_k [kNm]', 'trans. shear Q_k [m]']
    internal_forces_permanent = {'N': -200.0, 'M': 2000.0, 'Q': 500.0}
    internal_forces_transient = {'N': 0.0, 'M': 0.0, 'Q': 0.0}
    cols = st.columns(3)
    internal_forces_permanent['N'] = cols[0].number_input(force_keys_perm[0], value=internal_forces_permanent['N'], step=100.0)
    internal_forces_permanent['M'] = cols[1].number_input(force_keys_perm[1], value=internal_forces_permanent['M'], step=100.0)
    internal_forces_permanent['Q'] = cols[2].number_input(force_keys_perm[2], value=internal_forces_permanent['Q'], step=100.0)
    internal_forces_transient['N'] = cols[0].number_input(force_keys_trans[0], value=internal_forces_transient['N'], step=100.0)
    internal_forces_transient['M'] = cols[1].number_input(force_keys_trans[1], value=internal_forces_transient['M'], step=100.0)
    internal_forces_transient['Q'] = cols[2].number_input(force_keys_trans[2], value=internal_forces_transient['Q'], step=100.0)
    #internal_forces_characteristic = parameters['internal_forces_characteristic']
    internal_forces_characteristic = {}
    internal_forces_characteristic['N'] = internal_forces_permanent['N'] + internal_forces_transient['N']
    internal_forces_characteristic['M'] = internal_forces_permanent['M'] + internal_forces_transient['M']
    internal_forces_characteristic['Q'] = internal_forces_permanent['Q'] + internal_forces_transient['Q']
    #internal_forces_design = parameters['internal_forces_design']
    internal_forces_design = {}
    internal_forces_design['N'] = gamma_G * internal_forces_permanent['N'] + gamma_Q * internal_forces_transient['N']
    internal_forces_design['M']= gamma_G * internal_forces_permanent['M'] + gamma_Q * internal_forces_transient['M']
    internal_forces_design['Q']= gamma_G * internal_forces_permanent['Q'] + gamma_Q * internal_forces_transient['Q']
    cols[0].write('Design normal force N_d [kN]: {:.2f}'.format(internal_forces_design['N']))
    cols[1].write('Design bending moment M_d [kNm]: {:.2f}'.format(internal_forces_design['M']))
    cols[2].write('Design shear force Q_d [kNm]: {:.2f}'.format(internal_forces_design['Q']))

    st.subheader('Required reinforcement')
    pile = Pile(**cross_section_pile)
    A_s, a_s = pile.calculate_required_reinforcement_cross_section(code, params_psf, params_concrete, params_reinf, internal_forces_characteristic, min_reinf)
    st.write('Reinforcement requirements A_s = {0:.2f} cm$^2$, a_s = {1:.2f} cm$^2$/m'.format(A_s, a_s))

    # Download session state JSON file
    session_state = dict(st.session_state)  # LazySessionState to dict
    session_state.pop('fileuploader')   # do not save state for file uploader
    session_state = add_parameters_to_save(session_state, {'params_concrete': params_concrete, 'params_reinf': params_reinf, 'params_psf': params_psf, 'internal_forces_permanent': internal_forces_permanent, 'internal_forces_transient': internal_forces_transient})
    download_filename = 'piles_and_pannels' + '_concrete_reinf_circ' + '.JSON'
    href = st_json_download_button(session_state, download_filename)
    st.markdown(href, unsafe_allow_html=True)

    st.subheader('Reference')
    pdf_hyperlink_sharepoint = 'https://bauergroup-my.sharepoint.com/personal/luan_nguyen_bauer_de/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fluan%5Fnguyen%5Fbauer%5Fde%2FDocuments%2FMysite%20Documents%2FF%C3%BCr%20jeden%20freigegeben%2FStreamlit%5Fdocs%2FLinseThielen%5FBetonundStahlbetonbau1972%2Epdf&parent=%2Fpersonal%2Fluan%5Fnguyen%5Fbauer%5Fde%2FDocuments%2FMysite%20Documents%2FF%C3%BCr%20jeden%20freigegeben%2FStreamlit%5Fdocs'
    st.write("Linse, D, & Thielen G. (1972). Die Grundlagen der Biegebemessung der DIN 1045 aufbereitet für den Gebrauch an Rechenanlagen. [Open document]({})".format(pdf_hyperlink_sharepoint))

    st.subheader('Program history')
    st.write('The calculation procedure was converted from 0_stb.xlsx (coded by Dr. Klobe) to Python by Ragadeep Bojja.')


def add_parameters_to_save(session_state, parameters):
    """ Extends parameters to session_state dictionary"""
    #print(session_state)
    for key, value in parameters.items():
        session_state[key] = value

    #print(session_state)
    return session_state