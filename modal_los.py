import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
from scipy import stats
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, LeaveOneOut, KFold, cross_val_score, RandomizedSearchCV
from sklearn.linear_model import Ridge, RidgeCV, Lasso, LassoCV
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn import neighbors
from sklearn.metrics import r2_score
from sklearn.metrics.pairwise import cosine_similarity
import pickle


df = pd.read_pickle("data/pickles/data7_0")
pd.set_option("display.max_columns", None)
df.describe()
df = df[df["ccs_diagnosis_description"].str.contains("diabetes", case=False)] #26816 remains
df = df[~df["ccs_diagnosis_description"].str.contains("pancrea", case=False)]
# (19731, 35)

# Target only Age 65+
df = df[(df['age_group'].str.contains("75+", case=False)) | (df['age_group'].str.contains("65-74", case=False))]

df = df[df['gender'] != 'U'] # drop 5 rows whose Gender is 'U'

# cleaning the 'covid' column
df.loc[df['covid'] == 'FASLE', 'covid'] = 'FALSE'
df.loc[df['covid'] == '0', 'covid'] = 'FALSE'
df.loc[df['covid'] == '1', 'covid'] = 'TRUE'

# drop columns where there are only 1 or NAN values
df = df.drop(columns=['ccs_diagnosis_description','primary_adm_diag','apr_mdc_description','apr_drg_description', "cdc_2018_overall_svi"])
# drop the variables that are not useful in model: 'index', 'facility ID','zip code','area_name',attending_provider_license_number ''
df = df.drop(columns=['area_name', 'zip_code_3_digits', 'attending_provider_license_number', 'fips_code_x', 'lat', 'lon'])
# drop highly correlated columns
df = df.drop(columns=['apr_severity_of_illness_description'])
# drop non-related columns
df = df.drop(columns=['cdc_2018_diagnosed_diabetes_percentage'])

target_vars = ['length_of_stay', 'total_charges', 'total_costs']
for col in target_vars:
    temp_cols=df.columns.tolist()
    index=df.columns.get_loc(col)
    new_cols=temp_cols[index:index+1] + temp_cols[0:index] + temp_cols[index+1:]
    df=df[new_cols]

df['apr_drg_code'] = df['apr_drg_code'].astype(str)
df['apr_mdc_code'] = df['apr_mdc_code'].astype(str)
df['ccs_diagnosis_code'] = df['ccs_diagnosis_code'].astype(str)

for col in ['length_of_stay']:
    for i in range(1, len(df[col])):
        df = df.loc[np.abs(stats.zscore(df[col])) < 5]
facility_id = df['facility_id']
df = df.drop(columns=['facility_id'])
# Gender
gender_male = pd.get_dummies(df['gender'], prefix = 'gender',prefix_sep = '_', drop_first=True)
df = pd.concat([df.drop(labels=['gender'],axis=1),gender_male],axis=1)

# Race (4 races)
race_encode = pd.get_dummies(df['race'],prefix = 'race', prefix_sep = '_', drop_first=True)
df = pd.concat([df.drop(labels=['race'],axis=1),race_encode],axis=1)

# Covid
covid_encode = pd.get_dummies(df['covid'],prefix = 'covid', prefix_sep = '_', drop_first=True)
df = pd.concat([df.drop(labels=['covid'],axis=1),covid_encode],axis=1)

#ethnicity
ethnicity_encode = pd.get_dummies(df['ethnicity'],prefix = 'ethnicity', prefix_sep = '_',drop_first=True)
df = pd.concat([df.drop(labels=['ethnicity'],axis=1),ethnicity_encode],axis=1)

#type_of_admission
admin_type_encode = pd.get_dummies(df['type_of_admission'],prefix = 'type_of_admission', prefix_sep = '_',drop_first=True)
df = pd.concat([df.drop(labels=['type_of_admission'],axis=1),admin_type_encode],axis=1)

# payment typology
payment_encode = pd.get_dummies(df['payment_typology_1'],prefix = 'payment_typology_1', prefix_sep = '_',drop_first=True)
df = pd.concat([df.drop(labels=['payment_typology_1'],axis=1),payment_encode],axis=1)

# Patient Disposition
disposition_encode = pd.get_dummies(df['patient_disposition'],prefix = 'patient_disposition', prefix_sep = '_',drop_first=True)
df = pd.concat([df.drop(labels=['patient_disposition'],axis=1),disposition_encode],axis=1)

