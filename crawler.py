from bs4 import BeautifulSoup
import requests
import PIL.ImageChops as ImageChops
from PIL import Image
import mysql.connector
import sys

import crawler_equipe
ANNEE = "2019 - 2020"
 
def date_format(date):

    mois = ["","janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];
    date_split = date.split()
    if (int(date_split[1]) < 10): jour = "0"+date_split[1]
    else : jour = str(date_split[1])

    mois = str(mois.index(date_split[2].lower()))
    if (int(mois) < 10): mois = "0"+mois

    annee = date_split[3]

    return annee+"/"+mois+"/"+jour

def cherche_image (ch):

    chaine = ch.split("\n")
    chaine = chaine[1:len(chaine)-1]
    img = chaine[0].split("-")
    soup = BeautifulSoup(img[0], 'html.parser')
    news_links = soup("img",{'class':'number'})
    score1 = ""
    if (len(news_links) == 0):
        return [None,None]

    for elts in news_links:
        im1 = Image.open(elts["src"])
        for i in range (0,20):
            im2 = Image.open("score/"+str(i)+".png")
            if (im1 == im2):
                score1+=str(i)
                break
    soup = BeautifulSoup(img[1], 'html.parser')
    news_links = soup("img",{'class':'number'})
    score2 = ""
    for elts in news_links:
        im1 = Image.open(elts["src"])
        for i in range (0,20):
            im2 = Image.open("score/"+str(i)+".png")
            if (im1 == im2):
                score2+=str(i)
                break
    
    return [score1, score2]


conn = mysql.connector.connect(host="localhost", user="root", password="ScooterSlider46$", database="parionsamateur")
cursor = conn.cursor()

match = []

soup = BeautifulSoup(open("./"+sys.argv[1]), 'html.parser')

#Sélection des équipes à domicile et à l'extérieur et des numéros de journées
news_links = soup("span",{'class':'eqName'})
cpt = 0
elt=0
for elts in news_links:
    if (elt%2 == 0):
        tab = []
        tab.append(elts.parent.parent.find_previous_sibling("div",{'class':'title_box'}).text.strip().split()[1])
        tab.append(elts.a.text.strip())
    else:
        tab.append(elts.a.text.strip())
        match.append(tab)
        cpt+=1
    elt+=1

#Sélection des score
news_links = soup("span",{'class':'score'})
cpt = 0
elt=0
for elts in news_links:
    if (elts.find("span",{'class':'message'}) != None):
        if (elts.find("span",{'class':'message'}).text != "/"):
            match[cpt].append(-2)
            match[cpt].append(-2)
        else:
            score = cherche_image(str(elts))
            match[cpt].append(score[0])
            match[cpt].append(score[1])
    else:
        score = cherche_image(str(elts))
        match[cpt].append(score[0])
        match[cpt].append(score[1])
    cpt += 1


while (cpt < len(match)):
    match[cpt].append(None)
    match[cpt].append(None)
    cpt += 1

#Sélection des clés étrangères
news_links = soup.find("ul",{'class':'breadcrumb'}).find_all("li")
elt=0
for elem in news_links:
    if(elem.span != None):
        if (elt == 1):
            competition = elem.span.text.strip()
        elif (elt == 2):
            niveau = elem.span.text.strip()
        elif (elt == 3):
            division = elem.span.text.strip()
    elt+=1


#Récupération de la date
news_links = soup("div",{'class':'bloc_result'})
cpt = 0
for elts in news_links:
    date = elts.h4.text.split("-")
    index = division.find('REGIONAL')
    if index == -1: match[cpt].append(date_format(date[1])+date[2])
    else : match[cpt].append(date_format(date[2])+date[3])
    cpt+=1
    

#compétition
req = "SELECT idCompetitions FROM competitions WHERE libelle='"+competition.upper()+"' AND annee='"+ANNEE+"';"
cursor.execute(req)
rows = cursor.fetchall()
idCompetition = rows[0][0]

#division
req = "SELECT idDivisions FROM divisions WHERE libelle='"+division+"';"
cursor.execute(req)
rows = cursor.fetchall()
if (len(rows) == 0):
    req = "INSERT INTO divisions (idDivisions, libelle) VALUES (Null, '"+division+"');"
    cursor.execute(req)
    conn.commit() 
    req = "SELECT idDivisions FROM divisions WHERE libelle='"+division+"';"
    cursor.execute(req)
    rows = cursor.fetchall()

idDivision = rows[0][0]

for m in match:
    journ = m[0]
    dom = m[1]
    ext = m[2]
    if (m[3] == None): scoreDom = -1
    else : scoreDom = m[3]
    if (m[4] == None): scoreExt = -1
    else : scoreExt = m[4]
    date = m[5]

    req = "SELECT idEquipes FROM equipes WHERE libelle = '"+dom+"';"
    cursor.execute(req)
    rows = cursor.fetchall()
    idDom = rows[0][0]

    req = "SELECT idEquipes FROM equipes WHERE libelle = '"+ext+"';"
    cursor.execute(req)
    rows = cursor.fetchall()
    idExt = rows[0][0]

    req = "SELECT idNiveaux FROM niveaux WHERE libelle = '"+niveau+"';"
    cursor.execute(req)
    rows = cursor.fetchall()
    if (len(rows) == 0):
        req = "INSERT INTO niveaux (idNiveaux, libelle) VALUES (Null, '"+niveau+"');"
        cursor.execute(req)
        conn.commit() 
        req = "SELECT idNiveaux FROM niveaux WHERE libelle = '"+niveau+"';"
        cursor.execute(req)
        rows = cursor.fetchall()
    idNiveau = rows[0][0]

    req = "SELECT * FROM matchs WHERE domicile = "+str(idDom)+" AND exterieur = "+str(idExt)+" AND date = '"+date+"';"
    cursor.execute(req)
    rows = cursor.fetchall()
    if (len(rows) == 0):
        req = "INSERT INTO matchs (idMatchs, score_dom, score_ext, cote_dom, cote_ext, cote_nul, date , idCompetitions_COMPETITIONS, journee, idDivisions_DIVISIONS, domicile, exterieur, idNiveaux_NIVEAUX) \
            VALUES (Null, "+str(scoreDom)+","+str(scoreExt)+","+'0'+","+'0'+","+'0'+",'"+date+"',"+str(idCompetition)+","+str(journ)+","+str(idDivision)+","+str(idDom)+","+str(idExt)+","+str(idNiveau)+")"
        cursor.execute(req)
    else:
        req = "UPDATE matchs SET score_dom = "+str(scoreDom)+", score_ext = "+str(scoreExt)+";"
        cursor.execute(req)

    conn.commit()   
            
print(match)
    

        
        