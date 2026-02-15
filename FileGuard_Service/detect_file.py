from . import file_data_extracter

def detect_files(filename):
    file = file_data_extracter.pdf(filename)
    data = file.get_extracted_data()

    import pandas as pd
    df = pd.DataFrame([data])

    import joblib
    model = joblib.load("FileGuard_Service\models\pdf_model.pkl")
    prediction = model.predict(df)


    predictions = model.predict(df)
    file_predictions = "safe" if prediction == 0 else "malicious"
    return file_predictions

