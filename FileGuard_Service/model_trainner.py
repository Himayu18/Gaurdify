import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / "pdf_model.pkl"

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)

import pyarrow.parquet as pq
data_set = pq.read_table("FileGuard_Service/datasets/PDFMalware2022.parquet")
df = data_set.to_pandas(types_mapper=None)

df = df.drop(columns=["Header","FileName","Text","Endobj","Endstream","Xref","StartXref","PageNo","Encrypt","EmbeddedFile","Colors","XFA","JS","Acroform","ObjStm"])
df["Class"] = df["Class"].map({ "Benign": 0,"Malicious": 1})

import re

def clean_numeric(x):
    match = re.search(r'-?\d+(\.\d+)?', str(x))
    return float(match.group()) if match else 0.0

cat_features = ["Images","Obj","Javascript","AA","OpenAction",
                "JBIG2Decode","RichMedia","Launch"]

df[cat_features] = df[cat_features].applymap(clean_numeric).astype("float32")

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

X = df.drop(columns=["Class"])
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
num_cols = X.select_dtypes(include=["number"]).columns
preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
    ]
)

model = Pipeline(
    steps=[
        ("prep", preprocess),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced")),
    ]
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("prediction: ",y_pred)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nReport:\n", classification_report(y_test, y_pred))

import joblib
joblib.dump(model, MODEL_PATH)