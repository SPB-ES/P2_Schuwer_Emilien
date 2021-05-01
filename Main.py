from bs4 import BeautifulSoup as bs
import requests
import csv
import re
from slugify import slugify
import os

TITRES = [ #liste des entêtes
        'product_page_url',
        'universal_product_code',
        'title',
        'price_including_tax',
        'price_excluding_tax',
        'number_available',
        'product_description',
        'category',
        'review_rating',
        'image_url'
        ] 

repertoire = os.getcwd() 
print(repertoire)
print(os.listdir())
  
def scrap_produit(url):
    """
    Fonction : scrap_produit
    
    Obtenir toutes les informations d'une page produit à partir de l'argument (url)

    Puis les ajouter dans une liste qui s'ajoutera en tant que ligne 
    dans le fichier CSV de la catégorie concernée.
    
    """
    r = requests.get(url)
    soup = bs(r.content,features="lxml")
    resultat = list()

    product_page_url = url
    resultat.append(product_page_url)

    universal_product_code = soup.findAll('td')
    universal_product_code = universal_product_code[0].text
    resultat.append(universal_product_code)

    title = slugify(soup.find('h1').text) # Slugify a été choisi pour éviter les conflits avec les caractères interdits pour nommer un fichier   
    resultat.append(title)

    price_including_tax = soup.findAll('td')
    price_including_tax = price_including_tax[3].text
    resultat.append(price_including_tax.replace('£','')) 
    # Transformer le prix en nombre pour traitement simplifié par le client

    price_excluding_tax = soup.findAll('td')
    price_excluding_tax = price_excluding_tax[2].text
    resultat.append(price_excluding_tax.replace('£',''))
    # Transformer le prix en nombre pour traitement simplifié par le client

    number_available = (soup.find('p',class_="instock availability").text).strip()
    num = re.findall(r'\d+', number_available)
    resultat.append(num[0]) 


    product_description = soup.find_all(re.compile("^p"))
    resultat.append(product_description[3].text)


    category = soup.findAll('a',href = re.compile('category'))
    resultat.append(category[1].text)

    review_rating = soup.find_all('p')[2]
    note_brute = review_rating['class'][1]
    note = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5}
    review_rating = note[note_brute]
    resultat.append(review_rating)


    image_url = soup.find_all('div',{'class':'item active'})
    image_url = image_url[0]
    debut_url_image = 'http://books.toscrape.com/'
    inter_image_url = str(image_url).find('media')
    image_url = (str(image_url)[inter_image_url:-10])
    image_url = debut_url_image + image_url
    resultat.append(image_url)
    with open (f'{resultat[7]}.csv','a',newline='',encoding="utf-8") as test: # Créer le CSV et placer les entêtes
        test_writer = csv.writer(test, quoting=csv.QUOTE_ALL)
        test_writer.writerow(TITRES)
        test_writer.writerow(resultat)
    

    img_data = requests.get(resultat[9]).content #Télécharge l'image depuis l'url
    with open(f'{resultat[2]}.jpg', 'wb') as handler:
        handler.write(img_data)
    



def recuperer_categorie():
    """
    Fonction qui récupère le nom et l'url de chaque catégorie 
    sous format dictionnaire

    """
    re = requests.get('http://books.toscrape.com/catalogue/category/books_1/index.html')
    soup = bs(re.content,'lxml')
    categories = soup.find_all('a',href=True)
    categories = categories[3:]
    a = 0
    cat_name = list()
    taille_categorie = len(cat_name)
    cat_url = list()
    for category in categories:
        if a <=49: 
            # bonne valeur 52
            # nombre de lien résultat pertinent pour les liens de catégories
            # Faiblesse de cette méthode si le nombre de catégorie augmente les prochaines ne seront pas prisent en compte
            cat_name.append((category.text).strip())
            cat_url.append('http://books.toscrape.com/catalogue/category'+((category.get('href'))[2:]))
        else:
            break
        a += 1
    return cat_url



def recup_url_livre(urlcat):
    """

    Fonction utilisée pour récupérer l'url de chaque livre d'une catégorie donnée
    en tenant compte du nombre de page si plus de 20 livres dans une catégorie

    """
   
    r = requests.get(urlcat)
    soup = bs(r.content,'lxml')
    liste_livres = list()

    nombre_livres_categorie = soup.find('form',{'class':'form-horizontal'}).text #Extrait le texte nombre de livre de la catégorie
    nombre_livres_categorie = int(re.findall(r'\d+', nombre_livres_categorie)[0]) #regex utilsée pour extraire seulement le nombre

    nombres_pages_categorie = nombre_livres_categorie // 20 # Détermine le nombre de page à partir d'un nombre d'article

    if nombre_livres_categorie % 20 > 0:
        nombres_pages_categorie += 1
    
    url_livres = (soup.find_all('h3'))
    taille = len(url_livres)
    completion = 0
    for url_livre in url_livres:
        completion += 1
        scrap_produit('http://books.toscrape.com/catalogue/'+ (url_livre.a['href'])[9:])

        print(f'Avancement: {completion} sur {nombre_livres_categorie}')
        print('-----------------------------------------------------------------')
    
    if nombres_pages_categorie > 1:
        
        for num_page in range(2,nombres_pages_categorie + 1):
            url_page = urlcat[:-10] + 'page-'+ str(num_page) + '.html'
            r = requests.get(url_page)
            soup = bs(r.content,'lxml')
            url_livres = (soup.find_all('h3'))
            for url_livre in url_livres:
                completion += 1
                scrap_produit('http://books.toscrape.com/catalogue/'+ (url_livre.a['href'])[9:])
                print(f'Avancement: {completion} sur {nombre_livres_categorie}')

    nombre_livres_categorie = 0
    url_livres =''


completion_categorie = 0
taille_categorie = 0 


# for x in recuperer_categorie():
#         completion_categorie += 1
#         recup_url_livre(x)
#         print(f'Avancement catégorie : {completion_categorie} sur {taille_categorie}')
