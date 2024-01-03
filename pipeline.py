import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from shutil import make_archive, rmtree


def handle_NA(data, miss_value: str, standardize_cols: list, one_hot_encoding_cols: list, figures: str=""):

    if figures:
        missing_values = {col: data[col].isna().sum() for col in data.columns}
        y_axis = range(1, len(missing_values.keys()) + 1)
        plt.figure(figsize=(24, 16))
        plt.barh(y_axis, missing_values.values())
        plt.title("Missing values in dataframe\n")
        plt.yticks(y_axis, missing_values.keys())
        plt.savefig(os.path.join(figures, "missing_values_per_columns"))
        plt.close()

    if miss_value == "Drop NA":
        data = data.dropna().reset_index(drop=True)
    elif "Fill" in miss_value:
        for col in standardize_cols:
            if miss_value == "Fill with column mean":
                data[col].fillna(data[col].mean(), inplace=True)
            elif miss_value == "Fill with column median":
                data[col].fillna(data[col].median(), inplace=True)
        for col in one_hot_encoding_cols:
            data[col].fillna("none", inplace=True)

    return data


def standardize_columns(data, num_cols: list, figures: str=""):

    for col in num_cols:

        if figures:
            plt.figure(figsize=(24, 16))
            plt.boxplot(data[col])
            plt.gca().get_xaxis().set_visible(False)
            plt.title(col)
            plt.savefig(os.path.join(figures, f"boxplot_{col}"))
            plt.close()

            plt.figure(figsize=(24, 16))
            plt.hist(data[col], density=False)
            plt.title(col)
            plt.savefig(os.path.join(figures, f"hist_{col}"))
            plt.close()

            plt.figure(figsize=(24, 16))
            plt.hist(data[col], density=True)
            plt.title(col + "\n(probability density)")
            plt.savefig(os.path.join(figures, f"hist_{col}" + "_density"))
            plt.close()

        mu = data[col].mean()
        sigma = data[col].std()
        data[col] = (data[col] - mu) / sigma if sigma else 0
    
    return data


def one_hot_encode_cols(data, object_cols: list, figures: str=""):

    if figures:
        # Bar plot for each object column
        for col in object_cols:
            values, frequencies = np.unique(data[col], return_counts=True)
            percent = frequencies / frequencies.sum()
            y_axis = range(1, len(frequencies) + 1)

            plt.figure(figsize=(24, 16))
            plt.barh(y_axis, frequencies)
            plot_name = os.path.join(figures, f"barplot_{col}_(raw)")
            plt.yticks(y_axis, values)
            plt.title(col)
            plt.savefig(plot_name)
            plt.close()

            plt.figure(figsize=(24, 16))
            plt.barh(y_axis, percent)
            plot_name = os.path.join(figures, f"barplot_{col}_(percentage)")
            plt.yticks(y_axis, values)
            plt.title(col)
            plt.savefig(plot_name)
            plt.close()
    
    # One hot encoding categorical variables
    data_dummies = pd.get_dummies(data, columns=object_cols)

    return data_dummies


def plot_corrs(data, figures: str, sep: str):
    corr = data.corr()
    corr.to_csv(os.path.join(figures, "correlations.csv"), sep=sep, index=False)
    mask = 1 - np.tril(np.ones_like(corr))
    plt.figure(figsize=(24, 16))
    sns.heatmap(corr, mask=mask, vmin=-1, vmax=1, annot=True, cmap='coolwarm')
    plt.title("Correlation between variables\nCategorical variables are one-hot encoded")
    plt.savefig(os.path.join(figures, "correlations"))
    plt.close()


def delete_dir(path: str):

    if not os.path.exists(path):
        return
    
    if os.path.isdir(path):
        rmtree(path)
    else:
        os.remove(path)


def pipeline(data: pd.DataFrame, miss_value: str, standardize_cols: list, one_hot_encoding_cols: list, drop_columns: list, csv_separator: str, figures: bool=False):

    folder_name = "eda_data"
    if not os.path.isdir(folder_name): os.mkdir(folder_name)

    data.to_csv(os.path.join(folder_name, "raw_data.csv"), sep=csv_separator, index=False)
    
    # Descriptive statistics
    if figures: data.describe().to_csv(os.path.join(folder_name, "descriptive_statistics.csv"), sep=csv_separator, index=False)

    # Drop columns
    data = data.drop(drop_columns, axis=1)
    standardize_cols = [c for c in standardize_cols if c not in drop_columns]
    one_hot_encoding_cols = [c for c in one_hot_encoding_cols if c not in drop_columns]
    datetype_cols = [c for c in data.columns if c not in standardize_cols and c not in one_hot_encoding_cols]

    # Handle missing values
    data = handle_NA(data, miss_value, standardize_cols, one_hot_encoding_cols, folder_name*figures)

    # Standardize desired columns
    data = standardize_columns(data, standardize_cols, folder_name*figures)
    
    # One-hot encoding desired columns
    data = one_hot_encode_cols(data, one_hot_encoding_cols, folder_name*figures)

    # Correlations
    if figures: plot_corrs(data.drop(datetype_cols, axis=1), folder_name, csv_separator)

    # Save results in zip
    data.to_csv(os.path.join(folder_name, "eda_processed_data.csv"), sep=csv_separator, index=False)
    make_archive(folder_name, 'zip', folder_name)
    delete_dir(folder_name)

    return folder_name + ".zip"
