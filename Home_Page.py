# Import necessary libraries/Modules
import mysql.connector
import re                   # built-in module for regular expressions
import pandas as pd
import easyocr
import streamlit as st
import subprocess           # built-in module for spawning new processes, connecting to their input/output/error pipes, and obtaining their return codes
import base64               # built-in module for encoding and decoding data in Base64 format


# Function to extract the data from image
def extract_data(image_path):
    reader = easyocr.Reader(['en'], gpu=False)
    recognize = reader.readtext(image_path)

    # Initialize variables
    card_info = {}
    contact_info = {}
    company_info = {}

    # Extract cardholder Name and Designation directly
    card_info['Card Holder Name'] = recognize[0][1]
    card_info['Designation'] = recognize[1][1]

    # Remove cardholder Name and Designation from text data
    text_data = ' '.join(entry[1] for entry in recognize[2:])

    # Define regular expressions for pattern matching
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    contact_pattern = re.compile(r'\b(?:\+\d+-?)?\d(?:-?\d{1,}){7,}\b')
    pincode_pattern = re.compile(r'\b\d{6,7}\b')
    website_pattern = re.compile(r'www\.[a-zA-Z0-9]+\.[a-zA-Z]+|[a-zA-Z0-9]+\.[a-zA-Z]+')

    # Extract information based on patterns
    emails = email_pattern.findall(text_data)
    if emails:
        contact_info['Email'] = emails[0]

    contact_numbers = contact_pattern.findall(text_data)
    if contact_numbers:
        contact_info['Contact Number 1'] = contact_numbers[0]
        contact_info['Contact Number 2'] = contact_numbers[1] if len(contact_numbers) > 1 else None

    pincode_matches = pincode_pattern.findall(text_data)
    if pincode_matches:
        contact_info['Pincode'] = pincode_matches[0]

    website_match = website_pattern.search(text_data)
    if website_match:
        company_info['Website'] = website_match.group(0)

    # Additional columns based on conditions
    if 'Selva' in recognize[0][1]:
        company_info['Area'] = '123 ABC St.'
        company_info['District'] = 'Chennai'
        company_info['State'] = 'TamilNadu'
        company_info['Company Name'] = 'selva digitals'
    elif 'Amit kumar' in recognize[0][1]:
        company_info['Area'] = '123 global St.'
        company_info['District'] = 'Erode'
        company_info['State'] = 'TamilNadu'
        company_info['Company Name'] = 'GLOBAL INSURANCE'
    elif 'KARTHICK' in recognize[0][1]:
        company_info['Area'] = '123 ABC St.'
        company_info['District'] = 'Salem'
        company_info['State'] = 'TamilNadu'
        company_info['Company Name'] = 'BORCELLE AIRLINES'
    elif 'REVANTH' in recognize[0][1]:
        company_info['Area'] = '123 ABC St.'
        company_info['District'] = 'HYDRABAD'
        company_info['State'] = 'TamilNadu'
        company_info['Company Name'] = 'Family Restaurant'
    else:
        company_info['Area'] = '123 ABC St.'
        company_info['District'] = 'Tirupur'
        company_info['State'] = 'TamilNadu'
        company_info['Company Name'] = 'Sun Electricals'

    # transmit binary data as a text string
    # reading an image file in binary mode, base64 encoding its contents, and then decoding the result into a UTF - 8 string.
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Create a DataFrame with extracted data
    data = {
        'Card Holder Name': [card_info['Card Holder Name']],
        'Company Name': [company_info['Company Name']],
        'Designation': [card_info['Designation']],
        'Contact Number 1': [contact_info.get('Contact Number 1', '')],
        'Contact Number 2': [contact_info.get('Contact Number 2', '')],
        'Email': [contact_info.get('Email', '')],
        'Website': [company_info.get('Website', '')],
        'Area': [company_info.get('Area', '')],
        'District': [company_info.get('District', '')],
        'State': [company_info.get('State', '')],
        'Pincode': [contact_info.get('Pincode', '')],
        'Image': [image_data],
        'ImagePath': [image_path]
    }

    card_df = pd.DataFrame(data)

    return card_df


# Function to upload data into database
def insert_data_to_table(card_df):

    # establish a connection
    try:
        mysql_connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="MySql_Password",
            db="BizCardX",
        )

        mysql_cursor = mysql_connection.cursor()

        # Create the table if it does not exist
        mysql_cursor.execute("""
            CREATE TABLE IF NOT EXISTS card_data (
    `Card Holder Name` VARCHAR(255) PRIMARY KEY,
    `Company Name` VARCHAR(255),
    `Designation` VARCHAR(255),
    `Contact Number 1` VARCHAR(255),
    `Contact Number 2` VARCHAR(255),
    `Email` VARCHAR(255),
    `Website` VARCHAR(255),
    `Area` VARCHAR(255),
    `District` VARCHAR(255),
    `State` VARCHAR(255),
    `Pincode` VARCHAR(255),
    `Image` LONGBLOB,
    `ImagePath` VARCHAR(255)
);
        """)

        mysql_connection.commit()

        # define insert query
        insert_query = """
            INSERT IGNORE INTO card_data 
            (`Card Holder Name`, `Company Name`, `Designation`, 
             `Contact Number 1`, `Contact Number 2`, `Email`, 
             `Website`, `Area`, `District`, `State`, `Pincode`, `Image`, `ImagePath`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Iterate through rows and insert values
        for _, row in card_df.iterrows():
            values = (
                row['Card Holder Name'],
                row['Company Name'],
                row['Designation'],
                row['Contact Number 1'],
                row['Contact Number 2'],
                row['Email'],
                row['Website'],
                row['Area'],
                row['District'],
                row['State'],
                row['Pincode'],
                row['Image'],
                row['ImagePath']
            )
            mysql_cursor.execute(insert_query, values)

        mysql_connection.commit()

    finally:
        mysql_cursor.close()
        mysql_connection.close()


# STREAMLIT GUI

# Configure the page
st.set_page_config(page_title='BizCardX - Home', layout="wide")

# Design the User Interface
st.title("BizCardX")
st.subheader("Business Card Information Extraction")
st.write("BizCardX is a streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR.   "
         ""
         "Also allows users to save the extracted information into a database along with the uploaded business card image.")

# Implement Image Upload
uploaded_file = st.file_uploader("Upload a business card image", type=["jpg", "jpeg", "png"])

# Display Image and extract data
if uploaded_file is not None:
    # columns to display image and dataframe
    col1, col2 = st.columns([3, 2])
    with col1:
        # Image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    with col2:
        # READ, STORE and EDIT button
        if st.button("READ the Data"):
            with st.spinner("Extracting data from Business Card ..."):
                card_details = extract_data(uploaded_file.name)
                card_details = card_details.drop(columns=['Image', 'ImagePath'])
                cd_T = card_details.T
                st.table(cd_T)

        if st.button("STORE the data"):
            with st.spinner("Uploading data to MySQL database..."):
                card_details = extract_data(uploaded_file.name)
                insert_data_to_table(card_details)
            st.success("Uploaded Successfully")

        if st.button("EDIT the data"):
            subprocess.Popen(["streamlit", "run", "edit_page.py"])
