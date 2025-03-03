import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# File uploader
files = st.file_uploader("Upload CSV or Excel files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        
        # Read file
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        # Remove Duplicates
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed Successfully.")
            st.dataframe(df.head())

        # Fill Missing Values
        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing Values Filled with Mean Successfully.")
            st.dataframe(df.head())

        # Column Selection
        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show Chart (Fix applied)
        numeric_df = df.select_dtypes(include="number")
        if not numeric_df.empty:
            if st.checkbox(f"Show Chart - {file.name}"):
                st.bar_chart(numeric_df.iloc[:, :2])  # Select first 2 numeric columns

        # Format Selection (Fix applied)
        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)

        # Download Button (Fix applied)
        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button("Download file", file_name=new_name, data=output, mime=mime)
            st.success("Process Completed Successfully!")
