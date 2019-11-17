from bs4 import BeautifulSoup
import requests
import PIL.ImageChops as ImageChops
from PIL import Image
import mysql.connector
import sys
 
conn = mysql.connector.connect(host="localhost", user="root", password="ScooterSlider46$", database="parionsamateur")
cursor = conn.cursor()

equipe = []
soup = BeautifulSoup(open("./"+sys.argv[1]), 'html.parser')
news_links = soup("td",{'class':'blackBold'})
for elt in news_links:
    if (elt.a != None):
        req = "SELECT idEquipes FROM equipes WHERE libelle='"+elt.a.text.strip()+"';"
        cursor.execute(req)
        rows = cursor.fetchall()
        if (len(rows) == 0):
            newEquipe = (None, elt.a.text.strip())
            cursor.execute("INSERT INTO equipes (idEquipes, libelle) VALUES (Null, '"+elt.a.text.strip()+"')")
        conn.commit()     
        equipe.append(elt.a.text.strip())
print(equipe)