import mysql.connector
import json
import sys

fichier = sys.argv[1]
#Année en cours
ANNEE = "2019 - 2020"
#Connexion à la base de données
conn = mysql.connector.connect(host="localhost", user="root", password="", database="parionsamateur")
cursor = conn.cursor()
#Lecture du fichier JSON
with open(fichier,"r") as f:
    resultats = json.load(f)
#POur chaque journée
for journ in resultats:
    #POur chaque match
    for match in resultats[journ]:
        #Selection de l'identifiant par rapport au nom
        competition = match["competition"]
        req = "SELECT idCompetitions FROM competitions WHERE libelle='"+competition.upper()+"' AND annee='"+ANNEE+"';"
        cursor.execute(req)
        rows = cursor.fetchall()
        idCompetition = rows[0][0]
        #Selection de l'identifiant par rapport au nom
        division = match["division"]
        req = "SELECT idDivisions FROM divisions WHERE libelle='"+division+"';"
        cursor.execute(req)
        rows = cursor.fetchall()
        #Si elle n'existe pas on l'insert
        if (len(rows) == 0):
            req = "INSERT INTO divisions (idDivisions, libelle) VALUES (Null, '"+division+"');"
            cursor.execute(req)
            conn.commit() 
            req = "SELECT idDivisions FROM divisions WHERE libelle='"+division+"';"
            cursor.execute(req)
            rows = cursor.fetchall()  
        idDivision = rows[0][0]
        
        #Stockage des données du match dans des variables
        dom =  match["domicile"]
        ext = match["exterieur"]
        if (match["scoreDom"] == None): scoreDom = -1
        else : scoreDom = match["scoreDom"]
        if (match["scoreExt"] == None): scoreExt = -1
        else : scoreExt = match["scoreExt"]
        date = match["date"]
        niveau = match["niveau"]
        #Selection de l'identifiant de l'équipe à domicile
        req = "SELECT idEquipes FROM equipes WHERE libelle = '"+dom+"';"
        cursor.execute(req)
        rows = cursor.fetchall()
        idDom = rows[0][0]
        #Selection de l'identifiant de l'équipe à l'exterieur
        req = "SELECT idEquipes FROM equipes WHERE libelle = '"+ext+"';"
        cursor.execute(req)
        rows = cursor.fetchall()
        idExt = rows[0][0]
        #Selecion de l'identifiant du niveau
        req = "SELECT idNiveaux FROM niveaux WHERE libelle = '"+niveau+"';"
        cursor.execute(req)
        rows = cursor.fetchall()
        #Si il n'exsiste pas pas on l'insert
        if (len(rows) == 0):
            req = "INSERT INTO niveaux (idNiveaux, libelle) VALUES (Null, '"+niveau+"');"
            cursor.execute(req)
            conn.commit() 
            req = "SELECT idNiveaux FROM niveaux WHERE libelle = '"+niveau+"';"
            cursor.execute(req)
            rows = cursor.fetchall()
        idNiveau = rows[0][0]

        #Selection du match
        req = "SELECT * FROM matchs WHERE domicile = "+str(idDom)+" AND exterieur = "+str(idExt)+" AND date = '"+date+"';"
        cursor.execute(req)
        rows = cursor.fetchall()
        #Si il n'existe pas on l'insert
        if (len(rows) == 0):
            req = "INSERT INTO matchs (idMatchs, score_dom, score_ext, cote_dom, cote_ext, cote_nul, date , idCompetitions_COMPETITIONS, journee, idDivisions_DIVISIONS, domicile, exterieur, idNiveaux_NIVEAUX) \
                VALUES (Null, "+str(scoreDom)+","+str(scoreExt)+","+'0'+","+'0'+","+'0'+",'"+date+"',"+str(idCompetition)+","+str(journ)+","+str(idDivision)+","+str(idDom)+","+str(idExt)+","+str(idNiveau)+")"
            print(req)
            cursor.execute(req)
        #Sinon on le met à jour
        else:
            req = "UPDATE matchs SET score_dom = "+str(scoreDom)+", score_ext = "+str(scoreExt)+" WHERE domicile = "+str(idDom)+" AND exterieur = "+str(idExt)+" AND date = '"+date+"';"
            print(req)
            cursor.execute(req)

        conn.commit()   
