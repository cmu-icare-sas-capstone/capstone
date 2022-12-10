import pandas as pd
import numpy as np
from scipy import stats

def cleanDf(df):
    # Target only the diabetes patients
    df = df[df["ccs_diagnosis_description"].str.contains("diabetes", case=False)] #26816 remains
    df = df[~df["ccs_diagnosis_description"].str.contains("pancrea", case=False)]
    # (19731, 35)

    # Target only Age 65+
    df = df[(df['age_group'].str.contains("75+",case=False)) | (df['age_group'].str.contains("65-74",case=False))]
    
    df = df[df['gender'] != 'U'] # drop 5 rows whose Gender is 'U'

    # cleaning the 'covid' column
    df.loc[df['covid'] == 'FASLE', 'covid'] = 'FALSE'
    df.loc[df['covid'] == '0', 'covid'] = 'FALSE'
    df.loc[df['covid'] == '1', 'covid'] = 'TRUE'

    # drop columns where there are only 1 or NAN values
    collist = ['ccs_diagnosis_description','primary_adm_diag','apr_mdc_description','apr_drg_description',
            'area_name','zip_code_3_digits','attending_provider_license_number','fips_code_x','lat','lon',
            'apr_severity_of_illness_description','cdc_2018_diagnosed_diabetes_percentage','sum_countunique_rndrng_npi_physician_other_providers']
    # for col in collist :
    #     try:
    df = df.drop(columns=collist)
    #     except:
    #         print(col)
    #         pass
    # # drop the variables that are not useful in model: 'index', 'facility ID','zip code','area_name',attending_provider_license_number ''
    # df = df.drop(columns=['index','area_name','zip_code_3_digits','attending_provider_license_number','fips_code_x','lat','lon','county'])
    # # drop highly correlated columns
    # df = df.drop(columns=['apr_severity_of_illness_description'])
    # # drop non-related columns
    # df = df.drop(columns=['cdc_2018_diagnosed_diabetes_percentage','sum_countunique_rndrng_npi_physician_other_providers'])
    # # Note:the longtitde and latitude info will not be useful in linear regression model, but could be useful in tree model. 'longtitude','latitude'

    target_vars = ['length_of_stay','total_charges','total_costs']
    for col in target_vars:
        temp_cols=df.columns.tolist()
        index=df.columns.get_loc(col)
        new_cols=temp_cols[index:index+1] + temp_cols[0:index] + temp_cols[index+1:]
        df=df[new_cols]

    df['apr_drg_code'] = df['apr_drg_code'].astype(str)
    df['apr_mdc_code'] = df['apr_mdc_code'].astype(str)
    df['ccs_diagnosis_code'] = df['ccs_diagnosis_code'].astype(str)

    for col in ['length_of_stay']:
        for i in range(1,len(df[col])):
            df = df.loc[np.abs(stats.zscore(df[col])) < 5]
    
    # save columns needed for later use before dropping
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

    return df