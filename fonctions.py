from scrape import get_data_frame
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time


def show_bs4_scrapping_data(st, nb_page=1):
    st.markdown(f"## Bs4 Scrapping Data ({nb_page} pages)")

    st.markdown(f"### Start scrapping...")

    categories = {
        "chiens": "🐶 Chiens",
        "moutons": "🐑 Moutons",
        "other_animals": "🦔 Autres animaux",
        "volailles": "🐔 Poules, lapins et pigeons",
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
        "./data/chiens.csv": "🐶 Chiens",
        "./data/moutons.csv": "🐑 Moutons",
        "./data/other-animals.csv": "🦔 Autres animaux",
        "./data/volailles.csv": "🐔 Poules, lapins et pigeons",
    }

    for path, title in categories.items():
        st.markdown(f"#### {title}")

        df = pd.read_csv(path)

        st.dataframe(df)


def show_dashboard(st, cat_selected_key, cat_selected_label):

    st.markdown("## Tableau de board")

    st.write(cat_selected_label)

    all_df = generate_dataframe()

    if cat_selected_key == "all":
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 10), dpi=200)

        sns.countplot(x=all_df["article-type"], ax=axes[0])
        axes[0].set_xlabel("Catégorie d'article")
        axes[0].set_ylabel("Nombre d'articles")
        axes[0].set_title("Répartition des articles par catégorie")

        article_counts = all_df["article-type"].value_counts()
        labels = article_counts.index
        sizes = article_counts.values
        axes[1].pie(sizes, labels=labels, autopct='%1.1f%%',
                    startangle=140, colors=sns.color_palette("pastel"))
        axes[1].set_title("Répartition des articles (Cercle)")

        plt.tight_layout(h_pad=2)

        st.pyplot(fig)

    else:
        fig = plt.figure()
        df = all_df[all_df["article-type"] == cat_selected_key]
        sns.histplot(x=df["price"], bins=20)
        plt.xlabel("Catégorie d'article")
        plt.ylabel("Nombre d'articles")
        st.pyplot(fig)


def generate_dataframe():

    vehicules = pd.read_csv("./data-cleaned/vehicules.csv")
    motos = pd.read_csv("./data-cleaned/motos.csv")
    telephones = pd.read_csv("./data-cleaned/telephones.csv")
    locations_vehicules = pd.read_csv("./data-cleaned/locations_vehicules.csv")

    all_df = pd.DataFrame()

    keys = {"vehicules": vehicules, "locations_vehicules": locations_vehicules,
            "telephones": telephones, "motos": motos, }

    for key, df in keys.items():
        new_df = df
        new_df["article-type"] = key
        all_df = pd.concat([all_df, new_df])

    return all_df
