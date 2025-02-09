import streamlit as st
from fonctions import *

st.set_page_config(
    page_title="Moussa MALLE - Data Collection Project - Dakar Auto Project - DIT")

st.title("Moussa MALLE - Data Collection Project - Dakar Auto Project - DIT")


if st.button("Ressources"):
    st.session_state.dashboard_clicked = False
    st.switch_page("pages/ressources.py")


# Side Bar
st.sidebar.markdown("## Menu de control")
nb_page = int(st.sidebar.number_input(
    'Sélectionnez le nombre de page ?', step=1, min_value=1, max_value=5))

if st.sidebar.button("Bs4/Selenium"):
    st.session_state.dashboard_clicked = False
    show_bs4_scrapping_data(st, nb_page)

if st.sidebar.button("Web scrapper"):
    st.session_state.dashboard_clicked = False
    show_webscrapper_data(st)

if "dashboard_clicked" not in st.session_state:
    st.session_state.dashboard_clicked = False

if st.sidebar.button("Dashboard"):
    st.session_state.dashboard_clicked = True

if st.session_state.dashboard_clicked:

    categories = {
        "all": "Vue d'ensemble",
        "chiens": "🐶 Chiens",
        "moutons": "🐑 Moutons",
        "other_animals": "🦔 Autres animaux",
        "volailles": "🐔 Poules, lapins et pigeons",
    }

    cat_selected_label = st.selectbox(
        "Sélectionnez une catégorie d'article", list(categories.values()))

    cat_selected_key = [
        key for key, value in categories.items() if value == cat_selected_label][0]

    show_dashboard(st, cat_selected_key, cat_selected_label)

if st.sidebar.button("Evaluer le projet"):
    st.session_state.dashboard_clicked = False
    st.write('<iframe src="https://ee.kobotoolbox.org/i/xnuAwepx" width="800" height="600"></iframe>',
             unsafe_allow_html=True)
