# -*- coding: utf-8 -*-
"""DiseasePred.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1epsstUOpoYEjvTQel6kDJkebvylNsopv
"""

#Importing the libraries
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import json
import pickle
#Importing the datset used for training
# from google.colab import files

# uploaded = files.upload()

#Dataset Loading
import pandas as pd
import io
#  df=pd.read_csv(io.BytesIO(uploaded['Training.csv']))
# df = pickle.load(open("model.pkl", "rb"))
df=pd.read_csv('Training.csv')
# print(df)
df_orig=df.copy()

#Replace categorical labels with numeric values
df.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
'Migraine':11,'Cervical spondylosis':12,
'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
'(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
'Impetigo':40}},inplace=True)

#spliting features and targets from the dataset
x=df.drop('prognosis',axis=1)
y=df['prognosis']
y_orig=df_orig['prognosis']
sympt_samples=["muscle_pain","diarrhoea","constipation","back_pain","sweating","stomach_pain","itching","shivering"]
#First rows of the dataset
df.head()

#Exploratory data analysis(EDA)
  # Data types of all the features and targets
# df.info()
  #Understand the target variable(predicted disease)
df['prognosis'].value_counts()
df[sympt_samples].corr()
    #Data visualization


#Model Training
'''
We are going to compare the performance of 2 Learning algorithms(Softmax regression and Xgboost Classifier(Boosted trees),
 and pick the one with the highest F1-score(Precision and recall trade-off),
We are aiming to maintain a fair ratio between accuracy and recall because our dataset does not diagnosis rare diseases,and the goal of the project
is not to replace medical check-ups but instead to encourage them,hence we want to make sure that the trade-off between precision and recall is fair
'''
import warnings
warnings.filterwarnings('ignore')
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

#Train_set and validation_set and test creation
#70% of data is used for training


x_train,x_val,y_train,y_val=train_test_split(x,y,test_size=0.7,random_state=1)
#15% of data is used for the validation set and 15% is used for the test set


x_valid,x_test,y_valid,y_test=train_test_split(x_val,y_val,test_size=0.5,random_state=1)
#Learning algorithms initialization(Softmax Regression and XGB Classifier)

clf2=xgb.XGBClassifier()
clf3=LogisticRegression(multi_class='multinomial',max_iter=1000) #Softmax
#Hyperparameters tuning and model performance comparisons using GridSearchCv

models={
    'xgb_Classifier':{
       'model_name':clf2,
       'params':{

      'max_depth': [3, 5, 7],
      'learning_rate': [0.1, 0.01, 0.001],
         },
       },

       'LogisticRegression':{
        'model_name':clf3,
        'params':{
            'C':[3,6,9,11],
         },
     },

}

#F1 score (Precision vs accuracy trade off)
score=[]
for model_name,mp in models.items():
  clf=GridSearchCV(mp['model_name'],mp['params'],cv=3,return_train_score=False,scoring='f1_macro')
  clf.fit(x_train,y_train)
  score.append({
      'model':model_name,
      'best_score':clf.best_score_,
      'best_params':clf.best_params_
  })
#Convert the result in a panda dataframe
score_df=pd.DataFrame(score,columns=['model','best_score','best_params'])


#Model performances
 #Validation score
pred_val=clf.predict(x_valid),
pred_df=pd.DataFrame(pred_val)
y_valid_pred=pred_df.iloc[0,:]
val_score=sklearn.metrics.f1_score(y_valid,y_valid_pred, average='micro'),
# print("Performance of the best model on the validation set is F1_Score: ",val_score),
 #Test score\
pred_test=clf.predict(x_test),
pred_df_test=pd.DataFrame(pred_test)
y_test_pred=pred_df_test.iloc[0,:]
test_score=sklearn.metrics.f1_score(y_test,y_test_pred, average='micro'),
# print("Performance of the best model on the test set is F1_Score=: ",test_score),

#Predictions
def my_pred(my_symptoms):
 l=df.drop('prognosis',axis=1).columns.tolist()
 disease=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction',
 'Peptic ulcer diseae','AIDS','Diabetes','Gastroenteritis','Bronchial Asthma','Hypertension',
 ' Migraine','Cervical spondylosis',
 'Paralysis (brain hemorrhage)','Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A',
 'Hepatitis B','Hepatitis C','Hepatitis D','Hepatitis E','Alcoholic hepatitis','Tuberculosis',
 'Common Cold','Pneumonia','Dimorphic hemmorhoids(piles)',
 'Heartattack','Varicoseveins','Hypothyroidism','Hyperthyroidism','Hypoglycemia','Osteoarthristis',
 'Arthritis','(vertigo) Paroymsal  Positional Vertigo','Acne','Urinary tract infection','Psoriasis',
 'Impetigo']
 l2=[]
 for x in range(0,len(l)):
     l2.append(0)
 for k in range(0,len(l)):
        for z in my_symptoms:
            if(z==l[k]):
                l2[k]=1
 inputtest = [l2]

 predictions= clf.predict(inputtest)
 dict={'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
 'Peptic ulcer diseae':5,'AIDS':6,'Diaitemsbetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
 'Migraine':11,'Cervical spondylosis':12,
 'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
 'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
 'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
 'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
 '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
 'Impetigo':40}
 Disease_pred=[key for key,value in dict.items() if value==predictions]
 return Disease_pred

#Input examples
input_data =(sys.argv[1])
# input_data = ["belly_pain","diarrhoea","depression","internal_itching","sweating"]

def creer_array_depuis_virgules(chaine):
  """
  Fonction pour créer un array à partir d'une chaîne séparée par des virgules.

  Args:
      chaine: La chaîne à convertir en array.

  Returns:
      Une liste contenant des arrays.
  """
  elements = chaine.split(",")
  liste_array = []
  for element in elements:
    # Supprime les espaces avant et après chaque élément
    element = element.strip()
    # Si l'élément est vide, on ignore
    if not element:
      continue
    # Crée un array à partir de l'élément
    array = element.split(" ")
    liste_array.append(array)

  return liste_array

# Exemple d'utilisation
chaine =(input_data)
liste_array = creer_array_depuis_virgules(chaine)
# symptoms = ["belly_pain","diarrhoea","depression","internal_itching","sweating"]
# print(f"With the sysmptoms{symptoms} ,the prediction gives: ",my_pred(symptoms))
print(f"Decision : It might be {my_pred(liste_array)}")

#save the model

# with open('disease_pred.pkl', 'rb') as f:
#     model = pickle.load(f)
# Récupérez les données d'entrée depuis les arguments de la ligne de commande
# input_data = json.loads(sys.argv[1])

# Faites des prédictions avec le modèle
# predictions = model.predict(input_data)

# Imprimez les prédictions au format JSON pour que Node.js puisse les lire
# print(json.dumps(predictions.tolist()))







