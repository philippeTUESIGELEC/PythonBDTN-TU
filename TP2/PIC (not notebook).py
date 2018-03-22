# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 23:49:17 2018

@author: Philippe TU

1. Créez une série dont, pour chaque ligne :
l’index est un code pour chaque dominante de l’Esigelec
la valeur est le nom complet de la dominante
2. Ajoutez une colonne avec le département auquel chaque dominante appartient.
3. Créez une dataframe contenant le nom, prénom et code de dominante
pour chaque participant à l’activité.
4. Créez une dataframe contenant le pourcentage d’élèves par département
pour l’activité.
5. Enregistrez le résultat dans un fichier csv
"""

# Importing libraries

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib as mt

department_distrib =  pd.Series(['TIC','TIC','TIC','TIC','TIC','GEE','GEE','GEE','GEE','SEI','SEI','SEI','SEI','ET','ET'])
spe_name =pd.Series(['Architecture et securite des reseaux','Big Data pour la Transformation Numerique','Ingenieur d\'affaire-Ingenieur Reseaux','Ingenierie des Services du Numerique','Ingenieur Finance','Automatique et Robotique Industrielle','Energie et Développement Durable','Genie Électrique et Transport','Ingénieur d’Affaires : Distribution Energie et Signaux','Mécatronique Genie Electrique','Ingenierie des Systèmes Embarques : Vehicule Autonome','Ingenierie des Systèmes Embarques : Objets Communicants','Ingenierie des Systemes Medicaux','Electronique des Systemes pour l’Automobile et l’Aeronautique','Ingenierie Telecom'])
acro_spe_name = pd.Series(['ASR','BDTN','IA-IR','ISN','IF','ARI','EDD','GET','IA-DES','MCTGE','ISE-VA','ISE-OC','ISYMED','ESAA','ICOM'])
# Series in which we find specializations.
df1 = spe_name
df1.index=('ASR','BDTN','IA-IR','ISN','IF','ARI','EDD','GET','IA-DES','MCTGE','ISE-VA','ISE-OC','ISYMED','ESAA','ICOM')
df1.columns=['index','nom']
# Add a column with the name of department of each specialization
df2 = department_distrib
df2 = pd.Series(['TIC','TIC','TIC','TIC','TIC','GEE','GEE','GEE','GEE','SEI','SEI','SEI','SEI','ET','ET'])
df2.index = ('ASR','BDTN','IA-IR','ISN','IF','ARI','EDD','GET','IA-DES','MCTGE','ISE-VA','ISE-OC','ISYMED','ESAA','ICOM')
df3 = pd.concat([df1,df2],axis=1)


#Create a DataFrame with last name, first name and specialization code for each participant
first_name = pd.Series(['Lilian','Remi','Marian','Mathias','Jules','Edmond','Germain','Denis','Germain','Denis','Camille','Jules'])
last_name = pd.Series(['Gauthier','Lecocq','Pasquier','Hauet','Ballouhey','Delafosse','Hébras','Bourbeau','Garreau','Couturier','Delcroix','Philidor'])
specialization = pd.Series(['ASR','BDTN','ARI','EDD','GET','MCTGE','ISE-VA','ESAA','ICOM','BDTN','ARI','ESAA'])
depart_participants = pd.Series(['TIC','TIC','GEE','GEE','GEE','SEI','SEI','ET','ET','TIC','GEE','ET'])
participants = pd.concat([first_name,last_name],axis=1)
participants = pd.concat([participants,specialization],axis=1)
participants = pd.concat([participants,depart_participants],axis=1)
participants.columns = ['Fname','Lname','spe','department']
dict_count_depart = {"TIC":0,"GEE":0,"SEI":0,"ET":0}
# Percentage of people in each department in a new DataFrame
for row in participants.itertuples():
    print(row[4:][0])
    department = row[4:][0]
    if department in dict_count_depart:
        dict_count_depart[department]+=1
df_percentage = pd.DataFrame.from_dict(dict_count_depart,orient='index')
counter=0
for row in df_percentage.iterrows():
    counter+=row[1]
counter=counter.astype(float)
df_percentage[0]/12
percentage_serie = df_percentage[0]/12
df_percentage[0] = percentage_serie
df_percentage.columns=['Pourcentage']
df_percentage.to_csv('C:/Users/user/Desktop/RepositoryTP/PythonBDTN-TU/TP2/resultsPercentageExercice2')

#TP3 part :
# Utilisez matplotlib pour générer deux visualisations différentes de la répartition
# de votre groupe de PING :
# 1. sous forme de diagramme en barres,
# 2. sous forme de camembert.
import matplotlib.pyplot as plt
# Bar histogram
plt.hist(df_percentage,10,normed=1,facecolor='g',alpha=0.75)
# Cheese figure
labels = 'TIC','GEE','SEI','ET'
plt.pie(df_percentage,labels=labels,autopct='%1.1f%%',shadow=True, startangle=90)

    
    
    

        
    
