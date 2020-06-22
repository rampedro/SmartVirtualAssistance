import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#%matplotlib inline

# preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
#import pandas_profiling as pp
#from sklearn.externals import joblib
#import sklearn.external.joblib as extjoblib
import joblib


#!brew install libomp
#!pip install xgboost

# models

import xgboost as xgb
from xgboost import XGBClassifier


#class my_ml_predictor():
#  def __init__(self):
#    pass

def deserialize(age_ ,gen_, hei_,wei_,aph_,apl_,cho_,glu_,smo_,alc_,act_):
        data = pd.read_csv("http://www.sharecsv.com/dl/48a7ffbf15e4eb29b59d28d882241f7a/cardio_train.csv")


# FE - thanks to: https://www.kaggle.com/benanakca/comparison-of-classification-disease-prediction
#data.drop("id",axis=1,inplace=True)
        data.drop_duplicates(inplace=True)
        data["bmi"] = data["weight"] / (data["height"]/100)**2
        out_filter = ((data["ap_hi"]>250) | (data["ap_lo"]>200))
        data = data[~out_filter]
        #len(data)

        out_filter2 = ((data["ap_hi"] < 0) | (data["ap_lo"] < 0))
        data = data[~out_filter2]

        target_name = 'cardio'
        data_target = data[target_name]
        data = data.drop([target_name], axis=1)

        train, test, target, target_test = train_test_split(data, data_target, test_size=0.2, random_state=0)

#%% split training set to validation set
        Xtrain, Xval, Ztrain, Zval = train_test_split(train, target, test_size=0.2, random_state=0)



        


        XGB_Classifier = joblib.load( open( "2XGB_Classifier.pkl", "rb" ) )



        acc_test_XGB_Classifier = round(XGB_Classifier.score(test, target_test) * 100, 2)
        #acc_test_XGB_Classifier





        single_data = test[0:1:1]
        single_data['age'] = int(age_)*356
        single_data['gender'] = int(gen_)
        single_data['height'] = int(hei_)
        single_data['weight'] = int(wei_)
        single_data['ap_hi'] = int(aph_)

        single_data['ap_lo'] = int(apl_)
        single_data['cholesterol'] = int(cho_)
        single_data['gluc'] = int(glu_)
        single_data['smoke'] = int(smo_)
        single_data['alco'] = int(alc_)
        single_data['active'] = int(act_)
        single_data['bmi'] = int(wei_/float(hei_*hei_))



#print(single_data)
        pre_pros_data = ['age', 'gender','height','weight','ap_hi','ap_lo','cholesterol','gluc','smoke','alco','active','bmi']

        return XGB_Classifier, single_data

class my_ml_predictor():
  def __init__(self):
      pass

  def predict(age_ ,gen_, hei_,wei_,aph_,apl_,cho_,glu_,smo_,alc_,act_):

        XGB_Classifier, single_data = deserialize(age_ ,gen_, hei_,wei_,aph_,apl_,cho_,glu_,smo_,alc_,act_)
        result = XGB_Classifier.predict(single_data)
        #print("**********************")
        if result.any() == 1:
            #print("not healty")
            return "not healthy"
        elif result.all() == 0:
            #print("healthy")
            return "healthy"

#print("**********************")


