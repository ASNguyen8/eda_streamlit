import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# pipeline functions :
def standardize_col(data):
    mu = data.mean()
    sigma = data.std()
    return (data - mu)/sigma


def plot_column_by_dtype(col_data, col_name: str, dirname: str, figsize: tuple=(12, 8), percentage: bool=False):
    
    if col_data.dtype not in ['float64', 'int64', 'object']:
        return

    plt.figure(figsize=figsize)
    
    if col_data.dtype == "float64" or col_data.dtype == "int64":
        plt.boxplot(col_data)
        plt.gca().get_xaxis().set_visible(False)
        plot_name = os.path.join(dirname, f"boxplot_{col_name}")
    
    elif col_data.dtype == "object":
        values, frequencies = np.unique(col_data, return_counts=True)
        percent = frequencies / frequencies.sum()
        y_axis = range(1, len(frequencies) + 1)
        if percentage:
            plt.barh(y_axis, percent)
            plot_name = os.path.join(dirname, f"barplot_{col_name}_(percentage)")
        else:
            plt.barh(y_axis, frequencies)
            plot_name = os.path.join(dirname, f"barplot_{col_name}_(raw)")
        plt.yticks(y_axis, values)
    else:
        # print(col_name, col_data.dtype, sep="\t")
        plot_name = ""
    plt.title(col_name)
    plt.savefig(plot_name)
    plt.close()


def hist_col(data, title: str, figname: str, bins: int=10, density: bool=False, figsize: tuple=(12, 8)):
    title += "\n(probability density)" * (density)
    figname += "_density" * (density)
    plt.figure(figsize=figsize)
    plt.hist(data, bins=bins, density=density)
    plt.title(title)
    plt.savefig(figname)
    plt.close()


def barh_df(data, title: str, figname: str, figsize: tuple=(12, 8)):
    y_axis = range(1, len(data.columns) + 1)
    plt.figure(figsize=figsize)
    plt.barh(y_axis, data)
    plt.title(title)
    plt.yticks(y_axis, data.columns)
    plt.savefig(figname)
    plt.close()


def barh_dict(data, title: str, figname: str, figsize: tuple=(12, 8)):
    y_axis = range(1, len(data.keys()) + 1)
    plt.figure(figsize=figsize)
    plt.barh(y_axis, data.values())
    plt.title(title)
    plt.yticks(y_axis, data.keys())
    plt.savefig(figname)
    plt.close()


# app functions :
def form_columns(data):

    if data is None:
        return "<p>No file / filepath sent.</p>"

    def options(default_dtype):
        dtypes = ["float64", "int64", "object", "bool", "datetime64", "timedelta", "category",]
        option = ""
        for dt in dtypes:
            option += f"<option {"selected='selected'" * (dt == default_dtype)} value='{dt}'>{dt}</option>\n"
        return option

    to_return = ""

    for col in data.columns:
        to_return += f"<br><label for='{col}'>{col} -> </label>"
        to_return += f"<select name='{col}'>\n{options(data[col].dtype)}\n</select><br>\n"

    to_return += "<br><input type='submit' value='Correct dtypes'>"
    return to_return


def delete_folder(path: str):
    if not os.path.exists(path):
        return
    for elt in os.listdir(path):
        elt_path = os.path.join(path, elt)
        if os.path.isdir(elt_path):
            delete_folder(elt_path)
        else:
            os.remove(elt_path)
    os.rmdir(path)


def create_result_dir():
    dirname = os.path.join(os.getcwd(), "primary_data_pipeline_results")
    if os.path.isdir(dirname):
        delete_folder(dirname)
    os.mkdir(dirname)
    return dirname
