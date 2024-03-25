# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruites you want in your custom Smoothie!")

name = st.text_input("Name on Smoothie:")
cnx = st.connection("snowflake")
session = cnx.session()
dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredient_list = st.multiselect('Choose upto 5 ingredients',dataframe,max_selections = 5)

if ingredient_list:
    ingredient_string = ''
    for each_fruit in ingredient_list:
        ingredient_string += each_fruit+' '
        st.subheader(each_fruit+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+each_fruit)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)

    my_insert_stmt = """ insert into smoothies.public.orders (ingredients,name_on_order)
                        values('"""+ingredient_string+"""','"""+name+"""')"""
 
    if st.button('Order'):
        if ingredient_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is Ordered!,'+name+'',icon="✅")


    
