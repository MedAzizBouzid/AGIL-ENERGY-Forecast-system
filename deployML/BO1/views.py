from django.shortcuts import render
from joblib import load 
from .models   import PredictClient

import pandas as pd
import numpy as np 
from sklearn.preprocessing import MinMaxScaler

model=load('./notebooks/model_lgbm.joblib')
scaler = load('./notebooks/scaler.pkl')
df=pd.read_csv('./notebooks/to_read.csv')
lag_features = ['lag1_previous_order', 'lag3_previous_order', 'lag6_previous_order', 'lag9_previous_order']
# Define the columns to match on, excluding DATLIV
match_columns = ['ANCSCP', 'LIBPRD', 'LIBGVR', 'LIBLOC','DATLIV']
def add_date_features(df, date_column='DATLIV'):
    df[date_column] = pd.to_datetime(df[date_column])

    # Extract different date-related features
    df['Year'] = df[date_column].dt.year
    df['Month'] = df[date_column].dt.month
    df['Day'] = df[date_column].dt.day
    df['Weekday'] = df[date_column].dt.weekday
    df['Quarter'] = df[date_column].dt.quarter
    
    # Add cyclic features for month and day
    df['month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)
    df['day_sin'] = np.sin(2 * np.pi * df['Day'] / 31)
    df['day_cos'] = np.cos(2 * np.pi * df['Day'] / 31)

    return df
def predictor(request):
    return render(request,'main.html')
def formInfo(request):
    
    # Get the data from the form 

    ancscp=request.GET['ANCSCP']
    DATLIV=request.GET['DATLIV']
    LIBPRD=request.GET['LIBPRD']
    LIBGVR=request.GET['libgvr']
    LIBLOC=request.GET['libloc']
    prixHt=request.GET['prixHT']
    lag1_previous_order=request.GET['lag1_previous_order']
    lag3_previous_order=request.GET['lag3_previous_order']
    lag6_previous_order=request.GET['lag6_previous_order']
    lag9_previous_order=request.GET['lag9_previous_order']


    data = {
    'ANCSCP': [ancscp],
    'DATLIV': [DATLIV],
    'LIBPRD': [LIBPRD],
    'LIBGVR': [LIBGVR],
    'LIBLOC': [LIBLOC],
    'prixHT': [prixHt],
    'lag1_previous_order': [lag1_previous_order],
    'lag3_previous_order': [lag3_previous_order],
    'lag6_previous_order': [lag6_previous_order],
    'lag9_previous_order': [lag9_previous_order]



}

    x = pd.DataFrame(data)
    x['DATLIV'] = pd.to_datetime(x['DATLIV'])
    df['DATLIV'] = pd.to_datetime(df['DATLIV'])
    
        #enocde Categorical features
    categorical_columns = ['LIBPRD','LIBGVR','LIBLOC']
    #Add feature engineering (lag features)
    # x_transformed=x
    # for lag_feature in lag_features:
    #     # Extract the lag number from the feature name
    #     lag_number = int(lag_feature.split('_')[0][3:])

    #     # Create a new feature column
    #     x_transformed[lag_feature] = None

    #     # Loop through each row in x_transformed
    #     for index, row in x_transformed.iterrows():
    #         # Get the values for the match columns
    #         match_tuple = (row['ANCSCP'], row['LIBPRD'], row['LIBGVR'], row['LIBLOC'], row['DATLIV'].to_period('M'))
    #         # Find the row in data with the same values for the match columns
    #         matching_rows = df[df[list(match_columns)] == list(match_tuple)]
    #         print(df[(df['ANCSCP'] == x_transformed['ANCSCP']) & (df['DATLIV'] == "02/2019")])
    #         print(ancscp)
    #         # Filter the matching rows to exclude the current date
    #         #matching_rows = matching_rows[matching_rows['DATLIV'] != row['DATLIV']]

    #         # Sort the remaining rows by DATLIV in descending order
    #         matching_rows = matching_rows.sort_values(by='DATLIV', ascending=False)

    #         # Get the quantity from the first matching row
    #         if len(matching_rows) >= lag_number:
    #             quantity_value = matching_rows.iloc[lag_number - 1]['QTEPRD']
    #         else:
    #             quantity_value = None

    #         # Set the quantity value in the new feature column
    #         x_transformed.loc[index, lag_feature] = quantity_value

    # print(x_transformed)
    x_transformed = pd.get_dummies(x, columns=categorical_columns)
    #encode Date feature
    x_transformed=add_date_features(x_transformed)
    x_transformed.drop(columns=['DATLIV'], inplace=True)
    x_transformed[x_transformed.select_dtypes(include='bool').columns] = x_transformed.select_dtypes(include='bool').astype(int)
        # Add other features remaining
    expected_columns = scaler.feature_names_in_
    for col in expected_columns:
        if col not in x_transformed.columns:
            x_transformed[col] = 0
    x_transformed = x_transformed[expected_columns]
    

    print(x_transformed)
    print('--------------------------------------------')


    # Data normalization
    x_scaled = scaler.transform(x_transformed)
    x_scaled = pd.DataFrame(x_scaled, columns=x_transformed.columns)
    print(x_scaled)
    # Delete target feature
    x_scaled.drop(columns=['QTEPRD'], inplace=True)
    #Model prediction
    y_pred=model.predict(x_scaled)
    # temporairement
    y_pred=(y_pred*10)/0.28125

    PredictClient.objects.create(
    ANCSCP=ancscp,
    DATLIV=x['DATLIV'][0],  # Assurez-vous que la date est bien au format DateTime
    LIBPRD=LIBPRD,
    LIBGVR=LIBGVR,
    LIBLOC=LIBLOC,
    prixHT=prixHt,
    lag1_previous_order=lag1_previous_order,
    lag3_previous_order=lag3_previous_order,
    lag6_previous_order=lag6_previous_order,
    lag9_previous_order=lag9_previous_order,
    prediction=y_pred[0]  # y_pred est un tableau, donc on prend la première valeur
)


    return render(request,'result-summary-main/result.html',{'prediction':y_pred[0],
                                         'Client':ancscp,
                                         'Product':LIBPRD,
                                         'gvr':LIBGVR,
                                         'datliv':DATLIV,
                                         'loc':LIBLOC,
                                         'carb':LIBPRD,
                                         'x_scaled':x_transformed })