# BizCardX: Business Card Data Extraction with OCR

## Project Overview

BizCardX is a Streamlit application designed to simplify the extraction of relevant information from business cards. The application utilizes OCR (Optical Character Recognition) through the easyOCR library to extract data such as company name, cardholder name, designation, contact details, and address from uploaded business card images. Additionally, the extracted information can be stored in a database, enabling users to manage multiple entries.

## Technologies Used

- **OCR:** easyOCR
- **GUI:** Streamlit
- **Database:** SQLite or MySQL
- **Programming Language:** Python

## Problem Statement

The goal is to create a user-friendly interface for users to upload business card images, extract relevant information, and manage the data efficiently. The application should allow users to save the extracted information along with the business card image into a database. The key components to extract include the company name, cardholder name, designation, contact details, and address.

## Approach

1. **Install Required Packages:**
   - Python
   - Streamlit
   - easyOCR
   - SQLite or MySQL for the database management system

2. **Design the User Interface:**
   - Create an intuitive Streamlit GUI guiding users through the process.
   - Utilize widgets like file uploader, buttons, and text boxes for interactivity.

3. **Implement Image Processing and OCR:**
   - Use easyOCR to extract information from uploaded business card images.
   - Apply image processing techniques for quality enhancement.

4. **Display Extracted Information:**
   - Present the extracted information in a clean and organized manner using Streamlit widgets.

5. **Implement Database Integration:**
   - Use SQLite or MySQL to store extracted information and business card images.
   - Allow users to perform CRUD operations (Create, Read, Update, Delete) through the Streamlit UI.

6. **Test the Application:**
   - Thoroughly test the application to ensure proper functionality.
   - Run the application locally using the `streamlit run app.py` command.

7. **Improve the Application:**
   - Continuously enhance the application by adding features, optimizing code, and addressing bugs.
   - Consider adding user authentication and authorization for improved security.

## Results

The final application will be a Streamlit tool enabling users to upload business card images, extract relevant information through easyOCR, and manage the data in a database. The intuitive GUI will facilitate easy navigation, and the application will meet the needs of businesses and individuals requiring efficient business card information management.

## Dataset

Dataset Link: [Data Link](#)

## Project Evaluation Metrics

- Code modularization in functional blocks.
- Maintainability and scalability of the codebase.
- Portability across different environments.
- Code repository hosted on GitHub (public).
- Detailed README file with project development information.
- Adherence to Python coding standards (PEP 8).
- Creation of a demo/presentation video posted on LinkedIn.

## Code Organization and Workflow

Refer to the [GitHub Repository](#) for the complete codebase, workflow, and execution details. The README file provides essential information for project development and usage.

## Acknowledgments

Special thanks to the developers and contributors of easyOCR, Streamlit, SQLite, and MySQL for their valuable tools and resources.

## License

This project is licensed under the [MIT License](LICENSE).

--- 

Feel free to customize this README template based on your project's specific details and requirements.
