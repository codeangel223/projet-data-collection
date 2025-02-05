from scrape import get_data_frame
import pandas as pd
import time


def show_bs4_scrapping_data(st, nb_page=1):
    st.markdown(f"## Bs4 Scrapping Data ({nb_page} pages)")

    st.markdown(f"### Start scrapping...")

    categories = {
        "vehicules": "🚗 Véhicules",
        "motos": "🏍️ Motos",
        "location_vehicule": "🚕 Locations de véhicules",
        "telephones": "📱 Téléphones",
    }

    for key, title in categories.items():
        st.markdown(f"#### {title}")
        status = st.empty()
        status.markdown("⏳ En cours...")

        df = get_data_frame(nb_page, key)
        time.sleep(1)

        status.markdown("✅ OK")
        st.dataframe(df)

    st.markdown(f"### ✅ Fin de scrapping")


def show_webscrapper_data(st):
    st.markdown("## Web Scrapper")

    categories = {
        "./data/vehicules.csv": "🚗 Véhicules",
        "./data/motos.csv": "🏍️ Motos",
        "./data/locations-vehicules.csv": "🚕 Locations de véhicules",
        "./data/telephones.csv": "📱 Téléphones",
    }

    for path, title in categories.items():
        st.markdown(f"#### {title}")

        # df = pd.read_csv(path)

        # st.dataframe(df)


def show_dashboard(st):
    st.markdown("## Tableau de board")
