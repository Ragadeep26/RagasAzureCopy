import sys
import streamlit as st
from Reinforcement_helper import main_reinforced_concrete_helper

st.set_page_config(page_title='Piles & panels', layout="wide", page_icon="⚙️")


if __name__ == '__main__':
    # Sidebar
    st.sidebar.markdown('# Form selection')
    select_options = ['Concrete_helper']
    select_event = st.sidebar.selectbox('Select one of the forms', select_options, key='selected_form', index=0)

    if select_event == 'Concrete_helper':
        main_reinforced_concrete_helper(st)
