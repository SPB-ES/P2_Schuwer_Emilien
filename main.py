from bs4 import BeautifulSoup as bs
import requests
import csv
import re
from slugify import slugify
import os
from datetime import date
import concurrent.futures
from time import perf_counter

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

# Initialisation du répertoire de résultat de scrapping avec la mention du jour où le script a été éxécuté
# le nom du fichier comprendra la date en cas d'une utilisation par jour pour un suivi précis de l'activité du site ciblé

today = date.today().strftime("%d-%m-%Y") 
# Date du jour au format européen
repertoire = os.getcwd()
repdate = f'{repertoire}\Résultats du {today}'
try:
    os.mkdir(repdate)
    reptravail = os.chdir(repdate)
except:
    reptravail = os.chdir(repdate)

  
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



   
    '''--------------------------------------Version sans sous dossier en Threading ------------------------------'''

    with open (f'{resultat[7]}.csv','a',newline='',encoding="utf-8") as test: # Rempli le CSV crée
        test_writer = csv.writer(test, quoting=csv.QUOTE_ALL)
        test_writer.writerow(resultat)

    img_data = requests.get(resultat[9]).content 
    # Télécharge l'image depuis l'url
    # Mise en place d'une vérification que le titre ne fasse pas plus de 150 caractères (taille limite du titre d'un fichier)

    try:
        with open(f'{resultat[7]} - {resultat[2]}.jpg', 'wb') as handler:
            handler.write(img_data)
    except:
        titre = list()
        compteur = 0
        taillelimite = 149 - (len(resultat[7]) + 3)
        for i in resultat[2]:
            if compteur <= taillelimite:
                titre.append(resultat[2][compteur])
                compteur += 1
            else:
                continue
        titre = ''.join(titre)
        with open(f'{resultat[7]} - {titre}.jpg', 'wb') as handler:
            handler.write(img_data)
    
'''---------------------------------------------------------------------------------------------------------------'''


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
            # nombre de lien résultat pertinent pour les liens de catégories
            # Faiblesse de cette méthode si le nombre de catégorie augmente les prochaines ne seront pas prisent en compte

            cat_url.append([('http://books.toscrape.com/catalogue/category'+((category.get('href'))[2:])),((category.text).replace(' ','').replace('\n',''))]) 
            # Création Liste d'url des catégories avec nom pour afficher une progression de l'éxécution du multithreading
        else:
            break
        a += 1  
    return cat_url

'''---------------------------------------------------------------------------------------------------------------------'''

def recup_url_livre(urlcat):
    """

    Fonction utilisée pour récupérer l'url de chaque livre d'une catégorie donnée
    en tenant compte du nombre de page si plus de 20 livres dans une catégorie

    """
   
    r = requests.get(urlcat[0])
    soup = bs(r.content,'lxml')
    liste_livres = list()

    nombre_livres_categorie = soup.find('form',{'class':'form-horizontal'}).text # Extraction du texte nombre de livre de la catégorie
    nombre_livres_categorie = int(re.findall(r'\d+', nombre_livres_categorie)[0]) # Regex utilsée pour extraire seulement le nombre

    nombres_pages_categorie = nombre_livres_categorie // 20 # Détermine le nombre de page à partir d'un nombre d'article

    if nombre_livres_categorie % 20 > 0:
        nombres_pages_categorie += 1
    
    url_livres = (soup.find_all('h3'))
    taille = len(url_livres)
    completion = 0
    
    for url_livre in url_livres:
        completion += 1
        scrap_produit('http://books.toscrape.com/catalogue/'+ (url_livre.a['href'])[9:])

        print(f'Avancement {urlcat[1]}: {completion} sur {nombre_livres_categorie}')
        
    
    if nombres_pages_categorie > 1:
        
        for num_page in range(2,nombres_pages_categorie + 1):
            url_page = urlcat[0][:-10] + 'page-'+ str(num_page) + '.html'
            r = requests.get(url_page)
            soup = bs(r.content,'lxml')
            url_livres = (soup.find_all('h3'))
            for url_livre in url_livres:
                completion += 1
                scrap_produit('http://books.toscrape.com/catalogue/'+ (url_livre.a['href'])[9:])
                print(f'Avancement {urlcat[1]}: {completion} sur {nombre_livres_categorie}')
                

    nombre_livres_categorie = 0
    url_livres =''

'''--------------------------------------Préparation à l'utilisation du MultiThreading-------------------'''

completion_categorie = 0
taille_categorie = len(recuperer_categorie())

categorie = (recuperer_categorie()) # Création de la liste pour être utilisable en MultiThreading

Start = perf_counter()
with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(recup_url_livre,categorie)
Temps = perf_counter() - Start

print(f'Le script a été exécuté en {round(Temps,0)} secondes')
