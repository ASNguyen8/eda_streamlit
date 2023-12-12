import pandas as pd


def pipeline(data: pd.DataFrame, miss_value: str, standardize_cols: list, one_hot_encoding_cols: list, csv_separator: str):
    # Handle missing values
    if miss_value == "Drop NA":
        data = data.dropna().reset_index(drop=True)
    elif "Fill with column" in miss_value:
        for col in standardize_cols:
            if miss_value == "Fill with column mean":
                data[col].fillna(data[col].mean(), inplace=True)
            elif miss_value == "Fill with column median":
                data[col].fillna(data[col].median(), inplace=True)

    # Standardize desired columns
    for col in standardize_cols:
        mu = data[col].mean()
        sigma = data[col].std()
        data[col] = (data[col] - mu) / sigma if sigma else 0
    
    # One-hot encoding desired columns
    data_dummies = pd.get_dummies(data, columns=one_hot_encoding_cols)
    
    return data_dummies
    