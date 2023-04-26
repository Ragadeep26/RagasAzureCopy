import sys
import streamlit as st
import numpy as np
import matplotlib as mpl

st.set_page_config(page_title='Developer_Raga_Copy', layout="wide", page_icon="⚙️")
from src.main_co2_calculator import main_CO2_calculator

if __name__ == '__main__':
    main_CO2_calculator(st, parameters=None)


    #version notes

    st.sidebar.header('developernotes')
    st.sidebar.write('A Beta version of CO2 calculator which combines both with and without steel profiles')