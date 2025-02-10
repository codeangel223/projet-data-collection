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

        sns.countplot(x=all_df["category"], ax=axes[0], palette="hsv")
        axes[0].set_xlabel("Catégorie d'article")
        axes[0].set_ylabel("Nombre d'articles")
        axes[0].set_title("Répartition des articles par catégorie")

        article_counts = all_df["category"].value_counts()
        labels = article_counts.index
        sizes = article_counts.values
        axes[1].pie(sizes, labels=labels, autopct='%1.1f%%',
                    startangle=140, colors=sns.color_palette("pastel"))
        axes[1].set_title("Répartition des animaux (Cercle)")

        plt.tight_layout(h_pad=2)

        st.pyplot(fig)

    else:
        fig = plt.figure(figsize=(16, 12), dpi=200)

        df = all_df[all_df["category"] == cat_selected_key]
        sns.countplot(x=df["price"].value_counts(
            ascending=True),  palette="hsv")
        plt.xlabel("Les prix")
        plt.ylabel("Nombre total")
        plt.tick_params(axis="x", rotation=90)
        plt.title("Les prix en fonction du nombre total d'animaux")

        # villes_ser = df["ville"]
        # labels = villes_ser.value_counts().index
        # values = villes_ser.value_counts().values
        # axes[1].pie(values, labels=labels, autopct="%1.1f%%")

        plt.tight_layout(h_pad=2)
        st.pyplot(fig)


def generate_dataframe():

    chiens = pd.read_csv("./data-cleaned/chiens.csv")
    moutons = pd.read_csv("./data-cleaned/moutons.csv")
    volailles = pd.read_csv("./data-cleaned/volailles.csv")
    other_animals = pd.read_csv("./data-cleaned/other-animals.csv")

    all_df = pd.DataFrame()

    keys = {"chiens": chiens, "moutons": moutons,
            "volailles": volailles, "other_animals": other_animals, }

    for key, df in keys.items():
        new_df = df
        new_df["category"] = key
        all_df = pd.concat([all_df, new_df])

    return all_df
