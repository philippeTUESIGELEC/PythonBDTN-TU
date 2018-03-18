# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 00:44:15 2018

@author: Philippe TU - BDTN Promotion 2019
1. Créez un notebook "routes.ipynb"


2. Récupérez les informations "Open Data" sur les travaux routiers en
Seine-Maritime
Les métadonnées http://opendata76.blob.core.windows.net/se-deplacer/
CG76_DR_SGDR_DT_METAD.pdf
Les données http://www.opendata-27-76.fr/jeux-de-donnees/
cg76-routes-derniers-travaux/

3. Partie 1 : Chargement et nettoyage
— Téléchargez les données au format CSV
— Chargez les dans une dataframe
— Vérifiez que epaisseurdernierstravaux est bien de type réel.
— Identifiez et nettoyez les valeurs aberrantes. Justifiez votre stratégie
de nettoyage.


4. Partie 2 : Analyse
— Quels sont les 5 natures de travaux les plus fréquentes ?
— Pour chaque année, quel est le nombre de travaux réalisés et l’épaisseur
moyennne ? Triez le résultat par épaisseur descendante.
"""
# importing libraries
import pandas as pd
import numpy as np
import seaborn as sns
import re
#opening file
df = pd.read_csv('C:/Users/user/Desktop/RepositoryTP/PythonBDTN-TU/TP2/CGDRSGDRDTRoutesdernierstravaux.csv',sep=";")
pd.isna(df['epaisseurdernierstravaux']).sum()
#Okay, no Na values, at least no bad data in this dataset.

#1.Check if epaisseurdersnierstravaux is numeric format.
# Let's check if that epaisseurdernierstravaux is a numeric value.
df.dtypes

#It's an object value, let's convert that column into numeric values.
pd.to_numeric(df['epaisseurdernierstravaux'],errors='ignore')
df.dtypes
df.epaisseurdernierstravaux
#Commas will be a problem, python can't convert values with commas. Let's replace them with a dot.
df.epaisseurdernierstravaux = df.epaisseurdernierstravaux.apply(lambda x : x.replace(',','.'))
df.epaisseurdernierstravaux = df.epaisseurdernierstravaux.astype(float)
df.dtypes

# 2.Identify and clean aberrants values, please justify.
df.epaisseurdernierstravaux.describe()
# 9999.99 as max is too high, same for 0. lets delete those values in the column and let's see if that changes those stats
df[df.epaisseurdernierstravaux==min(df.epaisseurdernierstravaux)].count()
df[df.epaisseurdernierstravaux==max(df.epaisseurdernierstravaux)].count()

maxEpaisseur = df.epaisseurdernierstravaux.max()
minEpaisseur = df.epaisseurdernierstravaux.min()
#Dropping max and min values in the dataframe
df.drop(df.epaisseurdernierstravaux != maxEpaisseur)
df.drop(df.epaisseurdernierstravaux == minEpaisseur)

#Thats 246 wrong values. let's delete those as we can't make hypothesis on their real values.
#There are no duplicated rows.
