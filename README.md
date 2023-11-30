# eda_streamlit

This is an **EDA** (Exploratory Data Analysis) application created in Streamlit using the **pandas-profiling** library (now **ydata-profiling**).

This application needs Python version (3.7 <= 3.11) because of ydata-profiling library requirements. Download one of those Python version and build a virtual environment using the following command (on Windows Powershell) :
`py -<python-version> -m venv <venv-name>`

You can either upload your own CSV file from local directories or give the URL of your CSV (eg. https://raw.githubusercontent.com/ASNguyen8/ASNguyen8.github.io/master/docs/essence.csv).
To avoid having to autodetect the CSV separator or forcing anyone to format their CSV, one can specify the CSV separator directly in the sidebar. One can also use my [data pipeline](https://github.com/ASNguyen8/primary_data_pipeline) to format in one fell swoop its dataset. (;))

**Credit:** App built in `Python` + `Streamlit` by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) (aka [Data Professor](http://youtube.com/dataprofessor)) - adapted here for professionnal purposes.