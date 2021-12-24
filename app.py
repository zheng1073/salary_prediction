import streamlit as st
from prediction_scene import show_prediction_scene
from data_scene import show_data_scene

#
page_selected = st.sidebar.selectbox("Salary Prediction", ("Main Page", "Explore Data"))

if page_selected == "Main Page":
    # launch the main page; the main page will be the page where users can generate a predicted salary amount
    show_prediction_scene()
else:
    show_data_scene()