from bs4 import BeautifulSoup
import requests
import PIL.ImageChops as ImageChops
from PIL import Image
import mysql.connector
import sys

fichier = "./"+sys.argv[1]
#fichier = "./DIVISION3.html"
print ("Traitement du fichier : "+fichier+"\n")

hote = "localhost"
utilisateur = "root"
mdp = ""
bdd = "parionsamateur"

#Connexion à la base de données
conn = mysql.connector.connect(host=hote, user=utilisateur, password=mdp, database=bdd)
cursor = conn.cursor()

print ("### Connexion à la base de données ###\n")
print ("Host : "+hote)
print ("User : "+utilisateur)
print ("Password : "+mdp)
print ("Database : "+bdd+"\n")

equipe = []
print ("######### Listes des équipes #########\n")
#Création de l'objet HTML pour le parser
soup = BeautifulSoup(open(fichier), 'html.parser')
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
        print (elt.a.text.strip())
        equipe.append(elt.a.text.strip())
print ("\n####### Mise à jour réussies #######\n")
