from bs4 import BeautifulSoup
import requests
import PIL.ImageChops as ImageChops
from PIL import Image
import mysql.connector
import sys

#Connexion à la base de données
conn = mysql.connector.connect(host="localhost", user="root", password="", database="parionsamateur")
cursor = conn.cursor()

equipe = []
#Création de l'objet HTML pour le parser
soup = BeautifulSoup(open("./DIVISION3.html"), 'html.parser')
#Selection des tds
news_links = soup("td",{'class':'blackBold'})
#POur chaque td
for elt in news_links:
    #Si il possède un a
    if (elt.a != None):
        #Selection de l'identifiant par rapport au nom
        req = "SELECT idEquipes FROM equipes WHERE libelle='"+elt.a.text.strip()+"';"
        cursor.execute(req)
        rows = cursor.fetchall()
        #Si elle n'existe pas en l'insert
        if (len(rows) == 0):
            newEquipe = (None, elt.a.text.strip())
            cursor.execute("INSERT INTO equipes (idEquipes, libelle) VALUES (Null, '"+elt.a.text.strip()+"')")
        conn.commit()     
        equipe.append(elt.a.text.strip())
print(equipe)
