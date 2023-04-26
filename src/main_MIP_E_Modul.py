#import os
from PIL import Image
from matplotlib.backends.backend_pdf import PdfPages
from src.report.report_matplotlib import Report

# Initial parameter
password = 'ibh-1508'
parameters_init = {'password_user':'', 'fmk': 4.0, 'fines_content': 60.0}

def main_MIP_E_Modul(st, parameters=None):
    """ Getting E-Modulus for MIP material after DIN EN 12390-13"""
    #cwd = os.getcwd()
    #st.write(cwd)
    #onlyfiles = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
    #onlydirs = [f for f in os.listdir(cwd) if not os.path.isfile(os.path.join(cwd, f))]
    #st.write(onlyfiles)
    #st.write(onlydirs)
    #logo_bauer = Image.open('./common/BAUER_ohneSchriftzug_Logo_png.png')
    logo_bt = Image.open('./common/BT_Logo.jpg')
    col1, col2 = st.columns((1,9))
    #col1.image(logo_bauer, caption='BST')
    col1.image(logo_bt, caption='BST\BT')
    col2.title("Abschätzung des MIP Elastizitätsmoduls nach DIN EN 12390-13")

    if parameters is None:
        parameters = parameters_init
    
    parameters['password_user'] = ''    # initialize user password at every session restart
    
    placeholder = st.empty()
    with placeholder.container():
        #st.write('This program is password protected. Please enter your password to continue!')
        st.write('Dieses Programm ist passwortgeschützt. Bitte geben Sie Ihr Passwort ein, um fortzufahren!')
        st.write('Bitte das Passwort im BT-Sekretariat anfragen! :arrow_right: petra.ziegltrum@bauer.de')
        st.text_input('Password', value="", key="password", type="password", on_change=check_password(st, parameters))

#    print('user password is: ', parameters['password_user'])
#    print('defined password is: ', password)
#
    if parameters['password_user'] == password:
        placeholder.empty() # empty prompt for entering password if successfully entered
        continue_program(st, parameters)


def check_password(st, parameters):
    """ Checks if the entered password is correct"""
    session_state = dict(st.session_state)
    if 'password' in session_state:
        if session_state['password'] != password:
            #st.write('Your entered password is not correct!')
            st.write('Ihr eingegebenes Passwort ist nicht korrekt!')
        parameters['password_user'] = session_state['password']


def continue_program(st, parameters):
    """ Runs the main program"""
    col1, col2 = st.columns(2)
    col1.header('Basis, Normen und Probekörper')
    col1.markdown("""
                    - Interne BAUER-Datenbank/ Versuchsergebnisse
                    - DIN 4093:2015; vereinfachter Nachweis
                    - DIN EN 12390-13
                    - Probekörperabmessungen: h/d = 2/1
                """)

    col2.header('Anwendungsbereich')
    col2.markdown("""
                    - Druckfestigkeiten fm,k: 2,0 MPa bis 9,0 MPa
                    - Ton- und Schluffanteile: 10% bis 60% (Anteil im Boden < 0,063 mm)
                    - Bei Ton- und Schluffanteilen > 60% ist mit höherer Ungenauigkeit zu rechnen
                    - Bei Ton- und Schluffanteilen < 10% wird 10% angesetzt
                """)

    #col3.header('Ansprechpartner')
    #col3.markdown("""
    #                - Inhalte (bara,ibh)
    #                - WebApp (nya), konvertiert von ExcelApp (ceh)
    #            """)


    st.header('Die Applikation')
    col1, col2 = st.columns(2)
    fmk = col1.number_input('MIP fm,k [N/mm^2]', value=parameters['fmk'], min_value=2.0, max_value=9.0, step=0.5)
    fines_content = col2.number_input('Ton- und Schluffanteil [%]', value=parameters['fines_content'], min_value=0.0, max_value=100.0, step=5.0)
    a_factor = get_a_factor(fmk)
    #fm = fmk/a_factor
    fm_mittel = get_fm_mittel(fmk)
    #col3.text_area('MIP fm,mittel [N/mm^2]', '{0:.2f}'.format(fm_mittel).replace('.', ','), height=1)
    col1.write('MIP fm,mittel ist {0:.2f} [N/mm$^2$] '.format(fm_mittel))
    E_modul = calc_E_Modul(fm_mittel, fines_content)
    st.subheader('E-Modul ist {0:.0f} [N/mm$^2$]'.format(E_modul//50 * 50)) # value with a 50 N/mm^2 increament is showed

    message = ''
    if fines_content > 60.0:
        message = "Der Feinanteil ist >60%. E-Modul ist mit höhrer Ungenauigkeit zu rechnen."
    if fines_content < 10.0:
        message = "Der Feinanteil ist <10%. E-Modul wurde mit einem Feinanteil=10% berechnet."
    st.write(message)

    # PDF report
    #checkbox = st.checkbox('Download report in PDF', value=False)
    should_print_report_botton =  st.button('Erstellen von PDF-Bericht', key='create_pdf_report')
    if should_print_report_botton:
        pdf_fn = 'Bericht_MIP_E-Modul.pdf'
        pp = PdfPages(pdf_fn)
        report_page1 = Report()
        report_page1.add_project_info_MIP_E_Modul(form_title='Abschätzung des E-Moduls von MIP nach DIN EN 12390-13',
                                    project_title='BST\BT')
        report_page1.add_basis_info_MIP_E_Modul()
        report_page1.add_input_and_result_MIP_E_Modul(fmk, fines_content, fm_mittel, E_modul)
        if message is not '':
            report_page1.add_additional_message_MIP_E_Modul(message)

        report_page1.fig.savefig(pp, format='pdf', bbox_inches='tight')
        pp.close()

        with open(pdf_fn, 'rb') as h_pdf:
            st.download_button(
                label="PDF-Datei",
                data=h_pdf,
                file_name=pdf_fn,
                mime="application/pdf",
            )

def get_a_factor(fmk):
    """ Gets a-factor"""
    fmk_min = 4.0
    fmk_max = 12.0
    a_factor_fmk_min = 0.6
    a_factor_fmk_max = 0.75
    a_factor = (a_factor_fmk_max - a_factor_fmk_min) / (fmk_max - fmk_min) * (fmk - fmk_min) + a_factor_fmk_min
    if fmk <= fmk_min:
        a_factor = a_factor_fmk_min
    elif fmk >= fmk_max:
        a_factor = a_factor_fmk_max

    return a_factor

def get_fm_mittel(fm_k):
    """ Gets fm_mittel by searching"""
    fmk_found = False
    counter = 0
    tol = 0.0001

    search_fm_mittel = 0.0 
    decrease_factor = 2.0
    delta_fm = 1.0

    while not fmk_found:
        search_fm_mittel += delta_fm
        trail_fmk = get_a_factor(search_fm_mittel)*search_fm_mittel
        if abs(trail_fmk - fm_k) < tol:
            fmk_found = True
            break
        if trail_fmk > fm_k:
            search_fm_mittel -= delta_fm
            delta_fm = delta_fm/decrease_factor
        counter += 1

    return search_fm_mittel


def calc_E_Modul(fm, fines_content):
    """ Calculates E-Module"""
    if fines_content < 10.0:
        fines_content = 10.0
    E_modul = fm*550.0 + 79005.0 * fines_content**(-0.979)
    return E_modul