# BizCardX: Business Card Data Extraction with OCR

## Project Overview

BizCardX is a Streamlit application designed to simplify the extraction of relevant information from business cards. The application utilizes OCR (Optical Character Recognition) through the easyOCR library to extract data such as company name, cardholder name, designation, contact details, and address from uploaded business card images. Additionally, the extracted information can be stored in a database, enabling users to manage multiple entries.

## Technologies Used

- **OCR:** easyOCR
- **GUI:** Streamlit
- **Database:** MySQL
- **Programming Language:** Python

## Problem Statement

The goal is to create a user-friendly interface for users to upload business card images, extract relevant information, and manage the data efficiently. The application should allow users to save the extracted information along with the business card image into a database.

## Approach

1. **Install Required Packages:**
   - Python
   - Streamlit
   - easyOCR
   - MySQL for the database management system

2. **Design the User Interface:**
   - Create an intuitive Streamlit GUI guiding users through the process.
   - Utilize widgets like file uploader, buttons, and text boxes for interactivity.

3. **Implement Image Processing and OCR:**
   - Use easyOCR to extract information from uploaded business card images.
   - Apply image processing techniques for quality enhancement.

4. **Display Extracted Information:**
   - Present the extracted information in a clean and organized manner using Streamlit widgets.

5. **Implement Database Integration:**
   - Use MySQL to store extracted information and business card images.
   - Allow users to perform CRUD operations (Create, Read, Update, Delete) through the Streamlit UI.
  
6. **Manage Data:**
   - Use MySQL queries to edit/delete the data stored in the database.
   - Display the updated information.

## Install required Modules and Libraries
I have included Requirements.txt file. To install the required modules and libraries at once:

Download the file and save in your project directory.

using command prompt navigate to project directory.

Run the following command to install all the packages listed in the Requirements.txt file using pip:

pip install -r Requirements.txt
