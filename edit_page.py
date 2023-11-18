# Import necessary libraries/Modules
import streamlit as st
import pandas as pd
import mysql.connector


# Function to fetch data from MySQL table based on card holder name
def fetch_data(card_holder_name):
    try:
        # Connect to the MySQL database
        mysql_connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="MySql_Password",
            db="BizCardX",
        )

        # Execute a SELECT query to fetch data for the selected card holder name
        query = f"SELECT * FROM card_data WHERE `Card Holder Name` = '{card_holder_name}'"
        result_df = pd.read_sql(query, mysql_connection)

        return result_df

    finally:
        mysql_connection.close()

# Fetch data from MySQL and store it in a cache
@st.cache_data()
def fetch_and_cache_data(card_holder_name):
    return fetch_data(card_holder_name)


# Function to update data in MySQL table
def update_data(card_holder_name, field_to_edit, new_value):

    try:
        # Connect to the MySQL database
        mysql_connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="MySql_Password",
            db="BizCardX",
        )

        mysql_cursor = mysql_connection.cursor()

        # Define the update query based on the selected field
        update_query = f"UPDATE card_data SET `{field_to_edit}` = %s WHERE `Card Holder Name` = %s"

        # Execute the update query
        mysql_cursor.execute(update_query, (new_value, card_holder_name))

        # Commit the changes
        mysql_connection.commit()

    finally:
        mysql_cursor.close()
        mysql_connection.close()


# Function to delete the whole entry based on card holder name
def delete_whole_entry(card_holder_name):
    try:
        # Connect to the MySQL database
        mysql_connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="MySql_Password",
            db="BizCardX",
        )

        mysql_cursor = mysql_connection.cursor()

        # Execute the DELETE query to delete the whole entry
        delete_query = f"DELETE FROM card_data WHERE `Card Holder Name` = '{card_holder_name}'"
        mysql_cursor.execute(delete_query)

        # Commit the changes
        mysql_connection.commit()

        st.success("Deleted successfully!")

    finally:
        mysql_cursor.close()
        mysql_connection.close()


# Function to delete a single field based on card holder name and field name
def delete_single_field(card_holder_name, field_to_delete):
    try:
        # Connect to the MySQL database
        mysql_connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="MySql_Password",
            db="BizCardX",
        )

        mysql_cursor = mysql_connection.cursor()

        # Execute the UPDATE query to set the field value to NULL
        update_query = f"UPDATE card_data SET `{field_to_delete}` = NULL WHERE `Card Holder Name` = '{card_holder_name}'"
        mysql_cursor.execute(update_query)

        # Commit the changes
        mysql_connection.commit()

        st.success(f"{field_to_delete} deleted from the database!")

    finally:
        mysql_cursor.close()
        mysql_connection.close()


# STREAMLIT GUI

# Configure the page
st.set_page_config(page_title='BizCardX - Edit', layout="wide")

# Design the User Interface
st.title("BizCardX")
st.subheader("Business Card Information Extraction")
st.write("A web application which uses OCR to read through the Business Card")

# Custom CSS to control the width of the selectbox
custom_css = """
<style>
    div[data-baseweb="select"] {
        width: 50%; /* Adjust the width as needed */
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Selectbox
card_holder_name = st.selectbox("Select Card Holder Name", ['Select', 'Selva', 'Amit kumar', 'KARTHICK', 'REVANTH', 'SANTHOSH'])

# selecting a card holder to edit
# card_holder_name = st.selectbox("Select Card Holder Name", ['Select', 'Selva', 'Amit kumar', 'KARTHICK', 'REVANTH', 'SANTHOSH'])

# Splitting the screen into two columns
col1, col2 = st.columns([1, 2])

# Column to Display Data before change:
with col1:
    if card_holder_name != 'Select':
        st.write("Card detail as in database before editing: ")
        # Fetch and cache data from the database for the selected card holder
        fetched_data = fetch_and_cache_data(card_holder_name)
        fetched_data = fetched_data.drop(columns=['Image', 'ImagePath'])
        # Transpose the dataframe
        fd_T = fetched_data.T
        st.table(fd_T)

with col2:
    if card_holder_name != 'Select':
        col3, col4 = st.columns([1, 2])
        with col3:

            # Radio button for choosing between Edit and Delete options
            option = st.radio('',('Edit', 'Delete'),horizontal=True)

            if option == 'Edit':
                field_to_edit = st.selectbox("Select field to edit", ['Select', 'Company Name', 'Card Holder Name', 'Designation', 'Contact Number 1', 'Contact Number 2', 'Email', 'Website', 'Area', 'District', 'State', 'Pincode'])
                new_value = st.text_input(f"Enter new value for {field_to_edit}", "")
                if st.button("Update"):
                    # Trigger the update operation if conditions are met
                    if card_holder_name != 'Select' and field_to_edit != 'Select' and new_value:
                        update_data(card_holder_name, field_to_edit, new_value)
                        st.success("Updated in the database")

            elif option == 'Delete':
                # Add radio button for choosing between whole entry or a single field deletion
                delete_option = st.radio("Delete Option", ['Whole Entry', 'Single Field'], key='delete_option')

                if delete_option == 'Whole Entry':
                    # Add a button to execute the delete of the whole entry
                    if st.button("Delete Whole Entry"):
                        if card_holder_name != 'Select':
                            delete_whole_entry(card_holder_name)  # Implement this function as needed

                elif delete_option == 'Single Field':
                    field_to_delete = st.selectbox("Select field to delete",
                                                   ['Select', 'Company Name', 'Card Holder Name', 'Designation',
                                                    'Contact Number 1', 'Contact Number 2', 'Email', 'Website', 'Area',
                                                    'District', 'State', 'Pincode'])
                    # Add a button to execute the delete of a single field
                    if st.button("Delete Single Field"):
                        if card_holder_name != 'Select' and field_to_delete != 'Select':
                            delete_single_field(card_holder_name, field_to_delete)

        # Display Database After Edit
        with col4:
            if card_holder_name != 'Select' and field_to_edit != 'Select' and new_value:
                st.write("Card detail as in database after editing: ")
                # Fetch data from the database for the selected card holder
                updated_data = fetch_data(card_holder_name)
                updated_data = updated_data.drop(columns=['Image', 'ImagePath'])
                # Transpose the dataframe
                ud_T = updated_data.T
                st.table(ud_T)
