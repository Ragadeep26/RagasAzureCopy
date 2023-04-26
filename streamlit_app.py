import sys
import streamlit as st
from Reinforcement_helper import main_reinforced_concrete_helper

st.set_page_config(page_title='Ragatries', layout="wide", page_icon="⚙️")


if __name__ == '__main__':
    main_reinforced_concrete_helper(st)
