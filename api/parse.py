from bs4 import BeautifulSoup

def find_image_by_barcode(barcode):
    url = "https://fr.openfoodfacts.org/produit/" + barcode
    soup = BeautifulSoup(url, "html.parser")
    main_img = soup.find("img", {"id": "og_image"})
    food_name = soup.find("h2", {"property": "food:name"})
    url_img = main_img["src"]
    title = food_name.text
    return url_img, title

