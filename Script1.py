from bs4 import BeautifulSoup as bs
import requests
import csv
import re

# with open('test.csv', mode='r') as csvfile:

#     # writer = csv.writer(csvfile)
#     # writer.writerow(listdeux)
#     csv_reader = csv.reader(csvfile, delimiter=',')

#     with open('new_teeeeeeest.csv','w') as new_file:
#         csv_writer=csv.writer(new_file,delimiter=';')

#         for row in csv_reader:
#             csv_writer.writerow(line)

#     # print(reader)

liste=[1,2,3,4,5,6,7,8,9,7,10]
liste2=['a','b','c','rerer','gfdgrtr','a','b','c','adadadad']
liste3=["a",'c','d','e','d'',e','f','t','f','eeeeeeeee','eeeeeeeeeee']
dicttest={'Books to Scrape': 'http://books.toscrape.com/catalogue/category/../../index.html', 'Home': 'http://books.toscrape.com/catalogue/category/../../index.html', 'Books': 'http://books.toscrape.com/catalogue/categorydex.html', 'Travel': 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html', 'Mystery': 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html', 'Historical Fiction': 'http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html', 'Sequential Art': 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html', 'Classics': 'http://books.toscrape.com/catalogue/category/books/classics_6/index.html', 'Philosophy': 'http://books.toscrape.com/catalogue/category/books/philosophy_7/index.html', 'Romance': 'http://books.toscrape.com/catalogue/category/books/romance_8/index.html', 'Womens Fiction': 'http://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html', 'Fiction': 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html', 'Childrens': 'http://books.toscrape.com/catalogue/category/books/childrens_11/index.html', 'Religion': 'http://books.toscrape.com/catalogue/category/books/religion_12/index.html', 'Nonfiction': 'http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html', 'Music': 'http://books.toscrape.com/catalogue/category/books/music_14/index.html', 'Default': 'http://books.toscrape.com/catalogue/category/books/default_15/index.html', 'Science Fiction': 'http://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html', 'Sports and Games': 'http://books.toscrape.com/catalogue/category/books/sports-and-games_17/index.html', 'Add a comment': 'http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html', 'Fantasy': 'http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html', 'New Adult': 'http://books.toscrape.com/catalogue/category/books/new-adult_20/index.html', 'Young Adult': 'http://books.toscrape.com/catalogue/category/books/young-adult_21/index.html', 'Science': 'http://books.toscrape.com/catalogue/category/books/science_22/index.html', 'Poetry': 'http://books.toscrape.com/catalogue/category/books/poetry_23/index.html', 'Paranormal': 'http://books.toscrape.com/catalogue/category/books/paranormal_24/index.html', 'Art': 'http://books.toscrape.com/catalogue/category/books/art_25/index.html', 'Psychology': 'http://books.toscrape.com/catalogue/category/books/psychology_26/index.html', 'Autobiography': 'http://books.toscrape.com/catalogue/category/books/autobiography_27/index.html', 'Parenting': 'http://books.toscrape.com/catalogue/category/books/parenting_28/index.html', 'Adult Fiction': 'http://books.toscrape.com/catalogue/category/books/adult-fiction_29/index.html', 'Humor': 'http://books.toscrape.com/catalogue/category/books/humor_30/index.html', 'Horror': 'http://books.toscrape.com/catalogue/category/books/horror_31/index.html', 'History': 'http://books.toscrape.com/catalogue/category/books/history_32/index.html', 'Food and Drink': 'http://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html', 'Christian Fiction': 'http://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html', 'Business': 'http://books.toscrape.com/catalogue/category/books/business_35/index.html', 'Biography': 'http://books.toscrape.com/catalogue/category/books/biography_36/index.html', 'Thriller': 'http://books.toscrape.com/catalogue/category/books/thriller_37/index.html', 'Contemporary': 'http://books.toscrape.com/catalogue/category/books/contemporary_38/index.html', 'Spirituality': 'http://books.toscrape.com/catalogue/category/books/spirituality_39/index.html', 'Academic': 'http://books.toscrape.com/catalogue/category/books/academic_40/index.html', 'Self Help': 'http://books.toscrape.com/catalogue/category/books/self-help_41/index.html', 'Historical': 'http://books.toscrape.com/catalogue/category/books/historical_42/index.html', 'Christian': 'http://books.toscrape.com/catalogue/category/books/christian_43/index.html', 'Suspense': 'http://books.toscrape.com/catalogue/category/books/suspense_44/index.html', 'Short Stories': 'http://books.toscrape.com/catalogue/category/books/short-stories_45/index.html', 'Novels': 'http://books.toscrape.com/catalogue/category/books/novels_46/index.html', 'Health': 'http://books.toscrape.com/catalogue/category/books/health_47/index.html', 'Politics': 'http://books.toscrape.com/catalogue/category/books/politics_48/index.html', 'Cultural': 'http://books.toscrape.com/catalogue/category/books/cultural_49/index.html', 'Erotica': 'http://books.toscrape.com/catalogue/category/books/erotica_50/index.html', 'Crime': 'http://books.toscrape.com/catalogue/category/books/crime_51/index.html'}

with open ('test2.csv','w',newline='') as test: # Créer le CSV et placer les entêtes
    test_writer = csv.writer(test, quoting=csv.QUOTE_ALL)
    test_writer.writerow(liste)
    test_writer.writerow(liste2)
    test_writer.writerow(liste3)

# with open ('test2.csv','w',newline='') as test: # Créer le CSV et placer les entêtes
#     test_writer = csv.writer(test, quoting=csv.QUOTE_ALL)
#     test_writer.writerow(liste2)

# with open ('test2.csv','w',newline='') as test: # Créer le CSV et placer les entêtes
#     test_writer = csv.writer(test, quoting=csv.QUOTE_ALL)
#     test_writer.writerow(liste3)

print(dicttest(0))