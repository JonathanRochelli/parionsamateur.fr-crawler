from bs4 import BeautifulSoup
from unidecode import unidecode
import PIL.ImageChops as ImageChops
from PIL import Image
import mysql.connector
import json
import sys


fichier = "./"+sys.argv[1]
#fichier = "./DIVISION3.html"

# -*- coding: utf-8 -*-
import crawler_equipe

#Fonction permettante de changer le format de date de Dimanche 8 Septembre 2019 en 2019/09/08
def date_format(date):
    #Tableau de mois
    mois = ["","janvier","fa(c)vrier","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","da(c)cembre"];
    #Découpe de la chaîne de caractère
    date_split = date.split()
    #Stockage du jour
    jour = str(date_split[1])
    #Ajustement du jour : si il est inférieur à 10 ajouter un 0
    if (int(date_split[1]) < 10): jour = "0"+jour
    #Selection du mois par rapport à son numéro on connaît l'indice du tableau
    mois = str(mois.index(unidecode(date_split[2].lower())))
    #Ajustement du jour : si il est inférieur à 10 ajouter un 0
    if (int(mois) < 10): mois = "0"+mois
    #Stockage de l'année
    annee = date_split[3]
    #Retourne le format que l'on souhaite
    return annee+"/"+mois+"/"+jour

#Permet de trouver l'image qui correspond par rapport à la banque d'image (comparaison d'image)
def compare_image (indice, img):
    #Initisalisation
    score = ""
    #Création d'un objet HTML
    soup = BeautifulSoup(img[indice], 'html.parser')
    #Selection de la balise img
    news_links = soup("img",{'class':'number'})
    #Si il n'y en a pas retourn None
    if (len(news_links) == 0):
        return None
    #Pour chaque balise (score à domicile à plusieurs chiffres et score à l'exterieur)
    for elts in news_links:
        #Ouverture de l'image
        im1 = Image.open(elts["src"])
        #COnparaison avec toutes les images du répertoire
        for i in range (0,20):
            im2 = Image.open("score/"+str(i)+".png")
            #Si c'est las même on retourne le nom
            if (im1 == im2):
                return str(i)
    #Si pas trouvé retourn -1
    return -1 
    
#Traite la chaîne de caractère avant la comparaison
def cherche_image (ch):
    #Découpage par rapport au retour à la ligne
    chaine = ch.split("\n")
    #On ne prend pas le permier et le dernier caractère
    chaine = chaine[1:len(chaine)-1]
    #Découpage par rapport au tiret qui représente la jonction entre le score à domicile et celui exterieur
    img = chaine[0].split("-")
    #Comparaison de l'image pour le score à domicil
    score1 = compare_image (0, img)
    #Si la score à domicile est à None -> pas de score (reporté ou pas encore joué)
    if (score1 == None): return [None, None]
    #Affichage de l'erreur si une image est manquante
    if (score1 == -1) : print ("\n\n\n !!!!!!!!!!!!!!!!!!! Une image est manquante pour le score à domicile !!!!!!!!!!!!!!!!!!! \n\n\n")
    #Comparaison de l'image pour le score à l'extérieur
    score2 = compare_image (1, img)
    if (score2 == -1) : print ("\n\n\n !!!!!!!!!!!!!!!!!!! Une image est manquante pour le score à domicile !!!!!!!!!!!!!!!!!!! \n\n\n")
    #Retourne sous forme de tableau
    return [score1, score2]

print ("######## Lancement du crawler ########\n")
#Initialisation du document HTML pour le parser
soup = BeautifulSoup(open(fichier), 'html.parser')
#Sélection de la compétition et du niveau
news_links = soup.find("ul",{'class':'breadcrumb'}).find_all("li")
#Initialisation du numéro d'élement
elt=0
#Pour chaque li
for elem in news_links:
    #Si la span existe
    if(elem.span != None):
        #Et que c'est le deuxième (ca commence à 0)
        if (elt == 1):
            #C'est la compétition
            competition = elem.span.text.strip()
        #Si c'est le troisième
        elif (elt == 2):
            #C'est le niveau
            niveau = elem.span.text.strip()
    elt+=1

print ("############ Compétition #############")
print (competition+"\n")
print ("############### Niveau ###############")
print (niveau+"\n")
#Sélection de la poule
news_links = soup.find("div",{'id':'newcms-block-1618'})
#Si ca existe (il existe des championnats sans poule
if (news_links == None):
    poule = None
else:
    poule = news_links.text
print ("############### Poule ################")
print (str(poule)+"\n")

match = []
resultats = {}

print ("############# Les matchs #############\n")
#Sélection des informations d'un match
news_links = soup.find("div",{'class':'list-result'})
#Tous les elements de type div
children = news_links.findChildren("div")
#Pour chaques elements
for child in children:
    #Si la classe est title_boc
    if (child['class'][0] == "title_box"):
        #C'est la journée
        journee = child.text.strip().split(" ")[-1]
        print ("############## Journée "+journee+" #############\n")
        #Nouvalle journée pour le json
        resultats[journee] = []
    #Sinon c'est un match
    elif (child['class'][0] == "toshow"):
        #Initialisation du match
        match = {}
        #Selection de la date, l'heure et la division , séparées par des tirets
        infos_generales = child.find("h4").text.split(" - ")
        division = infos_generales[0]
        date = date_format(infos_generales[1])
        heure = infos_generales[2]
        #Selection du score en comparant les images
        score = cherche_image(str(child.find('p').find("span", {'class':'score'})))
        #L'équipe à domicile
        dom = child.find("p").find("span", {'class' : 'eqleft'}).find('a').text
        #L'équipe à  l'exterieur
        ext = child.find("p").find("span", {'class' : 'eqright'}).find('a').text
        #Stockage des informations
        match["competition"] = competition
        match["niveau"] = niveau
        match["poule"] = poule
        match["division"]= division
        match["date"] = date
        match["heure"] = heure
        match["domicile"] = dom
        match["exterieur"] = ext
        match["scoreDom"] = score[0]
        match["scoreExt"]=score[1]
        print(str(match)+"\n")
        #Ajout du match
        resultats[journee].append(match)

#Enregistrement dans le fichier JSON
with open("resultat_"+sys.argv[1].split(".")[0]+".json", "w") as f:
    json.dump(resultats, f, indent=4)




            
