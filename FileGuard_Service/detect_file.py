from . import file_data_extracter

def detect_files(filename):
    try:
        from . import file_data_extracter
        file = file_data_extracter.pdf(filename)
    except Exception as e:
        raise Exception(f"[PDF INIT ERROR] {str(e)}")

    try:
        data = file.get_extracted_data()
    except Exception as e:
        raise Exception(f"[FEATURE EXTRACTION ERROR] {str(e)}")

    try:
        import pandas as pd
        df = pd.DataFrame([data])
    except Exception as e:
        raise Exception(f"[DATAFRAME ERROR] {str(e)}")

    try:
        import joblib
        import os
        base_dir = os.path.dirname(__file__)
        model_path = os.path.join(base_dir, "models", "pdf_model.pkl")
        model = joblib.load(model_path)
    except Exception as e:
        raise Exception(f"[MODEL LOAD ERROR] {str(e)}")

    try:
        prediction = model.predict(df)[0]
    except Exception as e:
        raise Exception(f"[PREDICTION ERROR] {str(e)}")

    return "safe" if prediction == 0 else "malicious"

