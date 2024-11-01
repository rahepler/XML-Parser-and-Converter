# XML-Parser-and-Converter

📄 XML to CSV/Excel/Google Sheets Converter and Editor

A basic Streamlit app designed to parse XML files, convert them to CSV/Excel, and upload data directly to Google Sheets. This project serves as a foundation for anyone looking to build more sophisticated XML data processing tools with Python and Streamlit.

![image](https://github.com/user-attachments/assets/b11284c8-831b-49f4-912e-0dcc8b00e824)


🛠️ Features
XML Parsing and Data Display: Upload an XML file, parse it, and preview the data in an interactive table.
Downloadable Data: Download the parsed data as CSV or Excel for easy local use.
Google Sheets Integration: Upload data directly to Google Sheets by entering the sheet URL and uploading Google API credentials.
Convert Back to XML: After editing, convert the data back to XML format and download the file.

📦 Installation

Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/xml-csv-editor.git
cd xml-csv-editor

Install Dependencies: This app requires Python 3.7+ and Streamlit. Install dependencies with:

bash
Copy code
pip install -r requirements.txt
🚀 Usage
Run the Streamlit App:

bash
Copy code
streamlit run app.py
Upload Your XML File:

Upload an XML file to parse and display its data.

Download Options:

Download the parsed data as CSV or Excel for local use.
Upload to Google Sheets:

In the "Upload to Google Sheets" section, follow the detailed setup instructions:
Enter your Google Sheets URL.
Upload your Google credentials JSON file (service account credentials).
Click Upload to Google Sheets to push data to Google Sheets.
Convert to XML:

After any edits, click "Convert to XML" to download the data as an XML file again.

📑 Google Sheets Setup
To enable Google Sheets integration, follow these steps:

Create a Google Cloud Project: Go to the Google Cloud Console and create a new project if needed.
Enable the Google Sheets API: Go to APIs & Services > Library and enable the Google Sheets API.
Create Service Account Credentials:
In APIs & Services > Credentials, click Create Credentials > Service Account.
Download the JSON file containing your credentials.
Share Your Google Sheet with the Service Account:
Open your Google Sheet, click Share, and add the service account’s email (found in the JSON file) as an Editor.

💡 Notes
This project is intended to be basic and extendable. Use this as a foundation to add additional features or customize it to your needs.
The app currently supports basic XML parsing. If you have more complex XML structures, consider extending the parsing logic.
Google Sheets Integration: Ensure that the Google Sheets URL and credentials JSON file are correctly provided to avoid authentication errors.

🌐 Future Improvements
This is a simple, foundational project, but here are a few ways you could expand upon it:

Advanced XML Parsing: Support for nested or more complex XML structures.

Data Cleaning: Add features to edit and clean data within the app.
Enhanced Google Sheets Integration: Add options to update specific rows/columns, or create new sheets dynamically.
Authentication for Multiple Users: Implement user-specific Google Sheets authentication.

🤝 Contributing
Contributions, suggestions, and improvements are always welcome! Please open an issue or submit a pull request.

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

📬 Contact
For questions or suggestions, feel free to reach out to your email address or create an issue on GitHub.

Enjoy building upon this foundation! 🛠️✨
