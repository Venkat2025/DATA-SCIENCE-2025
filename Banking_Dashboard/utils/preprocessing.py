import pandas as pd
import numpy as np
import string

def preprocess_data(file=None):
    """
    Complete preprocessing pipeline:
    1) Load dataset
    2) Optimize numeric columns
    3) Treat nulls
    4) Feature engineering
    5) Detect outliers
    6) Clean text
    Returns:
        df : pd.DataFrame
        outliers_dict: dict
        clean_text_column: function
    """

    # ------------------- Load Data -------------------
    def _load_data(file):
        default_path = "application_train_10000.csv"
        try:
            if file:
                return pd.read_csv(file)
            else:
                return pd.read_csv(default_path)
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return pd.DataFrame()

    df = _load_data(file)
    if df.empty:
        return pd.DataFrame(), {}, None

    # ------------------- Optimize Numeric Columns -------------------
    def optimize_dataframe(df):
        optimized = df.copy()
        for col in optimized.columns:
            s = optimized[col]
            if pd.api.types.is_integer_dtype(s):
                vals = s.astype("int64")
                if vals.min() >= np.iinfo(np.int8).min and vals.max() <= np.iinfo(np.int8).max:
                    optimized[col] = s.astype("int8")
                elif vals.min() >= np.iinfo(np.int16).min and vals.max() <= np.iinfo(np.int16).max:
                    optimized[col] = s.astype("int16")
                elif vals.min() >= np.iinfo(np.int32).min and vals.max() <= np.iinfo(np.int32).max:
                    optimized[col] = s.astype("int32")
            elif pd.api.types.is_float_dtype(s):
                s64 = s.astype("float64")
                if np.allclose(s64, s64.astype("float16"), rtol=1e-03, atol=1e-06, equal_nan=True):
                    optimized[col] = s64.astype("float16")
                else:
                    optimized[col] = s64.astype("float32")
        return optimized

    df = optimize_dataframe(df)

    # ------------------- Treat Nulls -------------------
    def treat_nulls(df):
        cleaned = df.copy()
        threshold = 0.6
        null_ratio = cleaned.isna().mean()
        to_drop = null_ratio[null_ratio > threshold].index.tolist()
        cleaned = cleaned.drop(columns=to_drop)
        if cleaned.shape[1] == 0:
            return cleaned

        num_cols = [c for c in cleaned.select_dtypes(include=[np.number]).columns if cleaned[c].isna().any()]
        cat_cols = [c for c in cleaned.select_dtypes(include=["object","category","bool"]).columns if cleaned[c].isna().any()]
        dt_cols  = [c for c in cleaned.select_dtypes(include=["datetime64"]).columns if cleaned[c].isna().any()]

        if num_cols:
            medians = cleaned[num_cols].median()
            cleaned[num_cols] = cleaned[num_cols].fillna(medians)

        for c in cat_cols:
            mode_val = cleaned[c].mode(dropna=True)
            if not mode_val.empty:
                cleaned[c] = cleaned[c].fillna(mode_val[0])
            else:
                cleaned[c] = cleaned[c].fillna("" if cleaned[c].dtype=="object" else 0)

        for c in dt_cols:
            cleaned[c] = cleaned[c].fillna(method="ffill").fillna(method="bfill")

        return cleaned

    df = treat_nulls(df)

    # ------------------- Detect Outliers -------------------
    def find_outliers_iqr(df, cols=None):
        if cols is None:
            cols = df.select_dtypes(include=np.number).columns
        outliers = {}
        for col in cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5*IQR
            upper = Q3 + 1.5*IQR
            mask = (df[col] < lower) | (df[col] > upper)
            outliers[col] = df[mask].index.tolist()
        return outliers

    outliers_dict = find_outliers_iqr(df)

    # ------------------- Clean Text Columns -------------------
    def clean_text_column(df, col):
        cleaned = df.copy()

        def to_lower(s): return s.str.lower()
        def remove_punctuation(s): return s.str.translate(str.maketrans("", "", string.punctuation))
        def remove_numbers(s): return s.str.translate(str.maketrans("", "", "0123456789"))
        def remove_extra_spaces(s): return s.str.split().str.join(" ")

        if col in cleaned.columns:
            text_series = cleaned[col].astype(str)
            text_series = to_lower(text_series)
            text_series = remove_punctuation(text_series)
            text_series = remove_numbers(text_series)
            text_series = remove_extra_spaces(text_series)
            cleaned[col] = text_series

        return cleaned

    # ------------------- Feature Engineering --Overview-------------------
    if "DAYS_BIRTH" in df.columns:
        df["AGE_YEARS"] = (-df["DAYS_BIRTH"] / 365.25).astype(int)

    if "DAYS_EMPLOYED" in df.columns:
        df["EMPLOYMENT_YEARS"] = df["DAYS_EMPLOYED"].apply(
            lambda x: -x / 365.25 if x < 0 else None
        )  
    # ------------------- Feature Engineering — Household -------------------
    if "NAME_FAMILY_STATUS" in df.columns:
        df["IS_MARRIED"] = df["NAME_FAMILY_STATUS"].apply(lambda x: 1 if x in ["Married","Civil marriage"] else 0)

    if "CNT_CHILDREN" in df.columns:
        df["HAS_CHILDREN"] = (df["CNT_CHILDREN"] > 0).astype(int)

    if "CNT_FAM_MEMBERS" in df.columns:
        df["FAMILY_SIZE"] = df["CNT_FAM_MEMBERS"].fillna(df["CNT_FAM_MEMBERS"].median())

    # ------------------- Feature Engineering -Financial Health -------------------
    if "AMT_INCOME_TOTAL" in df.columns and "AMT_CREDIT" in df.columns and "AMT_ANNUITY" in df.columns:
        df["LTI"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]           
        df["DTI"] = df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]         
        df["ANNUITY_TO_CREDIT_RATIO"] = df["AMT_ANNUITY"] / df["AMT_CREDIT"]  

    return df, outliers_dict, clean_text_column
