# Import required packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Title and instructions
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get user name input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Establish a Snowflake session via Streamlit connection
cnx = st.connection("snowflake")
session = cnx.session()

# Query fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_df = my_dataframe.to_pandas()  # Convert to pandas for multiselect options

# Let user select ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_df['FRUIT_NAME'],
    max_selections=5
)

# Show warning if max reached
if len(ingredients_list) == 5:
    st.info("You can only select up to 5 options. Remove an option first.")

# Handle selection
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    # Prepare insert SQL
    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order) 
        values ('{ingredients_string}', '{name_on_order}')
    """

    # Submit button
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
