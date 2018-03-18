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
from collections import Counter
#opening file
df = pd.read_csv('C:/Users/user/Desktop/RepositoryTP/PythonBDTN-TU/TP2/CGDRSGDRDTRoutesdernierstravaux.csv',sep=";")
pd.isna(df['epaisseurdernierstravaux']).sum()
#Okay, no Na values.

#Part 1 : 

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
sns.kdeplot(df['epaisseurdernierstravaux'])
# 9999.99 as max is too high, same for 0. lets delete those values in the column and let's see if that changes those stats
df[df.epaisseurdernierstravaux==min(df.epaisseurdernierstravaux)].count()
df[df.epaisseurdernierstravaux==max(df.epaisseurdernierstravaux)].count()

#Thats 246 wrong values. let's delete those as they are absurd values.
min(df.epaisseurdernierstravaux)
max(df.epaisseurdernierstravaux)
maxEpaisseur = df.epaisseurdernierstravaux.max()
minEpaisseur = df.epaisseurdernierstravaux.min()
#Dropping max and min values in the dataframe
df = df.loc[df['epaisseurdernierstravaux']!= maxEpaisseur]
df = df.loc[df['epaisseurdernierstravaux']!= minEpaisseur]

#There are no duplicated rows.
sns.kdeplot(df['epaisseurdernierstravaux'])
min(df.epaisseurdernierstravaux)
max(df.epaisseurdernierstravaux)

#That's better now, let's check stats now.
df.describe()

#Now let's clean other columns, age has 0 values, we can drop this column.
df = df.drop(['age'],axis=1)


# Part 2 : what are the 5 most kind of construction.
df.dtypes
#anneedernierstravaux is an object type, let's change it to string value, count and finally plot.
df['naturedernierstravaux'] = df['naturedernierstravaux'].astype(str)
construction_kind_list = df['naturedernierstravaux']
most_kinds_construction = pd.DataFrame(Counter(construction_kind_list).most_common(5))
# Now let's plot
most_kinds_construction.plot.bar(x=0,rot=0,title='The 5 most kind of construction')

# Here we have the 5 most kind of construction in the dataset.
# For each year, what's the number of construction made and the mean thickness ? 

#Number of construction each year : 
construction_year_list = df['anneedernierstravaux']
number_construction_year = pd.DataFrame.from_dict(Counter(construction_year_list),orient='index').reset_index()
number_construction_year.plot.barh(x='index',rot=0,title='Construction per year',fontsize=5)

#Mean thickness per year.
mean_thickness_year = df.groupby(['anneedernierstravaux'],as_index=False).mean()
mean_thickness_year = mean_thickness_year.sort_values(by='epaisseurdernierstravaux',ascending=False)
mean_thickness_year = mean_thickness_year[['anneedernierstravaux','epaisseurdernierstravaux']]
mean_thickness_year.plot.barh(x='anneedernierstravaux',rot=0,title='Construction per year',fontsize=5)

# It seems that thickness diminished through time. Maybe quality of the product has increased, that is curious.