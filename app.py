import streamlit as st
from fonctions import *

st.set_page_config(
    page_title="Moussa MALLE - Data Collection Project - Dakar Auto Project - DIT")

st.title("Moussa MALLE - Data Collection Project - Dakar Auto Project - DIT")


if st.button("Ressources"):
    st.switch_page("pages/ressources.py")


# Side Bar
st.sidebar.markdown("## Menu de control")
nb_page = int(st.sidebar.number_input(
    'Sélectionnez le nombre de page ?', step=1, min_value=1, max_value=5))

if st.sidebar.button("Bs4/Selenium"):
    show_bs4_scrapping_data(st, nb_page)

if st.sidebar.button("Web scrapper"):
    show_webscrapper_data(st)

if st.sidebar.button("Dashboard"):
    show_dashboard(st)

if st.sidebar.button("Evaluer le projet"):
    st.write('<iframe src="https://ee.kobotoolbox.org/i/xnuAwepx" width="800" height="600"></iframe>',
             unsafe_allow_html=True)
