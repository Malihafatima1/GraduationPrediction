import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

def load_data():
    data = pd.read_csv("graduation_dataset.csv")
    return data

def prepare_data(data, target_column, categorical_mappings):
    features = data.drop(target_column, axis=1)
    target = data[target_column]
    for col, mapping in categorical_mappings.items():
        if col in features.columns:
            features[col] = features[col].map(mapping)
    target = target.map({"No": 0, "Yes": 1})  # adjust if needed
    return features, target

def train_or_load_models(features, target):
    if not os.path.exists("svm_model.pkl") or not os.path.exists("rf_model.pkl"):
        X_train, _, y_train, _ = train_test_split(features, target, test_size=0.2, random_state=42)
        svm = SVC(probability=True)
        rf = RandomForestClassifier()
        svm.fit(X_train, y_train)
        rf.fit(X_train, y_train)
        joblib.dump(svm, "svm_model.pkl")
        joblib.dump(rf, "rf_model.pkl")
    else:
        svm = joblib.load("svm_model.pkl")
        rf = joblib.load("rf_model.pkl")
    return svm, rf
