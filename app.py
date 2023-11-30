import numpy as np
import pandas as pd
import streamlit as st
# from pandas_profiling import ProfileReport
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Web App Title
st.markdown('''
# **Exploratory Data Analysis**

**Credit:** App built in `Python` + `Streamlit` by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) (aka [Data Professor](http://youtube.com/dataprofessor)) - adapted here for professionnal purposes.

---
''')

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    sep = st.sidebar.text_input("First indicate CSV separator", ",")
    uploaded_file = st.sidebar.file_uploader("Then upload your input CSV file", type=["csv"])
    path = st.sidebar.text_input("Or give the online path of the CSV", "")
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)
""")

# Pandas Profiling Report
if uploaded_file is not None or len(path)>0:
    @st.cache_data
    def load_csv(csv_path: str, csv_sep: str):
        if uploaded_file is None and len(csv_path) > 0:
            csv = pd.read_csv(csv_path, sep=csv_sep)
        else:
            csv = pd.read_csv(uploaded_file, sep=csv_sep)
        return csv
    df = load_csv(path, sep)
    pr = ProfileReport(df, explorative=True)
    st.header('**Input DataFrame**')
    st.write(df)
    st.write('---')
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
