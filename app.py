import os
import numpy as np
import pandas as pd
import streamlit as st
# from pandas_profiling import ProfileReport
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from pipeline import pipeline, delete_dir

st.set_page_config(
    page_title="EDA CSV",
    page_icon="📊"
)
st.title("Exploratory Data Analysis")
# Web App Title
st.markdown('''
**Credit:** App built in `Python` + `Streamlit` by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) (aka [Data Professor](http://youtube.com/dataprofessor)) - adapted here for professionnal purposes.

---
''')

# Upload CSV data
with st.sidebar.header('Upload your CSV data'):
    sep = st.sidebar.text_input("Specify CSV separator", ",")
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    path = st.sidebar.text_input("Or give the online path of the CSV", "")
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)
""")

if uploaded_file is not None or len(path)>0:

    @st.cache_data
    def load_csv(csv_path: str, csv_sep: str):
        if uploaded_file is None and len(csv_path) > 0:
            csv = pd.read_csv(csv_path, sep=csv_sep)
        else:
            csv = pd.read_csv(uploaded_file, sep=csv_sep)
        csv.rename(columns={col: col.replace("/", "_slash_") for col in csv.columns}, inplace=True)
        return csv
    df = load_csv(path, sep)

    st.header('**Input DataFrame**')
    st.write(df)
    st.write('---')

    ## Transform data
    st.header("**Modify CSV data**")
    with st.form("my_form"):
        missing_values = st.selectbox(
            'Handle missing values (NA)',
            ('Do not handle', 'Drop NA', 'Fill with column mean', 'Fill with column median', 'Fill only object columns')
        )
        st.write("*Note : filling missing values with mean/median only works for numerical values; categorical columns will be filled with 'none' string.")
        stand = st.multiselect(
            "Standardize columns",
            list(df.columns),
            [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
        )

        one_hot = st.multiselect(
            "One-hot encoding columns",
            list(df.columns),
            [col for col in df.columns if df[col].dtype not in ['float64', 'int64']]
        )

        drops = st.multiselect(
            "Drop column(s)",
            list(df.columns),
            []
        )

        new_sep = st.text_input("Specify desired CSV separator", ",")

        get_zip = st.checkbox("Get descriptive analysis figures ?")

        submitted = st.form_submit_button("Apply transformations")

    if submitted:
            
        dirname = pipeline(
            data=df,
            miss_value=missing_values,
            standardize_cols=stand,
            one_hot_encoding_cols=one_hot,
            drop_columns=drops,
            csv_separator=new_sep,
            figures=get_zip)

        with open(dirname, "rb") as fp:
            dl_btn = st.download_button(
                label="Download processed data",
                data=fp,
                file_name=dirname,
                mime="application/zip"
                )
    
    else:
        filetree = [".env", ".git", ".gitignore", "app.py", "helpers.py", "pipeline.py", "README.md", "requirements.txt"]
        for obj in os.listdir(os.getcwd()):
            if obj not in filetree: delete_dir(obj)

    ## Pandas Profiling Report
    st.markdown("_ _ _")
    pr = ProfileReport(df, explorative=True)
    st.header('**Pandas Profiling Report**')
    st_profile_report(pr)

else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        # Example data
        @st.cache_data
        def load_data():
            a = pd.DataFrame(
                np.random.rand(100, 5),
                columns=['a', 'b', 'c', 'd', 'e']
            )
            return a
        df = load_data()
        pr = ProfileReport(df, explorative=True)
        st.header('**Input DataFrame**')
        st.write(df)
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)
