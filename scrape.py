from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

base_url = "https://sn.coinafrique.com"
category_base_path = "/categorie"
paths = {
    "chiens": "/chiens",
    'moutons': "/moutons",
    "other_animals": "/autres-animaux",
    "volailles": "/poules-lapins-et-pigeons",
}

# name - price - adresse - article_link
initial_columns = ["name", "price", "adresse",
                   "price", "article_link", "image_link_src"]
new_columns = ["name", "price", "devise", "quartier", "ville",
               "pays", "adresse", "article_link", "image_link_src"]


def create_url_list(nb_page, category, numero_page=None):

    urls = []

    if numero_page:
        return [f"{base_url}{category_base_path}{value}?page={numero_page}"]

    for key, value in paths.items():

        if key == category:
            for page in range(1, nb_page+1):

                url = f"{base_url}{category_base_path}{value}?page={page}"
                urls.append(url)
    return urls


def get_page_links(page_url):
    content = requests.get(page_url)
    soup = BeautifulSoup(content.text, "html.parser")

    urls = []
    links = soup.select(".ad__card-description a")
    for a in links:
        try:
            urls.append(base_url + a["href"])
        except:
            continue

    return urls


# Pepline de nettoyage
def clean_data(data):
    data_cleaned = data.copy()
    data_cleaned["adresse"] = data["adresse"].strip()

    # features created
    data_cleaned["pays"] = data["adresse"].split(",")[-1]
    data_cleaned["ville"] = data["adresse"].split(",")[1]
    data_cleaned["quartier"] = data["adresse"].split(",")[0]

    # Transform Prix
    try:
        data_cleaned["price"] = int("".join(data["price"].split(" ")[:-1]))
        data_cleaned["devise"] = data["price"].strip().split(" ")[-1]
    except:
        data_cleaned["price"] = "Prix sur demande" if data["price"] == "Sur demande" else None
        data_cleaned["devise"] = None
    return data_cleaned


def get_now_article_data(article_link):

    content = requests.get(article_link)
    soup = BeautifulSoup(content.text, "html.parser")

    name = soup.select_one(".hide-on-med-and-down h1").getText()
    price = soup.select_one(".hide-on-med-and-down p.price").getText()
    adresse = soup.select_one(
        ".hide-on-med-and-down [data-address] span").getText()
    image_link_src = None

    image_div = soup.find('div', class_='swiper-slide')
    if image_div and 'style' in image_div.attrs:
        style = image_div['style']
        match = re.search(r'background-image:\s*url\((.*?)\)', style)
        if match:
            image_link_src = match.group(1).strip("'\"")

    sep = ".com/"

    article_data = {
        "name": name,
        "price": price,
        "adresse": adresse,
        "image_link_src": image_link_src,
        "article_link": article_link
    }
    # return article_data
    data_cleaned = clean_data(article_data)

    return data_cleaned


def get_all_items_data_for_category(nb_page, category, numero_page):
    print("Start...")

    data_table = []

    # Recuperer toutes les pages contanant les articles
    urls = create_url_list(nb_page=nb_page, category=category,
                           numero_page=numero_page)  # 40 pages

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
            print("Error", e)
            continue

    print("FINISHED")
    return data_table


def get_data_frame(nb_page=1, category="chiens", numero_page=None):
    data_table = get_all_items_data_for_category(
        nb_page, category, numero_page)
    df = pd.DataFrame(columns=new_columns, data=data_table)
    return df


# get_data_frame()
