import sys
import streamlit as st
import numpy as np
import matplotlib as mpl
from src.main_MIP_E_Modul import main_MIP_E_Modul
from src.main_co2_calculator import main_CO2_calculator
from src.main_co2_calculator_EPD import main_CO2_calculator_EPD
#from PIL import Image
from src.main_secant_piled_shaft import main_secant_piled_shaft
from src.main_secant_piled_wall import main_secant_piled_wall
from src.main_diaphragm_panel_shaft import main_diaphragm_panel_shaft
from src.main_diaphragm_panel_wall import main_diaphragm_panel_wall
from src.main_micropile_buckling import main_micropile_buckling
from src.main_duki_buckling import main_duki_buckling
from src.main_dim_cross_section_rectangular import main_dim_cross_section as main_dim_cross_section_rect
from src.main_dim_cross_section_circular import main_dim_cross_section as main_dim_cross_section_circ
from src.main_reinforced_concrete_helper import main_reinforced_concrete_helper
from src.main_revit_dynamo_resources import main_revit_dynamo_resources
from src.main_about import main_about
#img = Image.open("favicon.ico")
#st.set_page_config(page_title='Piles & panels', layout="wide", page_icon=":eyeglasses:")
st.set_page_config(page_title='Piles & panels', layout="wide", page_icon="⚙️")


if __name__ == '__main__':
    # Sidebar
    st.sidebar.markdown('# Form selection')
    select_options = ['MIP E-Modul', 'CO2 Evaluator', 'CO2 Evaluator EPD Test', 'Secant piled shaft', 'Secant piled wall', 'Diaphragm panel shaft', 'Diaphragm panel wall', 'Duki-pile buckling',
                    'Micropile buckling', 'Concrete reinforcement rect. section', 'Concrete reinforcement circ. section',
                    'Reinforced concrete helper', 'Revit/ Dynamo/ Generative design resources', 'About & known issues' ]

    select_event = st.sidebar.selectbox('Select one of the forms', select_options, key='selected_form', index=0)

    if select_event == 'Secant piled shaft':
        main_secant_piled_shaft(st)

    elif select_event == 'Secant piled wall':
        main_secant_piled_wall(st)

    elif select_event == 'Diaphragm panel shaft':
        main_diaphragm_panel_shaft(st)

    elif select_event == 'Diaphragm panel wall':
        main_diaphragm_panel_wall(st)
    
    elif select_event == 'Micropile buckling':
        main_micropile_buckling(st)

    elif select_event == 'Duki-pile buckling':
        main_duki_buckling(st)

    elif select_event == 'Concrete reinforcement rect. section':
        main_dim_cross_section_rect(st)

    elif select_event == 'Concrete reinforcement circ. section':
        main_dim_cross_section_circ(st)

    elif select_event == 'Reinforced concrete helper':
        main_reinforced_concrete_helper(st)

    elif select_event == 'Revit/ Dynamo/ Generative design resources':
        main_revit_dynamo_resources(st)

    elif select_event == 'About & known issues':
        main_about(st)

    elif select_event == 'MIP E-Modul':
        main_MIP_E_Modul(st)

    elif select_event == 'CO2 Evaluator':
        main_CO2_calculator(st, parameters=None)

    elif select_event == 'CO2 Evaluator EPD Test':
        main_CO2_calculator_EPD(st, parameters=None)

    else:
        pass


    # Version notes
    st.sidebar.header('Version and used packages')
    st.sidebar.write('piles&panels=nya.11.2022')
    st.sidebar.write('python=' + sys.version[:6] + ', streamlit=' + st.__version__)
    st.sidebar.write('numpy=' + np.__version__ + ', matplotlib=' + mpl.__version__)


    st.sidebar.header('Development notes')
    st.sidebar.write("""Code devopment is based on Python with continuous integration deployed on Microsoft Azure Web Apps.
    Information about the implemented calculation methods and procedures is provided as much as possible.
    As of now, printing PDF report is only available for the forms MIP E-Modul and CO2 Evaluator.
    """)

    st.sidebar.header('Contact')
    st.sidebar.write('BST-GBT-BK\Ragadeep Bojja')
    st.sidebar.write('ragadeep.bojja@bauer.de')