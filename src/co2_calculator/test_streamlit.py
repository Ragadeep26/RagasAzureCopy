# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 09:54:21 2022

@author: nya
"""
import streamlit as st
import numpy as np

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

   st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

   # expander
   with st.expander("See explanation", expanded=True):
       st.write("""
           The chart above shows some numbers I picked for you.
           I rolled actual dice for these, so they're *guaranteed* to
           be random.
       """)
       st.image("https://static.streamlit.io/examples/dice.jpg")

   # container
   with st.container():
      st.write("This is inside the container")

      # You can call any Streamlit command, including custom components:
      st.bar_chart(np.random.randn(50, 3))

   st.write("This is outside the container")

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)