# apr_drg_code
apr_drg_encode = pd.get_dummies(df['apr_drg_code'],prefix = 'apr_drg_code', prefix_sep = '_',drop_first=True)
df = pd.concat([df.drop(labels=['apr_drg_code'],axis=1),apr_drg_encode],axis=1)

# apr_mdc_code
apr_mdc_encode = pd.get_dummies(df['apr_mdc_code'],prefix = 'apr_mdc_code', prefix_sep = '_',drop_first=True)
df = pd.concat([df.drop(labels=['apr_mdc_code'],axis=1),apr_mdc_encode],axis=1)

# ccs_diagnosis_code
ccs_diagnosis_encode = pd.get_dummies(df['ccs_diagnosis_code'],prefix = 'ccs_diagnosis_code', prefix_sep = '_',drop_first=True)
df = pd.concat([df.drop(labels=['ccs_diagnosis_code'],axis=1),ccs_diagnosis_encode],axis=1)

# Age Group (5 age groups)
enc_age_dict = {'0-17':0,'18-44':1,'45-64':2,'65-74':3,'75+':4} # Define a dictionary for encoding target variable
df['age_group'] = df['age_group'].map(enc_age_dict) # Replace temp column values with the mapped values

X = df.iloc[:, 3:-1]
y = df['length_of_stay']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
print(X.columns)
from sklearn.linear_model import RidgeCV
ridge_cv = RidgeCV(normalize=True, cv=10, scoring='neg_mean_squared_error').fit(X,y)

print(" Ridge CV Score ", ridge_cv.best_score_)
print(" Ridge CV Best Alpha ", ridge_cv.alpha_)

ridge = Ridge(alpha=0.1)
ridge.fit(X_train, y_train)
print(X_train.columns)
pickle.dump(ridge, open('ridge.pkl', 'wb'))
print(f"The Metrics for Regularized Ridge Regression model are :-","\n")
print("Training MSE", mean_squared_error(y_train, ridge.predict(X_train)))
print("Test MSE:", mean_squared_error(y_test, ridge.predict(X_test)))
# import xgboost as xgb
# from sklearn.metrics import mean_squared_error
# xgb_model = xgb.XGBRegressor(n_jobs = -1)
# xgb_model.get_params() #default parameters
# xgb_model.fit(X_train, y_train)
# y_pred = xgb_model.predict(X_test)
# pickle.dump(xgb_model, open('xgb_model.pkl', 'wb'))
# print(f"The Metrics for Linear Regression model are :-","\n")
# print("Training R-squared: ", xgb_model.score(X_train,y_train))
# print("Testing R-squared: ", xgb_model.score(X_test,y_test), "\n")
# #
# print("Training MSE", mean_squared_error(y_train, xgb_model.predict(X_train)) )
# print("Test MSE:", mean_squared_error(y_test, xgb_model.predict(X_test)))
#
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred = lr_model.predict(X_test)
print(f"The Metrics for Linear Regression model are :-","\n")
print("Training R-squared: ", lr_model.score(X_train,y_train))
print("Testing R-squared: ", lr_model.score(X_test,y_test), "\n")
#
print("Training MSE", mean_squared_error(y_train, lr_model.predict(X_train)) )
print("Test MSE:", mean_squared_error(y_test, lr_model.predict(X_test)))
#
# pickle.dump(lr_model, open("lr_model.pkl", "wb"))
#
# # poly_lr = LinearRegression()
# # for i in range(1,4):
# #     pm = PolynomialFeatures(degree=i)
# #
# #     pm_X_train = pm.fit_transform(X_train)  # Fit data in X_train & X_test into training and testing variables for Polynomial model
# #     pm_X_test = pm.fit_transform(X_test)
# #
# #     poly_lr.fit(pm_X_train, y_train)    # Since we have fitted the data according to polynomial characteristic of the curve,
# #                                         # we can now model it with the Linear regression model
# #
# #     print("Training Mean squared error for Degree " + str(i)," is     :", mean_squared_error(y_train, poly_lr.predict(pm_X_train)))
# #     print("Testing Mean squared error for Degree "+ str(i)," is      :", mean_squared_error(y_test, poly_lr.predict(pm_X_test)))
# #     print("\n")
# x=x.append([0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
# x = x.fillna(0)
# x = x.astype(float)
# y=lr_model.predict(x)
# print(y)
# """
# age
# gender
# race
# covid_hosp
# ethnicity
# type of admission
# payment typology
# patient disposition
# apr drg code
#
# """