#!/bin/bash

python crawler.py Division1_PouleA.html
python crawler.py Division2_PouleA.html
python crawler.py Division2_PouleB.html
python crawler.py Division3_PouleA.html
python crawler.py Division3_PouleB.html
python crawler.py Division3_PouleC.html
python crawler.py Division4_PouleA.html
python crawler.py Division4_PouleB.html

python majBDD.py resultat_Division1_PouleA.json
python majBDD.py resultat_Division2_PouleA.json
python majBDD.py resultat_Division2_PouleB.json
python majBDD.py resultat_Division3_PouleA.json
python majBDD.py resultat_Division3_PouleB.json
python majBDD.py resultat_Division3_PouleC.json
python majBDD.py resultat_Division4_PouleA.json
python majBDD.py resultat_Division4_PouleB.json
