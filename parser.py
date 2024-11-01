import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
from io import BytesIO
import json
import gspread
from google.oauth2.service_account import Credentials

def parse_xml(file):
    """Parse XML file and return a DataFrame."""
    tree = ET.parse(file)
    root = tree.getroot()
    
    data = []
    for book in root.findall('book'):
        data.append({
            "id": book.get("id"),
            "author": book.find("author").text,
            "title": book.find("title").text,
            "genre": book.find("genre").text,
            "price": float(book.find("price").text),
            "publish_date": book.find("publish_date").text,
            "description": book.find("description").text.strip()
        })
    
    return pd.DataFrame(data)

def convert_to_xml(dataframe):
    """Convert DataFrame back to XML format."""
    root = ET.Element("catalog")
    for _, row in dataframe.iterrows():
        book = ET.SubElement(root, "book", id=row["id"])
        ET.SubElement(book, "author").text = row["author"]
        ET.SubElement(book, "title").text = row["title"]
        ET.SubElement(book, "genre").text = row["genre"]
        ET.SubElement(book, "price").text = str(row["price"])
        ET.SubElement(book, "publish_date").text = row["publish_date"]
        ET.SubElement(book, "description").text = row["description"]
        
    tree = ET.ElementTree(root)
    xml_buffer = BytesIO()
    tree.write(xml_buffer, encoding='utf-8', xml_declaration=True)
    return xml_buffer.getvalue()

def main():
    st.title("XML to CSV Converter and Editor")

    # Step 1: Upload XML File
    xml_file = st.file_uploader("Upload an XML file", type=["xml"])
    if xml_file is not None:
        # Parse XML and display data
        df = parse_xml(xml_file)
        
        # Preview first 5 rows of the table
        st.write("### Table Preview (first 5 rows)")
        st.write(df.head())

        # Full table view in an expander
        with st.expander("View Full Table"):
            st.write(df)

        # Step 2: Download options for CSV and Excel
        st.write("### Download Options")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download as CSV", data=csv_data, file_name="data.csv", mime="text/csv")
        
        excel_data = BytesIO()
        df.to_excel(excel_data, index=False, engine='xlsxwriter')
        excel_data.seek(0)
        st.download_button("Download as Excel", data=excel_data, file_name="data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # Google Sheets Upload in an Expander
        with st.expander("Upload to Google Sheets"):
            st.write("""
                Enter your Google Sheets URL and upload the Google credentials JSON file below. 
                Ensure that the service account in your JSON file is added as an **Editor** in the Google Sheets document.
            """)
                
            # Toggle for showing detailed instructions
            if "show_instructions" not in st.session_state:
                st.session_state.show_instructions = False

            def toggle_instructions():
                st.session_state.show_instructions = not st.session_state.show_instructions

            st.button("Show Detailed Instructions", on_click=toggle_instructions)
            
            # Conditionally display instructions for setting up Google Sheets and API Keys
            if st.session_state.show_instructions:
                st.write("### Instructions for Setting up Google Sheets and API Keys")
                st.markdown("""
                    1. **Create a Google Cloud Project**: Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project if you don’t already have one.
                    2. **Enable the Google Sheets API**: In your Google Cloud project, go to **APIs & Services > Library**, search for "Google Sheets API," and enable it.
                    3. **Create Service Account Credentials**:
                        - Go to **APIs & Services > Credentials** and click **Create Credentials > Service Account**.
                        - Fill in the required details and create the service account.
                    4. **Download the Service Account JSON**:
                        - Once the service account is created, go to **APIs & Services > Credentials**, click on your service account, and select **Add Key > Create new key**.
                        - Choose **JSON** and download the credentials file.
                    5. **Share Your Google Sheet with the Service Account**:
                        - Open the Google Sheet you want to use, click **Share**, and enter the service account’s email (found in your JSON file as `"client_email"`).
                        - Grant it **Editor** access to allow data updates.
                    6. **Enter the Google Sheets URL and Upload JSON File Below**.
                """)
                st.button("Hide Instructions", on_click=toggle_instructions)  # Button to hide instructions

            # Input fields for Google Sheets URL and JSON credentials
            google_sheet_url = st.text_input("Enter Google Sheets URL:")
            google_credentials = st.file_uploader("Upload Google Credentials JSON", type=["json"])

            # Upload to Google Sheets functionality
            if google_credentials and google_sheet_url:
                try:
                    sheet_id = google_sheet_url.split("/d/")[1].split("/")[0]
                    google_credentials_data = json.load(google_credentials)
                    scopes = [
                        "https://www.googleapis.com/auth/spreadsheets",
                        "https://www.googleapis.com/auth/drive"
                    ]
                    creds = Credentials.from_service_account_info(google_credentials_data, scopes=scopes)
                    client = gspread.authorize(creds)
                    sheet = client.open_by_key(sheet_id)
                    
                    # Button to upload data
                    if st.button("Upload to Google Sheets"):
                        try:
                            worksheet = sheet.get_worksheet(0) or sheet.add_worksheet(title="Sheet1", rows="100", cols="20")
                            worksheet.clear()
                            worksheet.update([df.columns.values.tolist()] + df.values.tolist())
                            st.success("Data uploaded to Google Sheets successfully!")
                        except Exception as e:
                            st.error(f"Failed to upload to Google Sheets: {e}")
                except (IndexError, KeyError) as e:
                    st.error("Invalid Google Sheets URL or credentials file.")
            else:
                st.warning("Please enter the Google Sheets URL and upload the credentials JSON file.")

        # Step 3: Convert back to XML
        if st.button("Convert to XML"):
            modified_xml_data = convert_to_xml(df)
            st.download_button("Download Edited XML", data=modified_xml_data, file_name="edited_data.xml", mime="application/xml")

if __name__ == "__main__":
    main()
