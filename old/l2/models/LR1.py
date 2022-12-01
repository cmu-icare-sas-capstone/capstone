"""

@author: Luyu Huang
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import old.l1.etl.DatabaseIO as dbio

def model():
    df = dbio.read_from_db('hospital_inpatient_discharges')    
    df = df[df['gender'] != 'U'] # drop 5 rows whose Gender is 'U'
    df.loc[df['covid'] == 'FASLE', 'covid'] = 'FALSE'
    df.loc[df['covid'] == '0', 'covid'] = 'FALSE'
    df.loc[df['covid'] == '1', 'covid'] = 'TRUE'
    
    # Gender
    gender_male = pd.get_dummies(df['gender'], drop_first=True)
    df = pd.concat([df.drop(labels=['gender'],axis=1), gender_male], axis=1)
    df.rename(columns={'M': 'gender_male'}, inplace=True)
    
    # Race (4 races)
    race_encode = pd.get_dummies(df['race'], drop_first=True)
    df = pd.concat([df.drop(labels=['race'], axis=1), race_encode], axis=1)
    
    # Age Group (5 age groups)
    # Define a dictionary for encoding target variable
    enc_age_dict = {'0-17':0,
                '18-44':1,
                '45-64':2,
                '65-74':3,
                '75+':4}
    # Replace original column values with the mapped values
    df['age_group'] = df['age_group'].map(enc_age_dict)
    
    # Covid 
    covid_encode = pd.get_dummies(df['covid'],drop_first=True)
    df = pd.concat([df.drop(labels=['covid'],axis=1),covid_encode],axis=1)
    df.rename(columns={'TRUE': 'covid'}, inplace=True)
    
    
    lr_features = ['county','facility_id','age_group','ccs_diagnosis_code','apr_drg_code','gender_male','Multi-racial','Other Race','White','covid']
    
    # Split the data into training and testing
    X = df[lr_features]
    y = df['length_of_stay']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred = lr_model.predict(X_test)
    
    return lr_model, X_train, y_train, X_test, y_pred, lr_features