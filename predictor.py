import pandas as pd
import joblib

def preprocess_data(data_frame):
    data_frame = data_frame.copy()
    X = data_frame.drop(columns=['Season', 'Date', 'HomeTeam', 'AwayTeam'])

    return X

def predict(model, X):
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)
    
    return y_pred, y_proba

def get_predictions(model, data_frame):
    X = preprocess_data(data_frame)
    y_pred, y_proba = predict(model, X)
    
    ftr_mapping_rev = {1: 'H', 0: 'D', -1: 'A'}
    y_pred_text = [ftr_mapping_rev[pred] for pred in y_pred]

    return y_pred_text, y_proba

def display_prediction(model, data_frame):
    y_pred_text, y_proba = get_predictions(model, data_frame)
    for i in range(len(data_frame)): 
        print(data_frame.iloc[i]['Date'], data_frame.iloc[i]['HomeTeam'], data_frame.iloc[i]['AwayTeam'])
        print('Przewidywany wynik: ', y_pred_text[i])
        print('Rozkład prawdopodobieństwa: ','H:', y_proba[i][2], 'D:', y_proba[i][1], 'A:', y_proba[i][0])
        print('\n')


