from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

base_url = "https://dakarvente.com/index.php?"

params = [
    {
        "id": "2",
        "__category": "vehicules",
        "page": "annonces_rubrique",
        "url_categorie_2": "vehicules",
        "sort": "",
    },
    {
        "id": "3",
        "__category": "motos",
        "page": "annonces_categorie",
        "sort": "",
    },
    {
        "id": "8",
        "__category": "location_vehicule",
        "page": "annonces_categorie",
        "sort": "",
    },
    {
        "id": "32",
        "__category": "telephones",
        "page": "annonces_categorie",
        "sort": "",
    },
]

url_1 = "https://dakarvente.com/annonces-rubrique-vehicules-2.html"
url_2 = " https://dakarvente.com/annonces-categorie-motos-3.html"
url_3 = " https://dakarvente.com/annonces-categorie-location-de-vehicules-8.html"
url_4 = " https://dakarvente.com/annonces-categorie-telephones-32.html"

# marque - price - adresse - image_link


def create_url_list(nb_page, category):
    urls = []

    for param_index, p in enumerate(params):

        if p["__category"] == category:
            for page in range(1, 101):

                param = params[param_index]

                url = base_url + ""
                for key, val in param.items():
                    url += "&" + key + "=" + val

                url += "&" + "nb=" + str(page)
                urls.append(url)
    return urls[:nb_page] if nb_page else urls


def get_page_links(page_url):
    content = requests.get(page_url)
    soup = BeautifulSoup(content.text, "html.parser")

    urls = []
    links = soup.select("div.content-desc > a")
    for a in links:
        try:
            urls.append(a["href"])
        except:
            continue

    return urls


# Pepline de nettoyage
def clean_data(data):
    data_cleaned = data.copy()
    data_cleaned["marque"] = data["marque"].split(":")[-1].strip()
    data_cleaned["adresse"] = data["adresse"].strip()
    data_cleaned["price"] = int(data["price"].strip().split(" ")[
                                0].replace(".", ""))
    data["devise"] = data["price"].strip().split(" ")[-1]

    return data_cleaned


def get_now_article_data(article_link):

    content = requests.get(article_link)
    soup = BeautifulSoup(content.text, "html.parser")

    price = soup.select_one("div.col-info-inner .new-price").getText()
    marque = soup.find("img", attrs={"alt": "marque"}).parent.getText()
    adresse = soup.find("img", attrs={"alt": "localisation"}).parent.getText()
    image_link = soup.select_one(
        "img.block-26-thumbs-img")

    sep = ".com/"

    article_data = {
        "image_link": base_url.split(sep)[0] + sep + image_link["src"] if image_link["src"] else None,
        "adresse": adresse,
        "marque": marque,
        "price": price,
        "article_link": article_link
    }

    data_cleaned = clean_data(article_data)

    return data_cleaned


def get_page_data(nb_page, category):
    print("Start...")

    data_table = []

    # Recuperer toutes les pages contanant les articles
    urls = create_url_list(nb_page=nb_page, category=category)  # 400 pages

    # filtered_urls = []
    # for url in urls:
    #     match = re.search(r"[?&]__category=([^&]*)", url)
    #     category = match.group(1) if match else None
    #     if category:
    #         filtered_urls.append(url)

    articles_link = []

    # pour chaque Page, je recup 1 par 1 les url de chaque article, et les stock dans articles_link
    for url in urls:
        page_link = get_page_links(url)
        for article_link in page_link:
            articles_link.append(article_link)

    # pour chaque lien d'article, je scrappe ces infos, puis mets à jour mon DataFrame
    for index, article_link in enumerate(articles_link):
        try:
            data_row = get_now_article_data(article_link)
            data_table.append(data_row)

        except Exception as e:
            # print("Error", e)
            continue

    print("FINISHED")
    return data_table


def get_data_frame(nb_page=1, category="vehicules"):
    data_table = get_page_data(nb_page, category)
    columns = ["image_link", "adresse", "marque", "price", "article_link"]
    df = pd.DataFrame(columns=columns, data=data_table)
    return df
