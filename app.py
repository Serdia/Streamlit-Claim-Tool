# activate venv: .venv\Scripts\Activate.ps1 
# run streamlit: streamlit run .\Streamlit_ClaimTool\main_API.py

import streamlit as st
from data_processing import * #load_data, clean_data, summarize_data


def main():
    st.title("DUAL TPA Claim Data Processing")

    # File uploader
    uploaded_file = st.file_uploader("Upload your data file", type=["csv", "xlsx"])
    
    if uploaded_file:
        # Get the name of the uploaded file
        file_name = uploaded_file.name
        
        # Extract name and date from the file name
        extracted_name, extracted_date = extract_name_date(file_name)

         # Create two columns
        col1, col2 = st.columns(2)
        
        # Display TPA name and date in separate columns
        col1.write(f"TPA: **{extracted_name}**")
        col2.write(f"Date: **{extracted_date}**")

        # Read the Excel file
        excel_file = pd.ExcelFile(uploaded_file)
        
        # Get sheet names
        sheet_names = excel_file.sheet_names
    
        # Display sheet names in a select box
        choice = st.selectbox("Select SheetName", sheet_names)

        # Load data from the selected sheet
        df = load_data(uploaded_file, sheet_name=choice)
        if df is not None:
            st.write("### Raw Data")
            st.dataframe(df)
            
        
            st.button("Process file")
            
        else:
            st.error("Looks like the file has no data. Please upload another file or choose a different sheet.")

if __name__ == "__main__":
    main()
